import re

with open('/home/yousefmsm1/Desktop/pdf_gen/output/html/ICPC-HUE-Community-Progress-Report-Gamma-Style.html', 'r', encoding='utf-8') as f:
    html = f.read()

# -------------------------------------------------------------
# FIX 1: Page 4 (ECPC Qualification)
# Delete any "Lead Team" or station / 2050 references
# -------------------------------------------------------------
html = html.replace('''          <div class="metric-card" style="padding: 12px 10px;">
            <div class="metric-val" style="font-size: 26px;">4</div>
            <div class="metric-label" style="font-size: 8.5px;">Lead Team</div>
            <p class="metric-desc">Within 1 problem of advancing.</p>
          </div>''', '''          <div class="metric-card" style="padding: 12px 10px;">
            <div class="metric-val" style="font-size: 26px;">4</div>
            <div class="metric-label" style="font-size: 8.5px;">Top Score</div>
            <p class="metric-desc">Within 1 problem of advancing.</p>
          </div>''')

# -------------------------------------------------------------
# FIX 2: Page 6 (Our 16 Competing Teams)
# Delete all "station", "Team 2050", "Lead Solvers", "Station Alpha", etc.
# Keep clean: Team 01, Team 02, ... Team 16
# -------------------------------------------------------------
# Subtitle in Page 6:
html = html.replace('across 16 official tournament stations at AASTMT, Alexandria.', 'across 16 official tournament teams at AASTMT, Alexandria.')

p6_teams_clean = [
    ('FB_IMG_1790132708823.jpg', 'Team 01'),
    ('FB_IMG_1790132683848.jpg', 'Team 02'),
    ('FB_IMG_1790132657082.jpg', 'Team 03'),
    ('FB_IMG_1790132659885.jpg', 'Team 04'),
    ('FB_IMG_1790132664255.jpg', 'Team 05'),
    ('FB_IMG_1790132668477.jpg', 'Team 06'),
    ('FB_IMG_1790132686754.jpg', 'Team 07'),
    ('FB_IMG_1790132690995.jpg', 'Team 08'),
    ('FB_IMG_1790132693865.jpg', 'Team 09'),
    ('FB_IMG_1790132696016.jpg', 'Team 10'),
    ('FB_IMG_1790132697858.jpg', 'Team 11'),
    ('FB_IMG_1790132699784.jpg', 'Team 12'),
    ('FB_IMG_1790132702043.jpg', 'Team 13'),
    ('FB_IMG_1790132703739.jpg', 'Team 14'),
    ('FB_IMG_1790132705475.jpg', 'Team 15'),
    ('FB_IMG_1790132707334.jpg', 'Team 16'),
]

clean_team_cards_html = ''
for img_name, team_name in p6_teams_clean:
    clean_team_cards_html += f'''        <div style="background: #FFFFFF; border: 1px solid var(--card-border); border-radius: 8px; overflow: hidden; display: flex; flex-direction: column;">
          <div class="photo-box" style="height: 86px; margin: 0; border-radius: 0;">
            <img src="../../report/ecpc_qulifcatio/{img_name}" alt="{team_name}">
          </div>
          <div style="text-align: center; padding: 5px 6px; background: #FFFFFF; font-size: 8.5px; font-weight: 700; color: #111;">
            {team_name}
          </div>
        </div>\n'''

# Find Page 6 grid in html and replace
p6_grid_start = '<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 10px;">'
idx_grid_s = html.find(p6_grid_start)
idx_grid_e = html.find('</div>\n\n    <div class="footer-bar">\n      <div><strong>ICPC HUE</strong> • Annual Progress Dossier 2025 – 2027</div>\n      <div>Page 06 of 14</div>', idx_grid_s)

if idx_grid_s != -1 and idx_grid_e != -1:
    html = html[:idx_grid_s + len(p6_grid_start) + 1] + clean_team_cards_html + '    ' + html[idx_grid_e:]
    print('Updated Page 6 team cards cleanly without any station or custom team text!')
else:
    print('Warning: could not locate Page 6 grid boundaries precisely:', idx_grid_s, idx_grid_e)

# -------------------------------------------------------------
# FIX 3: Reverse back the look of Page 11 (Curriculum & Milestones)
# Restore the clean white cards look
# -------------------------------------------------------------
original_page_11_curriculum = """  <!-- ================= PAGE 11: ACADEMIC CURRICULUM & MILESTONES ================= -->
  <section class="page">
    <div class="header-bar">
      <div class="inst-badge">
        <img src="../../report/assets/horus_logo.png" class="inst-logo" alt="Horus University Logo">
        <div class="inst-text">Horus University — Egypt • <span class="inst-sub">ICPC HUE Community</span></div>
      </div>
      <div class="pill-tag">10 / Academic Curriculum</div>
    </div>

    <div class="kicker">
      <div class="kicker-bar"></div>
      <span>Academic Appendix &amp; Milestones</span>
    </div>
    <h1 class="slide-title">2026/2027 Season Curriculum &amp; Milestones</h1>
    <p class="slide-sub">
      Comprehensive schedule of all 46 milestones across the academic year for faculty review and operational tracking.
    </p>

    <div class="grid-3" style="font-size: 9px; line-height: 1.45;">
      <!-- Column 1: Term 1 -->
      <div class="card-white" style="padding: 12px 14px;">
        <div style="font-size: 11px; font-weight: 700; color: var(--accent-dark); border-bottom: 1px solid var(--card-border); padding-bottom: 4px; margin-bottom: 8px;">
          Term 1: Foundations &amp; STL
        </div>
        <div style="display: flex; flex-direction: column; gap: 4px;">
          <div><strong>01.</strong> Promotion: Aug 29 – Sep 03</div>
          <div><strong>02.</strong> Applications Open: Sep 05 – Sep 10</div>
          <div><strong>03.</strong> Screening/Interviews: Sep 12 – Sep 17</div>
          <div><strong>04.</strong> Results: Sep 18</div>
          <div><strong>05.</strong> Orientation Day: Sep 26 – Oct 01</div>
          <div><strong>06.</strong> Form Reopen: Sep 26 – Oct 01</div>
          <div><strong>07.</strong> Intro Session: Oct 09 (8:30 PM)</div>
          <div><strong>08.</strong> Basics &amp; Conditions: Oct 16</div>
          <div><strong>09.</strong> Loops &amp; Nested Loops: Oct 23</div>
          <div><strong>10.</strong> Arrays &amp; Functions: Oct 30</div>
          <div><strong>11.</strong> Strings: Nov 06</div>
          <div><strong>12.</strong> Midterm Break: Nov 07 – Nov 12</div>
          <div><strong>13.</strong> Functions: Nov 13</div>
          <div><strong>14.</strong> Complexity (Big-O): Nov 20</div>
          <div><strong>15.</strong> Practice Contests: Nov 21 – Nov 26</div>
          <div><strong>16.</strong> Progress Check: Late Nov</div>
          <div><strong>17.</strong> STL Vector &amp; Pair: Nov 27</div>
          <div><strong>18.</strong> STL Stack &amp; Queue: Dec 04</div>
          <div><strong>19.</strong> STL Set &amp; Map: Dec 11</div>
          <div><strong>20.</strong> STL Priority Queue: Dec 18</div>
          <div><strong>21.</strong> Finals Break: Dec 20 – Jan 21</div>
          <div><strong>22.</strong> <span style="color: var(--accent-dark); font-weight: 800;">Warm-up Contest: Jan 29, 2027</span></div>
        </div>
      </div>

      <!-- Column 2: Term 2 -->
      <div class="card-white" style="padding: 12px 14px;">
        <div style="font-size: 11px; font-weight: 700; color: var(--accent-dark); border-bottom: 1px solid var(--card-border); padding-bottom: 4px; margin-bottom: 8px;">
          Term 2: Core Algorithms
        </div>
        <div style="display: flex; flex-direction: column; gap: 4px;">
          <div><strong>23.</strong> Prefix &amp; Freq Arrays: Feb 05</div>
          <div><strong>24.</strong> Two Pointers / Sliding Win: Feb 12</div>
          <div><strong>25.</strong> Form Reopen: Feb 13 – Feb 18</div>
          <div><strong>26.</strong> Binary Search: Feb 19</div>
          <div><strong>27.</strong> Greedy Algorithms: Feb 26</div>
          <div><strong>28.</strong> Recursion &amp; Brute Force: Mar 05</div>
          <div><strong>29.</strong> Diagnostic Review: Mar 06 – Mar 11</div>
          <div><strong>30.</strong> Backtracking: Mar 12</div>
          <div><strong>31.</strong> Bitmask &amp; Brute Force: Mar 19</div>
          <div><strong>32.</strong> Mathematics I: Mar 26</div>
          <div><strong>33.</strong> Mathematics II: Apr 02</div>
          <div><strong>34.</strong> Dynamic Programming I: Apr 09</div>
          <div><strong>35.</strong> Progress Check: Apr 10 – Apr 15</div>
          <div><strong>36.</strong> Midterm Break: Apr 17 – Apr 22</div>
          <div><strong>37.</strong> Dynamic Programming II: Apr 23</div>
          <div><strong>38.</strong> Graph Algorithms I: Apr 30</div>
        </div>
      </div>

      <!-- Column 3: Summer & ECPC -->
      <div class="card-white" style="padding: 12px 14px;">
        <div style="font-size: 11px; font-weight: 700; color: var(--accent-dark); border-bottom: 1px solid var(--card-border); padding-bottom: 4px; margin-bottom: 8px;">
          Summer: Selection &amp; ECPC
        </div>
        <div style="display: flex; flex-direction: column; gap: 4px;">
          <div><strong>39.</strong> Team Trials: Apr 24 – May 06</div>
          <div><strong>40.</strong> Team Selection Contest: May 08</div>
          <div><strong>41.</strong> Official Teams Announced: May 15</div>
          <div><strong>42.</strong> Eid Break: May 16 – May 19</div>
          <div><strong>43.</strong> Finals Break: May 22 – Jun 18</div>
          <div><strong>44.</strong> Weekly Contests: Jun 22 – Jul 27</div>
          <div><strong>45.</strong> Full Contest Simulation: Aug 01</div>
          <div><strong>46.</strong> <span style="color: var(--accent-dark); font-weight: 800;">Target ECPC 2027: Aug 15</span></div>
          <div style="margin-top: 14px; padding: 10px; background: var(--card-bg); border-radius: 8px; border: 1px solid var(--card-border);">
            <strong style="color: var(--text-head);">Governance Note:</strong><br>
            All technical content is peer-reviewed prior to delivery. Attendance, platform problem submissions, and contest logs are monitored continuously.
          </div>
        </div>
      </div>
    </div>

    <div class="footer-bar">
      <div><strong>ICPC HUE</strong> • Annual Progress Dossier 2025 – 2027</div>
      <div>Page 11 of 14</div>
    </div>
  </section>"""

idx_p11_s = html.find('<!-- ================= PAGE 11: ACADEMIC CURRICULUM & MILESTONES ================= -->')
idx_p11_e = html.find('<!-- ================= PAGE 12: CONCLUSION & NEXT STRATEGIC OBJECTIVES ================= -->')

if idx_p11_s != -1 and idx_p11_e != -1:
    html = html[:idx_p11_s] + original_page_11_curriculum + '\n\n  ' + html[idx_p11_e:]
    print('Reversed back the look of Page 11 successfully!')
else:
    print('Warning: could not find Page 11 boundaries:', idx_p11_s, idx_p11_e)

# -------------------------------------------------------------
# FIX 4: Meet the Team (Page 13)
# Make it EXACTLY like the uploaded Canva image media_1790146030808.png
# and do not change anything in it!
# -------------------------------------------------------------
exact_meet_the_team_html = """  <!-- ================= PAGE 13: MEET THE TEAM ================= -->
  <section class="page">
    <div class="header-bar">
      <div class="inst-badge">
        <img src="../../report/assets/horus_logo.png" class="inst-logo" alt="Horus University Logo">
        <div class="inst-text">Horus University — Egypt • <span class="inst-sub">ICPC HUE Community</span></div>
      </div>
      <div class="pill-tag">12 / Community Leadership</div>
    </div>

    <!-- Handshake Emoji & Big Title -->
    <div style="display: flex; align-items: center; gap: 10px; margin-top: 6px; margin-bottom: 6px;">
      <span style="font-size: 28px; line-height: 1;">🤝</span>
      <h1 style="font-size: 28px; font-weight: 800; color: #000000; margin: 0; letter-spacing: -0.02em;">Meet the Team</h1>
    </div>

    <!-- Gold Pill Tag -->
    <div style="display: inline-block; border: 1px solid #E19D1B; border-radius: 6px; padding: 3px 8px; font-size: 8.5px; font-weight: 700; color: #E19D1B; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 10px;">
      THE PEOPLE BEHIND ICPC HUE
    </div>

    <!-- Intro Text -->
    <p style="font-size: 10.2px; line-height: 1.5; color: #373737; margin-bottom: 14px;">
      ICPCHUE's success is built on the dedication and expertise of our talented team members. From visionary leadership to experienced instructors, each member plays a crucial role in shaping the future of competitive programming at Horus University.
    </p>

    <!-- 5 Cards matching Canva design -->
    <div style="display: flex; flex-direction: column; gap: 10px;">

      <!-- Card 1: Academic Supervision & Support -->
      <div style="display: flex; border: 1px solid #E2D9C8; border-radius: 10px; overflow: hidden; background: #FFFFFF;">
        <div style="width: 55px; background: #F9ECD1; flex-shrink: 0;"></div>
        <div style="padding: 10px 16px; flex: 1;">
          <div style="font-size: 13px; font-weight: 800; color: #000000; margin-bottom: 4px;">Academic Supervision &amp; Support</div>
          <ul style="margin: 0; padding-left: 18px; font-size: 10px; line-height: 1.55; color: #373737;">
            <li>Dr. Basma Mostafa</li>
            <li>Dr. Yasser Elawady</li>
            <li>Eng. Fatma Magdy</li>
            <li>Eng. Raafat Mohamed</li>
            <li>Eng. Sara</li>
          </ul>
        </div>
      </div>

      <!-- Card 2: Leadership -->
      <div style="display: flex; border: 1px solid #E2D9C8; border-radius: 10px; overflow: hidden; background: #FFFFFF;">
        <div style="width: 55px; background: #F9ECD1; flex-shrink: 0;"></div>
        <div style="padding: 10px 16px; flex: 1;">
          <div style="font-size: 13px; font-weight: 800; color: #000000; margin-bottom: 4px;">Leadership</div>
          <ul style="margin: 0; padding-left: 18px; font-size: 10px; line-height: 1.55; color: #373737;">
            <li>AbdelRahman Mohsen El-Shahat – Owner</li>
            <li>Youssef Mohamed Salah El-Din – Co-Founder</li>
            <li>Ahmed Waleed – The Lead</li>
          </ul>
        </div>
      </div>

      <!-- Card 3: Platform Developing -->
      <div style="display: flex; border: 1px solid #E2D9C8; border-radius: 10px; overflow: hidden; background: #FFFFFF;">
        <div style="width: 55px; background: #F9ECD1; flex-shrink: 0;"></div>
        <div style="padding: 10px 16px; flex: 1;">
          <div style="font-size: 13px; font-weight: 800; color: #000000; margin-bottom: 4px;">Platform Developing</div>
          <ul style="margin: 0; padding-left: 18px; font-size: 10px; line-height: 1.55; color: #373737;">
            <li>Youssef Mohamed Salah El-Din – Main Dev</li>
          </ul>
        </div>
      </div>

      <!-- Card 4: Instructors -->
      <div style="display: flex; border: 1px solid #E2D9C8; border-radius: 10px; overflow: hidden; background: #FFFFFF;">
        <div style="width: 55px; background: #F9ECD1; flex-shrink: 0;"></div>
        <div style="padding: 10px 16px; flex: 1;">
          <div style="font-size: 13px; font-weight: 800; color: #000000; margin-bottom: 4px;">Instructors</div>
          <ul style="margin: 0; padding-left: 18px; font-size: 10px; line-height: 1.55; color: #373737;">
            <li>Ahmed Waleed – Lead Instructor</li>
            <li>Ibrahim Matar – Co-Lead Instructor</li>
            <li>Omar El-Shayyal – Instructor</li>
          </ul>
        </div>
      </div>

      <!-- Card 5: Monitors -->
      <div style="display: flex; border: 1px solid #E2D9C8; border-radius: 10px; overflow: hidden; background: #FFFFFF;">
        <div style="width: 55px; background: #F9ECD1; flex-shrink: 0;"></div>
        <div style="padding: 10px 16px; flex: 1;">
          <div style="font-size: 13px; font-weight: 800; color: #000000; margin-bottom: 4px;">Monitors</div>
          <ul style="margin: 0; padding-left: 18px; font-size: 10px; line-height: 1.55; color: #373737;">
            <li>Noha – Lead Monitor</li>
          </ul>
        </div>
      </div>

    </div>

    <div class="footer-bar">
      <div><strong>ICPC HUE</strong> • Annual Progress Dossier 2025 – 2027</div>
      <div>Page 13 of 14</div>
    </div>
  </section>"""

idx_p13_s = html.find('<!-- ================= PAGE 13: MEET THE TEAM ================= -->')
idx_p13_e = html.find('<!-- ================= PAGE 14: ACADEMIC SUPERVISION & SPECIAL THANKS ================= -->')

if idx_p13_s != -1 and idx_p13_e != -1:
    html = html[:idx_p13_s] + exact_meet_the_team_html + '\n\n  ' + html[idx_p13_e:]
    print('Updated Meet the Team page to exact Canva format!')
else:
    print('Warning: could not find Page 13 boundaries:', idx_p13_s, idx_p13_e)

with open('/home/yousefmsm1/Desktop/pdf_gen/output/html/ICPC-HUE-Community-Progress-Report-Gamma-Style.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('All user fixes applied to HTML!')
