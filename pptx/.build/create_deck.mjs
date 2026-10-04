import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

const here = path.dirname(fileURLToPath(import.meta.url));
const workspaceDir = path.resolve(here, '..');
const projectDir = path.resolve(workspaceDir, '..');
const skillDir = process.env.SKILL_DIR;
const tmpDir = process.env.TMP_DIR ?? here;
const finalPath = process.env.FINAL_PPTX ?? path.join(workspaceDir, 'output', 'bataa-pitch-deck.pptx');

if (!skillDir || !path.isAbsolute(skillDir)) throw new Error('SKILL_DIR must be absolute');
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
  cream2: '#FBEAD4',
  paper: '#FFFDF8',
  ink: '#2D180B',
  brown: '#895F3C',
  brown2: '#6F4525',
  orange: '#FF8500',
  orangeDark: '#C45300',
  orangeSoft: '#FFD5A3',
  line: '#EDCFAD',
  green: '#2E9B62',
  greenSoft: '#DFF2E5',
  dark: '#1B100B',
  dark2: '#2B1910',
  violet: '#6E5BAA',
  white: '#FFFFFF',
  muted: '#7D5C42',
};

const ASSET = (name) => path.join(here, name);
const PROJECT_ASSET = (name) => path.join(projectDir, name);

const assetCache = new Map();
async function bytes(filePath) {
  if (!assetCache.has(filePath)) assetCache.set(filePath, new Uint8Array(await fs.readFile(filePath)));
  return assetCache.get(filePath);
}

const images = {
  hero: ASSET('assets-hero.png'),
  notsure: ASSET('assets-notsure.png'),
  aiCoding: ASSET('assets-ai-coding.png'),
  guided: ASSET('assets-guided.png'),
  aiMobile: ASSET('assets-ai-mobile.png'),
  duck: ASSET('assets-duck.png'),
  appLogo: ASSET('assets-applogo.png'),
  onboarding: path.join(workspaceDir, '.build/screens/onboarding-1.png'),
  home: path.join(workspaceDir, '.build/screens/lesson-1.png'),
  lesson: path.join(workspaceDir, '.build/screens/lesson-step-1.png'),
  lessonCorrect: path.join(workspaceDir, '.build/screens/lesson-step-1-correct.png'),
  onboardingTime: path.join(workspaceDir, '.build/screens/onboarding-4.png'),
  tiktok: ASSET('social-icons/tiktok.png'),
  instagram: ASSET('social-icons/instagram.png'),
  facebook: ASSET('social-icons/facebook.png'),
  linkedin: ASSET('social-icons/linkedin.png'),
};

const imageType = (filePath) => filePath.endsWith('.jpg') || filePath.endsWith('.jpeg') ? 'image/jpeg' : 'image/png';

function addShape(slide, geometry, position, fill = 'none', line = { fill: 'none', width: 0 }, extra = {}) {
  return slide.shapes.add({ geometry, position, fill, line, ...extra });
}

function addText(slide, text, position, style = {}, fill = 'none', line = { fill: 'none', width: 0 }) {
  const shape = addShape(slide, 'textbox', position, fill, line);
  shape.text = text;
  shape.text.style = {
    typeface: FONT,
    fontSize: 24,
    color: C.ink,
    autoFit: 'shrinkText',
    wrap: 'square',
    verticalAlignment: 'top',
    insets: { top: 0, right: 0, bottom: 0, left: 0 },
    ...style,
  };
  return shape;
}

function addRichText(slide, paragraphs, position, style = {}, fill = 'none', line = { fill: 'none', width: 0 }) {
  const shape = addShape(slide, 'textbox', position, fill, line);
  shape.text = paragraphs;
  shape.text.style = {
    typeface: FONT,
    fontSize: 24,
    color: C.ink,
    autoFit: 'shrinkText',
    wrap: 'square',
    verticalAlignment: 'top',
    insets: { top: 0, right: 0, bottom: 0, left: 0 },
    ...style,
  };
  return shape;
}

async function addImage(slide, filePath, position, options = {}) {
  return slide.images.add({
    blob: await bytes(filePath),
    contentType: imageType(filePath),
    alt: options.alt ?? path.basename(filePath),
    fit: options.fit ?? 'contain',
    position,
    ...(options.geometry ? { geometry: options.geometry } : {}),
    ...(options.borderRadius ? { borderRadius: options.borderRadius } : {}),
    ...(options.crop ? { crop: options.crop } : {}),
  });
}

function setBg(slide, color) {
  slide.background.fill = color;
}

function topMark(slide, number, section, dark = false) {
  const fg = dark ? C.cream : C.ink;
  const muted = dark ? '#D7BDA9' : C.brown;
  addText(slide, 'bataa', { left: 64, top: 28, width: 130, height: 32 }, { fontSize: 23, bold: true, color: C.orange });
  addText(slide, section.toUpperCase(), { left: 222, top: 33, width: 420, height: 22 }, { fontSize: 12, bold: true, color: muted });
  addText(slide, String(number).padStart(2, '0'), { left: 1180, top: 31, width: 36, height: 24 }, { fontSize: 14, bold: true, color: fg, alignment: 'right' });
  addShape(slide, 'line', { left: 64, top: 69, width: 1152, height: 0 }, 'none', { style: 'solid', fill: dark ? '#5D3B27' : C.line, width: 1 });
}

function footer(slide, text, dark = false) {
  addText(slide, text, { left: 64, top: 682, width: 920, height: 18 }, { fontSize: 11, color: dark ? '#C9A98C' : C.muted });
}

function title(slide, text, subtitle = '', dark = false, y = 104) {
  addText(slide, text, { left: 64, top: y, width: 900, height: 82 }, { fontSize: 50, bold: true, color: dark ? C.cream : C.ink });
  if (subtitle) addText(slide, subtitle, { left: 68, top: y + 92, width: 730, height: 52 }, { fontSize: 22, color: dark ? '#E3CDBB' : C.brown });
}

function pill(slide, text, position, fill = C.orangeSoft, color = C.orangeDark, width = null) {
  const p = { ...position, width: width ?? position.width };
  const s = addShape(slide, 'roundRect', p, fill, { style: 'solid', fill: fill, width: 0 }, { borderRadius: 'rounded-full' });
  s.text = text;
  s.text.style = { typeface: FONT, fontSize: 13, bold: true, color, alignment: 'center', verticalAlignment: 'middle', autoFit: 'shrinkText', insets: { top: 0, right: 10, bottom: 0, left: 10 } };
  return s;
}

function card(slide, position, fill = C.paper, lineColor = C.line, radius = 'rounded-2xl', shadow = 'shadow-sm') {
  return addShape(slide, 'roundRect', position, fill, { style: 'solid', fill: lineColor, width: 1 }, { borderRadius: radius, shadow });
}

function note(slide, text) {
  slide.speakerNotes.textFrame.setText(text);
}

function circle(slide, x, y, size, fill, textValue, textColor = C.ink, fontSize = 20) {
  const s = addShape(slide, 'ellipse', { left: x, top: y, width: size, height: size }, fill, { fill: fill, width: 0 });
  if (textValue) {
    s.text = textValue;
    s.text.style = { typeface: FONT, fontSize, bold: true, color: textColor, alignment: 'center', verticalAlignment: 'middle', autoFit: 'shrinkText', insets: { top: 0, right: 0, bottom: 0, left: 0 } };
  }
  return s;
}

function line(slide, x1, y1, x2, y2, color = C.orange, width = 3) {
  return addShape(slide, 'line', {
    left: Math.min(x1, x2),
    top: Math.min(y1, y2),
    width: Math.abs(x2 - x1),
    height: Math.abs(y2 - y1),
  }, 'none', { style: 'solid', fill: color, width });
}

const deck = Presentation.create({ slideSize: { width: W, height: H } });

// 1. Cover
{
  const s = deck.slides.add(); setBg(s, C.cream);
  addText(s, 'bataa', { left: 64, top: 38, width: 200, height: 44 }, { fontSize: 31, bold: true, color: C.orange });
  pill(s, 'PRODUCT STORY', { left: 64, top: 120, width: 150, height: 32 }, C.orangeSoft, C.orangeDark);
  addText(s, 'Learn by doing.', { left: 64, top: 182, width: 640, height: 90 }, { fontSize: 66, bold: true, color: C.ink });
  addText(s, 'A learning companion that gives people one doable next step, wherever they are.', { left: 70, top: 292, width: 520, height: 86 }, { fontSize: 25, color: C.brown });
  addText(s, 'Mobile practice  ·  Desktop guidance  ·  AI when the question appears', { left: 70, top: 410, width: 590, height: 28 }, { fontSize: 15, bold: true, color: C.orangeDark });
  await addImage(s, images.hero, { left: 650, top: 98, width: 560, height: 492 }, { alt: 'Bataa duck between a mobile learning path and desktop workspace', fit: 'contain' });
  addText(s, 'Pitch deck  |  September 2026', { left: 64, top: 670, width: 300, height: 20 }, { fontSize: 12, color: C.muted });
  note(s, 'Opening: People do not fail because content is unavailable. They stall at the moment they need to act. Bataa keeps the next action close. Visual source: public/hero.webp from the Bataa project.');
}

// 2. Problem
{
  const s = deck.slides.add(); setBg(s, C.dark);
  topMark(s, 2, 'The gap', true);
  title(s, 'Learning support disappears when the learner is ready to act', 'The hardest moment often comes after the video ends.', true);
  addText(s, '“I know what I want to learn. I just do not know what to click next.”', { left: 68, top: 280, width: 600, height: 96 }, { fontSize: 35, bold: true, color: C.orangeSoft });
  addText(s, 'The learner is alone when the question appears: late at night, between classes, or inside unfamiliar software.', { left: 70, top: 400, width: 550, height: 72 }, { fontSize: 21, color: '#E5CFBD' });
  card(s, { left: 755, top: 160, width: 400, height: 390 }, C.dark2, '#5D3B27', 'rounded-3xl', 'shadow-md');
  await addImage(s, images.notsure, { left: 785, top: 190, width: 340, height: 280 }, { alt: 'Bataa mascot thinking about what to do next', fit: 'contain' });
  pill(s, 'THE STALL', { left: 820, top: 500, width: 118, height: 30 }, C.orange, C.white);
  addText(s, 'Content is available. Context is missing.', { left: 820, top: 545, width: 275, height: 42 }, { fontSize: 20, bold: true, color: C.cream, alignment: 'center' });
  footer(s, 'Problem framing · user-provided brief', true);
  note(s, 'Framing based on the user-provided problem statement. The quoted sentence is a synthesized articulation, not a verbatim interview quote.');
}

// 3. Campus signal
{
  const s = deck.slides.add(); setBg(s, C.cream);
  topMark(s, 3, 'Discovery');
  addText(s, 'We heard the same friction in three moments', { left: 64, top: 106, width: 1110, height: 60 }, { fontSize: 45, bold: true, color: C.ink });
  addText(s, 'Qualitative discovery at Horus University. Synthesized from conversations, not verbatim quotes.', { left: 68, top: 178, width: 950, height: 30 }, { fontSize: 18, color: C.brown });

  // A concrete, clearly labelled signal gives the research a human centre.
  card(s, { left: 68, top: 255, width: 425, height: 300 }, C.dark2, '#5D3B27', 'rounded-3xl', 'shadow-md');
  pill(s, 'OBSERVED', { left: 100, top: 286, width: 102, height: 28 }, C.orange, C.white);
  addText(s, 'HORUS UNIVERSITY', { left: 220, top: 291, width: 220, height: 18 }, { fontSize: 11, bold: true, color: C.orangeSoft });
  addText(s, '“I can’t ask an instructor at 2 a.m.”', { left: 100, top: 345, width: 345, height: 100 }, { fontSize: 32, bold: true, color: C.cream });
  addText(s, 'PARAPHRASED STUDENT SIGNAL', { left: 100, top: 480, width: 260, height: 18 }, { fontSize: 11, bold: true, color: C.orangeSoft });
  addText(s, 'The question arrives after the lesson.', { left: 100, top: 510, width: 300, height: 24 }, { fontSize: 16, color: '#E3CDBB' });

  addText(s, 'Three moments, one pattern', { left: 560, top: 263, width: 560, height: 32 }, { fontSize: 25, bold: true, color: C.ink });
  const signals = [
    ['02:00 AM', 'Support stops when the question starts.', C.orange],
    ['TOO BASIC TO ASK', 'Anxiety turns a small blocker into a stall.', C.violet],
    ['TOO EXPENSIVE / TOO CROWDED', 'Existing options miss the moment of practice.', C.green],
  ];
  signals.forEach(([label, body, color], i) => {
    const y = 320 + i * 84;
    circle(s, 560, y, 42, color, String(i + 1), C.white, 16);
    addText(s, label, { left: 625, top: y + 1, width: 500, height: 18 }, { fontSize: 12, bold: true, color });
    addText(s, body, { left: 625, top: y + 26, width: 540, height: 30 }, { fontSize: 19, color: C.ink });
    if (i < signals.length - 1) line(s, 625, y + 70, 1175, y + 70, C.line, 2);
  });

  card(s, { left: 68, top: 600, width: 1112, height: 50 }, C.orange, C.orange, 'rounded-2xl', 'shadow-sm');
  addText(s, 'PRODUCT IMPLICATION', { left: 96, top: 616, width: 170, height: 18 }, { fontSize: 11, bold: true, color: C.ink });
  addText(s, 'Make the next step available, private, and easy to try.', { left: 295, top: 612, width: 830, height: 28 }, { fontSize: 20, bold: true, color: C.ink });
  footer(s, 'Evidence status: observed. Horus University conversations.', false);
  note(s, 'Evidence label: OBSERVED. Source: user-provided description of early qualitative conversations at Horus University. The large sentence is a paraphrased student signal, not a verbatim quote. Do not add a participant count until the team verifies it. The three moments are synthesized themes: instructor availability, anxiety about asking basic questions, and price or crowding in existing course options.');
}

// 4. Insight
{
  const s = deck.slides.add(); setBg(s, C.orange);
  topMark(s, 4, 'Insight', true);
  title(s, 'The missing layer is contextual guidance', 'Bataa helps at the exact moment the learner has to make a move.', true);
  card(s, { left: 72, top: 300, width: 410, height: 220 }, '#F78A17', '#FFB557', 'rounded-2xl', 'shadow-sm');
  pill(s, 'CONTENT ONLY', { left: 105, top: 335, width: 130, height: 30 }, C.cream, C.orangeDark);
  addText(s, 'Watch → pause → search → stall', { left: 105, top: 390, width: 330, height: 55 }, { fontSize: 31, bold: true, color: C.ink });
  addText(s, 'The learner has to translate theory into the next action alone.', { left: 105, top: 466, width: 315, height: 38 }, { fontSize: 16, color: C.ink });
  line(s, 520, 410, 700, 410, C.cream, 6); circle(s, 595, 385, 50, C.cream, '→', C.orangeDark, 28);
  card(s, { left: 738, top: 300, width: 470, height: 220 }, C.cream, C.cream, 'rounded-2xl', 'shadow-md');
  pill(s, 'BATAA', { left: 772, top: 335, width: 90, height: 30 }, C.ink, C.cream);
  addText(s, 'Try → get feedback → keep moving', { left: 772, top: 390, width: 390, height: 55 }, { fontSize: 31, bold: true, color: C.ink });
  addText(s, 'The next step appears beside the work, in plain English.', { left: 772, top: 466, width: 350, height: 38 }, { fontSize: 16, color: C.brown });
  footer(s, 'Product insight · contextual help at the moment of action', true);
  note(s, 'Narrative bridge: Bataa is not another content library. It is the guidance layer between intention and action.');
}

// 5. Product ecosystem
{
  const s = deck.slides.add(); setBg(s, C.cream);
  topMark(s, 5, 'Product');
  title(s, 'One product, two moments', 'The same learning loop follows the learner from a spare minute to the tool where the work happens.');
  card(s, { left: 74, top: 265, width: 470, height: 315 }, C.paper, C.line, 'rounded-3xl', 'shadow-md');
  await addImage(s, images.home, { left: 95, top: 285, width: 180, height: 275 }, { alt: 'Bataa mobile home screen with daily task', fit: 'contain' });
  addText(s, 'MOBILE', { left: 302, top: 322, width: 170, height: 22 }, { fontSize: 13, bold: true, color: C.orangeDark });
  addText(s, 'Keep momentum anywhere', { left: 302, top: 362, width: 200, height: 55 }, { fontSize: 29, bold: true, color: C.ink });
  addText(s, 'Short daily tasks make progress possible in transit, between classes, or at home.', { left: 302, top: 442, width: 190, height: 72 }, { fontSize: 17, color: C.brown });
  card(s, { left: 738, top: 265, width: 470, height: 315 }, C.dark, '#4F3323', 'rounded-3xl', 'shadow-md');
  await addImage(s, images.guided, { left: 760, top: 296, width: 426, height: 190 }, { alt: 'Bataa AI tutor inside a desktop coding workspace', fit: 'cover', geometry: 'roundRect', borderRadius: 'rounded-xl' });
  addText(s, 'DESKTOP', { left: 766, top: 512, width: 170, height: 22 }, { fontSize: 13, bold: true, color: C.orangeSoft });
  addText(s, 'Guide inside the tool', { left: 766, top: 540, width: 320, height: 34 }, { fontSize: 27, bold: true, color: C.cream });
  footer(s, 'Demonstrated surfaces · mobile and desktop product visuals', false);
  note(s, 'Visual sources: Bataa mobile capture from the running app (lesson-1.png) and public/guided-project-ai.webp. The desktop agent interaction should be demonstrated live or with a short clip when available.');
}

// 6. Mobile experience
{
  const s = deck.slides.add(); setBg(s, C.dark2);
  topMark(s, 6, 'Mobile practice', true);
  title(s, 'Mobile turns spare minutes into practice', 'A daily task can fit into the time a learner already has.', true);
  card(s, { left: 74, top: 252, width: 240, height: 380 }, C.dark, '#5D3B27', 'rounded-3xl', 'shadow-md');
  await addImage(s, images.onboardingTime, { left: 88, top: 267, width: 212, height: 352 }, { alt: 'Bataa onboarding time choice screen', fit: 'contain' });
  card(s, { left: 340, top: 252, width: 240, height: 380 }, C.dark, '#5D3B27', 'rounded-3xl', 'shadow-md');
  await addImage(s, images.lessonCorrect, { left: 354, top: 267, width: 212, height: 352 }, { alt: 'Bataa lesson with a selected answer', fit: 'contain' });
  const points = [
    ['8–10 min', 'A small session with a clear finish line'],
    ['No typing needed', 'The first days use three-choice recognition'],
    ['One real skill', 'Every step maps to a usable web concept'],
  ];
  points.forEach(([a, b], i) => {
    const y = 300 + i * 102;
    circle(s, 680, y, 42, i === 1 ? C.orange : C.cream, String(i + 1), i === 1 ? C.cream : C.orangeDark, 18);
    addText(s, a, { left: 742, top: y - 3, width: 340, height: 30 }, { fontSize: 25, bold: true, color: C.cream });
    addText(s, b, { left: 742, top: y + 33, width: 370, height: 44 }, { fontSize: 17, color: '#D8BBA4' });
  });
  footer(s, 'Demonstrated · beginner-friendly lesson flow', true);
  note(s, 'Visual sources: running Bataa app captures from the project. The “no typing needed” design is demonstrated in the first lesson step, which offers three choices.');
}

// 7. Desktop
{
  const s = deck.slides.add(); setBg(s, C.ink);
  topMark(s, 7, 'Desktop guidance', true);
  title(s, 'Desktop guidance meets the learner where work happens', 'For 3D, code, and other tools, Bataa can point to the next action instead of describing it from a distance.', true);
  await addImage(s, images.aiCoding, { left: 68, top: 260, width: 690, height: 360 }, { alt: 'AI explanation panel inside a code editor', fit: 'cover', geometry: 'roundRect', borderRadius: 'rounded-2xl' });
  card(s, { left: 808, top: 270, width: 375, height: 328 }, C.dark2, '#5D3B27', 'rounded-2xl', 'shadow-md');
  const labels = [
    ['01', 'Notice', 'Understand what the learner is trying to do'],
    ['02', 'Point', 'Highlight the exact control or line to inspect'],
    ['03', 'Try', 'Let the learner perform the action and see the result'],
  ];
  labels.forEach(([n, h, b], i) => {
    const y = 306 + i * 87;
    circle(s, 838, y, 36, i === 1 ? C.orange : C.cream2, n, i === 1 ? C.cream : C.orangeDark, 13);
    addText(s, h, { left: 892, top: y - 2, width: 230, height: 24 }, { fontSize: 19, bold: true, color: C.cream });
    addText(s, b, { left: 892, top: y + 25, width: 245, height: 42 }, { fontSize: 14, color: '#D8BBA4' });
  });
  pill(s, 'DEMONSTRATED', { left: 68, top: 640, width: 150, height: 28 }, C.green, C.white);
  addText(s, 'Autonomous control and deeper integrations are pilot work, not a promise of the current build.', { left: 220, top: 644, width: 790, height: 20 }, { fontSize: 13, color: '#D8BBA4' });
  footer(s, 'Desktop product visual · guided-project-ai.webp and ai-assisted-coding.webp', true);
  note(s, 'Visual sources: public/ai-assisted-coding.webp and public/guided-project-ai.webp. Evidence status: DEMONSTRATED for the guidance concept. State clearly that autonomous cursor control and broad software coverage remain pilot scope unless already shipped.');
}

// 8. Example journey
{
  const s = deck.slides.add(); setBg(s, C.cream);
  topMark(s, 8, 'Skill journey');
  title(s, 'A skill compounds one small day at a time', 'Illustrative 3D-modeling journey: the learner starts with a gesture, then builds a real artifact.');
  line(s, 160, 364, 1110, 364, C.orange, 5);
  const days = [
    ['DAY 1', 'Find the tool', 'Recognize the viewport, select an object, make one change.'],
    ['DAY 7', 'Shape a scene', 'Combine small actions into a simple modeled composition.'],
    ['DAY 30', 'Finish an artifact', 'Use the same guided loop to complete a portfolio-ready piece.'],
  ];
  days.forEach(([d, h, b], i) => {
    const x = 160 + i * 475;
    circle(s, x - 22, 342, 44, i === 1 ? C.orange : C.cream, String(i + 1), i === 1 ? C.cream : C.orangeDark, 18);
    addText(s, d, { left: x - 48, top: 395, width: 150, height: 20 }, { fontSize: 13, bold: true, color: C.orangeDark, alignment: 'center' });
    addText(s, h, { left: x - 90, top: 430, width: 240, height: 34 }, { fontSize: 25, bold: true, color: C.ink, alignment: 'center' });
    addText(s, b, { left: x - 135, top: 477, width: 330, height: 64 }, { fontSize: 17, color: C.brown, alignment: 'center' });
  });
  card(s, { left: 447, top: 262, width: 386, height: 76 }, C.paper, C.line, 'rounded-2xl', 'shadow-sm');
  addText(s, 'The product promise is a path, not a single lesson.', { left: 474, top: 286, width: 330, height: 28 }, { fontSize: 20, bold: true, color: C.ink, alignment: 'center' });
  pill(s, 'ILLUSTRATIVE', { left: 64, top: 615, width: 114, height: 28 }, C.cream2, C.brown);
  addText(s, 'Replace with a real Bataa skill path and learner artifact before the final pitch.', { left: 194, top: 620, width: 690, height: 20 }, { fontSize: 13, color: C.muted });
  footer(s, 'Product narrative · example journey, not a measured outcome', false);
  note(s, 'This is an illustrative journey for explaining the product loop. Do not present the day-30 outcome as a measured result until a real course and pilot validate it.');
}

// 9. Beginner lesson
{
  const s = deck.slides.add(); setBg(s, C.cream2);
  topMark(s, 9, 'Beginner design');
  addText(s, 'The first three days should feel approachable', { left: 64, top: 104, width: 900, height: 62 }, { fontSize: 43, bold: true, color: C.ink });
  addText(s, 'Recognition first. Typed code comes after the learner understands what the code is doing.', { left: 68, top: 184, width: 730, height: 44 }, { fontSize: 21, color: C.brown });
  card(s, { left: 72, top: 240, width: 450, height: 390 }, C.paper, C.line, 'rounded-3xl', 'shadow-md');
  await addImage(s, images.lesson, { left: 90, top: 255, width: 414, height: 358 }, { alt: 'Bataa first lesson with three answer choices', fit: 'contain' });
  const steps = [
    ['DAY 1', 'Choose the right HTML element', C.orange],
    ['DAY 2', 'Match CSS properties to a visual result', C.violet],
    ['DAY 3', 'Predict what a hover state will do', C.green],
  ];
  steps.forEach(([d, h, color], i) => {
    const y = 278 + i * 102;
    pill(s, d, { left: 610, top: y, width: 78, height: 28 }, color, C.white);
    addText(s, h, { left: 720, top: y + 2, width: 420, height: 28 }, { fontSize: 22, bold: true, color: C.ink });
    line(s, 610, y + 55, 1115, y + 55, C.line, 2);
  });
  addText(s, 'The learner gets a win before they get a keyboard-heavy challenge.', { left: 610, top: 590, width: 525, height: 45 }, { fontSize: 20, color: C.brown });
  footer(s, 'Demonstrated · first lesson uses three-choice recognition', false);
  note(s, 'Visual source: running Bataa app capture lesson-step-1.png. This design directly addresses beginner anxiety and keyboard friction from the user brief.');
}

// 10. Learning loop
{
  const s = deck.slides.add(); setBg(s, C.orangeSoft);
  topMark(s, 10, 'Learning loop');
  title(s, 'Bataa closes the gap between attempt and understanding', 'Every attempt returns a useful next step.');
  pill(s, 'THE BATAA LOOP', { left: 68, top: 245, width: 142, height: 30 }, C.ink, C.cream);

  const steps = [
    ['01', 'ATTEMPT', 'Make one move', C.paper, C.orange],
    ['02', 'FEEDBACK', 'See what changed', C.paper, C.orange],
    ['03', 'UNDERSTAND', 'Name the why', C.orange, C.cream],
    ['04', 'NEXT ATTEMPT', 'Apply the idea again', C.paper, C.orange],
  ];
  const loopCards = [];
  steps.forEach(([number, label, body, fill, badgeFill], i) => {
    const x = 72 + i * 288;
    const loopCard = card(s, { left: x, top: 300, width: 220, height: 142 }, fill, fill === C.orange ? C.orange : C.line, 'rounded-2xl', 'shadow-sm');
    loopCards.push(loopCard);
    circle(s, x + 20, 320, 32, badgeFill, number, badgeFill === C.cream ? C.orangeDark : C.cream, 12);
    addText(s, label, { left: x + 66, top: 323, width: 142, height: 20 }, { fontSize: 14, bold: true, color: fill === C.orange ? C.cream : C.orangeDark });
    addText(s, body, { left: x + 20, top: 378, width: 180, height: 44 }, { fontSize: 21, bold: true, color: fill === C.orange ? C.cream : C.ink });
  });
  for (let i = 0; i < loopCards.length - 1; i++) {
    s.shapes.connect(loopCards[i], loopCards[i + 1], {
      kind: 'straight',
      fromSide: 'right',
      toSide: 'left',
      line: { style: 'solid', fill: C.orangeDark, width: 3 },
      tail: { type: 'arrow', width: 'sm', length: 'sm' },
    });
  }

  card(s, { left: 72, top: 520, width: 1136, height: 86 }, C.dark, C.dark, 'rounded-2xl', 'shadow-sm');
  addText(s, 'Attempt  →  feedback  →  understanding  →  next attempt', { left: 104, top: 542, width: 650, height: 24 }, { fontSize: 21, bold: true, color: C.cream });
  addText(s, 'The learner keeps the work. Bataa makes the next move legible.', { left: 104, top: 574, width: 900, height: 20 }, { fontSize: 15, color: '#D8BBA4' });
  footer(s, 'Editable diagram · product hypothesis to validate in pilot', false);
  note(s, 'Product hypothesis: Bataa reduces the gap between doing and knowing by making feedback actionable. Validate in pilot with retry-after-feedback, time-to-first-success, explanation recall, task completion, hint use, and return rate. The diagram is not a measured funnel.');
}

// 11. Competitive position
{
  const s = deck.slides.add(); setBg(s, C.dark);
  topMark(s, 11, 'Positioning', true);
  title(s, 'Bataa sits between content and the moment of action', 'A positioning hypothesis, not a claim that competitors lack AI.', true);
  addText(s, 'GUIDANCE IN CONTEXT', { left: 120, top: 245, width: 200, height: 22 }, { fontSize: 13, bold: true, color: C.orangeSoft, alignment: 'center' });
  addText(s, 'LOW', { left: 286, top: 600, width: 80, height: 18 }, { fontSize: 12, bold: true, color: '#C9A98C', alignment: 'center' });
  addText(s, 'HIGH', { left: 1010, top: 600, width: 80, height: 18 }, { fontSize: 12, bold: true, color: '#C9A98C', alignment: 'center' });
  line(s, 180, 565, 1100, 565, '#6B4730', 2); line(s, 180, 565, 180, 260, '#6B4730', 2);
  addText(s, 'DAILY PRACTICE', { left: 77, top: 355, width: 80, height: 130 }, { fontSize: 13, bold: true, color: C.orangeSoft, alignment: 'center' });
  const dots = [
    ['Khan Academy', 330, 490, C.cream2],
    ['iSchool', 435, 420, '#BBA9E4'],
    ['Yanfaa / Nafham', 550, 470, '#B9D8C5'],
    ['Bataa', 930, 315, C.orange],
  ];
  dots.forEach(([name, x, y, fill]) => { circle(s, x - 22, y - 22, 44, fill, '', C.ink); addText(s, name, { left: x - 78, top: y + 32, width: 156, height: 22 }, { fontSize: 14, bold: name === 'Bataa', color: name === 'Bataa' ? C.orangeSoft : C.cream, alignment: 'center' }); });
  card(s, { left: 780, top: 155, width: 350, height: 82 }, C.dark2, '#6B4730', 'rounded-2xl', 'shadow-sm');
  addText(s, 'Bataa combines daily practice with help inside the work.', { left: 810, top: 180, width: 290, height: 34 }, { fontSize: 18, bold: true, color: C.cream, alignment: 'center' });
  pill(s, 'VERIFY BEFORE PRESENTING', { left: 68, top: 635, width: 185, height: 28 }, C.orange, C.white);
  footer(s, 'Qualitative positioning hypothesis · verify competitor names and feature claims', true);
  note(s, 'This is a qualitative positioning hypothesis based on the user-provided competitor list. Verify the exact local platform names and current features before presenting. Do not claim that competitors do not use AI without research.');
}

// 12. Revenue model
{
  const s = deck.slides.add(); setBg(s, C.cream);
  topMark(s, 12, 'Business model');
  title(s, 'Start with one clear revenue engine', 'Paid learning first. Optional AI usage and platform licensing expand the model later.');
  card(s, { left: 74, top: 260, width: 520, height: 290 }, C.orange, C.orange, 'rounded-3xl', 'shadow-md');
  pill(s, 'LAUNCH PRIORITY', { left: 108, top: 300, width: 145, height: 30 }, C.cream, C.orangeDark);
  addText(s, 'Course purchase', { left: 108, top: 356, width: 360, height: 52 }, { fontSize: 40, bold: true, color: C.ink });
  addText(s, 'Learners pay for a structured path that turns practice into a finished skill.', { left: 110, top: 430, width: 390, height: 62 }, { fontSize: 20, color: C.ink });
  card(s, { left: 650, top: 260, width: 255, height: 290 }, C.paper, C.line, 'rounded-3xl', 'shadow-sm');
  pill(s, 'OPTIONAL', { left: 682, top: 300, width: 95, height: 28 }, C.cream2, C.brown);
  addText(s, 'AI tokens', { left: 682, top: 354, width: 180, height: 38 }, { fontSize: 28, bold: true, color: C.ink });
  addText(s, 'Extra attempts, deeper explanations, or advanced model usage.', { left: 682, top: 420, width: 175, height: 72 }, { fontSize: 17, color: C.brown });
  card(s, { left: 945, top: 260, width: 260, height: 290 }, C.paper, C.line, 'rounded-3xl', 'shadow-sm');
  pill(s, 'LATER', { left: 976, top: 300, width: 75, height: 28 }, C.greenSoft, C.green);
  addText(s, 'Platform fees', { left: 976, top: 354, width: 190, height: 38 }, { fontSize: 28, bold: true, color: C.ink });
  addText(s, 'Commission from creator and institution courses.', { left: 976, top: 420, width: 180, height: 72 }, { fontSize: 17, color: C.brown });
  addText(s, 'Keep the first story simple: one learner pays for one useful outcome.', { left: 74, top: 604, width: 760, height: 28 }, { fontSize: 22, bold: true, color: C.ink });
  footer(s, 'Business model · planned streams, launch priority shown', false);
  note(s, 'Business model is based on the user-provided brief. Course purchases are the launch priority; token packs and platform fees are expansion paths unless already implemented and tested commercially.');
}

// 13. Marketplace and API
{
  const s = deck.slides.add(); setBg(s, C.dark2);
  topMark(s, 13, 'Platform expansion', true);
  title(s, 'The same learning engine can serve creators and institutions', 'Bataa can become the infrastructure behind guided practice, not only a destination app.', true);
  const boxes = [
    ['CREATORS + INSTITUTIONS', 'Publish a course or training path', 86, 315, 300, 140, C.cream2, C.ink],
    ['BATAA ENGINE', 'Guided tasks, feedback, progress, AI context', 490, 285, 310, 200, C.orange, C.ink],
    ['LEARNERS', 'Buy, practice, and finish the skill', 900, 245, 280, 140, C.cream2, C.ink],
    ['IDE / PRODUCT API', 'Bring the tutor into another workflow', 900, 445, 280, 140, '#BBA9E4', C.ink],
  ];
  boxes.forEach(([k, b, x, y, w, h, fill, textColor]) => {
    card(s, { left: x, top: y, width: w, height: h }, fill, fill, 'rounded-2xl', 'shadow-md');
    addText(s, k, { left: x + 22, top: y + 25, width: w - 44, height: 23 }, { fontSize: 12, bold: true, color: textColor });
    addText(s, b, { left: x + 22, top: y + 62, width: w - 44, height: h - 78 }, { fontSize: 22, bold: true, color: textColor });
  });
  line(s, 386, 385, 490, 385, C.orangeSoft, 4); line(s, 800, 385, 900, 315, C.orangeSoft, 4); line(s, 800, 385, 900, 515, C.orangeSoft, 4);
  pill(s, 'PLANNED EXPANSION', { left: 68, top: 630, width: 165, height: 28 }, C.orange, C.white);
  addText(s, 'Commission on course sales plus API licensing for organizations and tools.', { left: 252, top: 634, width: 780, height: 20 }, { fontSize: 14, color: '#D8BBA4' });
  footer(s, 'Platform architecture · future revenue paths', true);
  note(s, 'This diagram reflects planned expansion from the user-provided business model: institution and creator courses with commission, plus an API/base URL offering. Label as planned until commercially validated.');
}

// 14. Validation and GTM
{
  const s = deck.slides.add(); setBg(s, C.cream);
  topMark(s, 14, 'Validation');
  title(s, 'The first wedge is close to the learner', 'Start with campus communities, prove the learning loop, then widen the platform.');
  const stages = [
    ['OBSERVED', 'Campus conversations', 'Students described the support gap.', C.green],
    ['DEMONSTRATED', 'Working surfaces', 'Mobile lesson flow and desktop guidance visuals exist.', C.violet],
    ['NEXT TEST', 'Pilot cohort', 'Measure task completion, return rate, and confidence.', C.orange],
    ['NEXT TEST', 'Partners', 'Recruit one creator and one training institution.', C.brown],
  ];
  stages.forEach(([tag, h, b, color], i) => {
    const x = 70 + i * 293;
    card(s, { left: x, top: 290, width: 255, height: 220 }, C.paper, C.line, 'rounded-2xl', 'shadow-sm');
    pill(s, tag, { left: x + 20, top: 315, width: tag === 'DEMONSTRATED' ? 125 : 100, height: 28 }, color, C.white);
    addText(s, h, { left: x + 20, top: 365, width: 210, height: 45 }, { fontSize: 23, bold: true, color: C.ink });
    addText(s, b, { left: x + 20, top: 430, width: 210, height: 50 }, { fontSize: 16, color: C.brown });
    if (i < stages.length - 1) line(s, x + 255, 400, x + 293, 400, C.orange, 3);
  });
  addText(s, 'The next proof point is not reach. It is whether a learner returns because the next step felt doable.', { left: 70, top: 570, width: 1060, height: 45 }, { fontSize: 24, bold: true, color: C.ink });
  footer(s, 'Go-to-market sequence · observed → demonstrated → next test', false);
  note(s, 'Evidence ladder: OBSERVED = campus conversations; DEMONSTRATED = existing product surfaces; NEXT TEST = pilot metrics and partner recruitment. Do not claim retention or conversion before measurement.');
}

// 15. Team
{
  const s = deck.slides.add(); setBg(s, C.dark);
  topMark(s, 15, 'Team', true);
  title(s, 'The team built the core surfaces', 'The product is split across the places where the learner meets Bataa.', true);
  const members = [
    ['Abdelrahman Mohsen', 'Desktop app', 'Builds the guided workspace where the AI can meet the learner inside real software.', C.orange],
    ['Yousef', 'Mobile app', 'Builds the daily lesson loop for small, approachable practice sessions.', C.violet],
    ['Mostafa', 'Landing page', 'Shapes the public story, visual identity, and first touchpoint for Bataa.', C.green],
  ];
  members.forEach(([name, role, body, color], i) => {
    const x = 70 + i * 390;
    card(s, { left: x, top: 285, width: 345, height: 260 }, C.dark2, '#5D3B27', 'rounded-2xl', 'shadow-md');
    circle(s, x + 26, 315, 50, color, String(i + 1), C.cream, 20);
    addText(s, name, { left: x + 94, top: 318, width: 220, height: 28 }, { fontSize: 21, bold: true, color: C.cream });
    addText(s, role.toUpperCase(), { left: x + 94, top: 355, width: 220, height: 20 }, { fontSize: 12, bold: true, color });
    addText(s, body, { left: x + 26, top: 420, width: 286, height: 82 }, { fontSize: 17, color: '#D8BBA4' });
  });
  pill(s, 'TEAM PROOF', { left: 70, top: 600, width: 125, height: 28 }, C.orange, C.white);
  addText(s, 'Each role maps to a working surface already visible in the product.', { left: 198, top: 604, width: 700, height: 20 }, { fontSize: 15, color: '#D8BBA4' });
  footer(s, 'Team roles · supplied in the Bataa brief', true);
  note(s, 'Team names and roles are taken from the user-provided brief. Add concrete proof points, links, or advisor details if available before presenting.');
}

// 16. Roadmap and ask
{
  const s = deck.slides.add(); setBg(s, C.orange);
  topMark(s, 16, 'Next milestone', true);
  addText(s, 'The next milestone is a real pilot.', { left: 64, top: 112, width: 760, height: 70 }, { fontSize: 56, bold: true, color: C.ink });
  addText(s, 'Prove that one doable action can become a habit and a finished skill.', { left: 68, top: 205, width: 640, height: 44 }, { fontSize: 23, color: C.ink });
  card(s, { left: 70, top: 320, width: 690, height: 235 }, '#F78A17', '#FFB557', 'rounded-3xl', 'shadow-md');
  const roadmap = [
    ['01', 'Beginner mobile path', 'Ship the first week of simple daily tasks'],
    ['02', 'Desktop agent pilot', 'Guide one real workflow with safe user control'],
    ['03', 'Partner pilots', 'Test a creator course and an institutional path'],
  ];
  roadmap.forEach(([n, h, b], i) => {
    const y = 348 + i * 66;
    circle(s, 100, y, 32, C.cream, n, C.orangeDark, 12);
    addText(s, h, { left: 150, top: y + 1, width: 240, height: 22 }, { fontSize: 19, bold: true, color: C.ink });
    addText(s, b, { left: 415, top: y + 2, width: 300, height: 24 }, { fontSize: 15, color: C.ink });
  });
  card(s, { left: 820, top: 320, width: 370, height: 235 }, C.cream, C.cream, 'rounded-3xl', 'shadow-md');
  pill(s, 'OUR ASK', { left: 855, top: 352, width: 90, height: 28 }, C.ink, C.cream);
  addText(s, 'Pilot partners', { left: 855, top: 405, width: 280, height: 40 }, { fontSize: 31, bold: true, color: C.ink });
  addText(s, 'One campus, one creator, and one training team willing to measure the loop with us.', { left: 855, top: 468, width: 275, height: 58 }, { fontSize: 18, color: C.brown });
  addText(s, 'Bataa gives every learner a next step.', { left: 70, top: 625, width: 800, height: 36 }, { fontSize: 28, bold: true, color: C.ink });
  footer(s, 'Close with a specific pilot ask · replace with contact details before presenting', true);
  note(s, 'Close: ask for pilot partners, not a generic “thank you.” Replace the ask and roadmap with dates, owners, and contact details when confirmed.');
}

// 17. Social and website
{
  const s = deck.slides.add(); setBg(s, C.dark);
  topMark(s, 17, 'Stay connected', true);

  pill(s, 'FOLLOW THE BUILD', { left: 68, top: 118, width: 152, height: 30 }, C.orange, C.white);
  addText(s, 'Keep building\nwith Bataa', { left: 68, top: 172, width: 610, height: 122 }, { fontSize: 54, bold: true, color: C.cream });
  addText(s, 'Follow product updates, new lessons, and the next Bataa launch.', { left: 70, top: 312, width: 555, height: 58 }, { fontSize: 21, color: '#E3CDBB' });

  card(s, { left: 68, top: 420, width: 590, height: 148 }, C.orange, C.orange, 'rounded-3xl', 'shadow-md');
  addText(s, 'START HERE', { left: 100, top: 450, width: 112, height: 20 }, { fontSize: 12, bold: true, color: C.ink });
  addText(s, 'bataa.app', { left: 100, top: 484, width: 420, height: 56 }, { fontSize: 43, bold: true, color: C.ink });
  circle(s, 570, 468, 52, C.cream, '→', C.orangeDark, 25);

  card(s, { left: 748, top: 118, width: 468, height: 450 }, C.dark2, '#5D3B27', 'rounded-3xl', 'shadow-md');
  addText(s, 'Follow us on social', { left: 788, top: 157, width: 360, height: 32 }, { fontSize: 25, bold: true, color: C.cream });
  addText(s, 'Find Bataa on every platform', { left: 788, top: 193, width: 300, height: 21 }, { fontSize: 14, color: '#C9A98C' });

  const socialRows = [
    ['TikTok', images.tiktok],
    ['Instagram', images.instagram],
    ['Facebook', images.facebook],
    ['LinkedIn', images.linkedin],
  ];

  for (let i = 0; i < socialRows.length; i++) {
    const [platform, iconPath] = socialRows[i];
    const y = 232 + i * 76;
    card(s, { left: 788, top: y, width: 388, height: 60 }, '#351F14', '#5D3B27', 'rounded-xl', 'shadow-sm');
    circle(s, 806, y + 10, 40, C.cream, '', C.ink, 12);
    await addImage(s, iconPath, { left: 816, top: y + 20, width: 20, height: 20 }, { alt: `${platform} logo`, fit: 'contain' });
    addText(s, platform.toUpperCase(), { left: 866, top: y + 10, width: 180, height: 18 }, { fontSize: 11, bold: true, color: C.orangeSoft });
    addText(s, 'Bataa', { left: 866, top: y + 29, width: 220, height: 23 }, { fontSize: 18, bold: true, color: C.cream });
  }

  footer(s, 'Social channels · verify live profile handles before publishing', true);
  note(s, 'Website: bataa.app, supplied by the user. Social platforms requested by the user: TikTok, Instagram, Facebook, and LinkedIn. Account handles and profile URLs were not provided, so this slide labels each account as “Bataa” without inventing links. Verify and add the live handles before publishing. Logo sources: Simple Icons via jsDelivr (TikTok, Instagram, and Facebook from Simple Icons 14.15; LinkedIn from Simple Icons 13.0).');
}

const candidatePath = path.join(tmpDir, 'bataa-pitch-deck-candidate.pptx');
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
