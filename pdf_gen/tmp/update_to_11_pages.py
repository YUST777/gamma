import re

with open('/home/yousefmsm1/Desktop/pdf_gen/output/html/ICPC-HUE-Community-Progress-Report-Gamma-Style.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add CSS before </style>
css_to_add = """
    /* Executive Roadmap Steps (Page 2) */
    .roadmap-list {
      display: flex;
      flex-direction: column;
      gap: 9px;
      margin-bottom: 14px;
    }
    .roadmap-step {
      display: flex;
      gap: 14px;
      align-items: center;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 10px 14px;
    }
    .roadmap-step.highlight {
      background: var(--accent);
      border-color: var(--accent-dark);
      color: #000000;
    }
    .step-circle {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: var(--accent-dark);
      color: #FFFFFF;
      font-weight: 800;
      font-size: 13px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }
    .roadmap-step.highlight .step-circle {
      background: #000000;
      color: #FFFFFF;
    }
    .step-content {
      flex: 1;
    }
    .step-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 2px;
    }
    .step-title {
      font-size: 12.5px;
      font-weight: 700;
      color: var(--text-head);
    }
    .roadmap-step.highlight .step-title {
      color: #000000;
      font-weight: 800;
    }
    .step-tag {
      font-size: 8.5px;
      font-weight: 700;
      text-transform: uppercase;
      padding: 2px 8px;
      border-radius: 999px;
      background: #E8D8BF;
      color: #5B4018;
    }
    .roadmap-step.highlight .step-tag {
      background: rgba(0,0,0,0.15);
      color: #000000;
    }
    .step-desc {
      font-size: 10px;
      line-height: 1.45;
      color: var(--text-body);
      margin: 0;
    }
    .roadmap-step.highlight .step-desc {
      color: #1A1A1A;
      font-weight: 500;
    }
"""

if '</style>' in html and '.roadmap-step' not in html:
    html = html.replace('  </style>', css_to_add + '\n  </style>')

# 2. Define the new single Page 2
new_page_2 = """  <!-- ================= PAGE 2: ROAD TO DCC ROADMAP & RETROSPECTIVE ================= -->
  <section class="page">
    <div class="header-bar">
      <div class="inst-badge">
        <img src="../../report/assets/horus_logo.png" class="inst-logo" alt="Horus University Logo">
        <div class="inst-text">Horus University — Egypt • <span class="inst-sub">ICPC HUE Community</span></div>
      </div>
      <div class="pill-tag">01 / Season Retrospective</div>
    </div>

    <div class="kicker">
      <div class="kicker-bar"></div>
      <span>Institutional Trajectory & Roadmap</span>
    </div>
    <h1 class="slide-title">The Road to DCC: Building Our Competitive Foundation</h1>
    <p class="slide-sub">
      A strategic overview of how ICPC HUE established a collegiate training ecosystem, engineered a custom learning platform, and formed seven national teams before our regional debut.
    </p>

    <!-- Key Metrics Grid -->
    <div class="grid-4" style="margin-bottom: 14px;">
      <div class="metric-card">
        <div class="metric-val">650</div>
        <div class="metric-label">Curated Problems</div>
        <p class="metric-desc">Structured across 3 skill levels (Levels 0–2) on the custom icpchue.com platform.</p>
      </div>
      <div class="metric-card">
        <div class="metric-val">17+ hrs</div>
        <div class="metric-label">Live Training</div>
        <p class="metric-desc">Structured live lectures delivered covering foundational syntax to algorithmic logic.</p>
      </div>
      <div class="metric-card">
        <div class="metric-val">4.13K</div>
        <div class="metric-label">Monthly Trainees</div>
        <p class="metric-desc">Active student visits and platform interactions engaging with problem sheets.</p>
      </div>
      <div class="metric-card">
        <div class="metric-val">7 Teams</div>
        <div class="metric-label">21 Competitors</div>
        <p class="metric-desc">Formed, tested, and officially approved to represent Horus University in national ECPC.</p>
      </div>
    </div>

    <!-- 5-Step Visual Roadmap -->
    <div class="roadmap-list">
      <!-- Step 01 -->
      <div class="roadmap-step">
        <div class="step-circle">01</div>
        <div class="step-content">
          <div class="step-header">
            <span class="step-title">Community Inception & Winter Camp Launch</span>
            <span class="step-tag">Dec 2025 – Jan 2026</span>
          </div>
          <p class="step-desc">
            Established the competitive programming initiative at Horus University; launched a university-wide Winter Camp welcoming beginners starting from scratch while activating senior students.
          </p>
        </div>
      </div>

      <!-- Step 02 -->
      <div class="roadmap-step">
        <div class="step-circle">02</div>
        <div class="step-content">
          <div class="step-header">
            <span class="step-title">The ICPC HUE Educational Platform (icpchue.com)</span>
            <span class="step-tag">February 2026</span>
          </div>
          <p class="step-desc">
            Engineered and deployed our custom training hub with official university email authentication, automated problem evaluation, and categorized sheets from Level 0 to Level 2.
          </p>
        </div>
      </div>

      <!-- Step 03: Highlight -->
      <div class="roadmap-step highlight">
        <div class="step-circle">03</div>
        <div class="step-content">
          <div class="step-header">
            <span class="step-title">The Landmark Orientation Day (Faculty of AI)</span>
            <span class="step-tag">March 12, 2026</span>
          </div>
          <p class="step-desc">
            Under the sponsorship of <strong>Dr. Basma Mostafa</strong> & <strong>Dr. Yasser El-Awady</strong> and supervision of <strong>Eng. Fatima Magdy</strong> & <strong>Eng. Raafat Mohamed</strong>, hosted hundreds of students and six decorated ACPC DU national champions to inspire our community.
          </p>
        </div>
      </div>

      <!-- Step 04 -->
      <div class="roadmap-step">
        <div class="step-circle">04</div>
        <div class="step-content">
          <div class="step-header">
            <span class="step-title">High-Stakes Selection Trials & Campus Champions</span>
            <span class="step-tag">April 2026</span>
          </div>
          <p class="step-desc">
            Conducted two official selection contests to evaluate algorithmic mastery and team synergy, crowning student champions (🥇 <strong>Ebrahim Matar</strong>, 🥈 <strong>Ahmed Waleed</strong>, 🥉 <strong>Noha Kamal</strong>).
          </p>
        </div>
      </div>

      <!-- Step 05 -->
      <div class="roadmap-step">
        <div class="step-circle">05</div>
        <div class="step-content">
          <div class="step-header">
            <span class="step-title">Seven Official Teams Approved for National ECPC</span>
            <span class="step-tag">April 30 – May 2026</span>
          </div>
          <p class="step-desc">
            Assembled 21 student competitors into 7 balanced three-member teams (4 Level 1 teams, 3 Level 2 teams), completing official registration for the Egyptian Collegiate Programming Contest.
          </p>
        </div>
      </div>
    </div>

    <!-- Strategic Bridge Callout -->
    <div class="quote-callout" style="padding: 10px 14px; margin-bottom: 0;">
      <strong>Strategic Proving Ground:</strong> With seven official teams assembled and our digital training platform established, ICPC HUE partnered with ACPC Club Damietta University to co-organize DCC 2026 as an authentic regional tournament simulation.
    </div>

    <div class="footer-bar">
      <div><strong>ICPC HUE</strong> • Annual Progress Dossier 2025 – 2027</div>
      <div>Page 02 of 11</div>
    </div>
  </section>"""

# Replace old Page 2 and Page 3
start_marker = '  <!-- ================= PAGE 2: 2025/2026 CHRONICLE PART 1 (START TO MARCH) ================= -->'
end_marker = '  <!-- ================= PAGE 4: DCC 2026 WITH PHOTO GALLERY ================= -->'

p1 = html.find(start_marker)
p2 = html.find(end_marker)

if p1 != -1 and p2 != -1:
    html = html[:p1] + new_page_2 + '\n\n' + html[p2:]
    print('Replaced Page 2 and Page 3 successfully!')
else:
    print('Failed to find markers:', p1, p2)

# Update page titles / pill tags
html = html.replace('<!-- ================= PAGE 4: DCC 2026 WITH PHOTO GALLERY ================= -->', '<!-- ================= PAGE 3: DCC 2026 WITH PHOTO GALLERY ================= -->')
html = html.replace('<div class="pill-tag">03 / Regional Proving Ground</div>', '<div class="pill-tag">02 / Regional Proving Ground</div>')

html = html.replace('<!-- ================= PAGE 5: ECPC QUALIFICATION ================= -->', '<!-- ================= PAGE 4: ECPC QUALIFICATION ================= -->')
html = html.replace('<div class="pill-tag">04 / Field Experience</div>', '<div class="pill-tag">03 / Field Experience</div>')

html = html.replace('<!-- ================= PAGE 6: OUTREACH & RECRUITMENT ================= -->', '<!-- ================= PAGE 5: OUTREACH & RECRUITMENT ================= -->')
html = html.replace('<div class="pill-tag">05 / Outreach & Momentum</div>', '<div class="pill-tag">04 / Outreach & Momentum</div>')

html = html.replace('<!-- ================= PAGE 7: OPERATING COMMITTEES ================= -->', '<!-- ================= PAGE 6: OPERATING COMMITTEES ================= -->')
html = html.replace('<div class="pill-tag">06 / Operating Model</div>', '<div class="pill-tag">05 / Operating Model</div>')

html = html.replace('<!-- ================= PAGE 8: LEADERSHIP & PLATFORM ================= -->', '<!-- ================= PAGE 7: LEADERSHIP & PLATFORM ================= -->')
html = html.replace('<div class="pill-tag">07 / Talent & Systems</div>', '<div class="pill-tag">06 / Talent & Systems</div>')

html = html.replace('<!-- ================= PAGE 9: PARTNERSHIPS & INTRO DAY ================= -->', '<!-- ================= PAGE 8: PARTNERSHIPS & INTRO DAY ================= -->')
html = html.replace('<div class="pill-tag">08 / Ecosystem & Engagement</div>', '<div class="pill-tag">07 / Ecosystem & Engagement</div>')

html = html.replace('<!-- ================= PAGE 10: ROAD TO ICPC ROADMAP ================= -->', '<!-- ================= PAGE 9: ROAD TO ICPC ROADMAP ================= -->')
html = html.replace('<div class="pill-tag">09 / Season Roadmap</div>', '<div class="pill-tag">08 / Season Roadmap</div>')

html = html.replace('<!-- ================= PAGE 11: CONCLUSION & NEXT OBJECTIVES ================= -->', '<!-- ================= PAGE 10: CONCLUSION & NEXT OBJECTIVES ================= -->')
html = html.replace('<div class="pill-tag">10 / Strategic Objectives</div>', '<div class="pill-tag">09 / Strategic Objectives</div>')

html = html.replace('<!-- ================= PAGE 12: APPENDIX CALENDAR ================= -->', '<!-- ================= PAGE 11: APPENDIX CALENDAR ================= -->')

# Update footers
html = html.replace('<div>Page 01 of 12</div>', '<div>Page 01 of 11</div>')
html = html.replace('<div>Page 04 of 12</div>', '<div>Page 03 of 11</div>')
html = html.replace('<div>Page 05 of 12</div>', '<div>Page 04 of 11</div>')
html = html.replace('<div>Page 06 of 12</div>', '<div>Page 05 of 11</div>')
html = html.replace('<div>Page 07 of 12</div>', '<div>Page 06 of 11</div>')
html = html.replace('<div>Page 08 of 12</div>', '<div>Page 07 of 11</div>')
html = html.replace('<div>Page 09 of 12</div>', '<div>Page 08 of 11</div>')
html = html.replace('<div>Page 10 of 12</div>', '<div>Page 09 of 11</div>')
html = html.replace('<div>Page 11 of 12</div>', '<div>Page 10 of 11</div>')
html = html.replace('<div>Page 12 of 12</div>', '<div>Page 11 of 11</div>')

with open('/home/yousefmsm1/Desktop/pdf_gen/output/html/ICPC-HUE-Community-Progress-Report-Gamma-Style.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Update completed successfully!')
