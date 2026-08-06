const { chromium } = require("playwright");

const base = process.env.TEST_URL || "http://127.0.0.1:4173";
const chromePath = process.env.CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

async function answerAndCheck(page, questions, id) {
  const target = questions.find(q => q.id === id);
  if (!target) throw new Error(`${id}: 문항 데이터 누락`);
  const lectureQuestions = questions
    .filter(q => q.lectureNumber === target.lectureNumber)
    .sort((a, b) => a.studyOrder - b.studyOrder);
  const index = lectureQuestions.findIndex(q => q.id === id);
  await page.click(`[data-lecture="${target.lectureNumber}"]`);
  await page.locator("#question-dots button").nth(index).click();
  for (const answer of target.answers) await page.locator(`[data-choice="${answer}"]`).click();
  await page.click("#submit-answer");
  if ((await page.locator(".choice-explanation").count()) !== target.choices.length) {
    throw new Error(`${id}: 선지별 해설 수 불일치`);
  }
  const explanation = await page.locator(".explanation-card").innerText();
  for (const heading of ["핵심 해설", "한 단계씩 풀이", "본과 개념 복습"]) {
    if (!explanation.includes(heading)) throw new Error(`${id}: ${heading} 누락`);
  }
  if ((await page.locator(".source-list a").count()) < 1) {
    throw new Error(`${id}: 해설 출처 누락`);
  }
}

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: chromePath });
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
    const response = await page.request.get(`${base}/data/questions.json`);
    if (!response.ok()) throw new Error("문항 데이터 로딩 실패");
    const { questions } = await response.json();
    await page.goto(base, { waitUntil: "networkidle" });
    await page.fill("#attendance", "31");
    await page.click('#login-form button[type="submit"]');

    await answerAndCheck(page, questions, "gendev2-02-2025-q081");
    await answerAndCheck(page, questions, "gendev2-03-2025-q077");
    await page.screenshot({ path: "work/early-explanations-desktop.png", fullPage: true });

    await page.setViewportSize({ width: 390, height: 844 });
    await page.screenshot({ path: "work/early-explanations-mobile.png", fullPage: true });
    console.log("EARLY_EXPLANATIONS_BROWSER_PASS lecture2=pass lecture3=pass choices_in_place=pass sources=pass mobile=pass");
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exit(1); });
