const { chromium } = require("playwright");

const base = process.env.TEST_URL || "http://127.0.0.1:4173";
const chromePath = process.env.CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: chromePath });
  try {
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    await page.goto(base, { waitUntil: "networkidle" });
    await page.fill("#attendance", "71");
    await page.click('#login-form button[type="submit"]');
    await page.click('[data-lecture="11"]');
    const questionId = await page.locator("[data-note-id]").getAttribute("data-note-id");
    await page.locator(`[data-note-id="${questionId}"]`).fill("양압환기 먼저 확인");
    await page.click("[data-unknown-toggle]");
    await page.click('[data-mode="review"]');
    const reviewNote = page.locator(`#review-list [data-note-id="${questionId}"]`);
    if (await reviewNote.inputValue() !== "양압환기 먼저 확인") throw new Error("오답·모름 탭 메모 표시 실패");
    await reviewNote.fill("심박수 100 미만이면 PPV");
    await page.click('[data-mode="concepts"]');
    if (!(await page.locator("#concept-list").innerText()).includes("심박수 100 미만이면 PPV")) throw new Error("개념 탭 메모 표시 실패");

    await page.click("#switch-user");
    await page.fill("#attendance", "72");
    await page.click('#login-form button[type="submit"]');
    await page.click('[data-lecture="11"]');
    if (await page.locator(`#question-card [data-note-id="${questionId}"]`).inputValue() !== "") throw new Error("출석번호별 메모 분리 실패");

    await page.click("#switch-user");
    await page.fill("#attendance", "71");
    await page.click('#login-form button[type="submit"]');
    await page.click('[data-lecture="11"]');
    if (await page.locator(`#question-card [data-note-id="${questionId}"]`).inputValue() !== "심박수 100 미만이면 PPV") throw new Error("출석번호 복귀 후 메모 복원 실패");
    await page.setViewportSize({ width: 390, height: 844 });
    await page.screenshot({ path: "work/mobile-question-note.png", fullPage: true });
    console.log("NOTES_BROWSER_PASS per_question=pass review=pass concepts=pass attendance_isolation=pass mobile=pass");
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exit(1); });
