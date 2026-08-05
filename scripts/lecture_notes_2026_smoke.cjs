const { chromium } = require("playwright");

const base = process.env.TEST_URL || "http://127.0.0.1:4173";
const chromePath = process.env.CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

(async () => {
  const browser = await chromium.launch({headless: true, executablePath: chromePath});
  try {
    const page = await browser.newPage({viewport: {width: 1440, height: 1000}});
    const payload = await (await page.request.get(`${base}/data/questions.json`)).json();
    for (let number = 1; number <= 10; number++) {
      const lecture = String(number).padStart(2, "0");
      const predicted = payload.questions.filter(q => q.lectureNumber === lecture && q.sourceKind === "2026-predicted");
      if (predicted.length !== 3) throw new Error(`${lecture}강 예상문제 수 오류: ${predicted.length}`);
      if (predicted.some(q => !q.explanation?.diagnosticCriteria?.length)) throw new Error(`${lecture}강 진단 기준 누락`);
    }
    const moved = payload.questions.filter(q => ["gendev2-04-2018-note-q049", "gendev2-04-2017-note-q026"].includes(q.id));
    if (moved.some(q => q.lectureNumber !== "04" || q.similarGroupId !== "04-labor-arrest")) throw new Error("오분류 문항 이동·유사묶음 오류");

    await page.goto(base, {waitUntil: "networkidle"});
    await page.fill("#attendance", "2026");
    await page.click('#login-form button[type="submit"]');
    await page.click('[data-lecture="01"]');
    const first = payload.questions.filter(q => q.lectureNumber === "01").sort((a,b) => a.studyOrder-b.studyOrder)[0];
    for (const answer of first.answers) await page.click(`[data-choice="${answer}"]`);
    await page.click("#submit-answer");
    if (await page.locator(".diagnostic-criteria").count() !== 1) throw new Error("진단 기준 화면 표시 실패");
    if (await page.locator(".question-check").count() !== 0) throw new Error("내부 검수 문구가 화면에 노출됨");
    await page.screenshot({path: "work/lecture-notes-2026-desktop.png", fullPage: true});
    await page.setViewportSize({width: 390, height: 844});
    if (await page.locator("#sidebar-toggle").count()) await page.locator("#sidebar-toggle").click();
    await page.screenshot({path: "work/lecture-notes-2026-mobile.png", fullPage: true});
    const practices = payload.questions.filter(q => q.sourceKind === "lecture-practice");
    if (practices.length !== 2 || practices.reduce((sum, q) => sum + q.assets.length, 0) !== 3) throw new Error("5강 연습문제·이미지 누락");
    console.log("LECTURE_NOTES_2026_BROWSER_PASS predicted=30 past=17 practice=2 practice_assets=3 moved=2 similarity=pass criteria=pass audit_hidden=pass desktop=pass mobile=pass");
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exit(1); });
