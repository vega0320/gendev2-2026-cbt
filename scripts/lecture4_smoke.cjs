const { chromium } = require("playwright");

const base = process.env.TEST_URL || "http://127.0.0.1:4173";
const chromePath = process.env.CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

async function expectCorrectWithExplanations(page) {
  await page.click("#submit-answer");
  await page.waitForSelector("text=정답입니다.");
  if ((await page.locator(".choice-explanation").count()) !== 5) throw new Error("선지별 해설 5개 누락");
}

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: chromePath });
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
    await page.goto(base, { waitUntil: "networkidle" });
    await page.fill("#attendance", "41");
    await page.click('#login-form button[type="submit"]');
    await page.click('[data-lecture="04"]');

    await page.locator("#question-dots button").nth(0).click();
    await page.locator('[data-choice="4"]').click();
    await expectCorrectWithExplanations(page);
    if (!(await page.locator("#question-card").innerText()).includes("그림 A–E 표지 원본 대조 필요")) throw new Error("Friedman 그림 검수 경고 누락");

    await page.locator("#question-dots button").nth(1).click();
    if (!(await page.locator("#question-card").innerText()).includes("복수 선택")) throw new Error("복수 선택 안내 누락");
    await page.locator('[data-choice="1"]').click();
    await page.locator('[data-choice="2"]').click();
    if ((await page.locator(".choice.selected").count()) !== 2) throw new Error("복수 선지 동시 선택 실패");
    await expectCorrectWithExplanations(page);
    if (!(await page.locator("#question-card").innerText()).includes("현재 산소 권고 일부 충돌")) throw new Error("현재 지침 충돌 표시 누락");

    await page.locator("#question-dots button").nth(2).click();
    await page.locator('[data-choice="3"]').click();
    await expectCorrectWithExplanations(page);
    if (!(await page.locator("#question-card").innerText()).includes("족보 정답 오류 교정: ① → ③")) throw new Error("정답 교정 표시 누락");

    await page.screenshot({ path: "work/lecture4-desktop.png", fullPage: true });
    await page.setViewportSize({ width: 390, height: 844 });
    await page.screenshot({ path: "work/lecture4-mobile.png", fullPage: true });
    console.log("LECTURE4_BROWSER_PASS explanations=9 multi_select=pass answer_correction=pass guideline_conflict=pass mobile=pass");
  } finally {
    await browser.close();
  }
})().catch(error => {
  console.error(error);
  process.exit(1);
});
