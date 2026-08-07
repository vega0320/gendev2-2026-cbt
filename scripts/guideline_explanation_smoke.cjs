const { chromium } = require("playwright");

const base = process.env.TEST_URL || "http://127.0.0.1:4173";
const chromePath = process.env.CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: chromePath });
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
    await page.route("**/api/progress*", route => route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(route.request().method() === "GET" ? { responses: {}, lectureNotes: {} } : { ok: true }),
    }));
    await page.goto(base, { waitUntil: "networkidle" });
    await page.fill("#attendance", "80778");
    await page.click('#login-form button[type="submit"]');
    await page.click('[data-lecture="06"]');
    const target = await page.evaluate(async () => {
      const data = await (await fetch("data/questions.json")).json();
      const questions = data.questions.filter(q => q.lectureNumber === "06").sort((a, b) => a.studyOrder - b.studyOrder);
      const index = questions.findIndex(q => q.id === "gendev2-06-2023-q029");
      return { index, answer: questions[index].answers[0] };
    });
    await page.click(`[data-index="${target.index}"]`);
    await page.click(`[data-choice="${target.answer}"]`);
    await page.click("#submit-answer");
    if (await page.locator(".diagnostic-criteria li").count() < 2) throw new Error("산후출혈 진단 기준이 두 항목 미만");
    if (await page.locator(".treatment-guideline li").count() < 3) throw new Error("산후출혈 치료 지침이 세 단계 미만");
    if (await page.locator(".diagnostic-flow > div").count() < 3) throw new Error("산후출혈 흐름도가 세 단계 미만");
    const explanation = await page.locator(".explanation-card").innerText();
    if (explanation.includes("빈수축이 원인인 태아심박")) throw new Error("산후출혈 해설에 무관한 태아심박 문구가 남음");
    if (explanation.includes("한 단계씩 풀이")) throw new Error("치료 지침과 한 단계씩 풀이가 중복 표시됨");
    for (const label of ["초기 평가", "적응증 판단", "권고 처치", "추적·단계 상승"]) {
      if (!explanation.includes(label)) throw new Error(`치료 가이드라인 단계 누락: ${label}`);
    }
    await page.screenshot({ path: "work/desktop-guideline-explanation.png", fullPage: true });
    await page.setViewportSize({ width: 390, height: 844 });
    await page.screenshot({ path: "work/mobile-guideline-explanation.png", fullPage: true });
    console.log("GUIDELINE_EXPLANATION_BROWSER_PASS diagnosis=2+ treatment=4 staged flow=3+ reasoning_deduplicated=pass postpartum_regression=pass desktop=pass mobile=pass");
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exit(1); });
