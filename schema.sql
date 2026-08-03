CREATE TABLE IF NOT EXISTS discussions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  question_id TEXT NOT NULL,
  author TEXT NOT NULL,
  body TEXT NOT NULL,
  ip_hash TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_discussions_question_time ON discussions(question_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_discussions_ip_time ON discussions(ip_hash, created_at DESC);

