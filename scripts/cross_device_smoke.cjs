const { chromium } = require("playwright");

const base = process.env.TEST_URL || "http://127.0.0.1:4173";
const chromePath = process.env.CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const server = new Map();

async function installProgressMock(page) {
  await page.route("**/api/progress*", async route => {
    const request = route.request();
    if (request.method() === "GET") {
      const attendance = new URL(request.url()).searchParams.get("attendance");
      return route.fulfill({status: 200, contentType: "application/json", body: JSON.stringify({responses: server.get(attendance) || {}, updatedAt: null})});
    }
    const input = request.postDataJSON();
    server.set(String(input.attendance), input.responses || {});
    return route.fulfill({status: 200, contentType: "application/json", body: JSON.stringify({ok: true, responses: input.responses || {}})});
  });
}

async function login(page, attendance) {
  await page.goto(base, {waitUntil: "networkidle"});
  await page.fill("#attendance", attendance);
  await page.click('#login-form button[type="submit"]');
  await page.waitForSelector("#app:not([hidden])");
}

(async () => {
  const browser = await chromium.launch({headless: true, executablePath: chromePath});
  try {
    const first = await browser.newPage({viewport: {width: 1280, height: 900}});
    await installProgressMock(first);
    await login(first, "77");
    await first.locator('[data-choice="3"]').click();
    await first.click("#submit-answer");
    await first.waitForSelector("text=정답입니다.");
    await first.waitForFunction(() => document.querySelector("#sync-status")?.textContent === "기기 간 동기화됨");
    if (!server.get("77")?.["gendev2-01-2025-q051"]) throw new Error("첫 기기 기록 업로드 실패");

    const secondContext = await browser.newContext({viewport: {width: 390, height: 844}});
    const second = await secondContext.newPage();
    await installProgressMock(second);
    await login(second, "77");
    const meta = await second.locator("#question-card .question-meta").innerText();
    if (!meta.includes("시도 1 · 오답 0") || !(await second.locator(".choice.correct").count())) throw new Error("같은 출석번호 내려받기 실패");
    await second.click('[data-mode="progress"]');
    if ((await second.locator(".lecture-progress").count()) !== 41) throw new Error("강의별 풀이 현황 누락");
    const progressText = await second.locator("#progress-view").innerText();
    if (!progressText.includes("푼 문항") || !progressText.includes("1/10문항")) throw new Error("전체 또는 강의별 풀이 집계 오류");
    await second.screenshot({path: "work/cross-device-progress-mobile.png", fullPage: true});
    await second.locator('[data-progress-lecture="01"]').click();
    if ((await second.locator("#progress-view").isVisible())) throw new Error("현황에서 강의로 이동 실패");

    const otherContext = await browser.newContext({viewport: {width: 390, height: 844}});
    const other = await otherContext.newPage();
    await installProgressMock(other);
    await login(other, "78");
    const otherMeta = await other.locator("#question-card .question-meta").innerText();
    if (!otherMeta.includes("시도 0 · 오답 0")) throw new Error("다른 출석번호 기록 분리 실패");
    console.log("CROSS_DEVICE_BROWSER_PASS same_attendance=shared different_attendance=isolated progress_tab=pass mobile=pass");
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exit(1); });
