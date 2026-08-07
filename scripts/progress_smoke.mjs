import { readFileSync } from "node:fs";
import { onRequestGet, onRequestPost, validQuestionId } from "../functions/api/progress.js";

let row = null;
const calls = [];
const DB = {
  prepare(sql) {
    return {
      bind(...args) {
        calls.push({sql, args});
        return {
          async first() { return row; },
          async run() { row = {payload: args[1], updatedAt: "2026-08-04 00:00:00"}; return {success: true}; },
        };
      },
    };
  },
};

const responseState = {
  attempts: 2, wrong: 1, selected: [1, 2], revealed: true, unknown: true,
  lastCorrect: false, selfAssessed: false, selfCorrect: null, lastAt: "2026-08-04T01:02:03.000Z",
  ignoredPrivateText: "서버에 저장되면 안 됨",
};
const put = await onRequestPost({
  request: new Request("https://example.test/api/progress", {method: "POST", headers: {"content-type": "application/json"}, body: JSON.stringify({attendance: "77", responses: {"gendev2-04-2025-q080": responseState}, lectureNotes: {"14": {text: "HIE 6시간", updatedAt: "2026-08-06T01:02:03.000Z"}, "bad": {text: "저장 금지"}}})}),
  env: {DB, PROGRESS_SALT: "test-progress-salt"},
});
if (put.status !== 200 || !(await put.json()).ok) throw new Error("PUT progress failed");
if (JSON.stringify(row).includes("ignoredPrivateText") || JSON.stringify(calls).includes('"77"')) throw new Error("raw attendance or extra text was stored");

const get = await onRequestGet({request: new Request("https://example.test/api/progress?attendance=77"), env: {DB, PROGRESS_SALT: "test-progress-salt"}});
const payload = await get.json();
if (get.status !== 200 || payload.responses["gendev2-04-2025-q080"]?.attempts !== 2 || payload.lectureNotes["14"]?.text !== "HIE 6시간" || payload.lectureNotes.bad) throw new Error("GET progress failed");

const newerState = {...responseState, attempts: 3, wrong: 2, selected: 4, lastAt: "2026-08-04T02:00:00.000Z"};
await onRequestPost({
  request: new Request("https://example.test/api/progress", {method: "POST", headers: {"content-type": "application/json"}, body: JSON.stringify({attendance: "77", responses: {"gendev2-04-2025-q080": newerState}})}),
  env: {DB, PROGRESS_SALT: "test-progress-salt"},
});
const staleState = {...responseState, attempts: 1, wrong: 0, selected: 1, lastAt: "2026-08-04T00:00:00.000Z"};
await onRequestPost({
  request: new Request("https://example.test/api/progress", {method: "POST", headers: {"content-type": "application/json"}, body: JSON.stringify({attendance: "77", responses: {"gendev2-04-2025-q080": staleState}})}),
  env: {DB, PROGRESS_SALT: "test-progress-salt"},
});
const merged = JSON.parse(row.payload).responses["gendev2-04-2025-q080"];
if (merged.attempts !== 3 || merged.wrong !== 2 || merged.selected !== 4) throw new Error("stale progress overwrote newer answer");

const manyResponses = Object.fromEntries(Array.from({length: 600}, (_, index) => [
  `gendev2-04-2025-q080-v${index + 1}`,
  {...responseState, lastAt: new Date(Date.parse(responseState.lastAt) + index * 1000).toISOString()},
]));
const many = await onRequestPost({
  request: new Request("https://example.test/api/progress", {method: "POST", headers: {"content-type": "application/json"}, body: JSON.stringify({attendance: "78", responses: manyResponses})}),
  env: {DB, PROGRESS_SALT: "test-progress-salt"},
});
if (many.status !== 200 || Object.keys((await many.json()).responses).length < 600) throw new Error("more than 500 stable IDs were truncated");

const questions = JSON.parse(readFileSync(new URL("../site/data/questions.json", import.meta.url), "utf8")).questions;
const rejectedIds = questions.map(question => question.id).filter(id => !validQuestionId(id));
if (rejectedIds.length) throw new Error(`site question IDs rejected by progress API: ${rejectedIds.join(", ")}`);
row = null;
const addedKinds = await onRequestPost({
  request: new Request("https://example.test/api/progress", {method: "POST", headers: {"content-type": "application/json"}, body: JSON.stringify({attendance: "79", responses: {
    "gendev2-01-2019-note-q005": responseState,
    "gendev2-05-2026-practice-q001": responseState,
  }})}),
  env: {DB, PROGRESS_SALT: "test-progress-salt"},
});
if (addedKinds.status !== 200 || Object.keys((await addedKinds.json()).responses).length !== 2) throw new Error("note/practice progress was dropped");

const bad = await onRequestPost({request: new Request("https://example.test/api/progress", {method: "POST", headers: {"content-type": "application/json"}, body: JSON.stringify({attendance: "bad", responses: {}})}), env: {DB}});
if (bad.status !== 400) throw new Error("invalid attendance accepted");
console.log(`PROGRESS_API_SMOKE_PASS put=pass get=pass privacy=pass stale_merge=pass ids_600=pass site_ids=${questions.length} note_practice=pass validation=pass`);
