"""Generate the current two-page CV from the same data as the website."""
import json
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether, PageBreak, HRFlowable

ROOT = Path(__file__).resolve().parents[1]
p = json.loads((ROOT / "data/profile.json").read_text())
papers = json.loads((ROOT / "data/publications.json").read_text())
projects = json.loads((ROOT / "data/projects.json").read_text())
output = ROOT / "public/files/rui-yu-cv.pdf"
output.parent.mkdir(parents=True, exist_ok=True)
ink, muted, green = colors.HexColor('#25332e'), colors.HexColor('#526057'), colors.HexColor('#315e4e')
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='NameCV', fontName='Times-Roman', fontSize=30, leading=33, textColor=ink, spaceAfter=5))
styles.add(ParagraphStyle(name='RoleCV', fontName='Helvetica', fontSize=11, leading=15, textColor=green, spaceAfter=7))
styles.add(ParagraphStyle(name='ContactCV', fontName='Helvetica', fontSize=8.5, leading=12, textColor=muted, spaceAfter=12))
styles.add(ParagraphStyle(name='SectionCV', fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=green, spaceBefore=12, spaceAfter=7))
styles.add(ParagraphStyle(name='ItemCV', fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=ink, spaceAfter=2))
styles.add(ParagraphStyle(name='BodyCV', fontName='Helvetica', fontSize=8.5, leading=12, textColor=muted, spaceAfter=5))
styles.add(ParagraphStyle(name='SmallCV', fontName='Helvetica', fontSize=7.8, leading=11, textColor=muted, spaceAfter=3))

def text(value):
    return escape(str(value).replace('–','-').replace('—','-').replace('’',"'").replace('“','"').replace('”','"'))

def para(value, style='BodyCV'):
    return Paragraph(value, styles[style])

story = [para(text(p['name']),'NameCV'), para(text(p['role']+' at '+p['company']+' | Computer vision & machine learning'),'RoleCV'),
    para(f'<link href="mailto:{text(p["email"])}">{text(p["email"])}</link> &nbsp; | &nbsp; <link href="{text(p["site_url"])}">cvfish.github.io</link> &nbsp; | &nbsp; <link href="{text(p["github"])}">github.com/cvfish</link> &nbsp; | &nbsp; <link href="{text(p["scholar"])}">Google Scholar</link>','ContactCV'),
    HRFlowable(width='100%', thickness=.6, color=colors.HexColor('#dce0d6')),para(text(p['intro']))]

def section(title): story.append(para(text(title).upper(),'SectionCV'))
def item(title, body='', meta='', link=None):
    heading = text(title)
    if link: heading = f'<link href="{text(link)}">{heading}</link>'
    pieces = [para(heading,'ItemCV')]
    if meta: pieces.append(para(text(meta),'SmallCV'))
    if body: pieces.append(para(text(body)))
    pieces.append(Spacer(1,4))
    story.append(KeepTogether(pieces))

section('Experience')
for x in p['experience']:
    item(x['role']+' | '+x['organization'], x['description'], x['period'])
section('Education')
for x in p['education']:
    item(x['degree']+' | '+x['organization'], x['description'], x['period'])
section('Selected publications')
for paper in papers:
    if paper['id'] not in ['better-together','jigsaw','direct-dense-deformable','video-popup','hybrid-imaging']: continue
    item(paper['title'], meta=paper['authors']+' | '+paper['short_venue']+' '+str(paper['year'])+(' | '+paper['award'] if paper['award'] else ''), link=p['site_url']+'/#'+paper['id'])
story.append(PageBreak())
story += [para('Rui Yu','NameCV'),para('Research, engineering projects & technical background','RoleCV'),HRFlowable(width='100%',thickness=.6,color=colors.HexColor('#dce0d6'))]
section('Research')
item('Learning Dense 3D Models from Monocular Video','PhD thesis, University College London. Dense 3D reconstruction of dynamic scenes and deformable objects using a single camera.')
item('Vision-based autonomous landing of an unmanned aerial vehicle','Master\'s thesis. A real-time vision-based autonomous landing system.')
section('Earlier engineering projects')
for x in projects: item(x['title'],x['description'],link=x['video'])
section('Technical interests & tools')
story.append(para(text(' | '.join(p['skills']))))
section('Open source')
for x in p['code']:
    item(x['title'],x['description'],x['url'].replace('https://',''),link=x['url'])
section('Awards & scholarships')
for award in p['awards']:
    story.append(para('&#8226; '+text(award),'SmallCV'))

def footer(canvas, doc):
    canvas.setFont('Helvetica',7)
    canvas.setFillColor(muted)
    canvas.drawString(18*mm,12*mm,'Rui Yu | '+p['email'])
    canvas.drawRightString(A4[0]-18*mm,12*mm,'Updated '+p['updated']+' | '+str(doc.page))

doc = SimpleDocTemplate(str(output),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=15*mm,bottomMargin=19*mm,
    title='Rui Yu - Curriculum Vitae',author='Rui Yu',subject='Computer vision and machine learning',pageCompression=1)
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(output)
