const { chromium } = require("playwright");

const base = process.env.TEST_URL || "http://127.0.0.1:4173";
const chromePath = process.env.CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

(async () => {
  const browser = await chromium.launch({headless: true, executablePath: chromePath});
  try {
    const page = await browser.newPage({viewport: {width: 1440, height: 1000}});
    const payload = await (await page.request.get(`${base}/data/questions.json`)).json();
    const byId = new Map(payload.questions.map(q => [q.id, q]));
    const moved = {
      "gendev2-06-2020-q019": ["10", "10-pregnancy-loss"],
      "gendev2-06-2020-q020": ["10", "10-pul-ectopic"],
      "gendev2-10-2020-q015": ["06", "06-placenta-previa"],
      "gendev2-10-2020-q016": ["06", "06-abruption"],
    };
    for (const [id, [lecture, group]] of Object.entries(moved)) {
      const q = byId.get(id);
      if (q.lectureNumber !== lecture || q.similarGroupId !== group) throw new Error(`${id}: 오분류 재배치·유사문항 오류`);
    }
    if (payload.questions.some(q => (q.classificationStatus || "").includes("오분류 의심"))) throw new Error("오분류 의심 상태 잔존");

    const responses = {};
    for (const [lecture, corrects] of [["01", [true, true, true]], ["02", [true, false]], ["03", [false, false]]]) {
      payload.questions.filter(q => q.lectureNumber === lecture).slice(0, corrects.length).forEach((q, i) => {
        responses[q.id] = {attempts: 1, wrong: corrects[i] ? 0 : 1, lastCorrect: corrects[i], selected: corrects[i] ? q.answers : [q.answers[0] === 1 ? 2 : 1], revealed: true, lastAt: new Date().toISOString()};
      });
    }
    await page.route("**/api/progress*", route => route.fulfill({status: 200, contentType: "application/json", body: JSON.stringify({responses})}));
    await page.route("**/api/discussions*", route => route.fulfill({status: 200, contentType: "application/json", body: "[]"}));
    await page.goto(base, {waitUntil: "networkidle"});
    await page.fill("#attendance", "613");
    await page.click('#login-form button[type="submit"]');

    await page.fill("#question-search", "Marfan");
    if (Number((await page.locator("#question-filter-count").innerText()).replace(/\D/g, "")) < 1) throw new Error("전체 문제 검색 실패");
    if (!(await page.locator("#progress-scope").innerText()).includes("전체 검색")) throw new Error("전체 검색 범위 표시 실패");

    await page.click('[data-lecture="01"]');
    const sameExpected = payload.questions.filter(q => q.lectureNumber === "01" && q.importance === "high").length;
    await page.check("#same-professor-only");
    const sameActual = Number((await page.locator("#question-filter-count").innerText()).replace(/\D/g, ""));
    if (sameActual !== sameExpected) throw new Error(`동일 교수 필터 오류 ${sameActual}/${sameExpected}`);
    await page.uncheck("#same-professor-only");

    await page.click('[data-mode="progress"]');
    const colors = await page.locator(".progress-track > span").evaluateAll(nodes => nodes.slice(0, 3).map(node => getComputedStyle(node).backgroundColor));
    const rgb = color => color.match(/\d+/g).slice(0, 3).map(Number);
    const [green, yellow, red] = colors.map(rgb);
    if (!(green[1] > green[0] && green[1] > green[2])) throw new Error(`고정답률 초록 실패: ${colors[0]}`);
    if (!(Math.abs(yellow[0] - yellow[1]) < 15 && yellow[0] > yellow[2])) throw new Error(`중간 정답률 노랑 실패: ${colors[1]}`);
    if (!(red[0] > red[1] && red[0] > red[2])) throw new Error(`고오답률 빨강 실패: ${colors[2]}`);
    await page.screenshot({path: "work/progress-accuracy-gradient-desktop.png", fullPage: true});
    await page.setViewportSize({width: 390, height: 844});
    await page.click('[data-mode="solve"]');
    await page.screenshot({path: "work/question-search-mobile.png", fullPage: true});
    console.log(`SEARCH_PROGRESS_RECLASSIFICATION_PASS search=pass sameProfessor=${sameActual} gradient=red-yellow-green moved=4 mobile=pass`);
  } finally {
    await browser.close();
  }
})().catch(error => {console.error(error); process.exit(1);});
