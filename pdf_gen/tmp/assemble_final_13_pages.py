import re

with open('/home/yousefmsm1/Desktop/pdf_gen/output/html/ICPC-HUE-Community-Progress-Report-Gamma-Style.html', 'r', encoding='utf-8') as f:
    current_html = f.read()

# Load recovered Page 6 and 7
with open('/home/yousefmsm1/Desktop/pdf_gen/tmp/extracted_p6_p7.txt', 'r', encoding='utf-8') as f:
    p6_p7_text = f.read().strip()

# Make sure p6_p7_text has proper footer page numbers: Page 06 of 13 and Page 07 of 13
p6_p7_text = re.sub(r'Page \d+ of \d+', lambda m: 'Page 06 of 13' if '05 / Operating Model' in p6_p7_text[:p6_p7_text.find(m.group(0))] else 'Page 07 of 13', p6_p7_text)
# More specifically:
p6_p7_text = re.sub(r'<div>Page 05 of \d+</div>', '<div>Page 06 of 13</div>', p6_p7_text)
p6_p7_text = re.sub(r'<div>Page 06 of \d+</div>', '<div>Page 07 of 13</div>', p6_p7_text)
p6_p7_text = re.sub(r'<div>Page 07 of \d+</div>', '<div>Page 07 of 13</div>', p6_p7_text)

# Let's inspect current_html up to Page 5
idx_p1 = current_html.find('<!-- ================= PAGE 1: COVER SLIDE ================= -->')
if idx_p1 == -1:
    idx_p1 = current_html.find('<section class="page">')

idx_p5 = current_html.find('<!-- ================= PAGE 5: OUTREACH & RECRUITMENT ================= -->')
if idx_p5 == -1:
    idx_p5 = current_html.find('04 / Outreach & Momentum')
    idx_p5 = current_html.rfind('<section class="page">', 0, idx_p5)

# Page 1 to 4 is from start to idx_p5
html_p1_to_p4 = current_html[:idx_p5]

# Enlarge Page 3 photos in html_p1_to_p4:
html_p1_to_p4 = html_p1_to_p4.replace('class="photo-box" style="height: 125px;"', 'class="photo-box" style="height: 175px;"')
html_p1_to_p4 = html_p1_to_p4.replace('class="photo-box" style="height: 180px;"', 'class="photo-box" style="height: 175px;"')

# Build Page 5 with 16 photos and NO caption text
p5_photos = [
    ('FB_IMG_1790132541422.jpg', 'Bus travel to Alexandria'),
    ('FB_IMG_1790132708823.jpg', 'Team 2050 in cubicle'),
    ('FB_IMG_1790132619620.jpg', 'Team trio in jerseys'),
    ('FB_IMG_1790132740356.jpg', 'Delegation cheer'),
    ('FB_IMG_1790132657082.jpg', 'Team problem solving'),
    ('FB_IMG_1790132659885.jpg', 'Station focus'),
    ('FB_IMG_1790132664255.jpg', 'Code review'),
    ('FB_IMG_1790132668477.jpg', 'Collaborative coding'),
    ('FB_IMG_1790132686754.jpg', 'Typing solutions'),
    ('FB_IMG_1790132690995.jpg', 'Sheet analysis'),
    ('FB_IMG_1790132693865.jpg', 'Contest balloon station'),
    ('FB_IMG_1790132696016.jpg', 'Tournament arena desk'),
    ('FB_IMG_1790132697858.jpg', 'Algorithm discussion'),
    ('FB_IMG_1790132699784.jpg', 'Teamwork in hall'),
    ('FB_IMG_1790132702043.jpg', 'Intensive problem triage'),
    ('FB_IMG_1790132707334.jpg', 'Scoreboard review'),
]

grid_items = ''
for img_name, alt_text in p5_photos:
    grid_items += f'''        <div class="photo-box" style="height: 96px; margin: 0; border-radius: 6px;">
          <img src="../../report/ecpc_qulifcatio/{img_name}" alt="{alt_text}">
        </div>\n'''

page_5_html = f'''  <!-- ================= PAGE 5: OUTREACH & RECRUITMENT ================= -->
  <section class="page">
    <div class="header-bar">
      <div class="inst-badge">
        <img src="../../report/assets/horus_logo.png" class="inst-logo" alt="Horus University Logo">
        <div class="inst-text">Horus University — Egypt • <span class="inst-sub">ICPC HUE Community</span></div>
      </div>
      <div class="pill-tag">04 / Outreach &amp; Momentum</div>
    </div>

    <div class="kicker">
      <div class="kicker-bar"></div>
      <span>Outreach &amp; Community Momentum</span>
    </div>
    <h1 class="slide-title">Converting Contest Experience into Season-Wide Momentum</h1>
    <p class="slide-sub">
      Documenting the tournament journey transformed competitive programming into an exciting, high-visibility activity across Horus University.
    </p>

    <!-- 3 Compact Cards in Grid -->
    <div class="grid-3" style="margin-bottom: 12px;">
      <div class="card-white" style="border-left: 4px solid var(--accent); padding: 10px 12px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 3px;">
          <div class="card-title" style="margin: 0; font-size: 11.5px;">43K+ Facebook Views</div>
          <span class="pill-tag" style="font-size: 7.5px; padding: 2px 6px;">Reach</span>
        </div>
        <p class="card-body" style="font-size: 9.5px; line-height: 1.4;">
          A synchronized campaign published travel footage and updates, generating <strong>43,000+ views on Facebook</strong> and establishing competitive programming as a recognized university endeavor.
        </p>
      </div>

      <div class="card-white" style="border-left: 4px solid var(--accent); padding: 10px 12px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 3px;">
          <div class="card-title" style="margin: 0; font-size: 11.5px;">Educational Video Series</div>
          <span class="pill-tag" style="font-size: 7.5px; padding: 2px 6px;">Outreach</span>
        </div>
        <p class="card-body" style="font-size: 9.5px; line-height: 1.4;">
          Three professionally edited videos welcomed incoming freshmen, illustrating problem-solving concepts, showcasing student achievements, and outlining upcoming training cohorts.
        </p>
      </div>

      <div class="card-white" style="border-left: 4px solid var(--accent); padding: 10px 12px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 3px;">
          <div class="card-title" style="margin: 0; font-size: 11.5px;">Hire Up Recruitment</div>
          <span class="pill-tag" style="font-size: 7.5px; padding: 2px 6px;">Intake</span>
        </div>
        <p class="card-body" style="font-size: 9.5px; line-height: 1.4;">
          Launched recruitment via <a href="https://icpchue.com/job" class="custom-link">icpchue.com/job</a> for student instructors, mentors, media creators, and operations officers to formalize staffing.
        </p>
      </div>
    </div>

    <!-- Multi-Photo Delegation Gallery (16 Photos) -->
    <div style="background: #FDF9F2; border: 1px solid var(--card-border); border-radius: 12px; padding: 10px;">
      <div style="font-size: 10px; font-weight: 800; color: var(--accent-dark); text-transform: uppercase; margin-bottom: 8px; letter-spacing: 0.04em;">
        Field Documentation • Delegation Journey &amp; National Competition Arena (16 Delegation Moments)
      </div>
      <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 7px;">
{grid_items}      </div>
    </div>

    <div class="footer-bar">
      <div><strong>ICPC HUE</strong> • Annual Progress Dossier 2025 – 2027</div>
      <div>Page 05 of 13</div>
    </div>
  </section>
'''

# Find Page 8 in current_html:
idx_p8 = current_html.find('<!-- ================= PAGE 8: PARTNERSHIPS & INTRO DAY ================= -->')
if idx_p8 == -1:
    idx_p8 = current_html.find('07 / Ecosystem & Engagement')
    idx_p8 = current_html.rfind('<section class="page">', 0, idx_p8)

# Everything from Page 8 to the end
html_p8_to_end = current_html[idx_p8:]

# Assemble the whole document
full_html = html_p1_to_p4 + page_5_html + '\n\n' + p6_p7_text + '\n\n' + html_p8_to_end

with open('/home/yousefmsm1/Desktop/pdf_gen/output/html/ICPC-HUE-Community-Progress-Report-Gamma-Style.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print("Saved assembled HTML.")
