---
name: web-admin
description: 팀 표준 업무 시스템(관리자 대시보드) 화면 제작·수정. "관리자 화면", "어드민 대시보드", "업무 시스템 UI", "web-admin"으로 요청하거나 사내 업무 시스템의 목록·입력·서랍·대시보드 화면을 만들 때 사용. "다크 모드", "slate 테마", "딥 블루 톤"처럼 테마·색상을 지정한 대시보드 요청에도 사용. 업무 시스템 디자인 시스템(구조) + 교체 가능한 테마(색상 토큰, 라이트/다크)를 frontend-design·web-design-guidelines 스킬 위에 덮어씌워 같은 밀도·위계의 화면을 만든다.
---

# web-admin — 팀 표준 업무 시스템 화면

여러 엔진 스킬을 단계별로 쓰고, 이 스킬의 디자인 시스템을 **규칙**으로 적용하는 오버레이 스킬.

## 파일

| 파일 | 역할 |
| --- | --- |
| `references/DASHBOARD-DESIGN.md` | **구조** — 글꼴·간격·모서리·컴포넌트·레이아웃·화면 패턴·문구·접근성 (colors는 기본 테마 값) |
| `references/THEME-CONTRACT.md` | 테마 규칙 — 필수 토큰, 대비 기준, 라이트/다크 구현, 요청 문구 해석 |
| `references/themes/*.md` | **테마** — 색상 토큰 값 (`admin-navy` 기본, `slate` 딥 블루 다크 등) |
| `references/adapters/shadcn.md` | React·Next.js에서 shadcn/ui 부품 사용 시 테마 대응표 |
| `references/adapters/tailadmin.md` | TailAdmin 부품 이식 시 클래스 치환표·가져올 부품 목록 |
| `scripts/theme-to-css.py` | 테마 파일 → CSS 변수 생성·필수 토큰 검증 (`--plain` 순수 CSS, `--shadcn` shadcn/ui) |

## 엔진

| 단계 | 엔진 스킬 | 쓰는 범위 |
| --- | --- | --- |
| 구현 | `frontend-design` | 구현 품질·마감 요령만 참고 (미적 방향 제안은 쓰지 않음) |
| 점검 | `web-design-guidelines` | 접근성·인터랙션 점검 (설치된 경우) |

엔진 스킬이 없으면 이 문서와 `references/DASHBOARD-DESIGN.md`만으로 진행.

## 규칙 우선순위

1. 사용자의 이번 요청
2. 결과물 저장소의 CLAUDE.md·설계 문서 (스택, 빌드 결과 커밋 여부, 업무 메뉴·상태, 사용 테마)
3. 선택된 `references/themes/{테마}.md` — 색상 값
4. `references/DASHBOARD-DESIGN.md` — 구조와 나머지 토큰
5. 엔진 스킬 기본값 — 색·글꼴·레이아웃·모서리·그림자는 **항상 3·4번을 따름**. frontend-design의 "독특한 미적 방향" 제안은 적용하지 않음

> 요청에 들어온 화면 사양(카드 개수, 그리드 열 수, 들어갈 표·차트)은 1번으로 그대로 반영. 단, `bg-slate-900` 같은 팔레트 클래스는 코드에 쓰지 않고 테마 토큰으로 변환

## 실행 절차

1. **규칙 로드**: `references/DASHBOARD-DESIGN.md`, `references/THEME-CONTRACT.md` 끝까지 읽음
2. **프로젝트 확인**: CLAUDE.md에서 스택(PHP / Python·Java 서버 렌더링 / SPA) 확인 → DASHBOARD-DESIGN.md Implementation 표의 해당 행 적용. 없으면 사용자에게 스택 한 가지만 물음
3. **테마 결정** (`THEME-CONTRACT.md` 5장)
   - 테마 이름 지정 → 해당 파일 / 지정 없음 → 프로젝트 CLAUDE.md의 테마 → 그래도 없으면 `admin-navy`
   - "다크 모드 지원" → `dark` 블록이 있는 테마 사용 + 헤더에 테마 전환 버튼
   - 색 분위기만 설명 → 맞는 기존 테마를 고르고, 없으면 새 테마 파일을 계약 형식대로 작성·대비 측정 후 함께 제출
4. **토대 먼저**
   - 색 변수는 손으로 옮기지 않고 생성: `python3 scripts/theme-to-css.py references/themes/{테마}.md` (shadcn이면 `--shadcn`) → `app.css` 맨 위
   - 이어서 DASHBOARD-DESIGN.md 나머지 토큰(글꼴·간격·모서리·그림자)을 `@theme`에 + `@layer components`
   - 화면 코드에 `dark:` 접두어·팔레트 클래스 금지 — 토큰 유틸리티(`bg-canvas`, `text-fg-muted`)만
   - **부품 출처**
     - React·Next.js 스택: shadcn/ui 사용 가능 → `adapters/shadcn.md` 대응표로 CSS 생성(테마 파일 기준), 버튼 모서리 등 차이 보정
     - 차트·달력·날짜 선택처럼 만들기 번거로운 부품: TailAdmin(MIT)에서 가져올 수 있음 → `adapters/tailadmin.md` 치환표로 팔레트·`dark:` 클래스를 토큰으로 바꾸고, 레이아웃은 가져오지 않음
     - 사용자가 요청에서 "TailAdmin 기반", "shadcn으로"처럼 지정하면 해당 어댑터 적용
   - 토큰에 없는 색·크기는 화면 코드에 쓰지 않음 — 필요하면 사용자에게 토큰 추가 제안
5. **Default Screens 확인**: 로그인·첫 관리자·대시보드·사용자 관리·변경 이력·도움말(이슈·패치노트·API 문서)·내 정보·403/404가 없으면 업무 화면보다 먼저 만듦 (사용자가 범위를 한 화면으로 지정한 경우 제외, 누락 목록만 보고)
6. **업무 화면**: Page Patterns(목록·표 안 수정·서랍·일괄 업로드·대시보드·빈 화면) 중 맞는 패턴으로 작성, 문구는 Writing 규칙(해요체, 버튼은 동사)
7. **상태 확인**: 빈 결과·저장 중·저장 실패(409 포함)·권한 없음·375px 모바일 화면, 다크 테마면 **라이트·다크 두 모드**를 실제로 띄워 확인 (브라우저 도구가 있으면 스크린샷)
8. **점검**: `web-design-guidelines` 스킬이 있으면 실행 + DASHBOARD-DESIGN.md "Accessibility & Review Checklist" 전 항목 확인, 위반 수정
9. **보고**: 만든 화면 목록, 적용 테마·모드, 가져온 외부 부품(출처·라이선스), 새로 만든 테마 파일, 추가·변경한 토큰, 점검 결과(통과/수정), 미확인 상태
