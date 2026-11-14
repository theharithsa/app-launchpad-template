#!/usr/bin/env python3
"""Build the public site from curated inputs and validate local HTML links."""
import argparse
from html import escape
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
GUIDES = {
    'product': 'Product handbook',
    'technical': 'Technical guide',
    'settings': 'Settings reference',
    'sdlc': 'SDLC guide',
    'pipeline': 'CI/CD pipeline',
}
MEDIA_SUFFIXES = {'.jpg', '.jpeg', '.png', '.webp', '.avif', '.mp4', '.webm', '.vtt'}


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = set()
        self.links = []
        self.template_depth = 0
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        if tag == 'template':
            self.template_depth += 1
        if self.template_depth:
            return
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        self.links.extend(attrs[key] for key in ('href', 'src', 'poster') if attrs.get(key))

    def handle_endtag(self, tag):
        if tag == 'template':
            self.template_depth -= 1


def validate_links(output):
    pages = {file: Page(file.read_text()) for file in output.rglob('*.html')}
    for file, page in pages.items():
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            path = unquote(url.path)
            target = (file.parent / path).resolve() if path else file
            if path.startswith('/') or not target.is_relative_to(output):
                raise ValueError(f'{file.relative_to(output)}: use a relative site link for {link}')
            if target.is_dir():
                target /= 'index.html'
            if not target.is_file():
                raise ValueError(f'{file.relative_to(output)}: missing target {link}')
            if url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                raise ValueError(f'{file.relative_to(output)}: missing anchor {link}')


def render(slug, data):
    title = GUIDES[slug]
    menu = ''.join(
        f'<a href="{key}.html"' + (' aria-current="page"' if key == slug else '')
        + f'>{label}</a>'
        for key, label in GUIDES.items()
    )
    sections = ''.join(
        f'<section><h2>{escape(heading)}</h2><p>{escape(body)}</p></section>'
        for heading, body in data['sections']
    )
    if slug == 'pipeline':
        sections += '<section><h2>Delivery flow</h2><ol class="pipeline">' + ''.join(
            f'<li><strong>{escape(stage)}</strong><span>{escape(result)}</span></li>'
            for stage, result in data['stages']
        ) + '</ol></section>'
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | {escape(data['project'])}</title>
  <link rel="stylesheet" href="../landing.css">
  <link rel="stylesheet" href="../guides.css">
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="wrap header">
    <a class="brand" href="../">{escape(data['project'])}</a>
    <nav aria-label="Documentation">{menu}</nav>
  </header>
  <main id="main" class="wrap guide">
    <h1>{title}</h1>
    <p class="lead">{escape(data['intro'])}</p>
    {sections}
  </main>
</body>
</html>
'''


def build(root, output):
    config = json.loads((root / 'docs/public-guides.json').read_text())
    if not config['project'].strip() or set(config['guides']) != set(GUIDES):
        raise ValueError('Public guides must cover product, technical, settings, SDLC and pipeline.')
    revision = os.getenv('GITHUB_SHA')
    if revision and not re.fullmatch('[0-9a-f]{40}', revision):
        raise ValueError('Invalid GitHub source revision')
    output = output.resolve()
    with tempfile.TemporaryDirectory(prefix='app-launchpad-docs-') as scratch:
        staged = Path(scratch).resolve()
        for asset in ('index.html', 'landing.css', 'guides.css'):
            source = root / 'site' / asset
            if not source.is_file() or source.is_symlink():
                raise ValueError(f'Expected a regular site file at {asset}')
            shutil.copyfile(source, staged / asset)
        media = root / 'site/media'
        if media.is_dir() and not media.is_symlink():
            for source in sorted(media.iterdir()):
                if source.is_file() and not source.is_symlink() and source.suffix.lower() in MEDIA_SUFFIXES:
                    destination = staged / 'media' / source.name
                    destination.parent.mkdir(exist_ok=True)
                    shutil.copyfile(source, destination)
        guides = staged / 'docs'
        guides.mkdir()
        for slug, data in config['guides'].items():
            if not data['intro'].strip():
                raise ValueError(f'{slug}: introduction is required')
            for field in ('sections', 'stages') if slug == 'pipeline' else ('sections',):
                entries = data[field]
                if not isinstance(entries, list) or not entries or any(
                    not isinstance(entry, list) or len(entry) != 2
                    or any(not isinstance(value, str) or not value.strip() for value in entry)
                    for entry in entries
                ):
                    raise ValueError(f'{slug}: {field} must contain title and text pairs')
            page = render(slug, {**data, 'project': config['project']})
            if revision:
                page = page.replace('</head>', f'  <meta name="source-revision" content="{revision}">\n</head>')
            (guides / (slug + '.html')).write_text(page)
        validate_links(staged)
        if output.exists() and (not output.is_dir() or any(output.iterdir())):
            raise ValueError(f'Use an empty build output directory: {output}')
        shutil.copytree(staged, output, dirs_exist_ok=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Use an empty output directory. Omit for a temporary validation build.')
    args = parser.parse_args()
    try:
        if args.output:
            build(ROOT, args.output)
        else:
            with tempfile.TemporaryDirectory(prefix='app-launchpad-docs-check-') as scratch:
                build(ROOT, Path(scratch))
        print('Public documentation build and local links passed.')
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        raise SystemExit(f'Public documentation build failed: {error}')
