"""Check generated pages, local assets, and in-page links before publishing."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
errors = []

class Document(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.links = []
        self.ids = set()
        self.h1s = 0
        self.titles = 0
        self.publications = 0
    def handle_starttag(self, tag, attributes):
        attr = dict(attributes)
        if attr.get('id'):
            if attr['id'] in self.ids:
                errors.append(f"{self.path}: duplicate ID {attr['id']}")
            self.ids.add(attr['id'])
        if tag == 'h1': self.h1s += 1
        if tag == 'title': self.titles += 1
        if 'data-publication' in attr: self.publications += 1
        if tag == 'img' and 'alt' not in attr:
            errors.append(f"{self.path}: image has no alt attribute")
        for key in ('src', 'href'):
            if key in attr: self.links.append(attr[key])

documents = {}
for path in PUBLIC.rglob('*.html'):
    doc = Document(path.relative_to(PUBLIC))
    doc.feed(path.read_text())
    documents[path.resolve()] = doc
    if doc.h1s != 1 or doc.titles != 1:
        errors.append(f"{doc.path}: expected one h1 and one title")

for path, doc in documents.items():
    for link in doc.links:
        parts = urlsplit(link)
        if parts.scheme or parts.netloc:
            continue
        name = unquote(parts.path)
        target = (PUBLIC / name.lstrip('/')) if name.startswith('/') else (path.parent / name)
        if not name: target = path
        if target.is_dir(): target /= 'index.html'
        target = target.resolve()
        if not target.is_relative_to(PUBLIC.resolve()) or not target.exists():
            errors.append(f"{doc.path}: broken local link {link}")
        elif parts.fragment and target in documents and unquote(parts.fragment) not in documents[target].ids:
            errors.append(f"{doc.path}: missing anchor {link}")

expected = len(json.loads((ROOT / 'data/publications.json').read_text()))
if documents[(PUBLIC / 'index.html').resolve()].publications != expected:
    errors.append('Homepage does not contain every publication')
for path in PUBLIC.rglob('*.part'):
    errors.append(f"Incomplete download in deployment directory: {path.name}")
for path in PUBLIC.rglob('*'):
    if path.is_file() and path.stat().st_size > 95_000_000:
        errors.append(f"File too large for a normal GitHub repository: {path.name}")
if errors:
    raise SystemExit('\n'.join(errors))
print(f"Verified {len(documents)} HTML pages, {expected} publications, every local link/anchor, image alternatives, and file sizes.")
