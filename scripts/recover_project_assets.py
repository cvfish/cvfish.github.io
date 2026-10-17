"""Recover the figures and supporting documents linked by the three project pages."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
projects = [
    ("better-together", "better_together.html", "http://www0.cs.ucl.ac.uk/staff/Qi.Liu/bmvc16/"),
    ("direct-dense-deformable", "direct_nrsfm.html", "http://www0.cs.ucl.ac.uk/staff/R.Yu/direct_nrsfm/"),
    ("video-popup", "VideoPopup2.html", "http://www0.cs.ucl.ac.uk/staff/R.Yu/video_popup/")
]
items = []
for slug, source, base in projects:
    html = re.sub(r"<!--.*?-->", "", (ROOT / "migration/source" / source).read_text(), flags=re.S)
    for attr, href in re.findall(r'(src|href)="([^"]+)"', html):
        if href.startswith(("http", "//")):
            continue
        name = Path(href).name
        suffix = Path(name).suffix.lower()
        if suffix not in (".png", ".jpg", ".pdf", ".pptx"):
            continue
        if name in ("better_together.pdf", "direct_nrsfm.pdf", "VideoPopup.pdf"):
            continue
        items.append({"url": urljoin(base, href), "path": f"public/project-assets/{slug}/{name}"})

def recover(item):
    target = ROOT / item["path"]
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(target.suffix + ".part")
    result = subprocess.run(["curl", "-fLsS", "--connect-timeout", "12", "--max-time", "1800", "--max-filesize", "65000000", item["url"], "-o", str(temporary)], capture_output=True, text=True)
    if result.returncode:
        temporary.unlink(missing_ok=True)
        item.update(status="failed", error=result.stderr.strip())
    else:
        temporary.replace(target)
        item.update(status="recovered", bytes=target.stat().st_size, sha256=hashlib.sha256(target.read_bytes()).hexdigest())
    return item

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    result = list(pool.map(recover, items))
(ROOT / "migration/project-assets.json").write_text(json.dumps(result, indent=2) + "\n")
for item in result:
    print(item["status"], item["path"], item.get("bytes", item.get("error")))
