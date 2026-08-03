const json = (body, status = 200) => new Response(JSON.stringify(body), {
  status,
  headers: {"content-type": "application/json; charset=utf-8", "cache-control": "no-store"},
});

const validQuestionId = (value) => /^gendev2-[0-9]{2}(?:-[12])?-[0-9]{4}-q[0-9]{3}(?:-v[0-9]+)?$/.test(value || "");
const hashIp = async (ip, salt) => {
  const bytes = new TextEncoder().encode(`${salt}:${ip}`);
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return [...new Uint8Array(digest)].map((value) => value.toString(16).padStart(2, "0")).join("").slice(0, 24);
};

export async function onRequestGet(context) {
  const questionId = new URL(context.request.url).searchParams.get("questionId");
  if (!validQuestionId(questionId)) return json({error: "invalid questionId"}, 400);
  if (!context.env.DB) return json({error: "discussion database is not configured"}, 503);
  const result = await context.env.DB.prepare(
    "SELECT author, body, created_at AS createdAt FROM discussions WHERE question_id = ? ORDER BY id DESC LIMIT 100"
  ).bind(questionId).all();
  return json(result.results || []);
}

export async function onRequestPost(context) {
  if (!context.env.DB) return json({error: "discussion database is not configured"}, 503);
  let input;
  try { input = await context.request.json(); } catch { return json({error: "invalid JSON"}, 400); }
  const questionId = String(input.questionId || "");
  const author = String(input.author || "").trim();
  const body = String(input.body || "").trim();
  if (!validQuestionId(questionId) || !/^참여자-[0-9A-F]{4}$/.test(author) || body.length < 2 || body.length > 800) {
    return json({error: "invalid discussion"}, 400);
  }
  const ip = context.request.headers.get("CF-Connecting-IP") || "unknown";
  const ipHash = await hashIp(ip, context.env.DISCUSSION_SALT || "gendev2-public-discussion");
  const recent = await context.env.DB.prepare(
    "SELECT COUNT(*) AS count FROM discussions WHERE ip_hash = ? AND created_at > datetime('now', '-1 minute')"
  ).bind(ipHash).first();
  if ((recent?.count || 0) >= 5) return json({error: "rate limit"}, 429);
  await context.env.DB.prepare(
    "INSERT INTO discussions (question_id, author, body, ip_hash) VALUES (?, ?, ?, ?)"
  ).bind(questionId, author, body, ipHash).run();
  return json({ok: true}, 201);
}
