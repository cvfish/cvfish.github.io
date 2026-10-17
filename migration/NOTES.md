# Migration notes

## Content preserved

- Original biography, research interests, PhD thesis, nine publication entries, and three earlier engineering projects.
- Portrait and all fourteen images linked from the old homepage.
- The original five-page CV, with its contents and original UCL address unchanged, labeled as archived.
- Three linked research pages: Better Together, Direct/Dense/Deformable, and Video Pop-up, including their full abstracts and supporting resource links.
- Current role and public email updated from Rui's instructions: Staff Engineer at Apple; cvyurui@gmail.com.
- New web CV and a two-page PDF generated from the shared profile/publication/project data.

## Editorial decisions

- Historical research remains labeled as earlier work. The page is not presented as a complete account of recent Apple work.
- Apple's start date (February 2019), DJI tenure, and education dates come from the archived CV. The Staff Engineer promotion date is not supplied; the current title is shown alongside overall Apple tenure.
- The homepage called the NWPU degrees BSc/MSc; the PDF called them BEng/MEng. The new pages use neutral bachelor's/master's wording while preserving the subject and dates from the detailed CV.
- The preprint's 2017 year and its 'submitted to IJCV' status were checked against https://arxiv.org/abs/1708.01654. It is labeled a preprint, with no claim of journal acceptance.
- The CV and homepage differ slightly in a few author lists. The All-in-Focus author list has been corrected against the recovered paper, adding Wenguang Ma and Lingyan Ran. Other entries follow the homepage; original sources remain available for review.
- The CV includes an additional TCSVT 2013 item and talk titles not listed on the original homepage. These remain available in the archived CV; the new PDF has a selected-publications section.
- The old CV PDF keeps its original, obsolete contact details as an archival record. The new homepage, web CV, and current PDF use the updated address.
- The original CV's research, tools, projects, and awards inform the new CV; no additional employer accomplishments are inferred.

## Remaining external resources

- Better Together's synthetic dataset remains at its original UCL download URL.
- Video Pop-up's original OGV result video and additional-results page remain linked at UCL.
- Video Pop-up's PowerPoint slides exceed the migration's 65 MB download cap and remain linked at UCL. The equivalent PDF slides are hosted locally.
- YouTube demos, GitHub code, arXiv versions, and Google Scholar remain at their original service URLs.

`manifest.json` records the homepage assets and PDFs; `project-assets.json` records figures, slides, and posters recovered from linked project pages. The recovery scripts download only explicitly linked public files. HTML snapshots are parsed as data, never executed or deployed.

## UCL redirect

After the new homepage is verified live, request an HTTP 301 redirect for the old address from the university administrator, if available. A fallback redirect page is included in `ucl-redirect.html`; it must be installed on the old server by someone with access. No UCL files have been changed by this migration.
