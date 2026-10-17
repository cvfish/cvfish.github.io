# Rui Yu's homepage

Personal homepage, research archive, and CV for Rui Yu. Intended address: **https://cvfish.github.io/**.

## Editing content

- `data/profile.json`: biography, current role, email, experience, education, skills, and awards.
- `data/publications.json`: papers, thumbnails, descriptions, and links.
- `data/projects.json`: earlier engineering projects and video links.
- `public/assets/site.css`: responsive visual design.
- `templates/base.html` and `scripts/build.py`: page layout and static HTML generation.

Edits to `main` rebuild the pages and CV PDF, check local links, and publish through GitHub Actions. No JavaScript framework or database is needed.

## Preview locally

Python 3.10+ is required. To regenerate the PDF, install `requirements.txt` in your preferred Python environment first.

```sh
python3 -m pip install -r requirements.txt
python3 scripts/build_pdf.py
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8873 --directory public
```

Open http://localhost:8873. The static HTML and existing PDF also work without rebuilding.

## GitHub Pages setup

Use the public repository `cvfish/cvfish.github.io`. In **Settings → Pages → Build and deployment**, select **GitHub Actions**. The included `Publish homepage` workflow deploys `public/` on pushes to `main` and supports manual runs.

To add a custom domain later, configure it in GitHub Pages and update `site_url` in `data/profile.json`, then rebuild. The site includes a canonical URL, social metadata, sitemap, custom 404 page, reduced-motion styles, accessible navigation, and a layout for printing the CV.

## Migration and provenance

Original content: http://www0.cs.ucl.ac.uk/staff/Rui.Yu/ (last modified November 17, 2019). Source snapshots and file hashes are retained in `migration/`; only `public/` is deployed.

The current Staff Engineer title and public Gmail address were supplied by Rui in October 2026. Historical dates come from the original CV. No recent project accomplishments or promotion dates have been invented. The previous CV PDF remains available under a clearly marked archive link.

The homepage preserves all nine original publication entries and all three earlier engineering projects. Three linked research pages have been rebuilt with their original abstracts, figures, and resources. Large legacy datasets and videos may remain external; see `migration/NOTES.md` and the download manifests for the final inventory.

Original site design credit: Jon Barron's academic homepage template. This version uses a new layout and styling. Research figures, papers, and other materials retain their original authorship and publication rights.
