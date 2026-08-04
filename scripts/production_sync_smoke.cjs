const { chromium } = require("playwright");

const base = process.env.TEST_URL || "https://gendev2-2026-cbt.pages.dev";
const chromePath = process.env.CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const sameAttendance = "9876";
const otherAttendance = "9875";

async function login(page, attendance) {
  await page.goto(base, {waitUntil: "networkidle"});
  await page.fill("#attendance", attendance);
  await page.click('#login-form button[type="submit"]');
  await page.waitForSelector("#app:not([hidden])");
  await page.waitForFunction(() => ["기기 간 동기화됨", "이 기기에 저장됨"].includes(document.querySelector("#sync-status")?.textContent));
}

(async () => {
  const browser = await chromium.launch({headless: true, executablePath: chromePath});
  try {
    const setup = await browser.newContext();
    for (const attendance of [sameAttendance, otherAttendance]) {
      const response = await setup.request.post(`${base}/api/progress`, {data: {attendance, responses: {}}});
      if (!response.ok()) throw new Error(`시험 계정 초기화 실패: ${attendance} ${response.status()}`);
    }
    await setup.close();

    const desktopContext = await browser.newContext({viewport: {width: 1440, height: 1000}});
    const desktop = await desktopContext.newPage();
    await login(desktop, sameAttendance);
    await desktop.locator('[data-choice="3"]').click();
    await desktop.click("#submit-answer");
    await desktop.waitForSelector("text=정답입니다.");
    await desktop.waitForFunction(() => document.querySelector("#sync-status")?.textContent === "기기 간 동기화됨");

    const mobileContext = await browser.newContext({viewport: {width: 390, height: 844}});
    const mobile = await mobileContext.newPage();
    await login(mobile, sameAttendance);
    const meta = await mobile.locator("#question-card .question-meta").innerText();
    if (!meta.includes("시도 1 · 오답 0") || !(await mobile.locator(".choice.correct").count())) throw new Error("실제 서버의 같은 번호 기록 공유 실패");
    await mobile.click('[data-mode="progress"]');
    const progress = await mobile.locator("#progress-view").innerText();
    if (!progress.includes("1/10문항")) throw new Error("실제 서버 기록의 풀이 현황 반영 실패");

    const otherContext = await browser.newContext({viewport: {width: 390, height: 844}});
    const other = await otherContext.newPage();
    await login(other, otherAttendance);
    if (!(await other.locator("#question-card .question-meta").innerText()).includes("시도 0 · 오답 0")) throw new Error("실제 서버의 다른 번호 기록 분리 실패");
    console.log("PRODUCTION_SYNC_BROWSER_PASS cloudflare_d1=pass desktop_to_mobile=pass progress_tab=pass isolation=pass");
  } finally {
    await browser.close();
  }
})().catch(error => {console.error(error);process.exit(1);});
