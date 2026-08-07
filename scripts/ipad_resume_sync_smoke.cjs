const { chromium } = require("playwright");

const base = process.env.TEST_URL || "http://127.0.0.1:4173";
const chromePath = process.env.CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const server = new Map();

function mergeResponses(stored = {}, incoming = {}) {
  const merged = { ...stored };
  for (const [id, value] of Object.entries(incoming)) {
    const old = merged[id];
    merged[id] = !old || Date.parse(value.lastAt || 0) >= Date.parse(old.lastAt || 0)
      ? { ...value, attempts: Math.max(old?.attempts || 0, value.attempts || 0), wrong: Math.max(old?.wrong || 0, value.wrong || 0) }
      : old;
  }
  return merged;
}

async function installMock(page) {
  await page.route("**/api/progress*", async route => {
    const request = route.request();
    if (request.method() === "GET") {
      await new Promise(resolve => setTimeout(resolve, 200));
      const attendance = new URL(request.url()).searchParams.get("attendance");
      return route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ responses: server.get(attendance) || {}, lectureNotes: {} }) });
    }
    const input = request.postDataJSON();
    server.set(String(input.attendance), mergeResponses(server.get(String(input.attendance)), input.responses || {}));
    return route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ ok: true, responses: server.get(String(input.attendance)), lectureNotes: {} }) });
  });
}

async function login(page, attendance) {
  await page.goto(base, { waitUntil: "networkidle" });
  await page.fill("#attendance", attendance);
  const submit = page.click('#login-form button[type="submit"]');
  await page.waitForTimeout(60);
  if (await page.locator("#app").isVisible()) throw new Error("서버 기록을 받기 전에 풀이 화면이 먼저 표시됨");
  await submit;
  await page.waitForSelector("#app:not([hidden])");
}

const profiles = [
  {
    name: "ipad",
    attendance: "8066",
    viewport: { width: 820, height: 1180 },
    userAgent: "Mozilla/5.0 (iPad; CPU OS 18_6 like Mac OS X) AppleWebKit/605.1.15 Version/18.6 Mobile/15E148 Safari/604.1",
    hasTouch: true,
    isMobile: true,
  },
  {
    name: "iphone",
    attendance: "8067",
    viewport: { width: 390, height: 844 },
    userAgent: "Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) AppleWebKit/605.1.15 Version/18.6 Mobile/15E148 Safari/604.1",
    hasTouch: true,
    isMobile: true,
  },
  {
    name: "mac",
    attendance: "8068",
    viewport: { width: 1440, height: 1000 },
    userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 15_6) AppleWebKit/605.1.15 Version/18.6 Safari/605.1.15",
    hasTouch: false,
    isMobile: false,
  },
];

async function runProfile(browser, profile) {
  const desktopContext = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
  const desktop = await desktopContext.newPage();
  await installMock(desktop);
  const appleContext = await browser.newContext(profile);
  const apple = await appleContext.newPage();
  await installMock(apple);
  await login(apple, profile.attendance);
  if (!(await apple.locator("#question-card .question-meta").innerText()).includes("시도 0 · 오답 0")) throw new Error(`${profile.name} 초기 상태 오류`);

  await login(desktop, profile.attendance);
  const answer = await desktop.evaluate(async () => (await (await fetch("data/questions.json")).json()).questions.find(q => q.id === "gendev2-01-2026-q951").answers[0]);
  await desktop.click(`[data-choice="${answer}"]`);
  await desktop.click("#submit-answer");
  await desktop.waitForFunction(() => document.querySelector("#sync-status")?.textContent === "기기 간 동기화됨");

  await apple.evaluate(() => window.dispatchEvent(new PageTransitionEvent("pageshow", { persisted: true })));
  await apple.waitForFunction(() => document.querySelector("#question-card .question-meta")?.textContent.includes("시도 1 · 오답 0"));
  if (!(await apple.locator(".choice.correct").count())) throw new Error(`${profile.name} 복귀 뒤 서버 정답 상태가 반영되지 않음`);
  await apple.click('[data-mode="progress"]');
  if (!(await apple.locator("#progress-view").innerText()).includes("1/15문항")) throw new Error(`${profile.name} 풀이현황이 갱신되지 않음`);
  await apple.screenshot({ path: `work/${profile.name}-resume-sync.png`, fullPage: true });
  await appleContext.close();
  await desktopContext.close();
}

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: chromePath });
  try {
    for (const profile of profiles) await runProfile(browser, profile);
    console.log("APPLE_RESUME_SYNC_BROWSER_PASS ipad=pass iphone=pass mac=pass login_server_first=pass bfcache_refresh=pass progress=pass");
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exit(1); });
