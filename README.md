# 2026 생성발2 강의별 CBT

생성발2 족보를 강의별로 풀 수 있도록 만든 공개 학습 사이트입니다.

## 주요 기능

- 출석번호별로 브라우저 풀이 기록 분리
- 강의별 문제 선택, 다시 풀기, 누적 시도·오답 횟수
- 문제·선지는 CBT 형식으로 표시하고 표·사진은 원본 이미지로 연결
- 답 제출 뒤 각 선지 바로 아래에 해당 선지 해설 표시
- 생성발2 및 기존 임추·국시 문제은행의 비슷한 문제 연결
- 문제별 실시간 오류토의
- 2026년 강의에서 보여 준 비출제 예시를 실제 기출과 구분

출석번호는 서버로 전송하지 않습니다. 개인 풀이 기록은 해당 브라우저의 `localStorage`에만 저장되며, 오류토의 글만 모든 사용자에게 공유됩니다.

## 검사

```powershell
python scripts/validate_site.py
node --check site/app.js
node --check functions/api/discussions.js
node scripts/discussion_smoke.mjs
node scripts/browser_smoke.cjs
```

## 자료 및 근거

문제의 원본 정답과 의학 해설 검수 상태는 별도로 표시합니다. 교과서 원문·페이지 이미지는 저장소에 포함하지 않으며, 사이트에는 자체 작성한 해설과 출처 정보만 게시합니다.
