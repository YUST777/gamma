from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from PIL import Image
from pathlib import Path
import os, textwrap, html

ROOT = Path('/home/yousefmsm1/Desktop/pdf_gen')
OUT = ROOT/'output/pdf/ICPC-HUE-Community-Progress-Report-Gamma-Style.pdf'
HTML_OUT = ROOT/'output/html/ICPC-HUE-Community-Progress-Report-Gamma-Style.html'
OUT.parent.mkdir(parents=True, exist_ok=True); HTML_OUT.parent.mkdir(parents=True, exist_ok=True)

# Fonts
pdfmetrics.registerFont(TTFont('Noto', '/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Noto-Bold', '/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Noto-Black', '/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'))

W,H = A4
BG = colors.HexColor('#FBF7F1')
INK = colors.HexColor('#2C170E')
MUTED = colors.HexColor('#775F52')
ORANGE = colors.HexColor('#E97817')
GOLD = colors.HexColor('#F1B22D')
PALE = colors.HexColor('#F6E7D1')
PALE2 = colors.HexColor('#EFE0CC')
WHITE = colors.white
GREEN = colors.HexColor('#385C4A')
DARK = colors.HexColor('#24130D')

# image sources
DCC = sorted((ROOT/'report/dcc').glob('*.jpg'))
ECPC = sorted((ROOT/'report/ecpc_qulifcatio').glob('*.jpg'))
# selected from contact sheets by visual inspection; fall back deterministically
img_dcc_hero = ROOT/'report/dcc/FB_IMG_1790132479548.jpg'
img_dcc_award = ROOT/'report/dcc/FB_IMG_1790132765397.jpg'
img_dcc_group = ROOT/'report/dcc/FB_IMG_1790132476044.jpg'
img_ecpc_bus = ROOT/'report/ecpc_qulifcatio/FB_IMG_1790132541422.jpg'
img_ecpc_team = ROOT/'report/ecpc_qulifcatio/FB_IMG_1790132683848.jpg'
img_ecpc_group = ROOT/'report/ecpc_qulifcatio/FB_IMG_1790132738501.jpg'


def wrap_text(c, text, x, y, width, font='Noto', size=10, leading=None, color=INK, max_lines=None):
    leading = leading or size*1.35
    words = text.split()
    lines=[]; cur=''
    # approximate width in points with stringWidth
    for w in words:
        t = w if not cur else cur+' '+w
        if pdfmetrics.stringWidth(t,font,size) <= width:
            cur=t
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    if max_lines and len(lines)>max_lines:
        lines=lines[:max_lines]
        while pdfmetrics.stringWidth(lines[-1]+'…',font,size)>width and lines[-1]: lines[-1]=lines[-1][:-1]
        lines[-1]+='…'
    c.setFillColor(color); c.setFont(font,size)
    for i,line in enumerate(lines):
        c.drawString(x, y-i*leading, line)
    return y-len(lines)*leading

def draw_rich(c, text, x, y, width, size=10, leading=None, color=INK, bold=False):
    leading = leading or size*1.38
    style = ParagraphStyle('p', fontName='Noto-Bold' if bold else 'Noto', fontSize=size, leading=leading, textColor=color, spaceAfter=0)
    p = Paragraph(text, style)
    w,h = p.wrap(width, 1000)
    p.drawOn(c,x,y-h)
    return y-h

def rounded(c,x,y,w,h,fill,stroke=None,r=12,sw=0.8):
    c.setFillColor(fill); c.setStrokeColor(stroke or fill); c.setLineWidth(sw); c.roundRect(x,y,w,h,r,fill=1,stroke=1 if stroke else 0)

def line(c,x1,y1,x2,y2,color=PALE2,sw=1):
    c.setStrokeColor(color); c.setLineWidth(sw); c.line(x1,y1,x2,y2)

def img_crop(c,path,x,y,w,h, radius=0, overlay=None):
    if not Path(path).exists():
        rounded(c,x,y,w,h,PALE2); return
    im=Image.open(path); iw,ih=im.size
    scale=max(w/iw,h/ih); nw,nh=iw*scale,ih*scale
    # draw centered crop; preserve aspect
    xx=x+(w-nw)/2; yy=y+(h-nh)/2
    c.saveState()
    if radius:
        p=c.beginPath(); p.roundRect(x,y,w,h,radius); c.clipPath(p,stroke=0,fill=0)
    c.drawImage(ImageReader(im),xx,yy,width=nw,height=nh,mask='auto')
    if overlay:
        c.setFillColor(overlay); c.rect(x,y,w,h,fill=1,stroke=0)
    c.restoreState()

def chip(c, text, x, y, fill=PALE, color=INK, pad=7, size=7.5):
    tw=pdfmetrics.stringWidth(text,'Noto-Bold',size)+pad*2
    rounded(c,x,y-4,tw,18,fill,r=9)
    c.setFillColor(color); c.setFont('Noto-Bold',size); c.drawString(x+pad,y+2,text)
    return tw

def page_base(c, label, page, section=None, dark=False):
    c.setFillColor(DARK if dark else BG); c.rect(0,0,W,H,fill=1,stroke=0)
    if not dark:
        c.setFillColor(ORANGE); c.rect(38,H-33,26,4,fill=1,stroke=0)
        c.setFont('Noto-Bold',8); c.setFillColor(MUTED); c.drawString(74,H-34,label.upper())
        line(c,38,31,W-38,31,PALE2,0.8)
        c.setFont('Noto',7.2); c.setFillColor(MUTED); c.drawRightString(W-38,18,f'ICPC HUE  •  {page:02d}')
    else:
        c.setFillColor(GOLD); c.rect(38,H-33,26,4,fill=1,stroke=0)
        c.setFont('Noto-Bold',8); c.setFillColor(colors.HexColor('#D8BFA7')); c.drawString(74,H-34,label.upper())
        c.setFont('Noto',7.2); c.setFillColor(colors.HexColor('#BDA692')); c.drawRightString(W-38,18,f'ICPC HUE  •  {page:02d}')

def title(c, kicker, heading, sub=None, x=42, y=H-86, width=W-84, dark=False, size=28):
    c.setFont('Noto-Bold',8.5); c.setFillColor(GOLD if dark else ORANGE); c.drawString(x,y,kicker.upper())
    c.setFont('Noto-Black',size); c.setFillColor(WHITE if dark else INK)
    # wrap heading manually by words at ~width
    words=heading.split(); lines=[]; cur=''
    for w in words:
        t=w if not cur else cur+' '+w
        if pdfmetrics.stringWidth(t,'Noto-Black',size)<=width: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    for i,l in enumerate(lines): c.drawString(x,y-30-i*(size+4),l)
    yy=y-30-len(lines)*(size+4)
    if sub:
        yy=draw_rich(c,sub,x,yy-6,width,size=10.5,leading=15,color=colors.HexColor('#E4D4C4') if dark else MUTED)
    return yy

def metric(c,x,y,w,h,value,label,fill=PALE, value_color=INK):
    rounded(c,x,y,w,h,fill,r=16)
    c.setFont('Noto-Black',27); c.setFillColor(value_color); c.drawString(x+15,y+h-34,value)
    c.setFont('Noto-Bold',8); c.setFillColor(MUTED if fill!=DARK else colors.HexColor('#D8BFA7')); c.drawString(x+15,y+14,label.upper())

def small_arrow(c,x,y):
    c.setFillColor(ORANGE); c.circle(x,y,9,fill=1,stroke=0); c.setFillColor(WHITE); c.setFont('Noto-Bold',11); c.drawCentredString(x,y-4,'→')

def draw_footer_note(c,text,x=42,y=47,width=W-84,dark=False):
    c.setFont('Noto',7.6); c.setFillColor(colors.HexColor('#C7AF9B') if dark else MUTED)
    wrap_text(c,text,x,y,width,size=7.6,leading=10,color=colors.HexColor('#C7AF9B') if dark else MUTED)

c=canvas.Canvas(str(OUT), pagesize=A4)

# 1 cover
page_base(c,'Community progress report',1,dark=True)
img_crop(c,img_ecpc_group,0,0,W,H,overlay=colors.Color(0.12,0.06,0.03,alpha=0.48))
# dark left panel for legibility
c.setFillColor(colors.Color(0.12,0.06,0.03,alpha=0.63)); c.rect(0,0,W,H,fill=1,stroke=0)
c.setFillColor(GOLD); c.rect(42,H-92,40,6,fill=1,stroke=0)
c.setFont('Noto-Bold',10); c.setFillColor(colors.HexColor('#E6D6C5')); c.drawString(42,H-120,'ICPC HUE  /  COMMUNITY REPORT')
c.setFont('Noto-Black',38); c.setFillColor(WHITE); c.drawString(42,H-205,'From one contest')
c.drawString(42,H-250,'to a repeatable')
c.setFillColor(GOLD); c.drawString(42,H-295,'ICPC pipeline.')
wrap_text(c,'August - September 2026  •  DCC 2026, ECPC participation, community development, and the 2026/2027 season',42,H-350,W-84,size=12,leading=17,color=colors.HexColor('#F0E3D6'))
rounded(c,42,80,220,45,colors.Color(1,1,1,alpha=0.10),stroke=colors.Color(1,1,1,alpha=0.30),r=12,sw=0.6)
c.setFont('Noto-Bold',8); c.setFillColor(colors.HexColor('#E8D7C5')); c.drawString(57,108,'Prepared for academic review')
c.setFont('Noto',9); c.setFillColor(WHITE); c.drawString(57,91,'Horus University  •  2026')
c.setFont('Noto',7.5); c.setFillColor(colors.HexColor('#D8BFA7')); c.drawRightString(W-42,29,'Photo: ECPC qualification delegation')
c.showPage()

# 2 snapshot
page_base(c,'The story in one view',2)
y=title(c,'01 / season snapshot','A season became an operating system.','The community moved from event preparation to a repeatable model for training, follow-up, recruitment, and partnerships.',size=27)
# big thesis card
rounded(c,42,y-128,W-84,106,INK,r=18)
c.setFont('Noto-Bold',12); c.setFillColor(GOLD); c.drawString(60,y-50,'THE SHIFT')
draw_rich(c,'<b>Prepare teams → learn from the qualifier → build the system that makes the next cycle stronger.</b>',60,y-69,W-120,size=16,leading=22,color=WHITE)
# metrics
my=y-170; gap=11; mw=(W-84-gap*3)/4
metric(c,42,my,mw,93,'43K+','Facebook views',fill=PALE)
metric(c,42+mw+gap,my,mw,93,'100+','DCC contestants',fill=PALE)
metric(c,42+(mw+gap)*2,my,mw,93,'4','community committees',fill=PALE)
metric(c,42+(mw+gap)*3,my,mw,93,'12','ECPC qualifier problems',fill=PALE)
# arc
c.setFont('Noto-Bold',9); c.setFillColor(ORANGE); c.drawString(42,my-47,'THE ARC')
steps=[('01','DCC','A practical test in Damietta'),('02','ECPC','Travel, practice, qualify'),('03','SYSTEM','Committees, mentors, platform'),('04','NEXT','A full 2026/2027 roadmap')]
sy=my-92; boxw=(W-84-30)/4
for i,(n,h,desc) in enumerate(steps):
    x=42+i*(boxw+10)
    c.setFillColor(PALE2); c.circle(x+12,sy+12,12,fill=1,stroke=0)
    c.setFont('Noto-Bold',7); c.setFillColor(ORANGE); c.drawCentredString(x+12,sy+9,n)
    c.setFont('Noto-Bold',11); c.setFillColor(INK); c.drawString(x+31,sy+8,h)
    wrap_text(c,desc,x+31,sy-8,boxw-32,size=8.1,leading=11,color=MUTED,max_lines=2)
    if i<3: small_arrow(c,x+boxw+5,sy+12)
draw_footer_note(c,'Evidence note: the report keeps the 16-team figure out until its meaning is confirmed. “5 communities” refers to DCC participants; strategic partnerships are listed separately.',dark=False)
c.showPage()

# 3 DCC
page_base(c,'DCC 2026 / Damietta',3)
y=title(c,'02 / proving ground','DCC made competitive programming tangible in Damietta.','A two-stage contest gave students a realistic preparation environment before ECPC and connected five communities around one event.',size=25)
# photo strip
img_crop(c,img_dcc_hero,42,y-194,240,160,radius=18)
img_crop(c,img_dcc_award,294,y-194,122,160,radius=18)
img_crop(c,img_dcc_group,428,y-194,W-470,160,radius=18)
c.setFont('Noto',7.2); c.setFillColor(MUTED); c.drawString(42,y-208,'DCC classroom session'); c.drawString(294,y-208,'Awards and recognition'); c.drawString(428,y-208,'Community gathering')
# phases
py=y-255
c.setFont('Noto-Bold',9); c.setFillColor(ORANGE); c.drawString(42,py,'THE FORMAT')
phases=[('01','Online qualification','Students tested their readiness in a real contest environment.'),('02','Offline final','The event became a shared, in-person learning experience.')]
for i,(num,h,desc) in enumerate(phases):
    x=42+i*260
    rounded(c,x,py-102,242,78,PALE,r=14)
    c.setFont('Noto-Black',22); c.setFillColor(ORANGE); c.drawString(x+15,py-53,num)
    c.setFont('Noto-Bold',11); c.setFillColor(INK); c.drawString(x+54,py-42,h)
    wrap_text(c,desc,x+54,py-58,170,size=8.2,leading=11,color=MUTED,max_lines=2)
# bottom proof
rounded(c,42,84,W-84,82,INK,r=16)
c.setFont('Noto-Bold',8); c.setFillColor(GOLD); c.drawString(59,143,'WHAT IT PROVED')
draw_rich(c,'<b>ICPC HUE placed ninth in the online qualification</b> while also helping deliver the event infrastructure. Yousef Mohamed built <b>dcchub.xyz</b>, the official DCC website.',59,128,W-118,size=10.5,leading=15,color=WHITE)
draw_footer_note(c,'DCC participants: ICPC MNU, ICPC HUE, ICPC DELTA, ACPC DU, and ACPC NDETI.',y=66)
c.showPage()

# 4 ECPC
page_base(c,'ECPC qualification',4)
y=title(c,'03 / field experience','The qualifier turned preparation into evidence.','The delegation travelled on August 18, completed the practice contest, and faced a twelve-problem qualification round the following day.',size=25)
# journey line
jy=y-78
c.setStrokeColor(PALE2); c.setLineWidth(3); c.line(64,jy,530,jy)
journey=[('AUG 18','Travel & arrival'),('AUG 19','Practice contest'),('QUALIFIER','12 problems')]
for i,(lab,desc) in enumerate(journey):
    x=74+i*225
    c.setFillColor(ORANGE if i==2 else GOLD); c.circle(x,jy,10,fill=1,stroke=0)
    c.setFont('Noto-Bold',8); c.setFillColor(ORANGE if i<2 else ORANGE); c.drawString(x-15,jy-29,lab)
    c.setFont('Noto',8.2); c.setFillColor(MUTED); c.drawString(x-15,jy-43,desc)
# photos
img_crop(c,img_ecpc_bus,42,y-280,160,142,radius=16)
img_crop(c,img_ecpc_team,213,y-280,160,142,radius=16)
img_crop(c,img_ecpc_group,384,y-280,169,142,radius=16)
# metrics row
my=y-330; gap=12; mw=(W-84-gap*2)/3
metric(c,42,my,mw,86,'12','problems in the qualifier',fill=PALE)
metric(c,42+mw+gap,my,mw,86,'3+','solved by most teams',fill=PALE)
metric(c,42+(mw+gap)*2,my,mw,86,'4','solved by the leading team',fill=PALE)
rounded(c,42,84,W-84,62,PALE2,r=14)
c.setFont('Noto-Bold',8); c.setFillColor(ORANGE); c.drawString(58,125,'THE LESSON')
draw_rich(c,'The gap to the next stage became concrete: earlier preparation, consistent follow-up, and more practice under contest conditions.',58,111,W-116,size=10.2,leading=14,color=INK)
c.showPage()

# 5 what changed
page_base(c,'After ECPC',5)
y=title(c,'04 / turning proof into momentum','The competition experience became a recruitment engine.','The team published the journey, documented the people behind it, and used the attention to bring more students into the next season.',size=25)
# big number left
rounded(c,42,y-205,188,164,INK,r=18)
c.setFont('Noto-Black',45); c.setFillColor(GOLD); c.drawString(62,y-112,'43K+')
c.setFont('Noto-Bold',10); c.setFillColor(WHITE); c.drawString(63,y-139,'FACEBOOK VIEWS')
wrap_text(c,'Season-launch content widened awareness beyond the competition itself.',63,y-166,140,size=9.1,leading=13,color=colors.HexColor('#E6D6C5'))
# right cards
cards=[('Document','Teams, travel, and competition photos made the work visible.'),('Invite','Three additional videos introduced competitive programming and the community.'),('Convert','The next season opened with a clearer reason to join and a defined pathway.')]
for i,(h,desc) in enumerate(cards):
    yy=y-64-i*66
    rounded(c,254,yy-50,W-296,53,PALE,r=12)
    c.setFont('Noto-Bold',10); c.setFillColor(INK); c.drawString(270,yy-18,h)
    wrap_text(c,desc,270,yy-32,W-330,size=8.4,leading=11,color=MUTED,max_lines=2)
# takeaway
rounded(c,42,84,W-84,72,ORANGE,r=16)
c.setFont('Noto-Bold',8); c.setFillColor(WHITE); c.drawString(59,132,'THE CHANGE IN MINDSET')
draw_rich(c,'The contest stopped being a single event. It became the first chapter of the 2026/2027 operating model.',59,118,W-118,size=11,leading=15,color=WHITE)
c.showPage()

# 6 committees
page_base(c,'Operating model',6)
y=title(c,'05 / four committees','The new season has a clearer division of responsibility.','Each committee answers a different failure mode: technical gaps, inconsistent follow-up, low visibility, or weak operations.',size=25)
items=[('INSTRUCTORS','Teach, solve, and communicate with patience.','Technical confidence'),('MENTORS','Follow teams, review progress, and protect consistency.','Daily continuity'),('MEDIA','Document the work and make the invitation visible.','Reach and recruitment'),('OPERATIONS','Coordinate events, materials, logistics, and flow.','Reliable delivery')]
card_w=(W-84-12)/2; card_h=116
for i,(h,desc,tag) in enumerate(items):
    col=i%2; row=i//2; x=42+col*(card_w+12); yy=y-80-row*(card_h+14)-card_h
    rounded(c,x,yy,card_w,card_h,PALE if i!=2 else PALE2,r=16)
    c.setFillColor(ORANGE if i!=2 else GREEN); c.circle(x+25,yy+card_h-28,11,fill=1,stroke=0)
    c.setFont('Noto-Bold',9); c.setFillColor(WHITE); c.drawCentredString(x+25,yy+card_h-31,str(i+1))
    c.setFont('Noto-Bold',11); c.setFillColor(INK); c.drawString(x+45,yy+card_h-32,h)
    wrap_text(c,desc,x+18,yy+card_h-58,card_w-36,size=9,leading=13,color=MUTED,max_lines=3)
    chip(c,tag,x+18,yy+13,fill=WHITE,color=ORANGE if i!=2 else GREEN,pad=7,size=7.2)
rounded(c,42,75,W-84,50,INK,r=14)
c.setFont('Noto-Bold',8); c.setFillColor(GOLD); c.drawString(58,106,'DESIGN PRINCIPLE')
c.setFont('Noto',9.3); c.setFillColor(WHITE); c.drawString(58,90,'Students choose the role where they can contribute most effectively.')
c.showPage()

# 7 leadership/platform
page_base(c,'Leadership + platform',7)
y=title(c,'06 / from talent to follow-up','The system connects selection, teaching, and daily practice.','Top teams were interviewed, candidates taught back advanced topics, and the platform turned progress into a shared record.',size=25)
# workflow
steps=[('TOP 5','Interview the leading teams'),('5 DAYS','Study + teach back STL / vectors'),('HIRE UP','Invite students into roles'),('DAILY LOG','Students record sheets + problems'),('MENTOR LOOP','Review gaps and respond early')]
sy=y-92; start=42; gap=9; sw=(W-84-gap*4)/5
for i,(h,desc) in enumerate(steps):
    x=start+i*(sw+gap)
    rounded(c,x,sy-91,sw,78,PALE if i<3 else PALE2,r=13)
    c.setFont('Noto-Black',12); c.setFillColor(ORANGE); c.drawString(x+11,sy-39,h)
    wrap_text(c,desc,x+11,sy-57,sw-22,size=7.4,leading=10,color=MUTED,max_lines=3)
    if i<4: small_arrow(c,x+sw+gap/2,sy-52)
# platform panel
rounded(c,42,180,W-84,152,INK,r=18)
c.setFont('Noto-Bold',8); c.setFillColor(GOLD); c.drawString(59,307,'THE PLATFORM LOOP')
draw_rich(c,'<b>Student action</b> → submit a sheet or problem log  •  <b>Mentor signal</b> → see gaps and stalled progress  •  <b>Targeted support</b> → feedback before a small gap becomes a season-long one.',59,291,W-118,size=11,leading=16,color=WHITE)
line(c,59,240,W-59,240,colors.HexColor('#5F4030'),0.8)
c.setFont('Noto',8.8); c.setFillColor(colors.HexColor('#E6D6C5')); c.drawString(59,219,'The goal is not only to count solved problems. It is to understand how students are building reliable habits.')
rounded(c,42,88,W-84,58,ORANGE,r=15)
c.setFont('Noto-Bold',8); c.setFillColor(WHITE); c.drawString(59,125,'RECRUITMENT')
c.setFont('Noto',10); c.setFillColor(WHITE); c.drawString(59,106,'Hire Up applications:  icpchue.com/job')
c.showPage()

# 8 network & launch
page_base(c,'Ecosystem + launch',8)
y=title(c,'07 / beyond one campus','Partnerships make the learning network larger than Horus University.','DCC opened relationships with communities that can share experience, co-train instructors, and give students a broader competitive context.',size=24)
# partner nodes
cx,cy=170,y-150
c.setFillColor(ORANGE); c.circle(cx,cy,35,fill=1,stroke=0)
c.setFont('Noto-Black',11); c.setFillColor(WHITE); c.drawCentredString(cx,cy-4,'HUE')
partners=[('ACPC Club\nDamietta University',390,y-87),('ICPC PSU',390,y-155),('ICPC Assiut\nUniversity',390,y-223)]
for txt,x,yy in partners:
    line(c,cx+35,cy,x-16,yy,PALE2,1.8)
    c.setFillColor(GOLD); c.circle(x-16,yy,9,fill=1,stroke=0)
    for j,l in enumerate(txt.split('\n')):
        c.setFont('Noto-Bold',9); c.setFillColor(INK); c.drawString(x,yy+4-j*12,l)
wrap_text(c,'Collaboration around DCC, bronze-medal experience, and instructor development.',42,y-260,240,size=9,leading=13,color=MUTED)
# launch card
rounded(c,42,92,W-84,122,PALE,r=17)
c.setFont('Noto-Bold',9); c.setFillColor(ORANGE); c.drawString(60,188,'INTRODUCTION DAY / MAKE THE NEXT STEP FEEL REAL')
launch=['Recognition certificates for the top five teams','Financial prize checks and free T-shirts','Printed flyers, community flag, and roll-up banner','Welcome gifts and a qualified competitor as guest speaker']
for i,t in enumerate(launch):
    yy=166-i*18
    c.setFillColor(GREEN); c.circle(67,yy+2,4,fill=1,stroke=0)
    c.setFont('Noto',8.8); c.setFillColor(INK); c.drawString(79,yy-1,t)
c.showPage()

# 9 roadmap
page_base(c,'Road to ICPC 2026/2027',9)
y=title(c,'08 / the roadmap','Seven phases turn an intake into a competition-ready team.','The plan moves from orientation and foundations to advanced algorithms, internal selection, and final ECPC simulation.',size=25)
ph=[('01','RECRUIT','Aug-Oct 2026','Campaign → applications → orientation'),('02','FOUNDATIONS','Oct-Nov 2026','C++ basics, loops, arrays, strings, functions'),('03','STL','Nov 2026-Jan 2027','Vectors, stacks, queues, sets, maps, checkpoint'),('04','CORE','Feb-Mar 2027','Prefix sums, two pointers, binary search, greedy, recursion'),('05','ADVANCED','Mar-Apr 2027','Math, DP, graphs, progress review'),('06','SELECT','Apr-Jun 2027','Team formation, trials, selection contest'),('07','FINAL PREP','Jun-Aug 2027','Weekly contests → full simulation → ECPC')]
row_h=63; yy=y-84
for i,(n,h,dates,desc) in enumerate(ph):
    y0=yy-i*row_h
    rounded(c,42,y0-row_h+6,W-84,row_h-9,PALE if i%2==0 else colors.HexColor('#F3EBDD'),r=12)
    c.setFont('Noto-Black',13); c.setFillColor(ORANGE); c.drawString(57,y0-33,n)
    c.setFont('Noto-Bold',10); c.setFillColor(INK); c.drawString(99,y0-24,h)
    c.setFont('Noto-Bold',7.5); c.setFillColor(GREEN); c.drawString(99,y0-39,dates.upper())
    wrap_text(c,desc,245,y0-24,310,size=8.2,leading=11,color=MUTED,max_lines=2)
# note
rounded(c,42,74,W-84,38,INK,r=12)
c.setFont('Noto',7.8); c.setFillColor(colors.HexColor('#E7D7C8')); c.drawString(58,89,'Roadmap note: the warm-up contest is presented as January 29, 2027 to match the sequence after the winter break.')
c.showPage()

# 10 appendix detailed calendar
page_base(c,'Appendix / selected calendar',10)
y=title(c,'09 / selected checkpoints','The detailed calendar keeps the system accountable.','The full source roadmap contains 46 milestones. This condensed view keeps the dates visible without turning the narrative into a spreadsheet.',size=24)
# two-column tables
left=[('AUG 29-SEP 3','Promotion campaign'),('SEP 5-10','Application form open'),('SEP 12-17','Screening + interviews'),('SEP 18','Results announced'),('SEP 26-OCT 1','Orientation period'),('OCT 9','Introductory session'),('OCT 16','Variables, data types, conditions'),('OCT 23','Loops and nested loops'),('OCT 30','Arrays and built-in functions'),('NOV 6','Strings'),('NOV 13','Functions'),('NOV 20','Time + space complexity')]
right=[('NOV 27','STL: vectors + pairs'),('DEC 4','STL: stacks, queues, deques'),('DEC 11','STL: sets + maps'),('DEC 18','Priority queues + structs'),('JAN 29, 2027','Warm-up contest'),('FEB 5','Frequency + prefix arrays'),('FEB 12','Two pointers + sliding window'),('FEB 19','Binary search'),('FEB 26','Greedy algorithms'),('MAR 5','Recursion + brute force'),('MAR 12','Backtracking'),('MAR 19','Bitmasking')]
for col,data in enumerate([left,right]):
    x=42+col*263
    c.setFont('Noto-Bold',8); c.setFillColor(ORANGE); c.drawString(x,y-54,'FOUNDATIONS' if col==0 else 'TECHNIQUES')
    yy=y-73
    for i,(date,desc) in enumerate(data):
        h=33
        rounded(c,x,yy-h,242,h-3,PALE if i%2==0 else colors.HexColor('#F3EBDD'),r=8)
        c.setFont('Noto-Bold',7.4); c.setFillColor(GREEN); c.drawString(x+10,yy-17,date)
        c.setFont('Noto',8.1); c.setFillColor(INK); c.drawString(x+95,yy-17,desc)
        yy-=h
# bottom note
wrap_text(c,'The remaining checkpoints cover diagnostics, mathematics, dynamic programming, graph algorithms, team trials, the selection contest, weekly contests, and the full ECPC simulation.',42,93,W-84,size=8.5,leading=12,color=MUTED)
c.showPage()

# 11 conclusion
page_base(c,'Next objectives',11,dark=True)
c.setFont('Noto-Bold',8.5); c.setFillColor(GOLD); c.drawString(42,H-86,'10 / WHAT HAPPENS NEXT')
c.setFont('Noto-Black',31); c.setFillColor(WHITE); c.drawString(42,H-140,'Build the path')
c.setFillColor(GOLD); c.drawString(42,H-180,'one cycle earlier.')
wrap_text(c,'The 2026 ECPC cycle showed that ICPC HUE can organize, compete, learn, and build a stronger system at the same time.',42,H-225,W-84,size=12,leading=17,color=colors.HexColor('#E6D6C5'))
# four actions
acts=['Expand the instructor and mentor pipeline.','Use the platform as the daily training record.','Continue joint training with partner communities.','Start structured preparation earlier so more teams reach ECPC.']
for i,a in enumerate(acts):
    yy=H-335-i*62
    rounded(c,42,yy-43,W-84,48,colors.Color(1,1,1,alpha=0.10),stroke=colors.Color(1,1,1,alpha=0.22),r=12,sw=0.5)
    c.setFont('Noto-Black',15); c.setFillColor(GOLD); c.drawString(59,yy-24,f'0{i+1}')
    c.setFont('Noto-Bold',10.2); c.setFillColor(WHITE); c.drawString(102,yy-22,a)
rounded(c,42,76,W-84,60,ORANGE,r=16)
c.setFont('Noto-Bold',8); c.setFillColor(WHITE); c.drawString(59,116,'LONG-TERM OBJECTIVE')
draw_rich(c,'Create a sustainable competitive programming culture at Horus University-from the first problem solved to the highest levels of collegiate competition.',59,102,W-118,size=10.3,leading=14,color=WHITE)
c.setFont('Noto',7.5); c.setFillColor(colors.HexColor('#C7AF9B')); c.drawRightString(W-42,29,'ICPC HUE  •  August-September 2026')
c.showPage()

c.save()

# companion HTML prototype for Gamma-style editing / importing
html_content = '''<!doctype html><html><head><meta charset="utf-8"><title>ICPC HUE Community Progress Report</title><style>
:root{--ink:#2c170e;--orange:#e97817;--gold:#f1b22d;--bg:#fbf7f1;--muted:#775f52;--pale:#f6e7d1}*{box-sizing:border-box}body{margin:0;background:#eee7df;font-family:Arial,sans-serif;color:var(--ink)}.deck{max-width:1100px;margin:auto}.page{min-height:720px;background:var(--bg);padding:56px 64px;position:relative;overflow:hidden;margin:26px 0;box-shadow:0 12px 40px #0001}.dark{background:var(--ink);color:white}.kicker{color:var(--orange);font-weight:700;letter-spacing:.12em;font-size:12px}.dark .kicker{color:var(--gold)}h1{font-size:44px;line-height:1.02;margin:18px 0 12px;max-width:780px}h2{font-size:32px;line-height:1.08;margin:16px 0 12px}.sub{font-size:17px;line-height:1.45;color:var(--muted);max-width:780px}.dark .sub{color:#e4d4c4}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:34px}.metric,.card{background:var(--pale);border-radius:18px;padding:20px}.metric b{font-size:40px;display:block}.metric span{font-size:12px;text-transform:uppercase;font-weight:700;color:var(--muted)}.cards{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin-top:30px}.card h3{margin:0 0 8px}.card p{color:var(--muted);line-height:1.45}.hero{height:320px;width:100%;object-fit:cover;border-radius:20px;margin:25px 0}.footer{position:absolute;bottom:22px;left:64px;right:64px;color:#9d8677;font-size:11px;border-top:1px solid #eadbca;padding-top:12px}@media(max-width:700px){.page{padding:35px 26px}.grid,.cards{grid-template-columns:1fr 1fr}h1{font-size:36px}.footer{left:26px;right:26px}}
</style></head><body><div class="deck">
<section class="page dark"><div class="kicker">ICPC HUE / COMMUNITY REPORT</div><h1>From one contest<br>to a repeatable<br><span style="color:var(--gold)">ICPC pipeline.</span></h1><p class="sub">August - September 2026 · DCC 2026, ECPC participation, community development, and the 2026/2027 season</p><div class="footer">Prepared for academic review · Horus University · 2026</div></section>
<section class="page"><div class="kicker">01 / SEASON SNAPSHOT</div><h2>A season became an operating system.</h2><p class="sub">The community moved from event preparation to a repeatable model for training, follow-up, recruitment, and partnerships.</p><div class="grid"><div class="metric"><b>43K+</b><span>Facebook views</span></div><div class="metric"><b>100+</b><span>DCC contestants</span></div><div class="metric"><b>4</b><span>community committees</span></div><div class="metric"><b>12</b><span>ECPC qualifier problems</span></div></div><div class="footer">DCC participants and strategic partnerships are reported separately.</div></section>
<section class="page"><div class="kicker">02 / PROVING GROUND</div><h2>DCC made competitive programming tangible in Damietta.</h2><p class="sub">A two-stage contest gave students a realistic preparation environment before ECPC and connected five communities around one event.</p><div class="cards"><div class="card"><h3>01 · Online qualification</h3><p>Students tested their readiness in a real contest environment.</p></div><div class="card"><h3>02 · Offline final</h3><p>The event became a shared, in-person learning experience.</p></div></div><div class="footer">ICPC HUE placed ninth in the online qualification; dcchub.xyz was built by Yousef Mohamed.</div></section>
<section class="page"><div class="kicker">03 / FIELD EXPERIENCE</div><h2>The qualifier turned preparation into evidence.</h2><p class="sub">Travel → practice contest → twelve-problem qualifier. Most teams solved at least three problems; the leading team solved four.</p><div class="grid"><div class="metric"><b>12</b><span>problems</span></div><div class="metric"><b>3+</b><span>solved by most</span></div><div class="metric"><b>4</b><span>leading team</span></div><div class="metric"><b>Aug 18</b><span>delegation travel</span></div></div><div class="footer">The next cycle prioritizes earlier preparation, daily follow-up, and more practice under contest conditions.</div></section>
<section class="page"><div class="kicker">04 / THE SHIFT</div><h2>The competition experience became a recruitment engine.</h2><p class="sub">The team documented the journey, made the work visible, and used the attention to bring more students into the next season.</p><div class="cards"><div class="card"><h3>Document</h3><p>Teams, travel, and competition photos made the work visible.</p></div><div class="card"><h3>Invite</h3><p>Three additional videos introduced competitive programming and the community.</p></div><div class="card"><h3>Convert</h3><p>The next season opened with a clearer reason to join and a defined pathway.</p></div><div class="card"><h3>Result</h3><p>43K+ Facebook views from season-launch content.</p></div></div></section>
<section class="page"><div class="kicker">05 / OPERATING MODEL</div><h2>Four committees make the work legible.</h2><p class="sub">Each committee answers a different failure mode: technical gaps, inconsistent follow-up, low visibility, or weak operations.</p><div class="cards"><div class="card"><h3>Instructors</h3><p>Teach, solve, and communicate with patience.</p></div><div class="card"><h3>Mentors</h3><p>Follow teams, review progress, and protect consistency.</p></div><div class="card"><h3>Media</h3><p>Document the work and make the invitation visible.</p></div><div class="card"><h3>Operations</h3><p>Coordinate events, materials, logistics, and flow.</p></div></div></section>
<section class="page"><div class="kicker">06 / LEADERSHIP + PLATFORM</div><h2>Talent becomes follow-up.</h2><p class="sub">Top teams were interviewed, candidates taught back advanced topics, and the platform turned progress into a shared record.</p><div class="cards"><div class="card"><h3>Top 5 → 5-day teach-back</h3><p>Study STL, vectors, and advanced topics, then explain the material to the community.</p></div><div class="card"><h3>Daily log → mentor loop</h3><p>Students record sheets and problems; mentors spot gaps and respond early.</p></div></div></section>
<section class="page"><div class="kicker">07 / ECOSYSTEM</div><h2>Partnerships make the learning network larger than one campus.</h2><p class="sub">DCC opened relationships with ACPC Club Damietta University, ICPC PSU, and ICPC Assiut University Community.</p><div class="cards"><div class="card"><h3>Share experience</h3><p>Connect students to teams with more competition history.</p></div><div class="card"><h3>Co-train instructors</h3><p>Build a stronger teaching and mentoring pipeline.</p></div></div></section>
<section class="page"><div class="kicker">08 / ROAD TO ICPC</div><h2>Seven phases turn an intake into a competition-ready team.</h2><div class="cards"><div class="card"><h3>01-02 · Recruit + foundations</h3><p>Aug-Nov 2026 · applications, orientation, C++ basics.</p></div><div class="card"><h3>03-04 · STL + core techniques</h3><p>Nov 2026-Mar 2027 · containers, search, greedy, recursion.</p></div><div class="card"><h3>05-06 · Advanced + selection</h3><p>Mar-Jun 2027 · DP, graphs, team trials, selection contest.</p></div><div class="card"><h3>07 · Final preparation</h3><p>Jun-Aug 2027 · weekly contests, full simulation, ECPC.</p></div></div></section>
<section class="page dark"><div class="kicker">09 / NEXT OBJECTIVES</div><h2>Build the path one cycle earlier.</h2><p class="sub">The 2026 ECPC cycle showed that ICPC HUE can organize, compete, learn, and build a stronger system at the same time.</p><div class="cards"><div class="card"><h3>01</h3><p>Expand the instructor and mentor pipeline.</p></div><div class="card"><h3>02</h3><p>Use the platform as the daily training record.</p></div><div class="card"><h3>03</h3><p>Continue joint training with partner communities.</p></div><div class="card"><h3>04</h3><p>Start structured preparation earlier.</p></div></div><div class="footer">Create a sustainable competitive programming culture at Horus University.</div></section>
</div></body></html>'''
HTML_OUT.write_text(html_content, encoding='utf-8')
print(OUT)
print(HTML_OUT)
