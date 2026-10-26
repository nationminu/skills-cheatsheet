# 설치 없이 사용하기

> 오버레이 스킬(`ppt-report` 등)을 claude.ai에 업로드하지 않고, **레포의 md 파일을 첨부**해서 같은 결과를 얻는 방법
> 스킬 업로드 권한이 없거나, 한 번만 써 보거나, 표준을 고치면서 바로 시험할 때 사용

## 1. 필수 사항

**기본 스킬(엔진)은 반드시 설치·활성화되어 있어야 함** — 첨부 파일은 규칙만 전달하고, 실제 생성은 엔진이 담당

| 쓰려는 것 | 필수 기본 스킬 | 선택 기본 스킬 |
| --- | --- | --- |
| `ppt-proposal` / `ppt-report` / `ppt-briefing` | `ppt-master` | - |
| `web-admin` | - (없으면 Claude 기본 능력으로 진행) | `frontend-design`, `web-design-guidelines` |

- 확인: claude.ai 설정의 Skills 항목에서 활성화 여부 확인
- `ppt-master`가 없으면 Claude가 내장 `pptx` 스킬로 대신 만들 수 있으나, 결과 품질·구조는 표준과 다를 수 있음

## 2. 스킬별 첨부 파일

| 쓰려는 것 | 필수 첨부 | 권장 첨부 | 내용 자료 |
| --- | --- | --- | --- |
| `ppt-proposal` | `shared/ppt/PPT-MASTER.md` | `skills/ppt-proposal/SKILL.md` | 구성 문서, 근거 자료 |
| `ppt-report` | `shared/ppt/PPT-MASTER.md` + `skills/ppt-report/profile.md` | `skills/ppt-report/SKILL.md` | 점검 결과, 로그, 측정값 |
| `ppt-briefing` | `shared/ppt/PPT-MASTER.md` + `skills/ppt-briefing/profile.md` | `skills/ppt-briefing/SKILL.md` | 보고할 내용 |
| `web-admin` | `shared/web/DASHBOARD-DESIGN.md` | `skills/web-admin/SKILL.md`, 테마 지정 시 `THEME-CONTRACT.md` + `themes/{테마}.md` | 화면 요구사항, 설계 문서 |

| 파일 | 역할 | 빠지면 |
| --- | --- | --- |
| `PPT-MASTER.md` / `DASHBOARD-DESIGN.md` | 공통 표준 (디자인·문장·점검표) | 엔진 기본 스타일로 생성 |
| `profile.md` | 용도별 차이 (요약 장, 노트 여부, 장수 등) | 제안서 기준(`PPT-MASTER.md` 기본값)으로 생성 |
| `SKILL.md` | 실행 절차 (스토리라인 먼저, 점검 후 제출 등) | 절차가 생략되거나 순서가 달라질 수 있음 |
| `PPT-OUTLINE-TEMPLATE.md` | 구성 문서 양식 | 구성 문서가 없을 때만 첨부 — Claude가 양식대로 초안 작성 |
| `assets/cover-layout.svg` | 표지 고정 레이아웃 그림 | 표준 6.9 치수만으로 생성 (첨부하면 표지 재현이 더 정확) |

> ⚠️ `profile.md`·`SKILL.md`는 스킬마다 파일명이 같음 → **한 번에 한 스킬 것만 첨부**, 여러 스킬 것을 함께 쓸 때는 받은 파일명을 `ppt-report_profile.md`처럼 바꿔서 첨부

## 3. 요청 문구

### 최소형

```text
ppt-report로 첨부한 점검 결과 보고서를 PPT-MASTER.md를 이용하여 만들어줘
```

- 첨부: `PPT-MASTER.md` + 점검 결과 보고서
- 주의: 스킬이 설치되지 않은 상태에서 `ppt-report`는 **이름일 뿐** → 보고서 프로필(요약 장 필수, 노트 미작성 등)은 적용되지 않고 `PPT-MASTER.md` 기본값(제안서 기준)으로 생성

### 권장형 (설치한 것과 같은 결과)

```text
첨부한 SKILL.md 절차와 profile.md, PPT-MASTER.md 표준에 따라
ppt-master 스킬로 첨부한 점검 결과 보고서를 PPT로 만들어줘.
규칙 우선순위: 이번 요청 > profile.md > PPT-MASTER.md > ppt-master 기본값
```

- 첨부: `skills/ppt-report/SKILL.md` + `skills/ppt-report/profile.md` + `PPT-MASTER.md` + 점검 결과 보고서

### 스킬별 예시

| 스킬 | 첨부 | 요청 |
| --- | --- | --- |
| `ppt-proposal` | `PPT-MASTER.md`, 구성 문서 | `PPT-MASTER.md 표준에 따라 ppt-master 스킬로 첨부한 구성 문서 내용의 제안서 PPT 만들어줘` |
| `ppt-briefing` | `SKILL.md`, `profile.md`, `PPT-MASTER.md`, 보고 내용 | `첨부한 SKILL.md·profile.md·PPT-MASTER.md 기준으로 ppt-master 스킬로 3장 내부 브리핑 만들어줘` |
| `web-admin` | `SKILL.md`, `DASHBOARD-DESIGN.md`, 요구사항 | `첨부한 SKILL.md 절차와 DASHBOARD-DESIGN.md 디자인 시스템으로 자재 입고 목록 화면 만들어줘` |
| `web-admin` + 테마 | 위 파일 + `THEME-CONTRACT.md`, `slate.md` | `첨부한 SKILL.md 절차, DASHBOARD-DESIGN.md 구조, slate.md 테마로 다크 모드 기본 대시보드 만들어줘` |

## 4. 매번 첨부하지 않으려면

- **claude.ai 프로젝트 사용**: 프로젝트를 하나 만들고 표준·프로필·SKILL.md를 프로젝트 파일로 등록 → 그 프로젝트 안의 대화에서는 첨부 없이 바로 요청
  - 예: 프로젝트 "PPT 보고서" = `PPT-MASTER.md` + `ppt-report/SKILL.md` + `ppt-report/profile.md`
  - 프로젝트 지침에 한 줄 추가: `PPT 요청은 프로젝트 파일의 SKILL.md 절차와 profile.md, PPT-MASTER.md 표준을 따라 ppt-master 스킬로 생성`
- 계속 쓰게 되면 오버레이 스킬 설치로 전환 ([README 설치](../README.md#설치-claudeai))

## 5. 설치 방식과 비교

| 구분 | 설치 (스킬 업로드) | 설치 없이 (파일 첨부) |
| --- | --- | --- |
| 준비 | `scripts/build.sh` → zip 업로드 | 레포에서 md 파일 내려받기 |
| 요청 | 스킬 이름만 (`ppt-report로 …`) | 파일 첨부 + 파일 이름 언급 |
| 자동 호출 | 요청 문구로 자동 선택 | 안 됨 (첨부해야 적용) |
| 표준 수정 반영 | 다시 빌드·업로드 | 새 파일 첨부하면 즉시 |
| 적합한 경우 | 팀 상시 사용 | 시험, 일회성, 업로드 권한 없음 |
