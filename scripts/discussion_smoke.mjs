import { onRequestGet, onRequestPost } from "../functions/api/discussions.js";

const calls = [];
const DB = {
  prepare(sql) {
    return {
      bind(...args) {
        calls.push({ sql, args });
        return {
          async all() { return { results: [{ author: "참여자-AB12", body: "정답 검토가 필요합니다.", createdAt: "2026-08-03" }] }; },
          async first() { return { count: 0 }; },
          async run() { return { success: true }; },
        };
      },
    };
  },
};

const getResponse = await onRequestGet({
  request: new Request("https://example.test/api/discussions?questionId=gendev2-03-2026-q901"),
  env: { DB },
});
if (getResponse.status !== 200 || !(await getResponse.json())[0]?.body) throw new Error("GET discussion failed");

const postResponse = await onRequestPost({
  request: new Request("https://example.test/api/discussions", {
    method: "POST",
    headers: { "content-type": "application/json", "CF-Connecting-IP": "203.0.113.10" },
    body: JSON.stringify({ questionId: "gendev2-03-2026-q901", author: "참여자-AB12", body: "표의 고위험군 표시를 확인해 주세요." }),
  }),
  env: { DB, DISCUSSION_SALT: "test-salt" },
});
if (postResponse.status !== 201 || !(await postResponse.json()).ok) throw new Error("POST discussion failed");
if (!calls.some((entry) => entry.sql.startsWith("INSERT INTO discussions"))) throw new Error("INSERT was not called");

const badResponse = await onRequestPost({
  request: new Request("https://example.test/api/discussions", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ questionId: "bad-id", author: "실명", body: "x" }),
  }),
  env: { DB },
});
if (badResponse.status !== 400) throw new Error("invalid discussion was accepted");

console.log("DISCUSSION_API_SMOKE_PASS get=pass post=pass validation=pass");
