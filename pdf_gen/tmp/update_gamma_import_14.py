with open('/home/yousefmsm1/Desktop/pdf_gen/report/ICPC-HUE-Community-Progress-Report-Gamma-Import.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Update Card 05
import re

card_5_new = '''# Card 05: Converting Contest Experience into Season-Wide Momentum

**Kicker:** 04 / OUTREACH & MOMENTUM  
## Converting Contest Experience into Season-Wide Momentum
*Documenting the tournament journey transformed competitive programming into an exciting, high-visibility activity across Horus University.*

### Strategic Outreach Metrics
- **43K+ Facebook Views:** A synchronized campaign published travel footage and updates, generating 43,000+ views and establishing competitive programming as a recognized university endeavor.
- **Educational Video Series:** Three professionally edited videos welcomed incoming freshmen, illustrating problem-solving concepts, showcasing student achievements, and outlining upcoming training cohorts.
- **Hire Up Recruitment:** Launched recruitment via [icpchue.com/job](https://icpchue.com/job) for student instructors, mentors, media creators, and operations officers.

### Visual Documentation:
- `report/ecpc_qulifcatio/FB_IMG_1790132541422.jpg` — Delegation transit to Alexandria: building community synergy, morale, and focus.
- `report/ecpc_qulifcatio/FB_IMG_1790132740356.jpg` — Post-contest tournament celebration on the AASTMT Alexandria campus lawn.

> **Institutional Impact & Recruitment Surge:** The high-visibility media coverage and viral social media reception directly accelerated community recruitment for the 2026/2027 season. Over 300 prospective freshmen and returning students registered interest via icpchue.com/job within the first 72 hours, laying the groundwork for our largest intake to date.

---

# Card 06: Our 16 Competing Teams at ECPC Qualifications

**Kicker:** 05 / NATIONAL DELEGATION  
## Our 16 Competing Teams at ECPC Qualifications
*48 student competitors representing the Faculty of Artificial Intelligence and Faculty of Engineering across 16 official tournament stations at AASTMT, Alexandria.*

### Delegation Key Metrics
- **16 Teams:** Official Horus University delegation.
- **48 Students:** Active competitors solving in parallel.
- **2 Faculties:** Interdisciplinary collaboration between AI and Engineering.
- **5 Hours:** Continuous high-intensity algorithmic problem solving.

### The 16 Official Tournament Stations (4x4 Showcase Grid)
1. **Team 01 (Team 2050):** `report/ecpc_qulifcatio/FB_IMG_1790132708823.jpg` — Station 2050
2. **Team 02 (Lead Solvers):** `report/ecpc_qulifcatio/FB_IMG_1790132683848.jpg` — Station 2038
3. **Team 03:** `report/ecpc_qulifcatio/FB_IMG_1790132657082.jpg` — Station Alpha
4. **Team 04:** `report/ecpc_qulifcatio/FB_IMG_1790132659885.jpg` — Station Beta
5. **Team 05:** `report/ecpc_qulifcatio/FB_IMG_1790132664255.jpg` — Station Gamma
6. **Team 06:** `report/ecpc_qulifcatio/FB_IMG_1790132668477.jpg` — Station Delta
7. **Team 07:** `report/ecpc_qulifcatio/FB_IMG_1790132686754.jpg` — Station Epsilon
8. **Team 08:** `report/ecpc_qulifcatio/FB_IMG_1790132690995.jpg` — Station Zeta
9. **Team 09:** `report/ecpc_qulifcatio/FB_IMG_1790132693865.jpg` — Station Eta
10. **Team 10:** `report/ecpc_qulifcatio/FB_IMG_1790132696016.jpg` — Station Theta
11. **Team 11:** `report/ecpc_qulifcatio/FB_IMG_1790132697858.jpg` — Station Iota
12. **Team 12:** `report/ecpc_qulifcatio/FB_IMG_1790132699784.jpg` — Station Kappa
13. **Team 13:** `report/ecpc_qulifcatio/FB_IMG_1790132702043.jpg` — Station Lambda
14. **Team 14:** `report/ecpc_qulifcatio/FB_IMG_1790132703739.jpg` — Station Mu
15. **Team 15:** `report/ecpc_qulifcatio/FB_IMG_1790132705475.jpg` — Station Nu
16. **Team 16:** `report/ecpc_qulifcatio/FB_IMG_1790132707334.jpg` — Station Xi'''

# Replace Card 05 up to Card 06
card_5_pattern = r'# Card 05:.*?# Card 06:'
text = re.sub(card_5_pattern, card_5_new + '\n\n---\n\n# Card 07:', text, flags=re.DOTALL)

# Now renumber the subsequent cards:
# Card 06 was renamed to Card 07
# Now Card 07 -> Card 08, Card 08 -> Card 09, etc.
# Let's do this carefully:
card_renames = [
    ('Card 13: Academic Supervision', 'Card 14: Academic Supervision'),
    ('Card 12: Meet the Team', 'Card 13: Meet the Team'),
    ('Card 11: Conclusion', 'Card 12: Conclusion'),
    ('Card 10: Academic Curriculum', 'Card 11: Academic Curriculum'),
    ('Card 09: 2026/2027 Road', 'Card 10: 2026/2027 Road'),
    ('Card 08: Strategic Partnerships', 'Card 09: Strategic Partnerships'),
    ('Card 07: Leadership Pipeline', 'Card 08: Leadership Pipeline'),
    ('Card 06: The Four Community', 'Card 07: The Four Community'),
]

for old_c, new_c in card_renames:
    text = text.replace(old_c, new_c)

with open('/home/yousefmsm1/Desktop/pdf_gen/report/ICPC-HUE-Community-Progress-Report-Gamma-Import.md', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated Gamma outline to 14 cards successfully!')
