#!/usr/bin/env python3
"""Check local Markdown targets and fragments without accessing the network."""

import argparse
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import re
import unicodedata
from urllib.parse import unquote, urlsplit


QUOTE_MARKER = r' {0,3}> ?'
QUOTES = re.compile(rf'^(?:{QUOTE_MARKER})+')
LIST_ITEM = re.compile(r'^ {0,3}(?:[-+*]|[0-9]{1,9}[.)]) {1,4}(?=\S)')
FENCE = re.compile(r'^[ ]{0,3}(`{3,}|~{3,})(.*)$')
INLINE_CODE = re.compile(r'(?<!`)(`+)(?!`).*?(?<!`)\1(?!`)', re.DOTALL)
ATX = re.compile(r'^ {0,3}#{1,6}[ \t]+(.*)$')
SETEXT = re.compile(r'^ {0,3}(?:=+|-+)[ \t]*$')
LINK = re.compile(r'\]\(\s*(<[^>]+>|[^\s)]+)')
DEFINITION = re.compile(r'^[ \t]*\[[^\]]+\]:[ \t]*(<[^>]+>|\S+)', re.MULTILINE)


def visible_markdown(text):
    lines = text.splitlines()
    if lines and lines[0] == '---' and '---' in lines[1:]:
        end = lines.index('---', 1)
        if any(re.match(r'^\w[\w-]*:', line) for line in lines[1:end]):
            lines = [''] * (end + 1) + lines[end + 1:]
    output = []
    fence = None
    quote_depth = 0
    list_indents = []
    for raw_line in lines:
        line = raw_line.expandtabs(4)
        if fence:
            opening, quote_prefix, indent = fence
            prefix = quote_prefix.match(line)
            if prefix:
                tail = line[prefix.end():]
                if not tail.strip() or tail.startswith(' ' * indent):
                    marker = FENCE.match(tail[indent:])
                    if marker and marker[1][0] == opening[0] and len(marker[1]) >= len(opening) and not marker[2].strip():
                        fence = None
                    output.append('')
                    continue
            # An unclosed fence ends with its enclosing quote or list item.
            fence = None
        prefix = QUOTES.match(line)
        depth = prefix[0].count('>') if prefix else 0
        if depth != quote_depth:
            list_indents.clear()
            quote_depth = depth
        block = line[prefix.end():] if prefix else line
        if block.strip():
            while list_indents and not block.startswith(' ' * list_indents[-1]):
                list_indents.pop()
        indent = list_indents[-1] if list_indents else 0
        block = block[indent:]
        item = LIST_ITEM.match(block)
        if item:
            indent += item.end()
            list_indents.append(indent)
            block = block[item.end():]
        marker = FENCE.match(block)
        if marker:
            fence = (marker[1], re.compile(rf'^(?:{QUOTE_MARKER}){{{quote_depth}}}'), indent)
        output.append('' if marker or block.startswith('    ') else block)
    return '\n'.join(output)


class HTMLAnchors(HTMLParser):
    def __init__(self):
        super().__init__()
        self.anchors = set()

    def handle_starttag(self, tag, attributes):
        self.anchors.update(value for key, value in attributes
                            if value and (key == 'id' or (tag == 'a' and key == 'name')))


def heading_slug(heading):
    title = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', heading)
    title = unescape(re.sub(r'<[^>]*>', '', title)).strip().lower()
    return ''.join('-' if char.isspace() else char for char in title
                   if char.isalnum() or char.isspace() or char in '-_' or unicodedata.combining(char))


def anchors_for(file):
    content = file.read_text(encoding='utf-8')
    parser = HTMLAnchors()
    if file.suffix.lower() == '.html':
        parser.feed(content)
        return parser.anchors
    content = visible_markdown(content)
    parser.feed(INLINE_CODE.sub('', content))
    anchors = set()
    previous = ''
    for line in content.splitlines():
        atx = ATX.match(line)
        heading = None
        if atx:
            heading = re.sub(r'[ \t]+#+[ \t]*$', '', atx[1])
        elif previous.strip() and SETEXT.fullmatch(line):
            heading = previous.strip()
        if heading:
            base = heading_slug(heading)
            slug, suffix = base, 0
            while slug in anchors:
                suffix += 1
                slug = f'{base}-{suffix}'
            anchors.add(slug)
            previous = ''
        else:
            previous = line
    return anchors | parser.anchors


def check_links(root):
    errors = []
    anchor_cache = {}
    files = sorted(p for p in root.rglob('*') if p.is_file() and p.suffix in ('.md', '.mdc')
                   and not any(part in ('.git', 'node_modules', '.venv', '__pycache__') for part in p.parts))
    for file in files:
        content = visible_markdown(file.read_text(encoding='utf-8'))
        content = INLINE_CODE.sub(lambda match: '\n' * match[0].count('\n'), content)
        for value in LINK.findall(content) + DEFINITION.findall(content):
            target = value.strip('<>')
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not (parsed.path or parsed.fragment):
                continue
            decoded = unquote(parsed.path)
            destination = root / decoded.lstrip('/') if decoded.startswith('/') else file.parent / decoded
            if not decoded:
                destination = file
            if not destination.exists():
                errors.append(f'{file.relative_to(root)}: missing local link {target}')
                continue
            if not parsed.fragment:
                continue
            destination = destination.resolve()
            if destination.is_dir():
                destination = destination / 'README.md'
            if destination.is_file() and destination.suffix.lower() in ('.md', '.mdc', '.html'):
                if destination not in anchor_cache:
                    anchor_cache[destination] = anchors_for(destination)
                if unquote(parsed.fragment) not in anchor_cache[destination]:
                    errors.append(f'{file.relative_to(root)}: missing local anchor {target}')
    return sorted(set(errors))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    failures = check_links(args.root.resolve())
    for failure in failures:
        print('ERROR: ' + failure)
    if not failures:
        print('Local Markdown links and anchors passed.')
    raise SystemExit(bool(failures))
