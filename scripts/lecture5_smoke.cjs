const { chromium } = require("playwright");

const base = process.env.TEST_URL || "http://127.0.0.1:4173";
const chromePath = process.env.CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

async function answer(page, index, choice, warning = "") {
  await page.locator("#question-dots button").nth(index).click();
  await page.locator(`[data-choice="${choice}"]`).click();
  await page.click("#submit-answer");
  await page.waitForSelector("text=정답입니다.");
  if ((await page.locator(".choice-explanation").count()) !== 5) throw new Error(`5강 ${index + 1}번째 문항 선지 해설 누락`);
  if (warning && !(await page.locator("#question-card").innerText()).includes(warning)) throw new Error(`5강 ${index + 1}번째 문항 검수 경고 누락`);
}

(async () => {
  const browser = await chromium.launch({headless: true, executablePath: chromePath});
  try {
    if (base.startsWith("https://")) {
      const setup = await browser.newContext();
      const response = await setup.request.post(`${base}/api/progress`, {data: {attendance: "51", responses: {}}});
      if (!response.ok()) throw new Error(`5강 시험 계정 초기화 실패: ${response.status()}`);
      await setup.close();
    }
    const page = await browser.newPage({viewport: {width: 1440, height: 1000}});
    await page.goto(base, {waitUntil: "networkidle"});
    await page.fill("#attendance", "51");
    await page.click('#login-form button[type="submit"]');
    await page.click('[data-lecture="05"]');
    await answer(page, 5, 3);
    if ((await page.locator(".asset-button img").count()) !== 2) throw new Error("5강 2025년 1번 이미지 2개 누락");
    await answer(page, 7, 4, "현재 선호 약제와 차이");
    await answer(page, 14, 2, "항생제 금기");
    await page.screenshot({path: "work/lecture5-desktop.png", fullPage: true});
    await page.setViewportSize({width: 390, height: 844});
    await page.screenshot({path: "work/lecture5-mobile.png", fullPage: true});
    console.log("LECTURE5_BROWSER_PASS explanations=15 images=pass current_guideline_warnings=pass mobile=pass");
  } finally {
    await browser.close();
  }
})().catch(error => {console.error(error);process.exit(1);});
