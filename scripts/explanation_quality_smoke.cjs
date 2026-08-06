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
    if (new Set(judgments).size !== audited.length) throw new Error("핵심 해설 중복 잔존");
    if (new Set(reviews).size !== audited.length) throw new Error("개념 복습 중복 잔존");
    const reviewed = audited;
    const banned = ["결정 단서와 맞지 않는다", "관련되지 않는다", "구분해야 한다", "사례를 그 원칙에 대입해"];
    for (const q of reviewed) {
      const expectedMarker = Number(q.lectureNumber) <= 13 ? "manual-choice-independent-audit-01-13" : "manual-choice-independent-audit-14-20";
      if (q.explanationReviewStatus !== expectedMarker) throw new Error(`${q.id} 독립 선지 재검수 상태 누락`);
      if (!["applicable", "not-applicable"].includes(q.explanation?.numericReview?.status)) throw new Error(`${q.id} 수치 적용 검수 누락`);
      if (q.explanation.numericReview.status === "applicable" && !(q.explanation.numericReference || []).length) throw new Error(`${q.id} 수치 기준 누락`);
      for (const text of q.explanation?.choiceExplanations || []) {
        if (banned.some(phrase => text.includes(phrase))) throw new Error(`${q.id} 빈 선지 해설 문구 잔존`);
      }
      const explanations = q.explanation?.choiceExplanations || [];
      if (new Set(explanations).size !== explanations.length) throw new Error(`${q.id} 문항 내 선지 해설 중복`);
      explanations.forEach((text,index)=>{
        const body=text.split(". ").slice(1).join(". ");
        q.choices.forEach((choice,otherIndex)=>{if(index!==otherIndex&&choice.trim().length>=12&&body.includes(choice.trim()))throw new Error(`${q.id} ${index+1}번 해설에 ${otherIndex+1}번 선지 혼입`);});
      });
    }

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
    if (await page.locator("#question-card > .question-meta > .pill").nth(1).isVisible()) throw new Error("문제 카드 2026 교수명 태그가 표시됨");
    let mismatchCheck = "";
    for (let index = 0; index < lecture7.length; index++) {
      const q = lecture7[index];
      await page.locator("#question-dots button").nth(index).click();
      for (const answer of q.answers) await page.click(`[data-choice="${answer}"]`);
      await page.click("#submit-answer");
      await page.waitForSelector("text=정답입니다.");
      if (await page.locator(".choice-explanation").count() !== 5) throw new Error(`${q.id} 선지별 해설 5개 표시 실패`);
      if (await page.locator(".question-check").count() !== 0) throw new Error(`${q.id} 내부 검수 문구가 화면에 노출됨`);
      if (q.id === "gendev2-07-2020-q014") mismatchCheck = q.explanation.questionCheck || "";
    }
    if (!mismatchCheck.includes("3개") || !mismatchCheck.includes("2개")) throw new Error(`2020-014 정답 개수 불일치 경고 누락: ${mismatchCheck}`);
    await page.setViewportSize({width: 390, height: 844});
    await page.screenshot({path: "work/mobile-lecture7-audit.png", fullPage: true});
    console.log(`EXPLANATION_QUALITY_BROWSER_PASS unique=${audited.length} choices=${choiceExplanations.length} lecture7=${lecture7.length} corrected_answers=pass count_warning=pass mobile=pass`);
  } finally {
    await browser.close();
  }
})().catch(error => {console.error(error); process.exit(1);});
