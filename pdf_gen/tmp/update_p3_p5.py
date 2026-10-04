import re

with open('/home/yousefmsm1/Desktop/pdf_gen/output/html/ICPC-HUE-Community-Progress-Report-Gamma-Style.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Page 3: make photo boxes bigger (180px instead of 125px)
old_p3 = '''    <!-- 2x2 Photo Mosaic ("Too Much Photos") -->
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 10px;">
      <div>
        <div class="photo-box" style="height: 125px;">
          <img src="../../report/dcc/FB_IMG_1790132479548.jpg" alt="DCC Contest Lab">
        </div>
        <div class="photo-caption">Contestants in the computer lab during the DCC offline final.</div>
      </div>

      <div>
        <div class="photo-box" style="height: 125px;">
          <img src="../../report/dcc/FB_IMG_1790132765397.jpg" alt="First Place Award Ceremony">
        </div>
        <div class="photo-caption">First Place winners receiving their championship check.</div>
      </div>

      <div>
        <div class="photo-box" style="height: 125px;">
          <img src="../../report/dcc/FB_IMG_1790132770668.jpg" alt="Awards Ceremony with DCC and HUE logos">
        </div>
        <div class="photo-caption">Official DCC stage featuring ACPC DU and Horus University organizers.</div>
      </div>

      <div>
        <div class="photo-box" style="height: 125px;">
          <img src="../../report/dcc/FB_IMG_1790132476044.jpg" alt="Opening Address and Orientation">
        </div>
        <div class="photo-caption">Opening address and contest orientation delivered by faculty and organizers.</div>
      </div>
    </div>'''

new_p3 = '''    <!-- 2x2 Photo Mosaic (Enlarged High-Impact Gallery) -->
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 14px;">
      <div>
        <div class="photo-box" style="height: 175px;">
          <img src="../../report/dcc/FB_IMG_1790132479548.jpg" alt="DCC Contest Lab">
        </div>
        <div class="photo-caption" style="font-size: 9.5px; margin-top: 4px;">Contestants in the computer lab during the DCC offline final.</div>
      </div>

      <div>
        <div class="photo-box" style="height: 175px;">
          <img src="../../report/dcc/FB_IMG_1790132765397.jpg" alt="First Place Award Ceremony">
        </div>
        <div class="photo-caption" style="font-size: 9.5px; margin-top: 4px;">First Place winners receiving their championship check.</div>
      </div>

      <div>
        <div class="photo-box" style="height: 175px;">
          <img src="../../report/dcc/FB_IMG_1790132770668.jpg" alt="Awards Ceremony with DCC and HUE logos">
        </div>
        <div class="photo-caption" style="font-size: 9.5px; margin-top: 4px;">Official DCC stage featuring ACPC DU and Horus University organizers.</div>
      </div>

      <div>
        <div class="photo-box" style="height: 175px;">
          <img src="../../report/dcc/FB_IMG_1790132476044.jpg" alt="Opening Address and Orientation">
        </div>
        <div class="photo-caption" style="font-size: 9.5px; margin-top: 4px;">Opening address and contest orientation delivered by faculty and organizers.</div>
      </div>
    </div>'''

if old_p3 in html:
    html = html.replace(old_p3, new_p3)
    print("Page 3 photo size updated successfully.")
else:
    print("Warning: old_p3 snippet not found verbatim.")

# 2. Update Page 5: 16-photo grid & delete caption
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
    grid_items += f'''        <div class="photo-box" style="height: 84px; margin: 0; border-radius: 6px;">
          <img src="../../report/ecpc_qulifcatio/{img_name}" alt="{alt_text}">
        </div>\n'''

new_p5_collage = f'''    <!-- Multi-Photo Delegation Gallery (16 Photos) -->
    <div style="background: #FDF9F2; border: 1px solid var(--card-border); border-radius: 12px; padding: 10px;">
      <div style="font-size: 10px; font-weight: 800; color: var(--accent-dark); text-transform: uppercase; margin-bottom: 8px; letter-spacing: 0.04em;">
        Field Documentation • Delegation Journey &amp; National Competition Arena (16 Delegation Moments)
      </div>
      <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 7px;">
{grid_items}      </div>
    </div>'''

# Find the old Page 5 collage block using regex or string match
p5_regex = r'<!-- Multi-Photo Delegation Collage \(5 Photos\) -->.*?</div>\s*</div>\s*</div>'
match = re.search(r'<!-- Multi-Photo Delegation Collage.*?</div>\s*</div>\s*</div>', html, re.DOTALL)
if match:
    # Let's inspect what's matched
    print("Found Page 5 collage block.")
    html = html[:match.start()] + new_p5_collage + html[match.end():]
    print("Page 5 collage replaced successfully.")
else:
    print("Warning: Page 5 regex did not match.")

with open('/home/yousefmsm1/Desktop/pdf_gen/output/html/ICPC-HUE-Community-Progress-Report-Gamma-Style.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done writing updated HTML.")
