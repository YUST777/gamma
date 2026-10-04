import subprocess
import os

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

:root {
  --bg: #FFFFFF;
  --text-head: #000000;
  --text-body: #373737;
  --text-muted: #6B7280;
  --accent: #E19D1B;
  --accent-dark: #B47E17;
  --card-bg: #F9ECD1;
  --card-border: #DED1B8;
  --page-border: #EAE2D5;
}

body {
  margin: 0;
  padding: 0;
  background: #f0f0f0;
  font-family: 'Plus Jakarta Sans', sans-serif;
  color: var(--text-body);
}

.page {
  width: 210mm;
  height: 297mm;
  margin: 0 auto;
  box-sizing: border-box;
  background: #FFFFFF;
  padding: 16mm 18mm;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
}

.header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1.5px solid var(--page-border);
  padding-bottom: 8px;
  margin-bottom: 12px;
}

.inst-badge {
  display: flex;
  align-items: center;
  gap: 10px;
}

.inst-logo {
  height: 24px;
  width: auto;
  object-fit: contain;
}

.inst-text {
  font-size: 11px;
  font-weight: 700;
  color: var(--text-head);
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.inst-sub {
  color: var(--accent-dark);
  font-weight: 600;
}

.pill-tag {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  color: var(--accent-dark);
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.kicker {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.kicker-bar {
  width: 24px;
  height: 4px;
  background: var(--accent);
  border-radius: 2px;
}

.kicker span {
  font-size: 11px;
  font-weight: 700;
  color: var(--accent-dark);
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

.slide-title {
  font-size: 23px;
  font-weight: 800;
  color: var(--text-head);
  line-height: 1.15;
  margin: 0 0 6px 0;
  letter-spacing: -0.3px;
}

.slide-sub {
  font-size: 11.5px;
  color: var(--text-body);
  margin: 0 0 16px 0;
  line-height: 1.4;
}

.card-title {
  font-size: 14px;
  font-weight: 800;
  color: var(--text-head);
  letter-spacing: -0.2px;
}

.card-body {
  font-size: 10.5px;
  color: var(--text-body);
  line-height: 1.45;
}

.footer-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1.5px solid var(--page-border);
  padding-top: 8px;
  font-size: 9.5px;
  color: var(--text-muted);
}
</style>
</head>
<body>

<section class="page">
  <div>
    <div class="header-bar">
      <div class="inst-badge">
        <img src="/home/yousefmsm1/Desktop/pdf_gen/report/assets/horus_logo.png" class="inst-logo" alt="Horus University Logo">
        <div class="inst-text">Horus University — Egypt • <span class="inst-sub">ICPC HUE Community</span></div>
      </div>
      <div class="pill-tag">08 / Ecosystem & Engagement</div>
    </div>

    <div class="kicker">
      <div class="kicker-bar"></div>
      <span>Ecosystem & Campus Engagement</span>
    </div>
    <h1 class="slide-title">Strategic Partnerships & Community Introduction Day</h1>
    <p class="slide-sub">
      Expanding Horus University's learning network and preparing a professional orientation for incoming freshmen.
    </p>

    <!-- TOP HALF: STRATEGIC REGIONAL PARTNERSHIPS (HORIZONTAL 3 COLUMNS) -->
    <div style="margin-bottom: 18px;">
      <div class="card-title" style="margin-bottom: 10px; font-size: 13.5px; display: flex; align-items: center; gap: 8px;">
        <span>Strategic Regional Partnerships</span>
        <span style="font-size: 10px; font-weight: 600; color: var(--text-muted); background: #F3F4F6; padding: 2px 8px; border-radius: 12px;">3 Partner Communities</span>
      </div>

      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;">
        <!-- Damietta -->
        <div style="background: #FFFFFF; border: 1px solid var(--card-border); border-left: 5px solid var(--accent); border-radius: 12px; padding: 14px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
          <div>
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 10px;">
              <div style="width: 58px; height: 58px; min-width: 58px; border-radius: 10px; overflow: hidden; background: #FFFFFF; border: 1px solid #EAE2D5; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 6px rgba(0,0,0,0.04);">
                <img src="/home/yousefmsm1/Desktop/pdf_gen/report/assets/logo_damietta_cropped.png" style="width: 100%; height: 100%; object-fit: contain;">
              </div>
              <div>
                <div style="font-weight: 800; font-size: 12px; color: var(--text-head); line-height: 1.25;">ACPC Club Damietta Univ.</div>
                <div style="font-size: 9.5px; font-weight: 700; color: var(--accent-dark); margin-top: 3px;">Regional Co-Host</div>
              </div>
            </div>
            <p class="card-body" style="font-size: 10px; line-height: 1.45; margin: 0;">
              Established through the joint organization of DCC 2026. This ongoing relationship enables shared problem setting, contest hosting infrastructure, and combined local competitions.
            </p>
          </div>
        </div>

        <!-- Port Said -->
        <div style="background: #FFFFFF; border: 1px solid var(--card-border); border-left: 5px solid var(--accent); border-radius: 12px; padding: 14px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
          <div>
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 10px;">
              <div style="width: 58px; height: 58px; min-width: 58px; border-radius: 10px; overflow: hidden; background: #F8F9FA; border: 1px solid #EAE2D5; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 6px rgba(0,0,0,0.04);">
                <img src="/home/yousefmsm1/Desktop/pdf_gen/report/assets/logo_psu_cropped.jpg" style="width: 100%; height: 100%; object-fit: contain;">
              </div>
              <div>
                <div style="font-weight: 800; font-size: 12px; color: var(--text-head); line-height: 1.25;">ICPC PSU Community</div>
                <div style="font-size: 9.5px; font-weight: 700; color: var(--accent-dark); margin-top: 3px;">Port Said University</div>
              </div>
            </div>
            <p class="card-body" style="font-size: 10px; line-height: 1.45; margin: 0;">
              A direct connection to a seasoned regional community with proven ECPC bronze-medal experience, creating valuable peer mentoring opportunities for advanced HUE teams.
            </p>
          </div>
        </div>

        <!-- Assiut -->
        <div style="background: #FFFFFF; border: 1px solid var(--card-border); border-left: 5px solid var(--accent); border-radius: 12px; padding: 14px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
          <div>
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 10px;">
              <div style="width: 58px; height: 58px; min-width: 58px; border-radius: 10px; overflow: hidden; background: #000000; border: 1px solid #333333; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 6px rgba(0,0,0,0.12);">
                <img src="/home/yousefmsm1/Desktop/pdf_gen/report/assets/logo_assiut_cropped.png" style="width: 100%; height: 100%; object-fit: contain;">
              </div>
              <div>
                <div style="font-weight: 800; font-size: 12px; color: var(--text-head); line-height: 1.25;">ICPC Assiut Community</div>
                <div style="font-size: 9.5px; font-weight: 700; color: var(--accent-dark); margin-top: 3px;">Assiut University</div>
              </div>
            </div>
            <p class="card-body" style="font-size: 10px; line-height: 1.45; margin: 0;">
              Cooperation focused on pedagogical standards and instructor training, drawing upon one of the largest and most successful competitive programming ecosystems in Egypt.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- BOTTOM HALF: COMMUNITY INTRODUCTION DAY PREPARATIONS (HORIZONTAL FULL WIDTH) -->
    <div style="background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 14px; padding: 18px 20px;">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
        <div>
          <div class="card-title" style="color: var(--accent-dark); font-size: 15px; margin-bottom: 4px;">Community Introduction Day Preparations</div>
          <p class="card-body" style="font-size: 11px; margin: 0; color: var(--text-head); font-weight: 500;">
            To welcome incoming students and establish professional standards from day one, ICPC HUE developed a comprehensive set of event assets:
          </p>
        </div>
        <div style="background: #FFFFFF; border: 1px solid var(--card-border); border-radius: 20px; padding: 4px 12px; font-size: 10px; font-weight: 700; color: var(--accent-dark); white-space: nowrap;">
          Freshmen Intake 2026/27
        </div>
      </div>

      <!-- 6 Event Assets Grid (3 columns x 2 rows) -->
      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 14px;">
        <div style="background: #FFFFFF; border: 1px solid var(--card-border); border-radius: 10px; padding: 10px 12px;">
          <div style="font-weight: 800; font-size: 11px; color: var(--text-head); margin-bottom: 2px; display: flex; align-items: center; gap: 6px;">
            <span>🏆</span> Award Certificates
          </div>
          <div style="font-size: 9.8px; color: var(--text-muted);">Honoring top 5 ECPC teams</div>
        </div>

        <div style="background: #FFFFFF; border: 1px solid var(--card-border); border-radius: 10px; padding: 10px 12px;">
          <div style="font-weight: 800; font-size: 11px; color: var(--text-head); margin-bottom: 2px; display: flex; align-items: center; gap: 6px;">
            <span>💵</span> Financial Prizes
          </div>
          <div style="font-size: 9.8px; color: var(--text-muted);">Reward checks for top achievers</div>
        </div>

        <div style="background: #FFFFFF; border: 1px solid var(--card-border); border-radius: 10px; padding: 10px 12px;">
          <div style="font-weight: 800; font-size: 11px; color: var(--text-head); margin-bottom: 2px; display: flex; align-items: center; gap: 6px;">
            <span>👕</span> Official T-Shirts
          </div>
          <div style="font-size: 9.8px; color: var(--text-muted);">Branded community apparel</div>
        </div>

        <div style="background: #FFFFFF; border: 1px solid var(--card-border); border-radius: 10px; padding: 10px 12px;">
          <div style="font-weight: 800; font-size: 11px; color: var(--text-head); margin-bottom: 2px; display: flex; align-items: center; gap: 6px;">
            <span>📄</span> Printed Flyers
          </div>
          <div style="font-size: 9.8px; color: var(--text-muted);">Season roadmap & intake guides</div>
        </div>

        <div style="background: #FFFFFF; border: 1px solid var(--card-border); border-radius: 10px; padding: 10px 12px;">
          <div style="font-weight: 800; font-size: 11px; color: var(--text-head); margin-bottom: 2px; display: flex; align-items: center; gap: 6px;">
            <span>🚩</span> Flag & Banners
          </div>
          <div style="font-size: 9.8px; color: var(--text-muted);">Official HUE roll-ups and flags</div>
        </div>

        <div style="background: #FFFFFF; border: 1px solid var(--card-border); border-radius: 10px; padding: 10px 12px;">
          <div style="font-weight: 800; font-size: 11px; color: var(--text-head); margin-bottom: 2px; display: flex; align-items: center; gap: 6px;">
            <span>🎁</span> Welcome Gifts
          </div>
          <div style="font-size: 9.8px; color: var(--text-muted);">Chocolates and intake merchandise</div>
        </div>
      </div>

      <!-- Keynote Speaker (Horizontal Banner) -->
      <div style="background: #FFFFFF; border-radius: 10px; border: 1px solid var(--card-border); border-left: 4px solid var(--accent); padding: 12px 16px; display: flex; align-items: center; gap: 14px;">
        <div style="width: 40px; height: 40px; min-width: 40px; border-radius: 50%; background: var(--card-bg); display: flex; align-items: center; justify-content: center; font-size: 18px;">
          🎤
        </div>
        <div>
          <div style="font-weight: 800; font-size: 11.5px; color: var(--text-head); margin-bottom: 2px;">
            Keynote Speaker: Official Collegiate Guest Address
          </div>
          <p style="font-size: 10.2px; margin: 0; color: var(--text-body); line-height: 1.45;">
            Contacted an <strong>ICPC-qualified veteran</strong> to deliver a guest address on real-world problem-solving value, algorithmic careers, and the discipline needed to excel in collegiate contests.
          </p>
        </div>
      </div>
    </div>
  </div>

  <div class="footer-bar">
    <div><strong>ICPC HUE</strong> • Annual Progress Dossier 2025 – 2027</div>
    <div>Page 09 of 14</div>
  </div>
</section>

</body>
</html>
"""

with open('/home/yousefmsm1/Desktop/pdf_gen/tmp/test_page9.html', 'w') as f:
    f.write(html_template)

print("Test page written.")
