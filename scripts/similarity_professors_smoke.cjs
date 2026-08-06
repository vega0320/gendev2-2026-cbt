const { chromium } = require("playwright");

(async () => {
  const baseURL = process.env.BASE_URL || "http://127.0.0.1:4173";
  const browser = await chromium.launch({
    headless: true,
    executablePath: process.env.CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  });
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto(baseURL, { waitUntil: "networkidle" });
    await page.getByLabel("출석번호", { exact: true }).fill("9997");
    await page.getByRole("button", { name: "내 문제풀이 시작", exact: true }).click();
    await page.locator('[data-lecture="09"]').click();
    await page.locator("#question-dots button").nth(3).click();
    const meta = await page.locator(".question-meta").innerText();
    if (!meta.includes("유사문항 1/3")) throw new Error("유사문항 위치 표지가 보이지 않음");
    const lectureText = await page.locator('[data-lecture="09"]').innerText();
    if (!/동일 교수 \d+\s*\/\s*15문항/.test(lectureText)) throw new Error("강의 탭 동일 교수/전체 문항 표기 오류");

    const dataCheck = await page.evaluate(async () => {
      const data = await (await fetch("data/questions.json")).json();
      const groups = new Map();
      for (const q of data.questions.filter(q => q.similarGroupId)) {
        if (!groups.has(q.similarGroupId)) groups.set(q.similarGroupId, []);
        groups.get(q.similarGroupId).push(q);
      }
      return [...groups.values()].every(items => {
        const orders = items.map(q => q.studyOrder).sort((a, b) => a - b);
        return orders.every((value, index) => index === 0 || value === orders[index - 1] + 1);
      });
    });
    if (!dataCheck) throw new Error("같은 유사문항 묶음이 연속 순서가 아님");

    await page.locator('[data-mode="professors"]').click();
    if (await page.locator(".professors-table tbody tr").count() !== 41) throw new Error("연도별 교수 표 강의 수 오류");
    if (await page.locator(".current-professor").count() !== 41) throw new Error("2026 교수 강조 누락");
    if (await page.locator(".same-professor").count() < 1) throw new Error("2026 동일 교수 연도 강조 누락");

    await page.setViewportSize({ width: 390, height: 844 });
    const bodyFits = await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth);
    const tableScrolls = await page.locator(".professors-table-wrap").evaluate(el => el.scrollWidth > el.clientWidth);
    if (!bodyFits || !tableScrolls) {
      const wide = await page.evaluate(() => [...document.querySelectorAll("body *")].filter(el => el.getBoundingClientRect().right > innerWidth + 1).slice(0, 8).map(el => `${el.tagName}.${el.className}:${Math.round(el.getBoundingClientRect().right)}`));
      throw new Error(`모바일 교수 표 가로 스크롤 오류 bodyFits=${bodyFits} tableScrolls=${tableScrolls} wide=${wide.join("|")}`);
    }
    console.log("SIMILARITY_PROFESSORS_BROWSER_PASS groups_contiguous=pass professor_table=pass mobile=pass");
  } finally {
    await browser.close();
  }
})().catch(error => {
  console.error(error);
  process.exit(1);
});
