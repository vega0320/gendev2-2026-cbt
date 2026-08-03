const { chromium } = require("playwright");

const base = process.env.TEST_URL || "http://127.0.0.1:4173";
const chromePath = process.env.CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

async function answerAndCheck(page, lecture, index, answer, expectedMeta) {
  await page.click(`[data-lecture="${lecture}"]`);
  await page.locator("#question-dots button").nth(index).click();
  const meta = await page.locator("#question-card .question-meta").innerText();
  if (!meta.includes(expectedMeta)) throw new Error(`${lecture}강 문항 이동 실패: ${meta}`);
  await page.locator(`[data-choice="${answer}"]`).click();
  await page.click("#submit-answer");
  await page.waitForSelector("text=정답입니다.");
  if ((await page.locator(".choice-explanation").count()) !== 5) {
    throw new Error(`${lecture}강 ${expectedMeta}: 선지 위치 해설 5개 누락`);
  }
  const explanation = await page.locator(".explanation-card").innerText();
  for (const heading of ["핵심 해설", "한 단계씩 풀이", "본과 개념 복습", "검수 상태"]) {
    if (!explanation.includes(heading)) throw new Error(`${lecture}강 ${expectedMeta}: ${heading} 누락`);
  }
  if ((await page.locator(".source-list a").count()) < 1) {
    throw new Error(`${lecture}강 ${expectedMeta}: 해설 출처 누락`);
  }
}

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: chromePath });
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
    await page.goto(base, { waitUntil: "networkidle" });
    await page.fill("#attendance", "31");
    await page.click('#login-form button[type="submit"]');

    await answerAndCheck(page, "02", 0, 2, "2025년 81번");
    await answerAndCheck(page, "03", 2, 4, "2025년 77번");
    await page.screenshot({ path: "work/early-explanations-desktop.png", fullPage: true });

    await page.setViewportSize({ width: 390, height: 844 });
    await page.screenshot({ path: "work/early-explanations-mobile.png", fullPage: true });
    console.log("EARLY_EXPLANATIONS_BROWSER_PASS lecture2=pass lecture3=pass choices_in_place=pass sources=pass mobile=pass");
  } finally {
    await browser.close();
  }
})().catch(error => {
  console.error(error);
  process.exit(1);
});
