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
    'privacy': 'Privacy',
    'terms': 'Terms',
    'security': 'Security',
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


def validate_links(output, mount, workspace_path=None):
    pages = {file: Page(file.read_text(encoding='utf-8')) for file in output.rglob('*.html')}
    for file, page in pages.items():
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            path = unquote(url.path)
            if workspace_path and path == workspace_path:
                continue
            if path.startswith(mount):
                target = (output / path[len(mount):]).resolve()
            elif path.startswith('/'):
                raise ValueError(f'{file.relative_to(output)}: link leaves the site: {link}')
            else:
                target = (file.parent / path).resolve() if path else file
            if not target.is_relative_to(output):
                raise ValueError(f'{file.relative_to(output)}: use a relative site link for {link}')
            if target.is_dir():
                target /= 'index.html'
            if not target.is_file():
                raise ValueError(f'{file.relative_to(output)}: missing target {link}')
            if url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                raise ValueError(f'{file.relative_to(output)}: missing anchor {link}')


ERRORS = {
    404: ('Page not found', 'Check the spelling of the address or start again at the homepage.'),
    500: ('Something went wrong', 'Return home and check whether your last change was saved before trying again.'),
    501: ('This action is unavailable', 'The service does not support this action. Open the handbook to find the available steps.'),
    503: ('Temporarily unavailable', 'Give the service a little time and then return to the page you were using.'),
}


def https_url(value):
    url = urlsplit(value)
    if url.scheme != 'https' or not url.hostname or url.username or url.password:
        raise ValueError('Expected an HTTPS website URL.')
    return value


def primary_action(site, hosting):
    route = site.get('signInPath')
    if route:
        if not re.fullmatch(r'/(?:[A-Za-z0-9_-]+/)*[A-Za-z0-9_-]+', route):
            raise ValueError('Use a local path such as /signin.')
        origin = https_url(site['appOrigin'])
        parsed = urlsplit(origin)
        if parsed.path not in ('', '/') or parsed.query or parsed.fragment:
            raise ValueError('appOrigin must be an HTTPS origin.')
        label, url = 'Sign in', route if hosting else origin.rstrip('/') + route
    else:
        label, url = site['actionLabel'], https_url(site['actionUrl'])
    return f'<a class="cta" href="{escape(url)}">{escape(label)}</a>'


def shell(config, title, content, prefix, hosting, revision, error=False):
    site = config['publicSite']
    name = escape(config['project'])
    logo = f'<span class="brand-mark" aria-hidden="true">{escape(site["mark"])}</span>'
    stamp = f'<meta name="source-revision" content="{revision}">' if revision else ''
    docs = f'{prefix}docs/'
    footer = ' '.join(f'<a href="{docs}{key}.html">{GUIDES[key]}</a>' for key in ('privacy', 'terms', 'security'))
    robot = '<meta name="robots" content="noindex">' if error else ''
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} | {name}</title>{stamp}{robot}
<link rel="stylesheet" href="{prefix}landing.css"><link rel="stylesheet" href="{prefix}guides.css"></head>
<body><a class="skip-link" href="#main">Skip to content</a>
<header class="wrap header"><a class="brand" href="{prefix}index.html">{logo}{name}</a>
<nav aria-label="Main"><a href="{docs}product.html">Handbook</a><a href="{docs}technical.html">For developers</a>{primary_action(site, hosting)}</nav></header>
<main id="main" tabindex="-1">{content}</main>
<footer class="wrap footer"><a class="brand" href="{prefix}index.html">{name}</a><nav aria-label="Policies">{footer}</nav></footer></body></html>"""


def render(slug, data, config, hosting, revision):
    title = GUIDES[slug]
    menu = ' '.join(
        f'<a href="{key}.html"' + (' aria-current="page"' if key == slug else '') + f'>{label}</a>'
        for key, label in GUIDES.items() if key not in ('privacy', 'terms', 'security')
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
    links = list(data.get('links', []))
    if slug == 'security':
        links.insert(0, ('Report a vulnerability privately', config['publicSite']['securityReport']))
    if links:
        sections += '<ul>' + ''.join(
            f'<li><a href="{escape(https_url(url))}">{escape(label)}</a></li>' for label, url in links
        ) + '</ul>'
    content = (f'<div class="wrap guide"><h1>{title}</h1><p class="lead">{escape(data["intro"])}</p>'
               f'{sections}<nav aria-label="Documentation">{menu}</nav></div>')
    return shell(config, title, content, '../', hosting, revision)


def build(root, output, hosting=False, publish_for=None):
    config = json.loads((root / 'docs/public-guides.json').read_text(encoding='utf-8'))
    if not config['project'].strip() or set(config['guides']) != set(GUIDES):
        raise ValueError('Public guides must cover product, technical, settings, SDLC and pipeline.')
    site = config['publicSite']
    mount = '/' if hosting else site['pagesBase']
    if not re.fullmatch(r'/(?:[A-Za-z0-9_.-]+/)*', mount) or any(part in ('.', '..') for part in mount.split('/')):
        raise ValueError('Use a site mount such as / or /repository/.')
    if publish_for and site['repository'].casefold() != publish_for.casefold():
        raise ValueError('Set publicSite.repository and review the product, routes and policy facts for this repository before publishing.')
    revision = os.getenv('GITHUB_SHA')
    if revision and not re.fullmatch('[0-9a-f]{40}', revision):
        raise ValueError('Invalid GitHub source revision')
    output = output.resolve()
    with tempfile.TemporaryDirectory(prefix='app-launchpad-docs-') as scratch:
        staged = Path(scratch).resolve()
        for asset in ('landing.css', 'guides.css'):
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
        def write(relative, page):
            target = staged / relative
            target.parent.mkdir(exist_ok=True, parents=True)
            target.write_text(page, encoding='utf-8', newline='\n')

        home = (root / 'site/index.html').read_text(encoding='utf-8')
        home = home.replace('<!-- primary-action -->', primary_action(site, hosting))
        write('index.html', shell(config, 'Home', home, './', hosting, revision))
        for code, (title, explanation) in ERRORS.items():
            files = [(f'errors/{code}.html', '../')]
            if code == 404:
                files.append(('404.html', mount))
            for filename, prefix in files:
                content = (f'<section class="wrap hero recovery"><span class="recovery-mark" aria-hidden="true">{escape(site["mark"])}</span>'
                           f'<p class="eyebrow">Error {code}</p><h1>{title}</h1><p class="lead">{explanation}</p>'
                           f'<nav class="primary-action" aria-label="Recovery"><a href="{prefix}index.html">Go home</a>'
                           f'<a href="{prefix}docs/product.html">Open the handbook</a></nav></section>')
                write(filename, shell(config, title, content, prefix, hosting, revision, error=True))
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
            write('docs/' + slug + '.html', render(slug, data, config, hosting, revision))
        validate_links(staged, mount, site.get('signInPath') if hosting else None)
        if output.exists() and (not output.is_dir() or any(output.iterdir())):
            raise ValueError(f'Use an empty build output directory: {output}')
        shutil.copytree(staged, output, dirs_exist_ok=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Use an empty output directory. Omit for a temporary validation build.')
    parser.add_argument('--hosting', action='store_true', help='Use root-mounted links and the local sign-in route.')
    parser.add_argument('--publish-for', help='Verify the public site belongs to this owner/repository.')
    args = parser.parse_args()
    try:
        if args.output:
            build(ROOT, args.output, args.hosting, args.publish_for)
        else:
            with tempfile.TemporaryDirectory(prefix='app-launchpad-docs-check-') as scratch:
                build(ROOT, Path(scratch), args.hosting, args.publish_for)
        print('Public documentation build and local links passed.')
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        raise SystemExit(f'Public documentation build failed: {error}')
