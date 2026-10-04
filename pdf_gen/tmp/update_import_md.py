with open('/home/yousefmsm1/Desktop/pdf_gen/report/ICPC-HUE-Community-Progress-Report-Gamma-Import.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Update Card 03
text = text.replace('### Photo Gallery (2x2 Grid)', '### Photo Gallery (2x2 Enlarged Grid)')

# Find Card 05
import re
card_5_pattern = r'# Card 05:.*?---'
new_card_5 = '''# Card 05: Outreach & Community Momentum (16-Photo Delegation Gallery)

**Kicker:** 04 / OUTREACH & MOMENTUM  
## Converting Contest Experience into Season-Wide Momentum
*Documenting the tournament journey transformed competitive programming into an exciting, high-visibility activity across Horus University.*

### 1. Documenting the Journey & 43K+ Facebook Views
A synchronized media campaign published photos of participating teams, travel footage, and on-site tournament updates. This generated approximately **43,000 views on Facebook**, introducing collegiate problem solving to thousands of students and establishing competitive programming as a recognized university endeavor.

### 2. Educational Video Content Series
Three professionally edited introductory videos were released to welcome incoming freshmen, illustrating problem-solving concepts, showcasing student achievements, and outlining upcoming training cohorts.

### 3. Hire Up Recruitment via icpchue.com/job
Launched recruitment via [icpchue.com/job](https://icpchue.com/job) for student instructors, mentors, media creators, and operations officers to formalize staffing.

### Field Documentation Gallery (16 Delegation Moments Grid):
- `report/ecpc_qulifcatio/FB_IMG_1790132541422.jpg` — Delegation bus travel to Alexandria
- `report/ecpc_qulifcatio/FB_IMG_1790132708823.jpg` — Team 2050 in competition cubicle
- `report/ecpc_qulifcatio/FB_IMG_1790132619620.jpg` — Team trio in official jerseys
- `report/ecpc_qulifcatio/FB_IMG_1790132740356.jpg` — Delegation cheer & trophy celebration
- `report/ecpc_qulifcatio/FB_IMG_1790132657082.jpg` — Team problem solving at station
- `report/ecpc_qulifcatio/FB_IMG_1790132659885.jpg` — Station focus & code debugging
- `report/ecpc_qulifcatio/FB_IMG_1790132664255.jpg` — Reviewing algorithmic logic
- `report/ecpc_qulifcatio/FB_IMG_1790132668477.jpg` — Collaborative contest coding
- `report/ecpc_qulifcatio/FB_IMG_1790132686754.jpg` — High-speed keyboard problem solving
- `report/ecpc_qulifcatio/FB_IMG_1790132690995.jpg` — Sheet analysis & test case parsing
- `report/ecpc_qulifcatio/FB_IMG_1790132693865.jpg` — Contest desk with balloon markers
- `report/ecpc_qulifcatio/FB_IMG_1790132696016.jpg` — Official tournament arena workstation
- `report/ecpc_qulifcatio/FB_IMG_1790132697858.jpg` — Algorithm strategy & discussion
- `report/ecpc_qulifcatio/FB_IMG_1790132699784.jpg` — Concentrated teamwork in hall
- `report/ecpc_qulifcatio/FB_IMG_1790132702043.jpg` — Intensive problem triage
- `report/ecpc_qulifcatio/FB_IMG_1790132707334.jpg` — Scoreboard tracking & excitement

---'''

text = re.sub(card_5_pattern, new_card_5, text, flags=re.DOTALL)

with open('/home/yousefmsm1/Desktop/pdf_gen/report/ICPC-HUE-Community-Progress-Report-Gamma-Import.md', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated Gamma outline successfully!')
