# 2026 생성발2 강의별 CBT

생성발2 족보를 강의별로 풀 수 있도록 만든 공개 학습 사이트입니다.

## 주요 기능

- 출석번호별 풀이 기록 분리 및 같은 번호의 휴대폰·컴퓨터 자동 동기화
- 데스크톱과 휴대폰에서 강의 목록 접기·펼치기 및 상태 기억
- 강의별 문제 선택, 다시 풀기, 누적 시도·오답 횟수
- 마지막 오답과 직접 표시한 모름 문항을 모아 다시 풀기
- 현재 오답·모름 문항에서 복습 개념을 자동 추출해 묶어 보기
- 문제·선지는 CBT 형식으로 표시하고 표·사진은 원본 이미지로 연결
- 답 제출 뒤 각 선지 바로 아래에 해당 선지 해설 표시
- 생성발2 및 기존 임추·국시 문제은행의 비슷한 문제 연결
- 문제별 실시간 오류토의
- 2026년 강의에서 보여 준 비출제 예시를 실제 기출과 구분

출석번호는 서버에서 해시 키로 바꿔 저장하며 원문 번호는 데이터베이스에 남기지 않습니다. 풀이 기록에는 문제 본문 대신 문항 ID와 선택·정오·모름·횟수·수정시각만 저장됩니다. 출석번호는 비밀번호가 아니므로 같은 번호를 아는 사람은 같은 기록을 볼 수 있습니다.

## 검사

```powershell
python scripts/apply_lectures11_20_explanations.py
python scripts/apply_lectures6_10_explanations.py
python scripts/review_lectures_14_20.py
python scripts/review_lectures_01_13.py
python scripts/review_lecture01_reasoning.py
python scripts/review_lecture09_evidence.py
python scripts/repair_explanation_integrity.py
python scripts/enhance_reasoning_steps.py
python scripts/repair_reasoning_meta_language.py
python scripts/audit_explanation_integrity.py
python scripts/prepare_site.py
python scripts/validate_site.py
node --check site/app.js
node --check functions/api/discussions.js
node scripts/discussion_smoke.mjs
node scripts/browser_smoke.cjs
node scripts/review_smoke.cjs
node scripts/explanation_quality_smoke.cjs
node scripts/update_persistence_smoke.cjs
```

## 자료 및 근거

문제의 원본 정답과 의학 해설 검수 상태는 별도로 표시합니다. 교과서 원문·페이지 이미지는 저장소에 포함하지 않으며, 사이트에는 자체 작성한 해설과 출처 정보만 게시합니다.
