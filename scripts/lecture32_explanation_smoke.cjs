const { chromium } = require("playwright");

const base = process.env.TEST_URL || "http://127.0.0.1:4173";

async function check(browser, viewport, label) {
  const page = await browser.newPage({ viewport });
  await page.goto(base, { waitUntil: "networkidle" });
  await page.fill("#attendance", label === "mobile" ? "326" : "321");
  await page.click('#login-form button[type="submit"]');
  for (const lecture of ["26", "32"]) {
    await page.click(`[data-lecture="${lecture}"]`);
    const card = page.locator("#question-card");
    const choices = await card.locator(".choice-body").allTextContents();
    await card.locator('[data-choice="1"]').click();
    await card.locator("#submit-answer").click();
    const explanations = card.locator(".choice-explanation");
    if ((await explanations.count()) !== 5) throw new Error(`${label}: L${lecture} explanation count`);
    for (let index = 0; index < 5; index += 1) {
      const explanation = (await explanations.nth(index).innerText()).trim();
      const choice = choices[index].replace(/^\s*[①②③④⑤1-5][.)]?\s*/, "").trim();
      if (/^[‘'"]/.test(explanation) || (choice.length >= 12 && explanation.includes(`‘${choice}’`))) {
        throw new Error(`${label}: L${lecture} choice ${index + 1} repeats choice text`);
      }
    }
  }
  await page.screenshot({ path: `work/${label}-lecture32-explanations.png`, fullPage: true });
  await page.close();
}

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: process.env.CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  });
  await check(browser, { width: 1440, height: 1000 }, "desktop");
  await check(browser, { width: 390, height: 844 }, "mobile");
  await browser.close();
  console.log("LECTURE_26_32_EXPLANATION_BROWSER_PASS desktop=pass mobile=pass choice_echo=0");
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
