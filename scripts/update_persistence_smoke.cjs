const { chromium } = require("playwright");

const base = process.env.TEST_URL || "http://127.0.0.1:4173";
const chromePath = process.env.CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: chromePath });
  try {
    const context = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    const page = await context.newPage();
    await page.route("**/api/progress*", async route => {
      if (route.request().method() === "GET") {
        await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ responses: {}, lectureNotes: {} }) });
        return;
      }
      const body = JSON.parse(route.request().postData() || "{}");
      await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ ok: true, responses: body.responses || {}, lectureNotes: body.lectureNotes || {} }) });
    });
    await page.goto(base, { waitUntil: "networkidle" });
    await page.fill("#attendance", "818");
    await page.click('#login-form button[type="submit"]');
    const answer = await page.evaluate(async () => {
      const data = await (await fetch("data/questions.json")).json();
      return data.questions.filter(q => q.lectureNumber === "01").sort((a, b) => a.studyOrder - b.studyOrder)[0].answers[0];
    });
    await page.click(`[data-choice="${answer}"]`);
    await page.click("#submit-answer");
    await page.reload({ waitUntil: "networkidle" });
    await page.fill("#attendance", "818");
    await page.click('#login-form button[type="submit"]');
    const meta = await page.locator("#question-card .question-meta").innerText();
    if (!meta.includes("시도 1")) throw new Error(`제출 직후 새로고침 기록 복구 실패: ${meta}`);

    const updateContext = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    const updatePage = await updateContext.newPage();
    const source = await (await updateContext.request.get(`${base}/data/questions.json`)).json();
    const updated = structuredClone(source);
    updated.questions.find(q => q.lectureNumber === "01").stem = "[자동 업데이트 확인] " + updated.questions.find(q => q.lectureNumber === "01").stem;
    let version = { schemaVersion: 1, dataVersion: "data-v1", appVersion: "app-v1", buildVersion: "build-v1" };
    await updatePage.route("**/version.json*", route => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(version) }));
    await updatePage.route("**/data/questions.json*", route => {
      const useUpdated = new URL(route.request().url()).searchParams.get("v") === "data-v2";
      return route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(useUpdated ? updated : source) });
    });
    await updatePage.route("**/api/progress*", route => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(route.request().method() === "GET" ? { responses: {}, lectureNotes: {} } : { ok: true, responses: {}, lectureNotes: {} }) }));
    await updatePage.goto(base, { waitUntil: "networkidle" });
    await updatePage.fill("#attendance", "819");
    await updatePage.click('#login-form button[type="submit"]');
    version = { ...version, dataVersion: "data-v2", buildVersion: "build-v2" };
    await updatePage.evaluate(() => window.dispatchEvent(new Event("focus")));
    await updatePage.waitForFunction(() => document.querySelector(".stem")?.textContent.includes("[자동 업데이트 확인]"));
    if (await updatePage.locator("#login").isVisible()) throw new Error("데이터 자동 반영 중 출석 화면으로 잘못 이동함");

    version = { ...version, appVersion: "app-v2", buildVersion: "build-v3" };
    await updatePage.evaluate(() => window.dispatchEvent(new Event("focus")));
    await updatePage.waitForSelector("#login:not([hidden])");
    console.log("UPDATE_PERSISTENCE_BROWSER_PASS immediate_reload=pass hot_data=pass app_reload_to_login=pass");
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exit(1); });
