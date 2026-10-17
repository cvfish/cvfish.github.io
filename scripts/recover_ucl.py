"""Recover only linked public files from Rui Yu's UCL homepage.

Downloaded HTML is stored as source material and is never executed or published.
The manifest records provenance, successful downloads, and unresolved links.
"""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parents[1]
BASE = "http://www0.cs.ucl.ac.uk/staff/Rui.Yu/"
SOURCE = ROOT / "migration/source/ucl-index.html"
html = SOURCE.read_text()
items = {}
for attr, value in re.findall(r'(src|href)="([^"]+)"', html):
    url = urljoin(BASE, value)
    parsed = urlparse(url)
    if parsed.hostname != "www0.cs.ucl.ac.uk":
        continue
    name = Path(parsed.path).name
    suffix = Path(name).suffix.lower()
    if attr == "src":
        destination = "public/ryu_files/" + name
    elif suffix == ".pdf":
        destination = ("public/ryu_files/" if value.startswith("ryu_files/") else "public/papers/") + name
    elif suffix == ".html":
        destination = "migration/source/" + name
    elif suffix == ".zip":
        items[url] = {"url": url, "status": "external", "reason": "Dataset retained at original URL; size not yet verified."}
        continue
    else:
        continue
    items[url] = {"url": url, "path": destination}

def recover(item):
    if "path" not in item:
        return item
    target = ROOT / item["path"]
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and target.stat().st_size:
        item.update(status="recovered", bytes=target.stat().st_size, sha256=hashlib.sha256(target.read_bytes()).hexdigest())
        return item
    partial = target.with_suffix(target.suffix + ".part")
    result = subprocess.run(["curl", "-fLsS", "--connect-timeout", "12", "--max-time", "1800", "--max-filesize", "65000000", item["url"], "-o", str(partial)], capture_output=True, text=True)
    if result.returncode:
        partial.unlink(missing_ok=True)
        item.update(status="failed", error=result.stderr.strip())
    else:
        partial.replace(target)
        item.update(status="recovered", bytes=target.stat().st_size, sha256=hashlib.sha256(target.read_bytes()).hexdigest())
    return item

with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
    results = list(pool.map(recover, items.values()))
(ROOT / "migration/manifest.json").write_text(json.dumps({"source": BASE, "recovered_on": "2026-10-17", "source_last_modified": "2019-11-17", "files": results}, indent=2) + "\n")
for item in results:
    print(item["status"], item.get("path", item["url"]), item.get("bytes", item.get("error", "")))
