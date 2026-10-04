import re

with open('/home/yousefmsm1/Desktop/pdf_gen/output/html/ICPC-HUE-Community-Progress-Report-Gamma-Style.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update CSS
extra_css = """
    /* Multi-Photo Collage on Page 5 */
    .collage-top {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-top: 10px;
    }
    .collage-bottom {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 8px;
      margin-top: 8px;
    }
"""
if '.collage-top' not in html:
    html = html.replace('  </style>', extra_css + '\n  </style>')

# 2. Page 2: Remove ( Ebrahim Matar, Ahmed Waleed, Noha Kamal).
old_p2_names = "crowning student champions (🥇 <strong>Ebrahim Matar</strong>, 🥈 <strong>Ahmed Waleed</strong>, 🥉 <strong>Noha Kamal</strong>)."
new_p2_names = "crowning top campus solvers across competitive individual trials and finalizing collegiate lineups."
html = html.replace(old_p2_names, new_p2_names)

# 3. Page 4 (ECPC Qualification):
# Delete "Path Clarified: Qualification → ECPC → ACPC → ICPC World Finals"
# Add "within one single problem" highlight and update key takeaways
old_p4_journey = """        <div style="font-size: 9.5px; font-weight: 700; border-top: 1px solid rgba(0,0,0,0.15); padding-top: 8px; margin-top: 10px;">
          Path Clarified: Qualification → ECPC → ACPC → ICPC World Finals
        </div>"""

new_p4_journey = """        <div style="background: rgba(255,255,255,0.45); border-radius: 8px; padding: 10px 12px; margin-top: 10px;">
          <div style="font-size: 10.5px; font-weight: 800; color: #000; text-transform: uppercase;">National Benchmark</div>
          <div style="font-size: 10px; color: #111; line-height: 1.45; margin-top: 2px;">
            Horus University's leading team solved 4 complex algorithmic problems — finishing within just <strong>one single problem</strong> of officially advancing to the ECPC National Finals.
          </div>
        </div>"""

html = html.replace(old_p4_journey, new_p4_journey)

old_p4_takeaways = """    <div class="card" style="padding: 14px 18px; margin-top: 15px; border-left: 5px solid var(--accent);">
      <div class="card-title" style="color: var(--accent-dark); font-size: 13.5px; margin-bottom: 4px;">Key Takeaways for Next Season</div>
      <p class="card-body" style="font-size: 10.5px; line-height: 1.55;">
        The results validated student capability while pinpointing precise areas for growth: starting structured multi-hour practice contests months earlier, instituting daily mentor follow-ups, and conducting timed team selection trials.
      </p>
    </div>"""

new_p4_takeaways = """    <div class="card" style="padding: 14px 18px; margin-top: 14px; border-left: 5px solid var(--accent);">
      <div class="card-title" style="color: var(--accent-dark); font-size: 13.5px; margin-bottom: 4px;">Key Takeaways: One Problem Away from National Qualification</div>
      <p class="card-body" style="font-size: 10.2px; line-height: 1.55;">
        The official tournament results validated student capability while establishing our strategic priorities: finishing just <strong>one solved problem short of advancing to the ECPC National Finals</strong> proved that Horus University competitors can match top national teams. To bridge this final margin, our 2026/2027 plan initiates 5-hour simulated contests months earlier, mandates daily platform tracking on icpchue.com, and implements timed selection trials.
      </p>
    </div>"""

html = html.replace(old_p4_takeaways, new_p4_takeaways)

# 4. Page 5: Add Photo Collage (5 photos)
old_page_5_content_start = '  <!-- ================= PAGE 5: OUTREACH & RECRUITMENT ================= -->'
old_page_5_end = '  <!-- ================= PAGE 6: OPERATING COMMITTEES ================= -->'

idx_p5_s = html.find(old_page_5_content_start)
idx_p5_e = html.find(old_page_5_end)

new_page_5 = """  <!-- ================= PAGE 5: OUTREACH & RECRUITMENT ================= -->
  <section class="page">
    <div class="header-bar">
      <div class="inst-badge">
        <img src="../../report/assets/horus_logo.png" class="inst-logo" alt="Horus University Logo">
        <div class="inst-text">Horus University — Egypt • <span class="inst-sub">ICPC HUE Community</span></div>
      </div>
      <div class="pill-tag">04 / Outreach & Momentum</div>
    </div>

    <div class="kicker">
      <div class="kicker-bar"></div>
      <span>Outreach & Community Momentum</span>
    </div>
    <h1 class="slide-title">Converting Contest Experience into Season-Wide Momentum</h1>
    <p class="slide-sub">
      Documenting the tournament journey transformed competitive programming into an exciting, high-visibility activity across Horus University.
    </p>

    <!-- 3 Compact Cards in Grid -->
    <div class="grid-3" style="margin-bottom: 10px;">
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

    <!-- Multi-Photo Delegation Collage (5 Photos) -->
    <div style="background: #FDF9F2; border: 1px solid var(--card-border); border-radius: 14px; padding: 10px;">
      <div style="font-size: 10px; font-weight: 800; color: var(--accent-dark); text-transform: uppercase; margin-bottom: 6px; letter-spacing: 0.04em;">
        Field Documentation • Delegation Journey & Competition Arena
      </div>
      <!-- Top Collage Row: 2 Photos -->
      <div class="collage-top">
        <div class="photo-box" style="height: 125px; margin: 0;">
          <img src="../../report/ecpc_qulifcatio/FB_IMG_1790132541422.jpg" alt="Delegation Bus Travel to Alexandria">
        </div>
        <div class="photo-box" style="height: 125px; margin: 0;">
          <img src="../../report/ecpc_qulifcatio/FB_IMG_1790132708823.jpg" alt="Horus University Team 2050 in ECPC Arena">
        </div>
      </div>
      <!-- Bottom Collage Row: 3 Photos -->
      <div class="collage-bottom">
        <div class="photo-box" style="height: 95px; margin: 0;">
          <img src="../../report/ecpc_qulifcatio/FB_IMG_1790132657082.jpg" alt="Students Working Through Algorithmic Problems">
        </div>
        <div class="photo-box" style="height: 95px; margin: 0;">
          <img src="../../report/ecpc_qulifcatio/FB_IMG_1790132690995.jpg" alt="Contest Hall Focus and Solving">
        </div>
        <div class="photo-box" style="height: 95px; margin: 0;">
          <img src="../../report/ecpc_qulifcatio/FB_IMG_1790132740356.jpg" alt="Horus University Delegation Celebration">
        </div>
      </div>
      <div class="photo-caption" style="text-align: center; margin-top: 6px;">
        Clockwise from top left: Delegation bus travel to Alexandria; Team 2050 competing at AASTMT; problem analysis; contest floor; delegation tournament celebration.
      </div>
    </div>

    <div class="footer-bar">
      <div><strong>ICPC HUE</strong> • Annual Progress Dossier 2025 – 2027</div>
      <div>Page 05 of 13</div>
    </div>
  </section>
"""

if idx_p5_s != -1 and idx_p5_e != -1:
    html = html[:idx_p5_s] + new_page_5 + '\n\n' + html[idx_p5_e:]
    print('Updated Page 5 with photo collage!')
else:
    print('Failed to find Page 5 markers:', idx_p5_s, idx_p5_e)

# 5. Extract Curriculum / Appendix (formerly Page 11 of 11) and Conclusion (formerly Page 10 of 11)
# User request: "make page 9 after it page 11 page 10 make it 11"
# And "change term to semeseter and make it bigger font or smth"

curriculum_section_start = '  <!-- ================= PAGE 11: APPENDIX CALENDAR ================= -->'
curriculum_idx = html.find(curriculum_section_start)

conclusion_section_start = '  <!-- ================= PAGE 10: CONCLUSION & NEXT OBJECTIVES ================= -->'
conclusion_idx = html.find(conclusion_section_start)

# Let's extract the sections
# Let's see: before reordering, where is conclusion and where is curriculum?
print('curriculum_idx:', curriculum_idx, 'conclusion_idx:', conclusion_idx)

# Let's craft the new Page 10 (Curriculum Schedule with Semester 1 & 2 in bigger font)
new_page_10_curriculum = """  <!-- ================= PAGE 10: ACADEMIC CURRICULUM & MILESTONES ================= -->
  <section class="page">
    <div class="header-bar">
      <div class="inst-badge">
        <img src="../../report/assets/horus_logo.png" class="inst-logo" alt="Horus University Logo">
        <div class="inst-text">Horus University — Egypt • <span class="inst-sub">ICPC HUE Community</span></div>
      </div>
      <div class="pill-tag">09 / Academic Curriculum</div>
    </div>

    <div class="kicker">
      <div class="kicker-bar"></div>
      <span>Academic Appendix & Milestones</span>
    </div>
    <h1 class="slide-title">2026/2027 Season Curriculum & Milestones</h1>
    <p class="slide-sub">
      Comprehensive schedule of all 46 milestones across the academic year for faculty review and operational tracking.
    </p>

    <!-- 3 Term Columns -->
    <div class="grid-3">
      <!-- Semester 1 Column -->
      <div class="card" style="padding: 14px 16px;">
        <div class="card-title" style="color: var(--accent-dark); font-size: 15px; font-weight: 800; border-bottom: 2px solid var(--accent); padding-bottom: 5px; margin-bottom: 10px;">
          Semester 1: Foundations & STL
        </div>
        <ul class="timeline-list">
          <li><strong>01.</strong> Promotion: Aug 29 – Sep 03</li>
          <li><strong>02.</strong> Applications Open: Sep 05 – Sep 10</li>
          <li><strong>03.</strong> Screening/Interviews: Sep 12 – Sep 17</li>
          <li><strong>04.</strong> Results: Sep 18</li>
          <li><strong>05.</strong> Orientation Day: Sep 26 – Oct 01</li>
          <li><strong>06.</strong> Form Reopen: Sep 26 – Oct 01</li>
          <li><strong>07.</strong> Intro Session: Oct 09 (8:30 PM)</li>
          <li><strong>08.</strong> Basics & Conditions: Oct 16</li>
          <li><strong>09.</strong> Loops & Nested Loops: Oct 23</li>
          <li><strong>10.</strong> Arrays & Functions: Oct 30</li>
          <li><strong>11.</strong> Strings: Nov 06</li>
          <li><strong>12.</strong> Midterm Break: Nov 07 – Nov 12</li>
          <li><strong>13.</strong> Functions: Nov 13</li>
          <li><strong>14.</strong> Complexity (Big-O): Nov 20</li>
          <li><strong>15.</strong> Practice Contests: Nov 21 – Nov 26</li>
          <li><strong>16.</strong> Progress Check: Late Nov</li>
          <li><strong>17.</strong> STL Vector & Pair: Nov 27</li>
          <li><strong>18.</strong> STL Stack & Queue: Dec 04</li>
          <li><strong>19.</strong> STL Set & Map: Dec 11</li>
          <li><strong>20.</strong> STL Priority Queue: Dec 18</li>
          <li><strong>21.</strong> Finals Break: Dec 20 – Jan 21</li>
          <li style="color: var(--accent-dark); font-weight: 800;">22. Warm-up Contest: Jan 29, 2027</li>
        </ul>
      </div>

      <!-- Semester 2 Column -->
      <div class="card" style="padding: 14px 16px;">
        <div class="card-title" style="color: var(--accent-dark); font-size: 15px; font-weight: 800; border-bottom: 2px solid var(--accent); padding-bottom: 5px; margin-bottom: 10px;">
          Semester 2: Core Algorithms
        </div>
        <ul class="timeline-list">
          <li><strong>23.</strong> Prefix & Freq Arrays: Feb 05</li>
          <li><strong>24.</strong> Two Pointers / Sliding Win: Feb 12</li>
          <li><strong>25.</strong> Form Reopen: Feb 13 – Feb 18</li>
          <li><strong>26.</strong> Binary Search: Feb 19</li>
          <li><strong>27.</strong> Greedy Algorithms: Feb 26</li>
          <li><strong>28.</strong> Recursion & Brute Force: Mar 05</li>
          <li><strong>29.</strong> Diagnostic Review: Mar 06 – Mar 11</li>
          <li><strong>30.</strong> Backtracking: Mar 12</li>
          <li><strong>31.</strong> Bitmask & Brute Force: Mar 19</li>
          <li><strong>32.</strong> Mathematics I: Mar 26</li>
          <li><strong>33.</strong> Mathematics II: Apr 02</li>
          <li><strong>34.</strong> Dynamic Programming I: Apr 09</li>
          <li><strong>35.</strong> Progress Check: Apr 10 – Apr 15</li>
          <li><strong>36.</strong> Midterm Break: Apr 17 – Apr 22</li>
          <li><strong>37.</strong> Dynamic Programming II: Apr 23</li>
          <li><strong>38.</strong> Graph Algorithms I: Apr 30</li>
        </ul>
      </div>

      <!-- Summer Term Column -->
      <div class="card" style="padding: 14px 16px;">
        <div class="card-title" style="color: var(--accent-dark); font-size: 15px; font-weight: 800; border-bottom: 2px solid var(--accent); padding-bottom: 5px; margin-bottom: 10px;">
          Summer Term: Selection & ECPC
        </div>
        <ul class="timeline-list">
          <li><strong>39.</strong> Team Trials: Apr 24 – May 06</li>
          <li><strong>40.</strong> Team Selection Contest: May 08</li>
          <li><strong>41.</strong> Official Teams Announced: May 15</li>
          <li><strong>42.</strong> Eid Break: May 16 – May 19</li>
          <li><strong>43.</strong> Finals Break: May 22 – Jun 18</li>
          <li><strong>44.</strong> Weekly Contests: Jun 22 – Jul 27</li>
          <li><strong>45.</strong> Full Contest Simulation: Aug 01</li>
          <li style="color: var(--accent-dark); font-weight: 800;">46. Target ECPC 2027: Aug 15</li>
        </ul>

        <div style="margin-top: 18px; background: rgba(225, 157, 27, 0.15); border-radius: 8px; padding: 10px 12px; border-left: 3px solid var(--accent);">
          <div style="font-size: 10.5px; font-weight: 800; color: var(--accent-dark);">Academic Governance:</div>
          <div style="font-size: 9px; color: var(--text-body); line-height: 1.45; margin-top: 2px;">
            All technical content is reviewed prior to delivery. Attendance, problem submissions, and contest logs are monitored continuously.
          </div>
        </div>
      </div>
    </div>

    <div class="footer-bar">
      <div><strong>ICPC HUE</strong> • Annual Progress Dossier 2025 – 2027</div>
      <div>Page 10 of 13</div>
    </div>
  </section>
"""

# Let's craft the new Page 11 (Conclusion & Next Strategic Objectives)
new_page_11_conclusion = """  <!-- ================= PAGE 11: CONCLUSION & NEXT STRATEGIC OBJECTIVES ================= -->
  <section class="page">
    <div class="header-bar">
      <div class="inst-badge">
        <img src="../../report/assets/horus_logo.png" class="inst-logo" alt="Horus University Logo">
        <div class="inst-text">Horus University — Egypt • <span class="inst-sub">ICPC HUE Community</span></div>
      </div>
      <div class="pill-tag">10 / Strategic Objectives</div>
    </div>

    <div class="kicker">
      <div class="kicker-bar"></div>
      <span>Strategic Vision & Long-Term Trajectory</span>
    </div>
    <h1 class="slide-title">Conclusion and Next Strategic Objectives</h1>
    <p class="slide-sub">
      The full 2025/2026 trajectory proved that ICPC HUE can organize, compete, learn, and build a lasting system simultaneously.
    </p>

    <!-- 4 Pillars 2x2 -->
    <div class="grid-2">
      <div class="card">
        <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 8px;">
          <div class="step-circle" style="width: 24px; height: 24px; font-size: 11px;">1</div>
          <div class="card-title" style="margin: 0; font-size: 13.5px;">Expand Instructor & Mentor Pipeline</div>
        </div>
        <p class="card-body" style="font-size: 10.2px;">
          Institutionalize the teach-back interview framework to groom past top performers into certified student instructors and mentors, preventing knowledge loss as senior cohorts graduate.
        </p>
      </div>

      <div class="card">
        <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 8px;">
          <div class="step-circle" style="width: 24px; height: 24px; font-size: 11px;">2</div>
          <div class="card-title" style="margin: 0; font-size: 13.5px;">Standardize Daily Platform Tracking</div>
        </div>
        <p class="card-body" style="font-size: 10.2px;">
          Make daily submission logging on the ICPC HUE platform mandatory for all active trainees, providing mentors with transparent data to intervene early when solving momentum dips.
        </p>
      </div>

      <div class="card">
        <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 8px;">
          <div class="step-circle" style="width: 24px; height: 24px; font-size: 11px;">3</div>
          <div class="card-title" style="margin: 0; font-size: 13.5px;">Deepen Cross-University Cooperation</div>
        </div>
        <p class="card-body" style="font-size: 10.2px;">
          Expand joint contests and instructor exchanges with Assiut University, Port Said University, and Damietta University, ensuring HUE students are regularly benchmarked against top regional teams.
        </p>
      </div>

      <div class="card">
        <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 8px;">
          <div class="step-circle" style="width: 24px; height: 24px; font-size: 11px;">4</div>
          <div class="card-title" style="margin: 0; font-size: 13.5px;">Initiate Structured Simulation Earlier</div>
        </div>
        <p class="card-body" style="font-size: 10.2px;">
          Transition teams into 5-hour timed contest simulations months ahead of ECPC qualification, building the endurance, strategic problem triage, and team dynamics required to advance.
        </p>
      </div>
    </div>

    <!-- Long Term Objective -->
    <div class="card-stripe" style="margin-top: 14px; padding: 16px 20px;">
      <div class="card-title" style="color: var(--accent-dark); font-size: 14px; margin-bottom: 6px;">Institutional Long-Term Objective</div>
      <p class="card-body" style="font-size: 11px; line-height: 1.6;">
        Establish a self-sustaining competitive programming culture at Horus University — guiding students from their very first solved problem to the highest levels of collegiate excellence in the ECPC, ACPC, and ICPC World Finals.
      </p>
    </div>

    <div class="quote-callout" style="margin-top: 14px;">
      <em>"ICPC HUE is continuing to build that path one student, one team, and one well-organized training cycle at a time."</em>
    </div>

    <div class="footer-bar">
      <div><strong>ICPC HUE</strong> • Annual Progress Dossier 2025 – 2027</div>
      <div>Page 11 of 13</div>
    </div>
  </section>
"""

# Let's craft the new Page 12 (Meet the Team)
new_page_12_team = """  <!-- ================= PAGE 12: MEET THE TEAM ================= -->
  <section class="page">
    <div class="header-bar">
      <div class="inst-badge">
        <img src="../../report/assets/horus_logo.png" class="inst-logo" alt="Horus University Logo">
        <div class="inst-text">Horus University — Egypt • <span class="inst-sub">ICPC HUE Community</span></div>
      </div>
      <div class="pill-tag">11 / Community Leadership</div>
    </div>

    <div class="kicker">
      <div class="kicker-bar"></div>
      <span>Community Architecture & Leadership</span>
    </div>
    <h1 class="slide-title">Meet the Team: The People Behind ICPC HUE</h1>
    <p class="slide-sub">
      The dedicated student leaders, competitive programmers, and platform engineers driving Horus University's competitive programming movement.
    </p>

    <!-- Top 3 Grid: Executive Leadership, Instruction, Platform Dev -->
    <div class="grid-3" style="margin-bottom: 14px;">
      <!-- Leadership -->
      <div class="card-solid" style="padding: 14px 16px;">
        <div class="card-title" style="font-size: 13.5px; margin-bottom: 8px; color: #000;">Executive Leadership</div>
        <div style="display: flex; flex-direction: column; gap: 8px;">
          <div>
            <div style="font-weight: 800; font-size: 11.5px; color: #000;">Ahmed Waleed</div>
            <div style="font-size: 9.5px; color: #222;">Community Lead</div>
          </div>
          <div>
            <div style="font-weight: 800; font-size: 11.5px; color: #000;">Youssef Mohamed</div>
            <div style="font-size: 9.5px; color: #222;">Co-Founder & Technical Lead</div>
          </div>
          <div>
            <div style="font-weight: 800; font-size: 11.5px; color: #000;">AbdelRahman Mohsen</div>
            <div style="font-size: 9.5px; color: #222;">Co-Founder & Strategy Lead</div>
          </div>
        </div>
      </div>

      <!-- Instructors -->
      <div class="card" style="padding: 14px 16px;">
        <div class="card-title" style="color: var(--accent-dark); font-size: 13.5px; margin-bottom: 8px;">Instruction Committee</div>
        <div style="display: flex; flex-direction: column; gap: 8px;">
          <div>
            <div style="font-weight: 700; font-size: 11px; color: var(--text-head);">Ahmed Waleed</div>
            <div style="font-size: 9.5px; color: var(--text-muted);">Lead Instructor (Foundations Track)</div>
          </div>
          <div>
            <div style="font-weight: 700; font-size: 11px; color: var(--text-head);">Ibrahim Matar</div>
            <div style="font-size: 9.5px; color: var(--text-muted);">Co-Lead Instructor (Advanced Algorithms)</div>
          </div>
          <div>
            <div style="font-weight: 700; font-size: 11px; color: var(--text-head);">Omar El-Shayyal</div>
            <div style="font-size: 9.5px; color: var(--text-muted);">Core Instructor (Data Structures)</div>
          </div>
        </div>
      </div>

      <!-- Platform Dev -->
      <div class="card" style="padding: 14px 16px;">
        <div class="card-title" style="color: var(--accent-dark); font-size: 13.5px; margin-bottom: 8px;">Platform Engineering</div>
        <div style="margin-bottom: 6px;">
          <div style="font-weight: 700; font-size: 11px; color: var(--text-head);">Youssef Mohamed</div>
          <div style="font-size: 9.5px; color: var(--text-muted);">Lead Systems Architect</div>
        </div>
        <p class="card-body" style="font-size: 9.5px; line-height: 1.45;">
          Engineered <strong>icpchue.com</strong> (650 problems, auth, dashboard) and <strong>dcchub.xyz</strong> (DCC regional tournament portal).
        </p>
      </div>
    </div>

    <!-- Bottom 2 Grid: Mentorship & Media/Operations -->
    <div class="grid-2" style="margin-bottom: 14px;">
      <div class="card-white" style="border-left: 4px solid var(--accent); padding: 14px 16px;">
        <div class="card-title" style="color: var(--accent-dark); font-size: 13px; margin-bottom: 6px;">Mentorship & Monitoring</div>
        <div style="margin-bottom: 6px;">
          <span style="font-weight: 800; font-size: 11px;">Noha Kamal</span> — <span style="font-size: 9.5px; color: var(--text-muted);">Lead Monitor</span>
        </div>
        <p class="card-body" style="font-size: 9.8px; line-height: 1.5;">
          Coordinating small-group weekly check-ins, identifying student problem-solving roadblocks, and monitoring participation habits to maintain retention across all training cohorts.
        </p>
      </div>

      <div class="card-white" style="border-left: 4px solid var(--accent); padding: 14px 16px;">
        <div class="card-title" style="color: var(--accent-dark); font-size: 13px; margin-bottom: 6px;">Media & Operations Staff</div>
        <div style="font-size: 10px; font-weight: 700; color: var(--text-head); margin-bottom: 2px;">Media Production & Operations Officers</div>
        <p class="card-body" style="font-size: 9.8px; line-height: 1.5;">
          Managing on-ground event execution, computer lab reservations, video production (43K+ views), roll-up stage branding, and logistical execution during all offline contests.
        </p>
      </div>
    </div>

    <!-- Leadership Quote -->
    <div class="quote-callout" style="padding: 12px 16px;">
      <strong>Core Community Ethos:</strong> <em>"ICPCHUE's success is built on the dedication and expertise of our talented team members. From visionary student leadership to experienced instructors and monitors, each member plays a crucial role in shaping the future of competitive programming at Horus University."</em>
    </div>

    <div class="footer-bar">
      <div><strong>ICPC HUE</strong> • Annual Progress Dossier 2025 – 2027</div>
      <div>Page 12 of 13</div>
    </div>
  </section>
"""

# Let's craft the new Page 13 (Academic Supervision & Special Thanks - Thank You Page)
new_page_13_acknowledgments = """  <!-- ================= PAGE 13: ACADEMIC SUPERVISION & SPECIAL THANKS ================= -->
  <section class="page">
    <div class="header-bar">
      <div class="inst-badge">
        <img src="../../report/assets/horus_logo.png" class="inst-logo" alt="Horus University Logo">
        <div class="inst-text">Horus University — Egypt • <span class="inst-sub">Faculty of Artificial Intelligence</span></div>
      </div>
      <div class="pill-tag">12 / Academic Governance</div>
    </div>

    <div class="kicker">
      <div class="kicker-bar"></div>
      <span>Institutional Support & Governance</span>
    </div>
    <h1 class="slide-title">Academic Supervision & Special Thanks</h1>
    <p class="slide-sub">
      With profound gratitude to university leadership, faculty deanship, and supervising engineers who championed our community every step of the way.
    </p>

    <!-- 3 Academic Tiers -->
    <div style="display: flex; flex-direction: column; gap: 12px; margin-bottom: 14px;">
      <!-- Dean -->
      <div class="card-white" style="border-left: 5px solid var(--accent-dark); padding: 12px 18px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
          <div style="font-size: 13px; font-weight: 800; color: var(--text-head);">Prof. Dr. Hossam El-Din Mostafa</div>
          <span class="pill-tag" style="font-size: 8px;">Dean of Faculty of Artificial Intelligence</span>
        </div>
        <p class="card-body" style="font-size: 10px; line-height: 1.5;">
          We express our deepest gratitude to the Dean for his visionary leadership, continuous patronage of collegiate competitive programming, endorsement of university computer laboratory allocations, and championing our participation in regional and national arenas.
        </p>
      </div>

      <!-- Coordinators -->
      <div class="card-white" style="border-left: 5px solid var(--accent); padding: 12px 18px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
          <div style="font-size: 13px; font-weight: 800; color: var(--text-head);">Dr. Basma Mostafa & Dr. Yasser El-Awady</div>
          <span class="pill-tag" style="font-size: 8px;">Academic Program Coordinators</span>
        </div>
        <p class="card-body" style="font-size: 10px; line-height: 1.5;">
          Heartfelt thanks for their generous sponsorship of the landmark March 12 Orientation Day, providing continuous strategic guidance, bridging faculty resources with student initiatives, and mentoring teams throughout the entire competitive season.
        </p>
      </div>

      <!-- Supervising Engineers -->
      <div class="card-white" style="border-left: 5px solid var(--accent); padding: 12px 18px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
          <div style="font-size: 13px; font-weight: 800; color: var(--text-head);">Eng. Fatma Magdy • Eng. Sara Lotfy • Eng. Raafat Mohamed</div>
          <span class="pill-tag" style="font-size: 8px;">Faculty Supervising Engineers</span>
        </div>
        <p class="card-body" style="font-size: 10px; line-height: 1.5;">
          Our sincere appreciation for their tireless hands-on mentorship, conducting rigorous 5-day teach-back evaluations for student instructors, coordinating logistics across departments, and providing steadfast academic and moral guidance to every competitor.
        </p>
      </div>
    </div>

    <!-- Formal Leadership Letter (Solid Gold Card) -->
    <div class="card-solid" style="padding: 16px 20px;">
      <div style="font-size: 12px; font-weight: 800; text-transform: uppercase; margin-bottom: 6px; letter-spacing: 0.04em; color: #000;">
        Institutional Tribute to Horus University Leadership
      </div>
      <p style="font-size: 10.5px; line-height: 1.6; color: #111; margin: 0; font-style: italic;">
        "On behalf of all ICPC HUE competitors, instructors, and student members, we express our highest appreciation to the University Leadership, the Faculty Deanship, and our supervising engineers. Your unwavering trust and academic guidance transformed a student initiative into an official collegiate powerhouse. We pledge to continue building on this foundation and carrying Horus University's flag to the highest podiums in the ECPC, ACPC, and ICPC World Finals."
      </p>
    </div>

    <div class="footer-bar">
      <div><strong>ICPC HUE</strong> • Annual Progress Dossier 2025 – 2027</div>
      <div>Page 13 of 13</div>
    </div>
  </section>
"""

# Let's replace the tail of the document starting from page 9
# Page 9 is Road to ICPC
# Find where Page 10 (or Page 9) is located
p9_marker = '  <!-- ================= PAGE 9: ROAD TO ICPC ROADMAP ================= -->'
if p9_marker not in html:
    p9_marker = '  <!-- ================= PAGE 10: ROAD TO ICPC ROADMAP ================= -->'

idx_p9 = html.find(p9_marker)
print('idx_p9:', idx_p9)

# We want Page 9 to stay, but with footer "Page 09 of 13"
# Let's see what follows Page 9 in the current html:
# In current html:
# After Page 9 comes Page 10 (Conclusion), then Page 11 (Appendix).
# Let's find end of Page 9 section </section>
idx_p9_end = html.find('</section>', idx_p9) + len('</section>')

# Extract Page 9 HTML
page_9_html = html[idx_p9:idx_p9_end]

# Update page 9 footer to Page 09 of 13
page_9_html = re.sub(r'<div>Page \d+ of \d+</div>', '<div>Page 09 of 13</div>', page_9_html)
page_9_html = re.sub(r'<!-- ================= PAGE \d+: ROAD TO ICPC ROADMAP ================= -->', '<!-- ================= PAGE 9: ROAD TO ICPC ROADMAP ================= -->', page_9_html)
page_9_html = re.sub(r'<div class="pill-tag">\d+ / Season Roadmap</div>', '<div class="pill-tag">08 / Season Roadmap</div>', page_9_html)

# Now, we assemble from start up to idx_p9, then page_9_html, then new_page_10_curriculum, then new_page_11_conclusion, then new_page_12_team, then new_page_13_acknowledgments, then </body></html>!

html_before_p9 = html[:idx_p9]

# Update footers in html_before_p9:
html_before_p9 = re.sub(r'<div>Page 01 of \d+</div>', '<div>Page 01 of 13</div>', html_before_p9)
html_before_p9 = re.sub(r'<div>Page 02 of \d+</div>', '<div>Page 02 of 13</div>', html_before_p9)
html_before_p9 = re.sub(r'<div>Page 03 of \d+</div>', '<div>Page 03 of 13</div>', html_before_p9)
html_before_p9 = re.sub(r'<div>Page 04 of \d+</div>', '<div>Page 04 of 13</div>', html_before_p9)
html_before_p9 = re.sub(r'<div>Page 05 of \d+</div>', '<div>Page 05 of 13</div>', html_before_p9)
html_before_p9 = re.sub(r'<div>Page 06 of \d+</div>', '<div>Page 06 of 13</div>', html_before_p9)
html_before_p9 = re.sub(r'<div>Page 07 of \d+</div>', '<div>Page 07 of 13</div>', html_before_p9)
html_before_p9 = re.sub(r'<div>Page 08 of \d+</div>', '<div>Page 08 of 13</div>', html_before_p9)

final_html = html_before_p9 + page_9_html + '\n\n' + new_page_10_curriculum + '\n\n' + new_page_11_conclusion + '\n\n' + new_page_12_team + '\n\n' + new_page_13_acknowledgments + '\n</body>\n</html>\n'

with open('/home/yousefmsm1/Desktop/pdf_gen/output/html/ICPC-HUE-Community-Progress-Report-Gamma-Style.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print('Assembled complete 13-page report successfully!')
