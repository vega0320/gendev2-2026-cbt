const json = (body, status = 200) => new Response(JSON.stringify(body), {
  status,
  headers: {"content-type": "application/json; charset=utf-8", "cache-control": "no-store"},
});

const validAttendance = value => /^\d{1,4}$/.test(value || "");
export const validQuestionId = value => /^gendev2-[0-9]{2}(?:-[12])?-[0-9]{4}(?:-(?:note|practice))?-q[0-9]{3}(?:-v[0-9]+)?$/.test(value || "");
const safeInteger = value => Number.isInteger(value) && value >= 0 && value <= 100000 ? value : 0;
const safeDate = value => typeof value === "string" && !Number.isNaN(Date.parse(value)) ? value : new Date(0).toISOString();

async function attendanceHash(attendance, env) {
  const salt = env.PROGRESS_SALT || env.DISCUSSION_SALT || "gendev2-progress-v1";
  const bytes = new TextEncoder().encode(`${salt}:${attendance}`);
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return [...new Uint8Array(digest)].map(value => value.toString(16).padStart(2, "0")).join("");
}

function normalizeSelected(value) {
  const values = Array.isArray(value) ? value : value == null ? [] : [value];
  const clean = [...new Set(values.filter(item => Number.isInteger(item) && item >= 1 && item <= 5))].sort();
  return Array.isArray(value) ? clean : clean[0] || null;
}

function normalizeResponses(input) {
  const output = {};
  if (!input || typeof input !== "object" || Array.isArray(input)) return output;
  // 재분류 전의 안정 ID도 복구용으로 남을 수 있으므로 현재 문항 수에 딱 맞춘
  // 500개 제한을 두지 않는다. 본문은 저장하지 않아 2,000개도 충분히 작다.
  for (const [questionId, raw] of Object.entries(input).slice(0, 2000)) {
    if (!validQuestionId(questionId) || !raw || typeof raw !== "object" || Array.isArray(raw)) continue;
    output[questionId] = {
      attempts: safeInteger(raw.attempts), wrong: safeInteger(raw.wrong), selected: normalizeSelected(raw.selected),
      revealed: Boolean(raw.revealed), unknown: Boolean(raw.unknown),
      lastCorrect: typeof raw.lastCorrect === "boolean" ? raw.lastCorrect : null,
      selfAssessed: Boolean(raw.selfAssessed), selfCorrect: typeof raw.selfCorrect === "boolean" ? raw.selfCorrect : null,
      lastAt: safeDate(raw.lastAt),
    };
  }
  return output;
}

function mergeResponses(stored = {}, incoming = {}) {
  const output = {};
  for (const id of new Set([...Object.keys(stored), ...Object.keys(incoming)])) {
    const older = stored[id];
    const newer = incoming[id];
    if (!older) { output[id] = newer; continue; }
    if (!newer) { output[id] = older; continue; }
    const olderTime = Date.parse(older.lastAt || 0) || 0;
    const newerTime = Date.parse(newer.lastAt || 0) || 0;
    const latest = newerTime >= olderTime ? newer : older;
    output[id] = {
      ...latest,
      attempts: Math.max(older.attempts || 0, newer.attempts || 0),
      wrong: Math.max(older.wrong || 0, newer.wrong || 0),
    };
  }
  return output;
}

function mergeLectureNotes(stored = {}, incoming = {}) {
  const output = {};
  for (const id of new Set([...Object.keys(stored), ...Object.keys(incoming)])) {
    const older = stored[id];
    const newer = incoming[id];
    if (!older) { output[id] = newer; continue; }
    if (!newer) { output[id] = older; continue; }
    output[id] = (Date.parse(newer.updatedAt || 0) || 0) >= (Date.parse(older.updatedAt || 0) || 0) ? newer : older;
  }
  return output;
}

function normalizeLectureNotes(input) {
  const output = {};
  if (!input || typeof input !== "object" || Array.isArray(input)) return output;
  for (const [lectureNumber, raw] of Object.entries(input).slice(0, 50)) {
    if (!/^\d{2}(?:-[12])?$/.test(lectureNumber) || !raw || typeof raw !== "object" || Array.isArray(raw)) continue;
    const text = typeof raw.text === "string" ? raw.text.trim().slice(0, 80) : "";
    if (text) output[lectureNumber] = {text, updatedAt: safeDate(raw.updatedAt)};
  }
  return output;
}

export async function onRequestGet(context) {
  if (!context.env.DB) return json({error: "progress database is not configured"}, 503);
  const attendance = new URL(context.request.url).searchParams.get("attendance") || "";
  if (!validAttendance(attendance)) return json({error: "invalid attendance"}, 400);
  const key = await attendanceHash(String(Number(attendance)), context.env);
  const row = await context.env.DB.prepare("SELECT payload, updated_at AS updatedAt FROM progress WHERE attendance_hash = ?").bind(key).first();
  if (!row) return json({responses: {}, lectureNotes: {}, updatedAt: null});
  try {
    const payload = JSON.parse(row.payload);
    return json({responses: normalizeResponses(payload.responses), lectureNotes: normalizeLectureNotes(payload.lectureNotes), updatedAt: row.updatedAt});
  } catch {
    return json({responses: {}, lectureNotes: {}, updatedAt: row.updatedAt});
  }
}

export async function onRequestPost(context) {
  if (!context.env.DB) return json({error: "progress database is not configured"}, 503);
  let input;
  try { input = await context.request.json(); } catch { return json({error: "invalid JSON"}, 400); }
  const attendance = String(input.attendance || "");
  if (!validAttendance(attendance)) return json({error: "invalid attendance"}, 400);
  const incomingResponses = normalizeResponses(input.responses);
  const incomingLectureNotes = normalizeLectureNotes(input.lectureNotes);
  const key = await attendanceHash(String(Number(attendance)), context.env);
  const existing = await context.env.DB.prepare("SELECT payload FROM progress WHERE attendance_hash = ?").bind(key).first();
  let storedResponses = {};
  let storedLectureNotes = {};
  if (existing?.payload) {
    try {
      const stored = JSON.parse(existing.payload);
      storedResponses = normalizeResponses(stored.responses);
      storedLectureNotes = normalizeLectureNotes(stored.lectureNotes);
    } catch { /* 손상된 예전 payload는 새 정상 payload로 교체한다. */ }
  }
  const responses = mergeResponses(storedResponses, incomingResponses);
  const lectureNotes = mergeLectureNotes(storedLectureNotes, incomingLectureNotes);
  const payload = JSON.stringify({responses, lectureNotes});
  if (payload.length > 600000) return json({error: "progress payload too large"}, 413);
  await context.env.DB.prepare(`INSERT INTO progress (attendance_hash, payload, updated_at)
    VALUES (?, ?, CURRENT_TIMESTAMP)
    ON CONFLICT(attendance_hash) DO UPDATE SET payload = excluded.payload, updated_at = CURRENT_TIMESTAMP`).bind(key, payload).run();
  return json({ok: true, responses, lectureNotes, updatedAt: new Date().toISOString()});
}
