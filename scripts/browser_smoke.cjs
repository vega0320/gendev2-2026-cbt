const { chromium } = require("playwright");

const base = process.env.TEST_URL || "http://127.0.0.1:4173";

async function checkViewport(browser, viewport, label) {
  const page = await browser.newPage({ viewport });
  await page.goto(base, { waitUntil: "networkidle" });
  await page.fill("#attendance", label === "mobile" ? "18" : "17");
  await page.click('#login-form button[type="submit"]');
  await page.click('[data-lecture="03"]');

  await page.locator("#question-dots button").nth(0).click();
  await page.waitForSelector('text=강의에서 제시 · 비출제');
  if ((await page.locator(".choice").count()) !== 5) throw new Error(`${label}: q901 선택지 수 오류`);
  if ((await page.locator(".crop-frame img").count()) !== 1) throw new Error(`${label}: q901 표 이미지 누락`);
  await page.locator('[data-choice="2"]').click();
  await page.click("#submit-answer");
  await page.waitForSelector('text=정답입니다.');
  if ((await page.locator(".choice-explanation").count()) !== 5) throw new Error(`${label}: q901 선지별 해설 누락`);

  await page.locator("#question-dots button").nth(1).click();
  await page.fill("#self-answer", "NST와 탯줄동맥 도플러");
  await page.click("#reveal-self");
  await page.click("#self-correct");
  await page.waitForSelector('text=맞았다고 기록했습니다.');
  const meta = await page.locator("#question-card .question-meta").innerText();
  if (!meta.includes("시도 1 · 오답 0")) throw new Error(`${label}: q902 누적 표시 오류`);

  await page.screenshot({ path: `work/${label}-lecture3.png`, fullPage: true });
  await page.close();
}

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: process.env.CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  });
  try {
    await checkViewport(browser, { width: 1440, height: 1000 }, "desktop");
    await checkViewport(browser, { width: 390, height: 844 }, "mobile");
    console.log("BROWSER_SMOKE_PASS lecture3_examples=2 desktop=pass mobile=pass");
  } finally {
    await browser.close();
  }
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
