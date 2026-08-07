const { chromium } = require("playwright");

const base = process.env.TEST_URL || "http://127.0.0.1:4173";
const chromePath = process.env.CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: chromePath });
  try {
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    await page.route("**/api/progress*", route => route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(route.request().method() === "GET" ? { responses: {}, lectureNotes: {} } : { ok: true }),
    }));
    await page.goto(base, { waitUntil: "networkidle" });
    await page.fill("#attendance", "80777");
    await page.click('#login-form button[type="submit"]');
    const info = await page.evaluate(async () => {
      const data = await (await fetch("data/questions.json")).json();
      const q = data.questions.filter(item => item.lectureNumber === "01").sort((a, b) => a.studyOrder - b.studyOrder)[0];
      return { answer: q.answers[0], wrong: [1, 2, 3, 4, 5].find(value => !q.answers.includes(value)) };
    });

    await page.click("[data-unknown-toggle]");
    const note = page.locator("#question-card [data-note-id]");
    await note.fill("다시 풀어도 보존할 메모");
    await page.click(`[data-choice="${info.wrong}"]`);
    await page.click("#submit-answer");
    await page.click("#retry-current-question");
    let meta = await page.locator("#question-card .question-meta").innerText();
    if (!meta.includes("시도 1 · 오답 1")) throw new Error(`오답 뒤 누적값 보존 실패: ${meta}`);
    if ((await note.inputValue()) !== "다시 풀어도 보존할 메모") throw new Error("다시 풀기 뒤 메모가 사라짐");
    if ((await page.locator("[data-unknown-toggle]").getAttribute("aria-pressed")) !== "true") throw new Error("다시 풀기 뒤 모름 표시가 사라짐");

    await page.click(`[data-choice="${info.answer}"]`);
    await page.click("#submit-answer");
    await page.click("#retry-current-question");
    meta = await page.locator("#question-card .question-meta").innerText();
    if (!meta.includes("시도 2 · 오답 1")) throw new Error(`정답 뒤 누적값 보존 실패: ${meta}`);
    if (await page.locator("#retry-current-question").count()) throw new Error("미제출 상태에 다시 풀기 버튼이 남음");
    console.log("RETRY_CURRENT_BROWSER_PASS correct=pass wrong=pass attempts=preserved memo=preserved unknown=preserved");
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exit(1); });
