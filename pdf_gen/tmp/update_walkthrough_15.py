with open('/home/yousefmsm1/.gemini/antigravity/brain/8d42f6dc-2245-44cf-8d50-2f03b9093fe9/walkthrough.md') as f:
    text = f.read()

# Update title and deliverables
text = text.replace('14-Page Complete Edition', '15-Page Complete Edition')
text = text.replace('High-Resolution Vector PDF (14 A4 Pages):', 'High-Resolution Vector PDF (15 A4 Pages):')
text = text.replace('Gamma 1-Click Markdown Import (14 Cards):', 'Gamma 1-Click Markdown Import (15 Cards):')

# Add slide 15 to carousel
slide_14 = '![Page 14 — Meet the Team (Exact Canva Styling)](/home/yousefmsm1/.gemini/antigravity/brain/8d42f6dc-2245-44cf-8d50-2f03b9093fe9/images/page-14.png)\n````'
slide_15 = '![Page 14 — Meet the Team (Exact Canva Styling)](/home/yousefmsm1/.gemini/antigravity/brain/8d42f6dc-2245-44cf-8d50-2f03b9093fe9/images/page-14.png)\n<!-- slide -->\n![Page 15 — Official Channels & Digital Ecosystem (Large QR Codes)](/home/yousefmsm1/.gemini/antigravity/brain/8d42f6dc-2245-44cf-8d50-2f03b9093fe9/images/page-15.png)\n````'
text = text.replace(slide_14, slide_15)

# Add section 13
target_hr = '\n---\n\n\n## Deliverables'
section_13 = '''

13. **Page 04 "Within 1 Problem" Narrative & Brand New Page 15 (Digital Channels):**
    - **Amplified "Within 1 Problem" Strategic Narrative (Page 04):**
      - Emphasized that solving **4 complex algorithmic problems** in our rookie debut placed Horus University literally **within 1 single problem** of qualifying for the ECPC National Finals.
      - Framed this as definitive empirical proof that the ICPC HUE curriculum, instructor quality, and training rigor work.
      - Directly connected this baseline to Page 12, arguing that initiating 5-hour timed simulations earlier makes official National Qualification in 2026/2027 highly probable.
    - **Added Official Back Cover (Page 15 — Digital Channels & Community Portal):**
      - Dedicated portal page presenting the custom platform engine (`icpchue.com`), **Facebook** (`@icpchue`), **LinkedIn** (`ICPC HUE`), and **Telegram** (`@ICPCHUE`).
      - Purged paragraph text clutter per user request.
      - Rendered **large, scannable QR codes (105px x 105px)** centered inside each card, with clean direct links placed directly underneath.
      - Features official closing seal of Horus University & Faculty of Artificial Intelligence.
    - **Perfect Document Symmetry (15 Pages Total):**
      - Exactly 5 thematic pillars of 3 pages each:
        - *Pillar 1 (Pages 01–03):* Retrospective & DCC Proving Ground
        - *Pillar 2 (Pages 04–06):* National ECPC Qualification & Contingent
        - *Pillar 3 (Pages 07–09):* Organizational Model & Regional Network
        - *Pillar 4 (Pages 10–12):* 2026/2027 Season Roadmap & Curriculum
        - *Pillar 5 (Pages 13–15):* Governance, Team Roster & Official Portal
      - Zero overflow, verified vector PDF.
'''

text = text.replace(target_hr, section_13 + target_hr)

with open('/home/yousefmsm1/.gemini/antigravity/brain/8d42f6dc-2245-44cf-8d50-2f03b9093fe9/walkthrough.md', 'w') as f:
    f.write(text)

print('walkthrough.md updated with 15 pages!')
