"""Build the static homepage with Python's standard library only."""
from html import escape, unescape
from pathlib import Path
import hashlib
import json
import re
from string import Template
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public"
profile = json.loads((ROOT / "data/profile.json").read_text())
papers = json.loads((ROOT / "data/publications.json").read_text())
projects = json.loads((ROOT / "data/projects.json").read_text())
template = Template((ROOT / "templates/base.html").read_text())
asset_versions = {name: hashlib.sha256((OUT / "assets" / name).read_bytes()).hexdigest()[:12] for name in ("site.css", "site.js")}
manifest_file = ROOT / "migration/manifest.json"
manifest = json.loads(manifest_file.read_text()) if manifest_file.exists() else {"files": []}
origins = {item["path"].removeprefix("public/"): item["url"] for item in manifest["files"] if item.get("path", "").startswith("public/")}
extras_file = ROOT / "migration/project-assets.json"
if extras_file.exists():
    origins.update({item["path"].removeprefix("public/"): item["url"] for item in json.loads(extras_file.read_text()) if item.get("path")})

def e(value):
    return escape(str(value), quote=True)

def plain(html):
    html = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    return " ".join(unescape(re.sub(r"<[^>]+>", " ", html)).split())

def local_link(path, prefix=""):
    if re.match(r"^(https?://|mailto:)", path):
        return path
    if (OUT / path).exists() or path.endswith("/") or path.endswith(".html"):
        return prefix + path
    if path in origins:
        return origins[path]
    raise FileNotFoundError(f"Missing linked file: {path}")

def links(items, prefix=""):
    result = []
    for item in items:
        url = local_link(item["url"], prefix)
        label = item["label"]
        if url.startswith("http://www0.cs.ucl.ac.uk") and "UCL" not in label:
            label += " (UCL)"
        result.append(f'<a href="{e(url)}">{e(label)}</a>')
    return '<div class="pub-links">' + "".join(result) + '</div>'

def authors(value):
    return e(value).replace("Rui Yu", "<strong>Rui Yu</strong>")

def image(path, alt, prefix="", cls="", eager=False):
    return f'<img src="{e(prefix + path)}" alt="{e(alt)}" class="{e(cls)}" loading="{"eager" if eager else "lazy"}" decoding="async">'

def page(path, title, description, content, prefix="", body_class=""):
    canonical_path = "" if path == "index.html" else path
    home_base = "" if path == "index.html" else prefix + "index.html"
    output = template.substitute(title=e(title), description=e(description), prefix=prefix,
        site_url=e(profile["site_url"]), canonical=e(profile["site_url"] + "/" + canonical_path),
        body_class=body_class, content=content, home_base=e(home_base), home_link=e(home_base or "#"),
        cv_current=' aria-current="page"' if path == "cv.html" else "",
        email=e(profile["email"]), github=e(profile["github"]), scholar=e(profile["scholar"]), updated=e(profile["updated"]),
        css_version=asset_versions["site.css"], js_version=asset_versions["site.js"])
    target = OUT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(output)

def publication(p):
    award = f' · <span class="award">{e(p["award"])}</span>' if p["award"] else ""
    title_url = local_link(next((link["url"] for link in p["links"] if link["label"] == "Project"), p["links"][0]["url"]))
    return f'''<li class="publication" id="{e(p['id'])}" data-publication>
      <h3 class="pub-title"><a href="{e(title_url)}">{e(p['title'])}</a></h3>
      <p class="pub-meta">{e(p['short_venue'])} {p['year']}{award}</p>
      {links(p['links'])}</li>'''

def home():
    bio_html = "".join(f"<p>{e(paragraph)}</p>" for paragraph in profile["background"].split("\n\n"))
    content = f'''<header class="home-header"><h1>{e(profile['name'])}</h1>
      <p class="intro">I am a <strong>{e(profile['role'])}</strong> at <strong>{e(profile['company'])}</strong>, working on computer vision and machine learning. {e(profile['homepage_intro'])}</p></header>
    <section id="about"><h2 id="bio">Bio</h2>{bio_html}</section>
    <section id="research"><h2 id="publications">Selected Publications</h2>
      <ol class="publications">{''.join(publication(p) for p in papers)}</ol>
      <p class="thesis"><strong>PhD thesis:</strong> <a href="{e(local_link('papers/thesis_RuiYu.pdf'))}">Learning Dense 3D Models from Monocular Video</a> (UCL, 2017).</p></section>
    <section class="links-section"><h2>Links</h2><ul>
      <li><a href="{e(profile['github'])}">GitHub</a></li>
      <li><a href="{e(profile['scholar'])}">Google Scholar</a></li>
    </ul></section>'''
    page("index.html", "Rui Yu — Computer Vision & Machine Learning", f"Rui Yu, {profile['role']} at {profile['company']}. 3D computer vision, machine learning, and selected publications.", content, body_class="home-page")

def cv():
    def items(values, education=False):
        return "".join(f'<article class="cv-item"><h3>{e(x.get("degree") if education else x["role"])} · {e(x["organization"])}</h3><p class="cv-date">{e(x["period"])}</p><p>{e(x["description"])}</p></article>' for x in values)
    selected = [p for p in papers if p["id"] in ["better-together", "jigsaw", "direct-dense-deformable", "video-popup", "hybrid-imaging"]]
    selected_html = "".join(f'<article class="cv-item"><h3><a href="{e(local_link(p["links"][0]["url"]))}">{e(p["title"])}</a></h3><p>{authors(p["authors"])}</p><p class="cv-date">{e(p["short_venue"])} {p["year"]}{" · " + e(p["award"]) if p["award"] else ""}</p></article>' for p in selected)
    project_html = "".join(f'<article class="cv-item"><h3>{e(p["title"])}</h3><p>{e(p["description"])}</p></article>' for p in projects)
    code = "".join(f'<article class="cv-item"><h3><a href="{e(x["url"])}">{e(x["title"])}</a></h3><p>{e(x["description"])}</p></article>' for x in profile['code'])
    content = f'''<header class="page-top"><a class="back-link" href="index.html">← Back to homepage</a><h1>Rui Yu</h1><p class="lead">{e(profile['role'])} at {e(profile['company'])} · Computer vision & machine learning</p><div class="cv-contact"><a href="mailto:{e(profile['email'])}">{e(profile['email'])}</a><a href="{e(profile['github'])}">github.com/cvfish</a><a href="{e(profile['scholar'])}">Google Scholar</a></div><div class="page-actions"><a class="button" href="files/rui-yu-cv.pdf" download>Download CV (PDF)</a><button class="print-button" data-print>Print this page</button><a href="ryu_files/cv_ruiyu_detailed.pdf">Previous CV (archived)</a></div></header>
    <section class="cv-section"><h2>Profile</h2><p class="skills">{e(profile['intro'])}</p></section>
    <section class="cv-section"><h2>Experience</h2><div>{items(profile['experience'])}</div></section>
    <section class="cv-section"><h2>Education</h2><div>{items(profile['education'],True)}</div></section>
    <section class="cv-section"><h2>Research</h2><div><article class="cv-item"><h3>Learning Dense 3D Models from Monocular Video</h3><p>PhD thesis, University College London. Dense 3D reconstruction of dynamic scenes and deformable objects using a single camera.</p><p><a href="{e(local_link('papers/thesis_RuiYu.pdf'))}">Read thesis</a></p></article><article class="cv-item"><h3>Vision-based autonomous landing of an unmanned aerial vehicle</h3><p>Master’s thesis. A real-time vision-based autonomous landing system.</p></article></div></section>
    <section class="cv-section cv-publications"><h2>Selected publications</h2><div>{selected_html}<p class="skills"><a href="index.html#research">Publication archive</a> · <a href="{e(profile['scholar'])}">Full list on Google Scholar</a></p></div></section>
    <section class="cv-section"><h2>Earlier projects</h2><div>{project_html}</div></section>
    <section class="cv-section"><h2>Technical interests & tools</h2><p class="skills">{e(' · '.join(profile['skills']))}</p></section>
    <section class="cv-section"><h2>Code</h2><div>{code}</div></section>
    <section class="cv-section"><h2>Awards</h2><ul class="cv-list">{''.join('<li>'+e(x)+'</li>' for x in profile['awards'])}</ul></section>
    <p class="archive-note">Profile updated {e(profile['updated'])}. Earlier research, education, and projects are drawn from my previous homepage and CV. The archived PDF retains its original content.</p>'''
    page("cv.html", "Rui Yu — Curriculum Vitae", f"Curriculum vitae of Rui Yu, {profile['role']} at {profile['company']}.", content, body_class="cv-page")

def research_pages():
    definitions = [
        ("better-together", "better_together.html", "http://www0.cs.ucl.ac.uk/staff/Qi.Liu/bmvc16/", "bmvc16.png", "https://www.youtube.com/watch?v=gT25sLQw1IA"),
        ("direct-dense-deformable", "direct_nrsfm.html", "http://www0.cs.ucl.ac.uk/staff/R.Yu/direct_nrsfm/", "iccv2015.png", "https://www.youtube.com/watch?v=O9VV3FFWiGU"),
        ("video-popup", "VideoPopup2.html", "http://www0.cs.ucl.ac.uk/staff/R.Yu/video_popup/", "fig_cat6.png", "http://www0.cs.ucl.ac.uk/staff/R.Yu/video_popup/final_new_crop.ogv")
    ]
    prefix = "../../"
    for slug, source_name, base, figure, video in definitions:
        p = next(p for p in papers if p["id"] == slug)
        source = (ROOT / "migration/source" / source_name).read_text()
        source = re.sub(r"<!--.*?-->", "", source, flags=re.S)
        abstract = re.search(r'<h2>\s*Abstract\s*</h2>\s*<p[^>]*>(.*?)</p>', source, flags=re.S | re.I)
        abstract_text = plain(abstract.group(1)) if abstract else p["description"]
        figure_path = f"project-assets/{slug}/{figure}"
        if not (OUT / figure_path).exists():
            figure_path = p["image"]
        extra_links = []
        for href, label in re.findall(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', source, re.S):
            label = plain(label).strip("[]")
            if any(word in label.lower() for word in ["poster", "slides", "dataset", "more results"]):
                local = f"project-assets/{slug}/{Path(href).name}"
                url = local if (OUT / local).exists() else urljoin(base, href)
                extra_links.append({"label": label.capitalize(), "url": url})
        content = f'''<header class="detail-header"><a class="back-link" href="../../index.html#research">← All research</a><p class="eyebrow" style="margin-top:26px">{e(p['short_venue'])} {p['year']}{' · '+e(p['award']) if p['award'] else ''}</p><h1>{e(p['title'])}</h1><p class="pub-authors">{authors(p['authors'])}</p>{links([x for x in p['links'] if x['label'] != 'Project'],prefix)}</header>
        <figure class="detail-figure">{image(figure_path,p['image_alt'],prefix,eager=True)}</figure><div class="prose"><h2>Abstract</h2><p>{e(abstract_text)}</p><h2>Results</h2><a class="video-link" href="{e(video)}">Watch the research demo <span aria-hidden="true">↗</span><span>{'Original video hosted at UCL' if 'www0.cs.ucl.ac.uk' in video else 'Video on YouTube'}</span></a>{links(extra_links,prefix) if extra_links else ''}</div><div class="detail-footer"><a href="../../index.html#research">← Back to all publications</a></div>'''
        page(f"projects/{slug}/index.html", p["title"]+" — Rui Yu", p["description"], content, prefix)

home()
cv()
research_pages()
page("404.html", "Page not found — Rui Yu", "Return to Rui Yu’s homepage.", '<section class="page-top"><p class="eyebrow">404</p><h1>Let’s find your way back.</h1><p class="lead">This page may have moved. You can find the publications and CV on my homepage.</p><a class="button" href="/">Go to homepage</a></section>', prefix="/")
(OUT / ".nojekyll").touch()
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {profile['site_url']}/sitemap.xml\n")
paths = ["", "cv.html", "projects/better-together/", "projects/direct-dense-deformable/", "projects/video-popup/"]
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(f"<url><loc>{e(profile['site_url']+'/'+path)}</loc></url>" for path in paths) + '\n</urlset>\n')
print(f"Built homepage, CV, 3 research pages, 404, sitemap, and robots.txt in {OUT}")
