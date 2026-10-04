import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

const here = path.dirname(fileURLToPath(import.meta.url));
const workspaceDir = path.resolve(here, '..');
const skillDir = process.env.SKILL_DIR;
const tmpDir = process.env.TMP_DIR ?? path.join(workspaceDir, '.build', 'evidence-run');
const finalPath = process.env.FINAL_PPTX ?? path.join(workspaceDir, 'output', 'bataa-evidence-validation.pptx');
if (!skillDir || !path.isAbsolute(skillDir)) throw new Error('SKILL_DIR must be absolute');
if (!path.isAbsolute(tmpDir) || !path.isAbsolute(finalPath)) throw new Error('TMP_DIR and FINAL_PPTX must be absolute');

await fs.mkdir(tmpDir, { recursive: true });
await fs.mkdir(path.dirname(finalPath), { recursive: true });

const { finalizePresentation } = await import(
  pathToFileURL(path.join(skillDir, 'container_tools/artifact_tool_utils.mjs')).href,
);

const W = 1280;
const H = 720;
const FONT = 'Lato';
const C = {
  cream: '#FFF6E9',
  paper: '#FFFDF8',
  cream2: '#FBEAD4',
  ink: '#2D180B',
  dark: '#1B100B',
  dark2: '#2B1910',
  brown: '#895F3C',
  muted: '#7D5C42',
  line: '#E7C9A7',
  orange: '#FF8500',
  orangeDark: '#C45300',
  orangeSoft: '#FFD5A3',
  violet: '#6E5BAA',
  violetSoft: '#E8E2FF',
  green: '#2E9B62',
  greenSoft: '#DFF2E5',
  red: '#C64A39',
  redSoft: '#F8DFD9',
  white: '#FFFFFF',
};

function shape(slide, geometry, position, fill = 'none', line = { fill: 'none', width: 0 }, extra = {}) {
  return slide.shapes.add({ geometry, position, fill, line, ...extra });
}

function text(slide, value, position, style = {}, fill = 'none', line = { fill: 'none', width: 0 }) {
  const s = shape(slide, 'textbox', position, fill, line);
  s.text = value;
  s.text.style = {
    typeface: FONT,
    fontSize: 20,
    color: C.ink,
    autoFit: 'shrinkText',
    wrap: 'square',
    verticalAlignment: 'top',
    insets: { top: 0, right: 0, bottom: 0, left: 0 },
    ...style,
  };
  return s;
}

function rich(slide, paragraphs, position, style = {}, fill = 'none', line = { fill: 'none', width: 0 }) {
  const s = shape(slide, 'textbox', position, fill, line);
  s.text = paragraphs;
  s.text.style = {
    typeface: FONT,
    fontSize: 20,
    color: C.ink,
    autoFit: 'shrinkText',
    wrap: 'square',
    verticalAlignment: 'top',
    insets: { top: 0, right: 0, bottom: 0, left: 0 },
    ...style,
  };
  return s;
}

function card(slide, position, fill = C.paper, border = C.line, radius = 'rounded-2xl', shadow = 'shadow-sm') {
  return shape(slide, 'roundRect', position, fill, { style: 'solid', fill: border, width: 1 }, { borderRadius: radius, shadow });
}

function pill(slide, value, position, fill, color, opts = {}) {
  const s = shape(slide, 'roundRect', position, fill, { style: 'solid', fill, width: 0 }, { borderRadius: 'rounded-full' });
  s.text = value;
  s.text.style = {
    typeface: FONT,
    fontSize: opts.fontSize ?? 12,
    bold: true,
    color,
    alignment: 'center',
    verticalAlignment: 'middle',
    autoFit: 'shrinkText',
    insets: { top: 0, right: 8, bottom: 0, left: 8 },
  };
  return s;
}

function circle(slide, x, y, size, fill, value = '', color = C.ink, fontSize = 18) {
  const s = shape(slide, 'ellipse', { left: x, top: y, width: size, height: size }, fill, { fill, width: 0 });
  if (value) {
    s.text = value;
    s.text.style = { typeface: FONT, fontSize, bold: true, color, alignment: 'center', verticalAlignment: 'middle', autoFit: 'shrinkText', insets: { top: 0, right: 0, bottom: 0, left: 0 } };
  }
  return s;
}

function line(slide, x1, y1, x2, y2, color = C.line, width = 2) {
  return shape(slide, 'line', { left: Math.min(x1, x2), top: Math.min(y1, y2), width: Math.abs(x2 - x1), height: Math.abs(y2 - y1) }, 'none', { style: 'solid', fill: color, width });
}

function bg(slide, color) { slide.background.fill = color; }

function header(slide, index, section, dark = false) {
  text(slide, 'bataa', { left: 64, top: 26, width: 130, height: 32 }, { fontSize: 23, bold: true, color: C.orange });
  text(slide, section.toUpperCase(), { left: 222, top: 31, width: 500, height: 20 }, { fontSize: 11, bold: true, color: dark ? '#D7BDA9' : C.brown });
  text(slide, String(index).padStart(2, '0'), { left: 1176, top: 29, width: 40, height: 20 }, { fontSize: 13, bold: true, color: dark ? C.cream : C.ink, alignment: 'right' });
  line(slide, 64, 68, 1216, 68, dark ? '#5D3B27' : C.line, 1);
}

function footer(slide, value, dark = false) {
  text(slide, value, { left: 64, top: 683, width: 1100, height: 17 }, { fontSize: 10.5, color: dark ? '#C9A98C' : C.muted });
}

function title(slide, value, subtitle = '', dark = false, y = 102) {
  text(slide, value, { left: 64, top: y, width: 1030, height: 64 }, { fontSize: 44, bold: true, color: dark ? C.cream : C.ink });
  if (subtitle) text(slide, subtitle, { left: 68, top: y + 70, width: 970, height: 38 }, { fontSize: 19, color: dark ? '#E3CDBB' : C.brown });
}

function note(slide, value) { slide.speakerNotes.textFrame.setText(value); }

function metric(slide, x, y, width, value, label, color = C.orange, dark = false) {
  card(slide, { left: x, top: y, width, height: 132 }, dark ? C.dark2 : C.paper, dark ? '#5D3B27' : C.line, 'rounded-2xl', 'shadow-sm');
  text(slide, value, { left: x + 22, top: y + 18, width: width - 44, height: 52 }, { fontSize: 37, bold: true, color });
  text(slide, label, { left: x + 22, top: y + 79, width: width - 44, height: 33 }, { fontSize: 14, color: dark ? '#D8BBA4' : C.brown });
}

function bulletRow(slide, x, y, width, label, body, color = C.orange, dark = false, number = '') {
  circle(slide, x, y + 2, 28, color, number, C.white, 11);
  text(slide, label, { left: x + 42, top: y, width: width - 42, height: 21 }, { fontSize: 13, bold: true, color });
  text(slide, body, { left: x + 42, top: y + 25, width: width - 42, height: 39 }, { fontSize: 17, color: dark ? C.cream : C.ink });
}

function sourceNote({ urls, caveat = '' }) {
  return `Sources checked 19 September 2026:\n${urls.map(u => `- ${u}`).join('\n')}\n\n${caveat}`;
}

const deck = Presentation.create({ slideSize: { width: W, height: H } });

// 1. Cover
{
  const s = deck.slides.add(); bg(s, C.cream);
  text(s, 'bataa', { left: 64, top: 42, width: 200, height: 42 }, { fontSize: 31, bold: true, color: C.orange });
  pill(s, 'EVIDENCE APPENDIX', { left: 64, top: 126, width: 172, height: 31 }, C.orangeSoft, C.orangeDark);
  text(s, 'Is the problem real?', { left: 64, top: 188, width: 700, height: 76 }, { fontSize: 57, bold: true, color: C.ink });
  text(s, 'Evidence and validation so far', { left: 68, top: 286, width: 570, height: 40 }, { fontSize: 25, color: C.brown });
  card(s, { left: 68, top: 388, width: 604, height: 132 }, C.dark, C.dark, 'rounded-3xl', 'shadow-md');
  pill(s, 'CURRENT VERDICT', { left: 100, top: 416, width: 142, height: 28 }, C.orange, C.white);
  text(s, 'Credible problem.\nUnproven Bataa fit.', { left: 100, top: 456, width: 500, height: 56 }, { fontSize: 28, bold: true, color: C.cream });
  card(s, { left: 770, top: 120, width: 400, height: 438 }, C.paper, C.line, 'rounded-3xl', 'shadow-md');
  text(s, 'EVIDENCE LADDER', { left: 812, top: 158, width: 260, height: 20 }, { fontSize: 12, bold: true, color: C.brown });
  const ladder = [
    ['01', 'Direct', 'Bataa conversations + prototype', C.orange],
    ['02', 'External', 'Research and market behavior', C.violet],
    ['03', 'Unproven', 'Retention, outcomes, payment', C.green],
  ];
  ladder.forEach(([n, h, b, color], i) => {
    const y = 218 + i * 92;
    circle(s, 812, y, 42, color, n, C.white, 11);
    text(s, h, { left: 874, top: y + 1, width: 220, height: 23 }, { fontSize: 20, bold: true, color: C.ink });
    text(s, b, { left: 874, top: y + 28, width: 250, height: 25 }, { fontSize: 14, color: C.brown });
    if (i < 2) line(s, 832, y + 52, 832, y + 86, C.line, 2);
  });
  text(s, 'Prepared 19 September 2026  ·  external sources cited in notes', { left: 64, top: 672, width: 650, height: 18 }, { fontSize: 11, color: C.muted });
  note(s, sourceNote({ urls: [], caveat: 'Purpose of this appendix: answer the evidence / validation question without presenting unsupported Bataa claims as facts. “Credible problem” means the mechanism is supported by direct discovery plus external evidence. “Unproven Bataa fit” means the team has not yet measured Bataa-specific retention, learning gains, or willingness to pay.' }));
}

// 2. Honest answer
{
  const s = deck.slides.add(); bg(s, C.dark); header(s, 2, 'Executive verdict', true);
  title(s, 'The honest answer has two parts', 'External evidence supports the problem and mechanism. Bataa-specific proof is still ahead.', true);
  card(s, { left: 68, top: 252, width: 540, height: 315 }, C.dark2, '#5D3B27', 'rounded-3xl', 'shadow-md');
  pill(s, 'WE CAN DEFEND', { left: 102, top: 284, width: 140, height: 28 }, C.green, C.white);
  text(s, 'The problem mechanism', { left: 102, top: 332, width: 420, height: 38 }, { fontSize: 28, bold: true, color: C.cream });
  bulletRow(s, 102, 392, 455, 'BEHAVIOR', 'Learners already use on-demand online resources.', C.orange, true, '1');
  bulletRow(s, 102, 468, 455, 'PEDAGOGY', 'Practice and informative feedback improve learning.', C.violet, true, '2');
  card(s, { left: 660, top: 252, width: 540, height: 315 }, C.cream, C.cream, 'rounded-3xl', 'shadow-md');
  pill(s, 'WE CANNOT CLAIM', { left: 694, top: 284, width: 158, height: 28 }, C.red, C.white);
  text(s, 'Bataa product–market fit', { left: 694, top: 332, width: 430, height: 38 }, { fontSize: 28, bold: true, color: C.ink });
  bulletRow(s, 694, 392, 455, 'UNKNOWN', 'How many learners feel this pain often enough.', C.red, false, '1');
  bulletRow(s, 694, 468, 455, 'UNKNOWN', 'Whether Bataa improves outcomes or earns payment.', C.red, false, '2');
  card(s, { left: 68, top: 598, width: 1132, height: 48 }, C.orange, C.orange, 'rounded-2xl', 'shadow-sm');
  text(s, 'Decision-quality statement: defend the thesis, then run a measured pilot.', { left: 98, top: 611, width: 1000, height: 23 }, { fontSize: 20, bold: true, color: C.ink });
  footer(s, 'Interpretation · evidence strength is deliberately separated from confidence in Bataa', true);
  note(s, sourceNote({ urls: [
    'https://survey.stackoverflow.co/2024/',
    'https://pmc.ncbi.nlm.nih.gov/articles/PMC4060654/',
    'https://pmc.ncbi.nlm.nih.gov/articles/PMC6987456/',
    'https://pmc.ncbi.nlm.nih.gov/articles/PMC8966850/',
  ], caveat: 'These sources support the behavior, pedagogy, and regional context. None is a randomized test of Bataa, so none proves Bataa retention, learning gains, or willingness to pay.' }));
}

// 3. Direct evidence
{
  const s = deck.slides.add(); bg(s, C.cream); header(s, 3, 'Direct Bataa evidence');
  title(s, 'Bataa has a directional signal from real learners', 'The team heard a recurring support gap at Horus University and built around it.', false);
  card(s, { left: 68, top: 244, width: 510, height: 320 }, C.dark, '#5D3B27', 'rounded-3xl', 'shadow-md');
  pill(s, 'FOUNDER-REPORTED', { left: 102, top: 276, width: 154, height: 28 }, C.orange, C.white);
  text(s, '“The question arrives\nafter the lesson.”', { left: 102, top: 331, width: 410, height: 90 }, { fontSize: 34, bold: true, color: C.cream });
  text(s, 'Horus University conversations surfaced late-night questions, hesitation about asking “basic” questions, and concern about cost or crowded courses.', { left: 102, top: 456, width: 410, height: 70 }, { fontSize: 17, color: '#E3CDBB' });
  card(s, { left: 628, top: 244, width: 572, height: 320 }, C.paper, C.line, 'rounded-3xl', 'shadow-md');
  text(s, 'What exists today', { left: 664, top: 278, width: 320, height: 32 }, { fontSize: 27, bold: true, color: C.ink });
  bulletRow(s, 664, 338, 480, 'DISCOVERY', 'A problem statement grounded in conversations, not a quantified survey.', C.orange, false, '1');
  bulletRow(s, 664, 420, 480, 'PROTOTYPE', 'A mobile daily-task loop and a desktop guidance concept already exist.', C.violet, false, '2');
  bulletRow(s, 664, 502, 480, 'MISSING RECORD', 'No verified participant count, dates, recruitment method, or transcripts were supplied.', C.red, false, '3');
  card(s, { left: 68, top: 598, width: 1132, height: 48 }, C.orangeSoft, C.orangeSoft, 'rounded-2xl', 'shadow-sm');
  text(s, 'Use this as discovery evidence. Do not present it as prevalence data.', { left: 98, top: 611, width: 1000, height: 23 }, { fontSize: 19, bold: true, color: C.ink });
  footer(s, 'Evidence status · directional discovery, not yet audited', false);
  note(s, sourceNote({ urls: [], caveat: 'Internal evidence source: user-provided Bataa brief describing conversations at Horus University and the current prototype. The brief did not provide a verified sample size, dates, recruitment method, recordings, transcripts, or coding sheet. This slide intentionally uses “founder-reported” and “surfaced” rather than a percentage or a claim about a “huge number” of students.' }));
}

// 4. Egypt signal
{
  const s = deck.slides.add(); bg(s, C.cream); header(s, 4, 'Egypt context');
  title(s, 'Egypt survey: students wanted more interaction', 'A large medical-student survey gives local context for the support gap, with important limits.', false);
  metric(s, 68, 228, 245, '4,935', 'responses', C.orange);
  metric(s, 330, 228, 245, '26', 'Egyptian medical schools', C.violet);
  metric(s, 592, 228, 245, '>50%', 'wanted more interactive sessions', C.green);
  metric(s, 854, 228, 346, '63%', 'rated recorded video tutorials most effective', C.orangeDark);
  const rows = [
    ['54.6%', 'said online education was not as effective as face-to-face', C.red],
    ['23%', 'reported bad internet connection', C.orange],
    ['17%', 'found it difficult to commit because of home distractions', C.violet],
    ['18%', 'reported less communication than face-to-face learning', C.green],
  ];
  rows.forEach(([v, b, color], i) => {
    const y = 404 + i * 48;
    text(s, v, { left: 84, top: y, width: 120, height: 25 }, { fontSize: 22, bold: true, color });
    line(s, 214, y + 15, 330, y + 15, color, 7);
    text(s, b, { left: 360, top: y + 1, width: 760, height: 24 }, { fontSize: 17, color: C.ink });
  });
  card(s, { left: 68, top: 606, width: 1132, height: 43 }, C.dark, C.dark, 'rounded-2xl', 'shadow-sm');
  text(s, 'Limit: pandemic-era medical students, social-media recruitment, descriptive self-report. This is local context, not Bataa demand.', { left: 92, top: 617, width: 1080, height: 20 }, { fontSize: 14, color: C.cream });
  footer(s, 'Mortagy et al. · BMC Medical Education · 2022 · source and caveat in notes', false);
  note(s, sourceNote({ urls: [
    'https://pmc.ncbi.nlm.nih.gov/articles/PMC8966850/',
    'https://doi.org/10.1186/s12909-022-03249-2',
  ], caveat: 'Mortagy et al. used a 29-item Google Forms survey distributed through social media, collected 20 Aug–5 Sep 2021. The sample covered 26 Egyptian medical schools. Findings are descriptive and self-reported; the authors caution about representativeness and the abrupt COVID-era transition. The study is relevant regional context, not evidence that Bataa users will activate or pay.' }));
}

// 5. Coding learning behavior
{
  const s = deck.slides.add(); bg(s, C.dark); header(s, 5, 'Existing behavior', true);
  title(s, 'Self-directed coding learning is already normal', 'The opportunity is to make the next action more guided, not to invent online learning from zero.', true);
  metric(s, 68, 237, 260, '65,437', 'survey responses', C.orange, true);
  metric(s, 348, 237, 260, '185', 'countries represented', C.violetSoft, true);
  metric(s, 628, 237, 260, '82%', 'say online resources are their top choice', C.greenSoft, true);
  card(s, { left: 918, top: 237, width: 282, height: 132 }, C.orange, C.orange, 'rounded-2xl', 'shadow-sm');
  text(s, '37%', { left: 944, top: 254, width: 225, height: 44 }, { fontSize: 37, bold: true, color: C.ink });
  text(s, 'say AI helps them learn to code', { left: 944, top: 310, width: 220, height: 32 }, { fontSize: 14, color: C.ink });
  text(s, 'What the survey shows', { left: 68, top: 420, width: 340, height: 28 }, { fontSize: 24, bold: true, color: C.cream });
  const resources = [
    ['83.9%', 'technical documentation', C.orange],
    ['80.3%', 'Stack Overflow', C.violetSoft],
    ['37.0%', 'AI tools', C.greenSoft],
    ['29.3%', 'interactive tutorials', C.orangeSoft],
  ];
  resources.forEach(([v, label, color], i) => {
    const y = 468 + i * 37;
    text(s, v, { left: 70, top: y, width: 100, height: 22 }, { fontSize: 17, bold: true, color });
    text(s, label, { left: 188, top: y + 1, width: 350, height: 20 }, { fontSize: 16, color: '#E3CDBB' });
    line(s, 430, y + 12, 430 + Math.round(parseFloat(v) * 4.2), y + 12, color, 8);
  });
  card(s, { left: 670, top: 420, width: 530, height: 190 }, C.dark2, '#5D3B27', 'rounded-3xl', 'shadow-md');
  pill(s, 'WHAT THIS SUPPORTS', { left: 706, top: 452, width: 156, height: 26 }, C.green, C.white);
  text(s, 'On-demand learning behavior already exists.', { left: 706, top: 498, width: 430, height: 30 }, { fontSize: 22, bold: true, color: C.cream });
  text(s, 'It does not prove novice demand in Egypt, Bataa retention, or a willingness to pay.', { left: 706, top: 548, width: 420, height: 40 }, { fontSize: 17, color: '#D8BBA4' });
  footer(s, 'Stack Overflow Developer Survey 2024 · self-selected developer sample', true);
  note(s, sourceNote({ urls: [
    'https://survey.stackoverflow.co/2024/',
    'https://survey.stackoverflow.co/2024/developer-profile/#2-online-resources-to-learn-how-to-code',
    'https://survey.stackoverflow.co/2024/ai/',
    'https://survey.stackoverflow.co/2024/methodology/',
  ], caveat: 'The survey reports 65,437 responses from 185 countries. It is a self-selected developer survey, not a representative sample of all learners or Egyptian students. Percentages for resources are multi-select descriptive responses. Use this slide as evidence of existing behavior, not a market-size estimate.' }));
}

// 6. Active learning
{
  const s = deck.slides.add(); bg(s, C.cream); header(s, 6, 'Learning mechanism');
  title(s, 'Practice beats passive exposure', 'The research base supports a small action, a check, and another attempt.', false);
  card(s, { left: 68, top: 236, width: 540, height: 348 }, C.orange, C.orange, 'rounded-3xl', 'shadow-md');
  text(s, '225', { left: 104, top: 275, width: 220, height: 70 }, { fontSize: 65, bold: true, color: C.ink });
  text(s, 'undergraduate STEM studies\nin a meta-analysis', { left: 108, top: 355, width: 340, height: 55 }, { fontSize: 22, bold: true, color: C.ink });
  line(s, 108, 438, 554, 438, C.ink, 2);
  text(s, '+0.47 SD', { left: 108, top: 462, width: 210, height: 42 }, { fontSize: 33, bold: true, color: C.ink });
  text(s, 'exam performance with active learning', { left: 330, top: 473, width: 230, height: 30 }, { fontSize: 16, color: C.ink });
  card(s, { left: 650, top: 236, width: 550, height: 154 }, C.paper, C.line, 'rounded-2xl', 'shadow-sm');
  pill(s, 'FAILURE RISK', { left: 686, top: 268, width: 112, height: 26 }, C.red, C.white);
  text(s, '1.95×', { left: 686, top: 310, width: 150, height: 46 }, { fontSize: 39, bold: true, color: C.red });
  text(s, 'odds of failure under traditional lecture vs active learning', { left: 850, top: 317, width: 290, height: 38 }, { fontSize: 17, color: C.ink });
  card(s, { left: 650, top: 414, width: 550, height: 170 }, C.dark, '#5D3B27', 'rounded-2xl', 'shadow-md');
  pill(s, 'IMPORTANT DESIGN DETAIL', { left: 686, top: 444, width: 184, height: 26 }, C.violet, C.white);
  text(s, '149-student physics study', { left: 686, top: 486, width: 300, height: 26 }, { fontSize: 21, bold: true, color: C.cream });
  text(s, 'Active instruction improved actual learning (+0.46 SD), while students felt they learned less (−0.56 SD).', { left: 686, top: 526, width: 450, height: 42 }, { fontSize: 17, color: '#D8BBA4' });
  footer(s, 'Freeman et al. PNAS 2014 · Deslauriers et al. PNAS 2019', false);
  note(s, sourceNote({ urls: [
    'https://pmc.ncbi.nlm.nih.gov/articles/PMC4060654/',
    'https://doi.org/10.1073/pnas.1319030111',
    'https://pmc.ncbi.nlm.nih.gov/articles/PMC6765278/',
    'https://doi.org/10.1073/pnas.1821936116',
  ], caveat: 'Freeman et al. synthesized 225 undergraduate STEM studies; the result supports active-learning pedagogy, not mobile-app demand. Deslauriers et al. studied two introductory physics courses (149 participants) and found a gap between actual learning and perceived learning. Bataa should explain effort and provide clear feedback rather than assuming “easy” feels like progress.' }));
}

// 7. Feedback
{
  const s = deck.slides.add(); bg(s, C.cream); header(s, 7, 'Feedback and safety');
  title(s, 'Feedback works when it carries information', 'Correctness alone is not enough. The learner needs a reason and a next move.', false);
  card(s, { left: 68, top: 242, width: 445, height: 335 }, C.dark, '#5D3B27', 'rounded-3xl', 'shadow-md');
  text(s, '435', { left: 104, top: 278, width: 190, height: 66 }, { fontSize: 62, bold: true, color: C.orange });
  text(s, 'studies in a feedback\nmeta-analysis', { left: 108, top: 352, width: 310, height: 52 }, { fontSize: 23, bold: true, color: C.cream });
  text(s, 'd = 0.48', { left: 108, top: 448, width: 200, height: 38 }, { fontSize: 32, bold: true, color: C.greenSoft });
  text(s, 'medium overall effect on learning, with substantial variation by feedback content', { left: 108, top: 496, width: 320, height: 48 }, { fontSize: 16, color: '#D8BBA4' });
  card(s, { left: 552, top: 242, width: 648, height: 335 }, C.paper, C.line, 'rounded-3xl', 'shadow-md');
  pill(s, 'BATAA DESIGN RULE', { left: 590, top: 276, width: 146, height: 27 }, C.orange, C.white);
  const rules = [
    ['01', 'Explain what happened', 'Name the concept or step behind the result.'],
    ['02', 'Show the next move', 'Offer a hint or smaller action, not a wall of text.'],
    ['03', 'Protect the retry', 'Let a learner try privately without public embarrassment.'],
  ];
  rules.forEach(([n, h, b], i) => {
    const y = 329 + i * 73;
    circle(s, 590, y, 32, i === 0 ? C.orange : i === 1 ? C.violet : C.green, n, C.white, 11);
    text(s, h, { left: 644, top: y + 1, width: 330, height: 22 }, { fontSize: 19, bold: true, color: C.ink });
    text(s, b, { left: 644, top: y + 27, width: 490, height: 24 }, { fontSize: 15, color: C.brown });
  });
  card(s, { left: 68, top: 606, width: 1132, height: 43 }, C.orangeSoft, C.orangeSoft, 'rounded-2xl', 'shadow-sm');
  text(s, 'Caveat: 17% of feedback effects were negative in the review. Format and information content matter.', { left: 98, top: 617, width: 1050, height: 20 }, { fontSize: 15, bold: true, color: C.ink });
  footer(s, 'Wisniewski, Zierer & Hattie · Frontiers in Psychology · 2020', false);
  note(s, sourceNote({ urls: [
    'https://pmc.ncbi.nlm.nih.gov/articles/PMC6987456/',
    'https://doi.org/10.3389/fpsyg.2019.03087',
    'https://www.jld.edu.au/article/view/293',
    'https://doi.org/10.5204/jld.v9i3.293',
  ], caveat: 'The feedback meta-analysis covered 435 studies, 994 effects, and more than 61,000 participants. It found a medium average effect with high heterogeneity; do not claim every feedback format works. Gillett-Swan’s online-learning article is qualitative/critical commentary about isolation and support, not a prevalence survey. The product implication is a hypothesis to test.' }));
}

// 8. Contextual AI
{
  const s = deck.slides.add(); bg(s, C.dark); header(s, 8, 'Contextual AI', true);
  title(s, 'Contextual AI has an early evidence signal', 'Adjacent product experiments suggest that relevant history can improve the next step.', true);
  card(s, { left: 68, top: 240, width: 528, height: 365 }, C.dark2, '#5D3B27', 'rounded-3xl', 'shadow-md');
  pill(s, 'GITHUB COPILOT', { left: 102, top: 274, width: 136, height: 27 }, C.orange, C.white);
  text(s, '95 professional developers', { left: 102, top: 322, width: 390, height: 28 }, { fontSize: 22, bold: true, color: C.cream });
  text(s, '78% vs 70%', { left: 102, top: 370, width: 280, height: 46 }, { fontSize: 37, bold: true, color: C.orange });
  text(s, 'completed the same JavaScript HTTP-server task', { left: 102, top: 418, width: 370, height: 28 }, { fontSize: 16, color: '#D8BBA4' });
  text(s, '55% faster', { left: 102, top: 474, width: 230, height: 38 }, { fontSize: 29, bold: true, color: C.greenSoft });
  text(s, '1h11 vs 2h41 average completion time', { left: 102, top: 518, width: 350, height: 25 }, { fontSize: 16, color: '#D8BBA4' });
  pill(s, 'ADJACENT EVIDENCE', { left: 102, top: 558, width: 146, height: 25 }, C.violet, C.white, { fontSize: 10 });
  card(s, { left: 640, top: 240, width: 560, height: 365 }, C.cream, C.cream, 'rounded-3xl', 'shadow-md');
  pill(s, 'KHANMIGO', { left: 676, top: 274, width: 104, height: 27 }, C.green, C.white);
  text(s, '>15M tutoring threads', { left: 676, top: 322, width: 420, height: 28 }, { fontSize: 22, bold: true, color: C.ink });
  const aiRows = [
    ['+3.4%', 'recent problem history improved next-item correctness'],
    ['+2.7%', 'unmastered prerequisite review improved next-item correctness'],
    ['+6.1%', 'combined gain in next-item correctness'],
    ['+5.09%', 'prior-24h context increased cognitive engagement'],
  ];
  aiRows.forEach(([v, b], i) => {
    const y = 374 + i * 49;
    text(s, v, { left: 676, top: y, width: 104, height: 24 }, { fontSize: 20, bold: true, color: i === 2 ? C.orangeDark : C.green });
    text(s, b, { left: 796, top: y + 1, width: 340, height: 28 }, { fontSize: 14, color: C.brown });
  });
  text(s, 'Both are adjacent evidence, not novice coding proof.', { left: 676, top: 568, width: 440, height: 22 }, { fontSize: 14, bold: true, color: C.ink });
  footer(s, 'GitHub experiment · Khan Academy product-learning report · limitations in notes', true);
  note(s, sourceNote({ urls: [
    'https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-on-developer-productivity-and-happiness/',
    'https://blog.khanacademy.org/how-khan-academy-is-building-a-better-ai-tutor-our-most-recent-learnings/',
  ], caveat: 'GitHub’s study randomly assigned 95 professional developers to a JavaScript HTTP-server task; it is GitHub-affiliated and does not establish learning or novice outcomes. Khan Academy’s May 2026 report summarizes product tests from Oct 2025–Apr 2026 across more than 15 million tutoring threads. It reports +3.4% from structured recent problem history, +2.7% from prerequisite review, +6.1% combined, and +5.09% cognitive engagement from relevant prior-24-hour context. It is company-reported, math-focused, and not a Bataa experiment.' }));
}

// 9. Evidence matrix
{
  const s = deck.slides.add(); bg(s, C.cream); header(s, 9, 'Evidence matrix');
  title(s, 'What the evidence supports, and what it leaves open', 'A credible thesis is not the same thing as product–market fit.', false);
  const x = [68, 430, 590, 888];
  const widths = [340, 140, 278, 312];
  ['Question', 'Status', 'Evidence says', 'Still unproven'].forEach((h, i) => {
    text(s, h.toUpperCase(), { left: x[i], top: 220, width: widths[i], height: 20 }, { fontSize: 11, bold: true, color: C.brown });
  });
  line(s, 68, 250, 1200, 250, C.line, 2);
  const rows = [
    ['Is there a real need for on-demand support?', 'SUPPORTED', 'Online resources dominate coding learning; Egyptian students wanted more interaction.', 'How often Bataa’s target learners feel it.'],
    ['Does practice and feedback improve learning?', 'SUPPORTED', '225-study active-learning meta-analysis; 435-study feedback meta-analysis.', 'Which Bataa feedback designs transfer to coding.'],
    ['Can contextual AI reduce friction?', 'PROMISING', 'Copilot and Khanmigo experiments show adjacent performance gains.', 'Novice coding, trust, safety, and long-term learning.'],
    ['Do Bataa learners return and finish?', 'UNKNOWN', 'No Bataa behavioral cohort yet.', 'Activation, D7 retention, completion, transfer.'],
    ['Will users or partners pay?', 'UNKNOWN', 'No willingness-to-pay or paid pilot evidence yet.', 'Price, conversion, institution/creator demand.'],
  ];
  rows.forEach(([q, status, ev, gap], i) => {
    const y = 270 + i * 70;
    if (i % 2 === 0) shape(s, 'rect', { left: 68, top: y - 8, width: 1132, height: 60 }, '#FFF0DE', { fill: 'none', width: 0 });
    text(s, q, { left: 68, top: y, width: 340, height: 42 }, { fontSize: 16, bold: true, color: C.ink });
    const statusColor = status === 'SUPPORTED' ? C.green : status === 'PROMISING' ? C.violet : C.red;
    const statusFill = status === 'SUPPORTED' ? C.greenSoft : status === 'PROMISING' ? C.violetSoft : C.redSoft;
    pill(s, status, { left: 430, top: y + 2, width: status === 'PROMISING' ? 116 : 102, height: 24 }, statusFill, statusColor, { fontSize: 10 });
    text(s, ev, { left: 590, top: y, width: 278, height: 43 }, { fontSize: 14, color: C.brown });
    text(s, gap, { left: 888, top: y, width: 312, height: 43 }, { fontSize: 14, color: C.ink });
    if (i < rows.length - 1) line(s, 68, y + 53, 1200, y + 53, C.line, 1);
  });
  footer(s, 'Synthesis · source-level caveats are preserved in each slide’s notes', false);
  note(s, sourceNote({ urls: [
    'https://survey.stackoverflow.co/2024/',
    'https://pmc.ncbi.nlm.nih.gov/articles/PMC8966850/',
    'https://pmc.ncbi.nlm.nih.gov/articles/PMC4060654/',
    'https://pmc.ncbi.nlm.nih.gov/articles/PMC6987456/',
    'https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-on-developer-productivity-and-happiness/',
    'https://blog.khanacademy.org/how-khan-academy-is-building-a-better-ai-tutor-our-most-recent-learnings/',
  ], caveat: 'Status labels are an evidence synthesis, not a statistical score. “Supported” means multiple external sources converge on the mechanism. “Promising” means adjacent evidence with meaningful transfer caveats. “Unknown” means Bataa has not yet collected the decisive behavioral or commercial data.' }));
}

// 10. Next validation
{
  const s = deck.slides.add(); bg(s, C.orange); header(s, 10, 'Next validation', true);
  title(s, 'The next proof should be behavioral', 'Turn the thesis into a small, measured pilot before scaling the story.', true);
  card(s, { left: 68, top: 236, width: 590, height: 366 }, '#F78A17', '#FFB557', 'rounded-3xl', 'shadow-md');
  pill(s, 'PILOT SHAPE', { left: 102, top: 270, width: 112, height: 27 }, C.cream, C.orangeDark);
  const phases = [
    ['01', '15–20 discovery interviews', 'Record consented sessions, recruit across beginner skill levels, code recurring moments.'],
    ['02', '20–30 learner pilot', 'Run one beginner path for 14 days with simple daily tasks.'],
    ['03', 'Comparison condition', 'Compare contextual feedback against the current lesson flow or a baseline.'],
  ];
  phases.forEach(([n, h, b], i) => {
    const y = 322 + i * 86;
    circle(s, 102, y, 34, C.cream, n, C.orangeDark, 11);
    text(s, h, { left: 154, top: y + 1, width: 310, height: 22 }, { fontSize: 19, bold: true, color: C.ink });
    text(s, b, { left: 154, top: y + 28, width: 430, height: 39 }, { fontSize: 15, color: C.ink });
  });
  card(s, { left: 704, top: 236, width: 496, height: 366 }, C.cream, C.cream, 'rounded-3xl', 'shadow-md');
  pill(s, 'MEASURE BEFORE SCALE', { left: 740, top: 270, width: 170, height: 27 }, C.ink, C.cream);
  const measures = [
    ['Activation', 'first task started'],
    ['Task success', 'time-to-first-success'],
    ['Feedback loop', 'retry after a hint'],
    ['Retention', 'D1 and D7 return'],
    ['Transfer', 'delayed task without help'],
    ['Commercial', 'willingness to pay / partner ask'],
  ];
  measures.forEach(([h, b], i) => {
    const y = 322 + i * 40;
    circle(s, 742, y + 1, 21, i < 3 ? C.orange : i < 5 ? C.violet : C.green, '', C.white, 10);
    text(s, h, { left: 780, top: y, width: 172, height: 20 }, { fontSize: 16, bold: true, color: C.ink });
    text(s, b, { left: 958, top: y + 1, width: 190, height: 20 }, { fontSize: 14, color: C.brown });
  });
  card(s, { left: 68, top: 622, width: 1132, height: 34 }, C.cream, C.cream, 'rounded-xl', 'shadow-sm');
  text(s, 'Predefine pass / fail thresholds before the pilot starts.', { left: 98, top: 630, width: 930, height: 18 }, { fontSize: 16, bold: true, color: C.ink });
  footer(s, 'Proposed validation plan · no pilot results claimed yet', true);
  note(s, sourceNote({ urls: [
    'https://doi.org/10.1016/j.compedu.2016.03.016',
    'https://doi.org/10.19173/irrodl.v16i3.2112',
  ], caveat: 'This slide is a proposed measurement plan, not reported evidence. The suggested sample sizes are practical pilot targets, not statistical power claims. A Cairo MOOC retention study (Hone & El Said, 2016) and MOOC completion research motivate measuring early engagement and support, but neither predicts Bataa performance.' }));
}

// 11. Bottom line
{
  const s = deck.slides.add(); bg(s, C.dark); header(s, 11, 'Bottom line', true);
  text(s, 'We can defend the problem\nand the product thesis.', { left: 68, top: 124, width: 760, height: 118 }, { fontSize: 52, bold: true, color: C.cream });
  text(s, 'We cannot yet claim product–market fit.', { left: 72, top: 275, width: 720, height: 48 }, { fontSize: 30, bold: true, color: C.orangeSoft });
  card(s, { left: 68, top: 382, width: 350, height: 164 }, C.dark2, '#5D3B27', 'rounded-2xl', 'shadow-md');
  pill(s, 'REAL PROBLEM?', { left: 100, top: 414, width: 120, height: 26 }, C.green, C.white);
  text(s, 'Credible', { left: 100, top: 460, width: 250, height: 34 }, { fontSize: 29, bold: true, color: C.cream });
  text(s, 'External research and local context converge.', { left: 100, top: 502, width: 270, height: 26 }, { fontSize: 15, color: '#D8BBA4' });
  card(s, { left: 464, top: 382, width: 350, height: 164 }, C.dark2, '#5D3B27', 'rounded-2xl', 'shadow-md');
  pill(s, 'BATAA FIT?', { left: 496, top: 414, width: 100, height: 26 }, C.red, C.white);
  text(s, 'Unproven', { left: 496, top: 460, width: 250, height: 34 }, { fontSize: 29, bold: true, color: C.cream });
  text(s, 'No measured cohort or payment signal yet.', { left: 496, top: 502, width: 270, height: 26 }, { fontSize: 15, color: '#D8BBA4' });
  card(s, { left: 860, top: 382, width: 340, height: 164 }, C.orange, C.orange, 'rounded-2xl', 'shadow-md');
  pill(s, 'NEXT DECISION', { left: 892, top: 414, width: 126, height: 26 }, C.ink, C.cream);
  text(s, 'Run the pilot', { left: 892, top: 460, width: 260, height: 34 }, { fontSize: 29, bold: true, color: C.ink });
  text(s, 'Measure behavior before scaling claims.', { left: 892, top: 502, width: 255, height: 26 }, { fontSize: 15, color: C.ink });
  footer(s, 'Recommended public wording · evidence appendix', true);
  note(s, sourceNote({ urls: [
    'https://survey.stackoverflow.co/2024/',
    'https://pmc.ncbi.nlm.nih.gov/articles/PMC8966850/',
    'https://pmc.ncbi.nlm.nih.gov/articles/PMC4060654/',
    'https://pmc.ncbi.nlm.nih.gov/articles/PMC6987456/',
    'https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-on-developer-productivity-and-happiness/',
    'https://blog.khanacademy.org/how-khan-academy-is-building-a-better-ai-tutor-our-most-recent-learnings/',
  ], caveat: 'This is the defensible conclusion from the evidence assembled. It intentionally avoids claiming a large Horus sample, retention, learning gains, or revenue.' }));
}

// 12. Sources and limitations
{
  const s = deck.slides.add(); bg(s, C.cream); header(s, 12, 'Sources and limitations');
  title(s, 'Sources used in this appendix', 'Primary links are preserved in speaker notes for each slide.', false);
  card(s, { left: 68, top: 214, width: 560, height: 390 }, C.paper, C.line, 'rounded-3xl', 'shadow-md');
  card(s, { left: 652, top: 214, width: 548, height: 390 }, C.paper, C.line, 'rounded-3xl', 'shadow-md');
  text(s, 'Peer-reviewed / public research', { left: 102, top: 248, width: 420, height: 26 }, { fontSize: 21, bold: true, color: C.ink });
  const left = [
    'Freeman et al. (2014), PNAS · active learning meta-analysis',
    'Deslauriers et al. (2019), PNAS · actual vs perceived learning',
    'Wisniewski et al. (2020), Frontiers · feedback meta-analysis',
    'Mortagy et al. (2022), BMC Medical Education · Egypt survey',
    'Gillett-Swan (2017), Journal of Learning Design · online isolation',
  ];
  left.forEach((v, i) => {
    const y = 298 + i * 50;
    circle(s, 104, y + 1, 22, i === 3 ? C.orange : C.violet, String(i + 1), C.white, 10);
    text(s, v, { left: 142, top: y, width: 430, height: 36 }, { fontSize: 14, color: C.brown });
  });
  text(s, 'Official / company research', { left: 686, top: 248, width: 420, height: 26 }, { fontSize: 21, bold: true, color: C.ink });
  const right = [
    'Stack Overflow Developer Survey (2024)',
    'GitHub Copilot controlled experiment',
    'Khan Academy Khanmigo product tests (May 2026)',
    'Mimo, freeCodeCamp, and Codecademy were reviewed as market signals, not used as core proof',
    'Internal Bataa discovery account · founder-reported',
  ];
  right.forEach((v, i) => {
    const y = 298 + i * 50;
    circle(s, 688, y + 1, 22, i === 4 ? C.orange : C.green, String(i + 1), C.white, 10);
    text(s, v, { left: 726, top: y, width: 420, height: 36 }, { fontSize: 14, color: C.brown });
  });
  card(s, { left: 68, top: 622, width: 1132, height: 28 }, C.dark, C.dark, 'rounded-xl', 'shadow-sm');
  text(s, 'Limitations: selection bias · self-report · generalizability · vendor affiliation · no Bataa behavioral cohort', { left: 90, top: 628, width: 1080, height: 16 }, { fontSize: 11.5, bold: true, color: C.cream });
  footer(s, 'Accessed 19 September 2026 · full URLs and methodological caveats in notes', false);
  note(s, sourceNote({ urls: [
    'https://pmc.ncbi.nlm.nih.gov/articles/PMC4060654/',
    'https://pmc.ncbi.nlm.nih.gov/articles/PMC6765278/',
    'https://pmc.ncbi.nlm.nih.gov/articles/PMC6987456/',
    'https://pmc.ncbi.nlm.nih.gov/articles/PMC8966850/',
    'https://www.jld.edu.au/article/view/293',
    'https://survey.stackoverflow.co/2024/',
    'https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-on-developer-productivity-and-happiness/',
    'https://blog.khanacademy.org/how-khan-academy-is-building-a-better-ai-tutor-our-most-recent-learnings/',
    'https://mimo.org/',
    'https://www.freecodecamp.org/news/about/',
    'https://www.codecademy.com/about',
  ], caveat: 'The appendix distinguishes internal evidence, external behavior, learning-science evidence, and adjacent product experiments. The deck does not treat vendor-reported learner counts as independent validation and does not claim a verified size for the Horus discovery sample.' }));
}

const candidatePath = path.join(tmpDir, 'bataa-evidence-validation-candidate.pptx');
await (await PresentationFile.exportPptx(deck)).save(candidatePath);
const result = await finalizePresentation({
  workspaceDir,
  candidatePath,
  finalPath,
  pythonExecutable: process.env.RUNTIME_PYTHON,
  integrityValidatorPath: path.join(skillDir, 'container_tools/inspect_presentation_package_integrity.py'),
  layoutValidatorPath: path.join(skillDir, 'container_tools/inspect_presentation_layout_geometry.py'),
  layoutArgs: ['--expected-slide-size-emu', '12192000,6858000', '--validate-bullet-geometry', '--validate-heading-fit'],
  requiredNativeTableOwnerSlides: [],
  fontPolicy: { basis: 'design', families: [FONT] },
  verifyArtifactToolImport: true,
  receiptPath: path.join(tmpDir, `${path.basename(finalPath)}.validation.json`),
});
console.log(JSON.stringify({ finalPath, candidatePath, result }, null, 2));
