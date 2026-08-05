const { chromium } = require("playwright");

const base = process.env.TEST_URL || "http://127.0.0.1:4173";
const chromePath = process.env.CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

async function runViewport(browser, viewport, label) {
  const page = await browser.newPage({ viewport });
  const response = await page.request.get(`${base}/data/questions.json`);
  if (!response.ok()) throw new Error(`${label}: questions.json load failed`);
  const questions = (await response.json()).questions;
  const predicted = questions.find(q => q.id === "gendev2-01-2026-q951");
  const lecture1 = questions.filter(q => q.lectureNumber === "01").sort((a, b) => a.studyOrder - b.studyOrder);
  const predictedIndex = lecture1.findIndex(q => q.id === predicted.id);

  await page.goto(base, { waitUntil: "networkidle" });
  await page.fill("#attendance", label === "mobile" ? "95" : "94");
  await page.click('#login-form button[type="submit"]');
  await page.click('[data-lecture="01"]');
  await page.locator("#question-dots button").nth(predictedIndex).click();
  const badge = page.locator(".pill.prediction");
  if ((await badge.innerText()).trim() !== "예상문제 · 비출제") throw new Error(`${label}: predicted badge missing`);
  for (const answer of predicted.answers) await page.click(`[data-choice="${answer}"]`);
  await page.click("#submit-answer");
  if (await page.locator(".numeric-reference li").count() < 1) throw new Error(`${label}: numeric reference missing`);
  if (await page.locator(".common-pitfall").count() !== 1) throw new Error(`${label}: common pitfall missing`);
  if (await page.locator(".choice-explanation").count() !== 5) throw new Error(`${label}: choice explanations missing`);
  await page.screenshot({ path: `work/${label}-predicted-evidence.png`, fullPage: true });
  await page.close();
}

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: chromePath });
  try {
    await runViewport(browser, { width: 1440, height: 1000 }, "desktop");
    await runViewport(browser, { width: 390, height: 844 }, "mobile");
    console.log("PREDICTED_EVIDENCE_BROWSER_PASS desktop=pass mobile=pass badge=pass numeric=pass choices=pass");
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exit(1); });
