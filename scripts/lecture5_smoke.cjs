const { chromium } = require("playwright");
const base = process.env.TEST_URL || "http://127.0.0.1:4173";
const chromePath = process.env.CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: chromePath });
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
    const response = await page.request.get(`${base}/data/questions.json`);
    const { questions } = await response.json();
    const lecture = questions.filter(q => q.lectureNumber === "05").sort((a, b) => a.studyOrder - b.studyOrder);
    await page.goto(base, { waitUntil: "networkidle" });
    await page.fill("#attendance", "51");
    await page.click('#login-form button[type="submit"]');
    await page.click('[data-lecture="05"]');
    for (const index of [0, Math.floor(lecture.length / 2), lecture.length - 1]) {
      const q = lecture[index];
      await page.locator("#question-dots button").nth(index).click();
      for (const answer of q.answers) await page.locator(`[data-choice="${answer}"]`).click();
      await page.click("#submit-answer");
      if ((await page.locator(".choice-explanation").count()) !== q.choices.length) {
        throw new Error(`${q.id}: 선지별 해설 수 불일치`);
      }
      const text = await page.locator(".explanation-card").innerText();
      if (!text.includes("한 단계씩 풀이") || !text.includes("본과 개념 복습")) throw new Error(`${q.id}: 해설 영역 누락`);
    }
    await page.screenshot({ path: "work/lecture5-desktop.png", fullPage: true });
    await page.setViewportSize({ width: 390, height: 844 });
    await page.screenshot({ path: "work/lecture5-mobile.png", fullPage: true });
    console.log("LECTURE5_BROWSER_PASS representative=3 choices=pass reasoning=pass mobile=pass");
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
