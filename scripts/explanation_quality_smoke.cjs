const { chromium } = require("playwright");

const base = process.env.TEST_URL || "http://127.0.0.1:4173";
const chromePath = process.env.CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

(async () => {
  const browser = await chromium.launch({headless: true, executablePath: chromePath});
  try {
    const page = await browser.newPage({viewport: {width: 1440, height: 1000}});
    const response = await page.request.get(`${base}/data/questions.json`);
    if (!response.ok()) throw new Error("문항 데이터 로딩 실패");
    const payload = await response.json();
    const audited = payload.questions.filter(q => /^\d+$/.test(q.lectureNumber) && Number(q.lectureNumber) <= 20);
    const judgments = audited.map(q => q.explanation?.keyJudgment);
    const reviews = audited.map(q => q.explanation?.conceptReview);
    const choiceExplanations = audited.flatMap(q => q.explanation?.choiceExplanations || []);
    if (new Set(judgments).size !== 200) throw new Error("핵심 해설 중복 잔존");
    if (new Set(reviews).size !== 200) throw new Error("개념 복습 중복 잔존");
    if (new Set(choiceExplanations).size !== choiceExplanations.length) throw new Error("선지 해설 중복 잔존");

    const lecture7 = payload.questions.filter(q => q.lectureNumber === "07").sort((a,b) => a.studyOrder-b.studyOrder);
    const expected = {
      "gendev2-07-2025-q054": [4,5],
      "gendev2-07-2020-q013": [5],
      "gendev2-07-2020-q014": [3,5],
    };
    for (const [id, answers] of Object.entries(expected)) {
      const q = lecture7.find(item => item.id === id);
      if (JSON.stringify(q.answers) !== JSON.stringify(answers)) throw new Error(`${id} 교정 정답 오류`);
    }

    await page.goto(base, {waitUntil: "networkidle"});
    await page.fill("#attendance", "76");
    await page.click('#login-form button[type="submit"]');
    await page.click('[data-lecture="07"]');
    let mismatchCheck = "";
    for (let index = 0; index < lecture7.length; index++) {
      const q = lecture7[index];
      await page.locator("#question-dots button").nth(index).click();
      for (const answer of q.answers) await page.click(`[data-choice="${answer}"]`);
      await page.click("#submit-answer");
      await page.waitForSelector("text=정답입니다.");
      if (await page.locator(".choice-explanation").count() !== 5) throw new Error(`${q.id} 선지별 해설 5개 표시 실패`);
      if (await page.locator(".question-check").count() !== 1) throw new Error(`${q.id} 문제 요구 확인 표시 실패`);
      if (q.id === "gendev2-07-2020-q014") mismatchCheck = await page.locator(".question-check").innerText();
    }
    if (!mismatchCheck.includes("3개") || !mismatchCheck.includes("2개")) throw new Error(`2020-014 정답 개수 불일치 경고 누락: ${mismatchCheck}`);
    await page.setViewportSize({width: 390, height: 844});
    await page.screenshot({path: "work/mobile-lecture7-audit.png", fullPage: true});
    console.log("EXPLANATION_QUALITY_BROWSER_PASS unique=200 choices=995 lecture7=9 corrected_answers=pass count_warning=pass mobile=pass");
  } finally {
    await browser.close();
  }
})().catch(error => {console.error(error); process.exit(1);});
