const { chromium } = require("playwright");

const base = process.env.TEST_URL || "http://127.0.0.1:4173";
const chromePath = process.env.CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: chromePath });
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
    const response = await page.request.get(`${base}/data/questions.json`);
    if (!response.ok()) throw new Error("문항 데이터 로딩 실패");
    const payload = await response.json();
    const audited = payload.questions.filter(q => /^\d+$/.test(q.lectureNumber) && Number(q.lectureNumber) <= 32);
    const banned = [
      "재출제 포인트",
      "먼저 문제 요구를 확인한다",
      "각 선지를 이 단서와 대조",
      "사례를 그 원칙에 대입",
    ];

    for (const q of audited) {
      const explanation = q.explanation || {};
      const combined = [
        explanation.keyJudgment || "",
        explanation.conceptReview || "",
        ...(explanation.reasoningSteps || []),
        ...(explanation.choiceExplanations || []),
      ].join("\n");
      if (banned.some(phrase => combined.includes(phrase))) {
        throw new Error(`${q.id} 상투적 자동 해설 문구 잔존`);
      }
      if (q.questionMode !== "self-check" && (explanation.reasoningSteps || []).length < 4) {
        throw new Error(`${q.id} 한 단계씩 풀이 4단계 미만`);
      }
      const choiceExplanations = explanation.choiceExplanations || [];
      if (q.choices?.length && choiceExplanations.length !== q.choices.length) {
        throw new Error(`${q.id} 선지별 해설 수 불일치`);
      }
      if (new Set(choiceExplanations).size !== choiceExplanations.length) {
        throw new Error(`${q.id} 문항 내 선지 해설 중복`);
      }
      choiceExplanations.forEach((text, index) => {
        q.choices.forEach((choice, otherIndex) => {
          if (index !== otherIndex && choice.trim().length >= 12 && text.includes(choice.trim())) {
            throw new Error(`${q.id} ${index + 1}번 해설에 ${otherIndex + 1}번 선지 원문 혼입`);
          }
        });
      });
    }

    const postpartum = payload.questions.find(q => q.id === "gendev2-09-2023-q016");
    if (!postpartum) throw new Error("산욕기 2023년 16번 누락");
    const option5 = postpartum.explanation.choiceExplanations[4];
    if (/\bACE\b/i.test(option5)) throw new Error("산욕기 2023년 16번 ⑤ ACE inhibitor 오염 잔존");
    if (!/MEC 4/.test(option5) || !/21~29일 MEC 3/.test(option5)) {
      throw new Error("산욕기 2023년 16번 ⑤ 산후 복합호르몬피임 기준 누락");
    }
    if (!(postpartum.explanation.reasoningSteps || []).some(step => step.includes("문항 오류 가능성"))) {
      throw new Error("산욕기 2023년 16번 복수오답 가능성 안내 누락");
    }

    await page.goto(base, { waitUntil: "networkidle" });
    await page.fill("#attendance", "76");
    await page.click('#login-form button[type="submit"]');
    await page.click('[data-lecture="09"]');
    const lecture9 = payload.questions
      .filter(q => q.lectureNumber === "09")
      .sort((a, b) => a.studyOrder - b.studyOrder);
    const index = lecture9.findIndex(q => q.id === postpartum.id);
    if (index < 0) throw new Error("산욕기 2023년 16번 강의 9 순서 누락");
    await page.locator("#question-dots button").nth(index).click();
    for (const answer of postpartum.answers) await page.click(`[data-choice="${answer}"]`);
    await page.click("#submit-answer");
    if (await page.locator(".choice-explanation").count() !== postpartum.choices.length) {
      throw new Error("산욕기 2023년 16번 선지별 해설 렌더링 실패");
    }
    const rendered = await page.locator("#question-card").innerText();
    if (/\bACE\b/i.test(rendered)) throw new Error("산욕기 2023년 16번 화면에 ACE inhibitor 오염 잔존");
    if (!rendered.includes("MEC 4")) throw new Error("산욕기 2023년 16번 근거 기준 렌더링 실패");

    await page.setViewportSize({ width: 390, height: 844 });
    await page.screenshot({ path: "work/mobile-lecture9-postpartum-audit.png", fullPage: true });
    console.log(`EXPLANATION_QUALITY_BROWSER_PASS audited=${audited.length} min_steps=4 postpartum_regression=pass mobile=pass`);
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exit(1); });
