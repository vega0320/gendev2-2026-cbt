import { onRequestGet, onRequestPost } from "../functions/api/progress.js";

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

const bad = await onRequestPost({request: new Request("https://example.test/api/progress", {method: "POST", headers: {"content-type": "application/json"}, body: JSON.stringify({attendance: "bad", responses: {}})}), env: {DB}});
if (bad.status !== 400) throw new Error("invalid attendance accepted");
console.log("PROGRESS_API_SMOKE_PASS put=pass get=pass privacy=pass validation=pass");
