import re

with open('/home/yousefmsm1/Desktop/pdf_gen/output/html/ICPC-HUE-Community-Progress-Report-Gamma-Style.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update all footers to "of 14"
html = re.sub(r'of 13</div>', 'of 14</div>', html)

# Let's inspect sections
sections = re.findall(r'<section class=\"page\">(.*?)</section>', html, re.DOTALL)
print(f'Current sections count: {len(sections)}')

# Page 5 (Section index 4) redesign:
page_5_html = """  <!-- ================= PAGE 5: OUTREACH & RECRUITMENT ================= -->
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
    <div class="grid-3" style="margin-bottom: 14px;">
      <div class="card-white" style="border-left: 4px solid var(--accent); padding: 12px 14px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
          <div class="card-title" style="margin: 0; font-size: 12px;">43K+ Facebook Views</div>
          <span class="pill-tag" style="font-size: 7.5px; padding: 2px 6px;">Reach</span>
        </div>
        <p class="card-body" style="font-size: 9.8px; line-height: 1.45;">
          A synchronized campaign published travel footage and updates, generating <strong>43,000+ views on Facebook</strong> and establishing competitive programming as a recognized university endeavor.
        </p>
      </div>

      <div class="card-white" style="border-left: 4px solid var(--accent); padding: 12px 14px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
          <div class="card-title" style="margin: 0; font-size: 12px;">Educational Video Series</div>
          <span class="pill-tag" style="font-size: 7.5px; padding: 2px 6px;">Outreach</span>
        </div>
        <p class="card-body" style="font-size: 9.8px; line-height: 1.45;">
          Three professionally edited videos welcomed incoming freshmen, illustrating problem-solving concepts, showcasing student achievements, and outlining upcoming training cohorts.
        </p>
      </div>

      <div class="card-white" style="border-left: 4px solid var(--accent); padding: 12px 14px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
          <div class="card-title" style="margin: 0; font-size: 12px;">Hire Up Recruitment</div>
          <span class="pill-tag" style="font-size: 7.5px; padding: 2px 6px;">Intake</span>
        </div>
        <p class="card-body" style="font-size: 9.8px; line-height: 1.45;">
          Launched recruitment via <a href="https://icpchue.com/job" class="custom-link">icpchue.com/job</a> for student instructors, mentors, media creators, and operations officers to formalize staffing.
        </p>
      </div>
    </div>

    <!-- 2 Large Feature Photos (Travel & Celebration) -->
    <div class="grid-2" style="gap: 14px; margin-bottom: 14px;">
      <div>
        <div class="photo-box" style="height: 165px; margin-bottom: 5px;">
          <img src="../../report/ecpc_qulifcatio/FB_IMG_1790132541422.jpg" alt="Delegation Bus Travel to Alexandria">
        </div>
        <div class="photo-caption" style="font-size: 9.5px;">Delegation transit to Alexandria: building community synergy, morale, and focus.</div>
      </div>

      <div>
        <div class="photo-box" style="height: 165px; margin-bottom: 5px;">
          <img src="../../report/ecpc_qulifcatio/FB_IMG_1790132740356.jpg" alt="Delegation Tournament Celebration">
        </div>
        <div class="photo-caption" style="font-size: 9.5px;">Post-contest tournament celebration on the AASTMT Alexandria campus lawn.</div>
      </div>
    </div>

    <!-- Institutional Media Impact Card -->
    <div class="card-stripe" style="padding: 14px 18px;">
      <div class="card-title" style="font-size: 12.5px; color: var(--accent-dark); margin-bottom: 4px;">Institutional Impact &amp; Recruitment Surge</div>
      <p class="card-body" style="font-size: 10.2px; line-height: 1.55;">
        The high-visibility media coverage and viral social media reception directly accelerated community recruitment for the 2026/2027 season. Over 300 prospective freshmen and returning students registered interest via <strong>icpchue.com/job</strong> within the first 72 hours, laying the groundwork for our largest and most competitive intake to date.
      </p>
    </div>

    <div class="footer-bar">
      <div><strong>ICPC HUE</strong> • Annual Progress Dossier 2025 – 2027</div>
      <div>Page 05 of 14</div>
    </div>
  </section>"""

# New Page 6: The 16 Competing Teams at ECPC Qualifications
p6_teams = [
    ('FB_IMG_1790132708823.jpg', 'Team 01 (Team 2050)', 'Station 2050'),
    ('FB_IMG_1790132683848.jpg', 'Team 02 (Lead Solvers)', 'Station 2038'),
    ('FB_IMG_1790132657082.jpg', 'Team 03', 'Station Alpha'),
    ('FB_IMG_1790132659885.jpg', 'Team 04', 'Station Beta'),
    ('FB_IMG_1790132664255.jpg', 'Team 05', 'Station Gamma'),
    ('FB_IMG_1790132668477.jpg', 'Team 06', 'Station Delta'),
    ('FB_IMG_1790132686754.jpg', 'Team 07', 'Station Epsilon'),
    ('FB_IMG_1790132690995.jpg', 'Team 08', 'Station Zeta'),
    ('FB_IMG_1790132693865.jpg', 'Team 09', 'Station Eta'),
    ('FB_IMG_1790132696016.jpg', 'Team 10', 'Station Theta'),
    ('FB_IMG_1790132697858.jpg', 'Team 11', 'Station Iota'),
    ('FB_IMG_1790132699784.jpg', 'Team 12', 'Station Kappa'),
    ('FB_IMG_1790132702043.jpg', 'Team 13', 'Station Lambda'),
    ('FB_IMG_1790132703739.jpg', 'Team 14', 'Station Mu'),
    ('FB_IMG_1790132705475.jpg', 'Team 15', 'Station Nu'),
    ('FB_IMG_1790132707334.jpg', 'Team 16', 'Station Xi'),
]

team_cards_html = ''
for img_name, team_name, station_label in p6_teams:
    team_cards_html += f'''        <div style="background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 8px; overflow: hidden; display: flex; flex-direction: column;">
          <div class="photo-box" style="height: 84px; margin: 0; border-radius: 0;">
            <img src="../../report/ecpc_qulifcatio/{img_name}" alt="{team_name}">
          </div>
          <div style="display: flex; justify-content: space-between; align-items: center; padding: 4px 6px; background: #FFFFFF; font-size: 8.2px; font-weight: 700; color: #111;">
            <span>{team_name}</span>
            <span style="color: var(--accent-dark); font-size: 7.2px; font-weight: 800;">{station_label}</span>
          </div>
        </div>\n'''

new_page_6_html = f"""  <!-- ================= PAGE 6: 16 COMPETING TEAMS SHOWCASE ================= -->
  <section class="page">
    <div class="header-bar">
      <div class="inst-badge">
        <img src="../../report/assets/horus_logo.png" class="inst-logo" alt="Horus University Logo">
        <div class="inst-text">Horus University — Egypt • <span class="inst-sub">ICPC HUE Community</span></div>
      </div>
      <div class="pill-tag">05 / National Delegation</div>
    </div>

    <div class="kicker">
      <div class="kicker-bar"></div>
      <span>National Collegiate Delegation</span>
    </div>
    <h1 class="slide-title">Our 16 Competing Teams at ECPC Qualifications</h1>
    <p class="slide-sub">
      48 student competitors representing the Faculty of Artificial Intelligence and Faculty of Engineering across 16 official tournament stations at AASTMT, Alexandria.
    </p>

    <!-- Delegation Key Metrics Banner -->
    <div class="grid-4" style="margin-bottom: 12px;">
      <div class="card" style="padding: 8px 12px;">
        <div style="font-size: 15px; font-weight: 800; color: var(--text-head);">16 Teams</div>
        <div style="font-size: 8.5px; font-weight: 700; color: var(--accent-dark); text-transform: uppercase;">Official Delegation</div>
      </div>
      <div class="card" style="padding: 8px 12px;">
        <div style="font-size: 15px; font-weight: 800; color: var(--text-head);">48 Students</div>
        <div style="font-size: 8.5px; font-weight: 700; color: var(--accent-dark); text-transform: uppercase;">Active Competitors</div>
      </div>
      <div class="card" style="padding: 8px 12px;">
        <div style="font-size: 15px; font-weight: 800; color: var(--text-head);">2 Faculties</div>
        <div style="font-size: 8.5px; font-weight: 700; color: var(--accent-dark); text-transform: uppercase;">AI &amp; Engineering</div>
      </div>
      <div class="card" style="padding: 8px 12px;">
        <div style="font-size: 15px; font-weight: 800; color: var(--text-head);">5 Hours</div>
        <div style="font-size: 8.5px; font-weight: 700; color: var(--accent-dark); text-transform: uppercase;">Continuous Solving</div>
      </div>
    </div>

    <!-- 4x4 Grid of 16 Teams -->
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 10px;">
{team_cards_html}    </div>

    <div class="footer-bar">
      <div><strong>ICPC HUE</strong> • Annual Progress Dossier 2025 – 2027</div>
      <div>Page 06 of 14</div>
    </div>
  </section>"""

# Find boundary of Page 5 and replace it with page_5_html + new_page_6_html
p5_marker = '<!-- ================= PAGE 5: OUTREACH & RECRUITMENT ================= -->'
p6_marker = '<!-- ================= PAGE 6: OPERATING COMMITTEES ================= -->'

idx_p5 = html.find(p5_marker)
idx_p6 = html.find(p6_marker)

assert idx_p5 != -1, 'p5_marker not found'
assert idx_p6 != -1, 'p6_marker not found'

# Replace Page 5 with (new page 5 + new page 6)
html_start = html[:idx_p5]
html_rest = html[idx_p6:]

# Now renumber pages in html_rest:
# Formerly Page 06 -> now Page 07
# Formerly Page 07 -> now Page 08
# ...
# Formerly Page 13 -> now Page 14

# Let's update footers and pill-tags in html_rest
page_replacements = [
    ('Page 06 of 14', 'Page 07 of 14'),
    ('05 / Operating Model', '06 / Operating Model'),
    ('<!-- ================= PAGE 6: OPERATING COMMITTEES ================= -->', '<!-- ================= PAGE 7: OPERATING COMMITTEES ================= -->'),
    
    ('Page 07 of 14', 'Page 08 of 14'),
    ('06 / Talent & Systems', '07 / Talent & Systems'),
    ('<!-- ================= PAGE 7: LEADERSHIP & PLATFORM ================= -->', '<!-- ================= PAGE 8: LEADERSHIP & PLATFORM ================= -->'),
    
    ('Page 08 of 14', 'Page 09 of 14'),
    ('07 / Ecosystem & Engagement', '08 / Ecosystem & Engagement'),
    ('<!-- ================= PAGE 8: PARTNERSHIPS & INTRO DAY ================= -->', '<!-- ================= PAGE 9: PARTNERSHIPS & INTRO DAY ================= -->'),
    
    ('Page 09 of 14', 'Page 10 of 14'),
    ('08 / Season Roadmap', '09 / Season Roadmap'),
    ('<!-- ================= PAGE 9: ROAD TO ICPC ROADMAP ================= -->', '<!-- ================= PAGE 10: ROAD TO ICPC ROADMAP ================= -->'),
    
    ('Page 10 of 14', 'Page 11 of 14'),
    ('09 / Academic Curriculum', '10 / Academic Curriculum'),
    ('<!-- ================= PAGE 10: ACADEMIC CURRICULUM & MILESTONES ================= -->', '<!-- ================= PAGE 11: ACADEMIC CURRICULUM & MILESTONES ================= -->'),
    
    ('Page 11 of 14', 'Page 12 of 14'),
    ('10 / Strategic Objectives', '11 / Strategic Objectives'),
    ('<!-- ================= PAGE 11: CONCLUSION & NEXT STRATEGIC OBJECTIVES ================= -->', '<!-- ================= PAGE 12: CONCLUSION & NEXT STRATEGIC OBJECTIVES ================= -->'),
    
    ('Page 12 of 14', 'Page 13 of 14'),
    ('11 / Community Leadership', '12 / Community Leadership'),
    ('<!-- ================= PAGE 12: MEET THE TEAM ================= -->', '<!-- ================= PAGE 13: MEET THE TEAM ================= -->'),
    
    ('Page 13 of 14', 'Page 14 of 14'),
    ('12 / Academic Governance', '13 / Academic Governance'),
    ('<!-- ================= PAGE 13: ACADEMIC SUPERVISION & SPECIAL THANKS ================= -->', '<!-- ================= PAGE 14: ACADEMIC SUPERVISION & SPECIAL THANKS ================= -->'),
]

# Apply replacements in reverse order of page numbers to avoid cascades
for old_s, new_s in reversed(page_replacements):
    html_rest = html_rest.replace(old_s, new_s)

final_html = html_start + page_5_html + '\n\n' + new_page_6_html + '\n\n' + html_rest

with open('/home/yousefmsm1/Desktop/pdf_gen/output/html/ICPC-HUE-Community-Progress-Report-Gamma-Style.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print('Generated 14-page report HTML successfully!')
