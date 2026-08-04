const { chromium } = require("playwright");

const base = process.env.TEST_URL || "http://127.0.0.1:4173";
const chromePath = process.env.CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: chromePath });
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
    await page.goto(base, { waitUntil: "networkidle" });
    await page.fill("#attendance", "27");
    await page.click('#login-form button[type="submit"]');
    const sidebarWidth = await page.locator(".sidebar").evaluate(node => node.getBoundingClientRect().width);
    await page.click("#toggle-sidebar");
    await page.waitForTimeout(300);
    const collapsedWidth = await page.locator(".sidebar").evaluate(node => node.getBoundingClientRect().width);
    if (!(sidebarWidth > 200 && collapsedWidth < 100)) throw new Error(`데스크톱 강의 탭 접기 실패: before=${sidebarWidth}, after=${collapsedWidth}, class=${await page.locator(".layout").getAttribute("class")}`);
    await page.reload({ waitUntil: "networkidle" });
    await page.fill("#attendance", "27");
    await page.click('#login-form button[type="submit"]');
    await page.waitForTimeout(300);
    const persistedWidth = await page.locator(".sidebar").evaluate(node => node.getBoundingClientRect().width);
    if (persistedWidth >= 100) throw new Error("강의 탭 접힘 상태 저장 실패");
    await page.click("#toggle-sidebar");
    await page.click('[data-lecture="03"]');

    await page.click("[data-unknown-toggle]");
    if ((await page.locator("#review-count").innerText()).trim() !== "1") throw new Error("모름 문항 수가 갱신되지 않음");
    await page.locator('[data-choice="1"]').click();
    await page.click("#submit-answer");
    await page.waitForSelector("text=오답입니다.");

    await page.click('[data-mode="review"]');
    if ((await page.locator(".review-card").count()) !== 1) throw new Error("오답·모름 목록 생성 실패");
    const reviewText = await page.locator(".review-card").innerText();
    if (!reviewText.includes("오답") || !reviewText.includes("모름") || !reviewText.includes("산전 염색체 선별·진단")) throw new Error("복습 상태 또는 개념 누락");

    await page.click('[data-mode="concepts"]');
    if ((await page.locator(".concept-card").count()) < 1) throw new Error("개념 정리 생성 실패");
    await page.click('[data-mode="review"]');
    await page.click("[data-review-retry]");
    await page.locator('[data-choice="2"]').click();
    await page.click("#submit-answer");
    await page.waitForSelector("text=정답입니다.");
    await page.click("[data-unknown-toggle]");
    await page.click('[data-mode="review"]');
    if ((await page.locator(".review-card").count()) !== 0) throw new Error("정답·모름 해제 후 복습 목록에서 빠지지 않음");

    await page.click("#switch-user");
    await page.fill("#attendance", "28");
    await page.click('#login-form button[type="submit"]');
    await page.click('[data-mode="review"]');
    if ((await page.locator(".review-card").count()) !== 0) throw new Error("출석번호별 복습 기록 분리 실패");

    await page.setViewportSize({ width: 390, height: 844 });
    await page.screenshot({ path: "work/mobile-review-empty.png", fullPage: true });
    console.log("REVIEW_BROWSER_PASS wrong=pass unknown=pass concepts=pass retry=pass isolation=pass sidebar=pass mobile=pass");
  } finally {
    await browser.close();
  }
})().catch(error => {
  console.error(error);
  process.exit(1);
});
