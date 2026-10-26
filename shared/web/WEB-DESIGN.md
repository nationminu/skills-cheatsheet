---
# gstack: design-md-format=spec
name: 업무 시스템 관리자 디자인 시스템
description: 국내 업무 시스템(관리자 대시보드)용 디자인 시스템 — Tailwind CSS v4 토큰 + Lucide 아이콘
colors:
  canvas: "#F3F5F8"
  surface: "#FFFFFF"
  surface-muted: "#F7F9FB"
  line: "#E3E8EF"
  line-strong: "#7B8797"
  fg: "#152033"
  fg-muted: "#4A5568"
  fg-subtle: "#8792A2"
  primary: "#1D5BD6"
  primary-hover: "#174BB3"
  primary-tint: "#EAF1FD"
  success: "#13794A"
  success-tint: "#E6F4EC"
  warning: "#8F5300"
  warning-tint: "#FDF2DF"
  chart-pending: "#C98A2E"
  danger: "#C0281B"
  danger-hover: "#9E2015"
  danger-tint: "#FDECEA"
  focus: "#1D5BD6"
  nav: "#0F2236"
  nav-raised: "#16304A"
  nav-active: "#1C3A5A"
  nav-fg: "#C3CFDD"
  nav-muted: "#8DA0B6"
  nav-accent: "#7FB0FF"
typography:
  display:
    fontFamily: "Pretendard Variable"
    fontSize: 22px
    fontWeight: 700
    lineHeight: 1.35
    letterSpacing: -0.01em
  title:
    fontFamily: "Pretendard Variable"
    fontSize: 18px
    fontWeight: 600
    lineHeight: 1.4
  heading:
    fontFamily: "Pretendard Variable"
    fontSize: 15px
    fontWeight: 600
    lineHeight: 1.5
  body:
    fontFamily: "Pretendard Variable"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.6
  table:
    fontFamily: "Pretendard Variable"
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.45
  caption:
    fontFamily: "Pretendard Variable"
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.45
  figure:
    fontFamily: "Pretendard Variable"
    fontSize: 28px
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: -0.02em
  hero:
    fontFamily: "Pretendard Variable"
    fontSize: 34px
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: -0.02em
rounded:
  control: 6px
  card: 10px
  modal: 12px
  pill: 9999px
spacing:
  "1": 4px
  "2": 8px
  "3": 12px
  "4": 16px
  "5": 20px
  "6": 24px
  "8": 32px
  "10": 40px
  control: 36px
  control-sm: 30px
  control-lg: 42px
  row: 44px
  topbar: 56px
  sidebar: 248px
  sidebar-collapsed: 68px
  drawer: 480px
  modal: 440px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    rounded: "{rounded.control}"
    height: "{spacing.control}"
    padding: 0 14px
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.fg}"
    borderColor: "{colors.line-strong}"
    rounded: "{rounded.control}"
    height: "{spacing.control}"
    padding: 0 14px
  button-danger:
    backgroundColor: "{colors.danger}"
    textColor: "{colors.surface}"
    rounded: "{rounded.control}"
    height: "{spacing.control}"
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.fg}"
    borderColor: "{colors.line-strong}"
    rounded: "{rounded.control}"
    height: "{spacing.control}"
    padding: 0 12px
  card:
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.line}"
    rounded: "{rounded.card}"
  table-row:
    height: "{spacing.row}"
    padding: 0 14px
    borderColor: "{colors.line}"
  badge:
    rounded: "{rounded.pill}"
    height: 22px
    padding: 0 10px
  sidebar:
    backgroundColor: "{colors.nav}"
    textColor: "{colors.nav-fg}"
    width: "{spacing.sidebar}"
---

# 업무 시스템 관리자 디자인 시스템

관리자 대시보드(업무 시스템) 화면을 만들거나 고칠 때 이 문서를 기준으로 삼는다.
토큰(위 YAML)이 값의 원본이고, 구현은 **Tailwind CSS v4의 `@theme`** 로 그대로 옮긴다. 본문은 그 값을 왜, 어떻게 쓰는지 설명한다.
업무별 상태·메뉴·지표는 각 프로젝트 설계 문서에 둔다 (이 문서는 공통 규칙만 담는다).

## Overview

**대상**: 회사 안에서 매일 데이터를 입력·조회·승인하는 실무자와 관리자.
**목표 인상**: "믿고 맡길 수 있는 사내 시스템". 정돈된 정보 위계, 일관된 컴포넌트, 빠른 입력, 상태가 한눈에 보이는 화면.

원칙:
1. **위계가 먼저 보인다.** 모든 화면은 `경로(breadcrumb) → 페이지 제목·설명·주 행동 → 카드(제목 + 내용)` 순서를 지킨다. 카드 머리에는 아이콘과 제목, 필요하면 건수 배지를 둔다.
2. **크롬은 어둡게, 작업 영역은 밝게.** 사이드바는 짙은 남색(`nav`)으로 고정하고, 본문은 밝은 회청색 바탕(`canvas`) 위 흰 카드로 구성한다. 사용자의 눈은 흰 카드(작업 영역)에 머문다.
3. **파랑은 행동, 상태색은 신호.** `primary`(파랑)는 버튼·링크·선택 상태에만 쓴다. 초록·주황·빨강은 상태(완료·대기·위험)를 알릴 때만 쓰고 항상 글자·아이콘을 함께 붙인다.
4. **아이콘은 의미를 돕는다.** 메뉴·카드 제목·버튼·상태에 Lucide 선형 아이콘을 일관된 크기로 쓴다. 아이콘만으로 뜻을 전달하지 않는다(버튼에는 글자 또는 `aria-label`).
5. **촘촘하되 숨 쉬게.** 표 행 44px, 컨트롤 36px, 카드 안쪽 20px. 구분은 여백보다 선(`line`)과 정렬로 한다.
6. **기본 구성은 처음부터 갖춘다.** 로그인·사용자 관리·변경 이력·도움말(이슈·패치노트·API 문서)은 업무 화면보다 먼저 만드는 뼈대다. 아래 "Default Screens"를 모든 프로젝트에 그대로 넣는다.

품질 기준: 참고 구현은 andiskorea(`projects/andiskorea`)다. 새 프로젝트는 그 화면과 같은 밀도·위계·완성도(빈 화면, 오류, 저장 중 상태, 모바일까지)를 첫 버전부터 갖춘다.

피하는 것: 장식용 그라데이션, 카드마다 다른 모서리·그림자, 영문 대문자 라벨, 색만으로 구분한 상태, 이모지 아이콘.

## Colors

| 토큰 | 값 | 용도 |
|---|---|---|
| `canvas` | #F3F5F8 | 앱 바탕 |
| `surface` | #FFFFFF | 카드·표·입력·서랍 |
| `surface-muted` | #F7F9FB | 표 머리행, 서랍 바닥, 보조 면 |
| `line` | #E3E8EF | 카드 테두리, 표 구분선 |
| `line-strong` | #7B8797 | 입력·보조 버튼 테두리 (UI 요소 대비 3:1 이상) |
| `fg` | #152033 | 본문·제목 |
| `fg-muted` | #4A5568 | 보조 글자, 설명, 표 머리행 |
| `fg-subtle` | #8792A2 | 비활성·장식 전용 (읽어야 하는 글자에는 쓰지 않는다, 3.2:1) |
| `primary` | #1D5BD6 | 주 버튼, 링크, 선택된 탭·페이지, 포커스 링 |
| `success` | #13794A | 완료·정상 상태 |
| `warning` | #8F5300 | 대기·확인 필요 |
| `chart-pending` | #C98A2E | 차트 막대·선 전용 "대기" 색. `warning`(#8F5300)은 글자색이라 `danger`와 나란히 칠하면 색약·정상 시력 모두 구분이 안 된다 (검사 결과 아래) |
| `danger` | #C0281B | 위험·삭제·오류 (프로젝트 요구로 다른 의미에 쓰면 반드시 글자 표시를 함께 붙인다) |
| `nav*` | #0F2236 계열 | 사이드바 전용 (본문에는 쓰지 않는다) |

`*-tint`는 같은 계열의 연한 배경(배지·알림·아이콘 칩), `*-hover`는 버튼 마우스 오버 상태다.

대비(측정값): `fg` 16.3:1, `fg-muted` 7.5:1, `primary` 6.0:1, 상태색 글자/연한 배경 4.8~5.6:1, 사이드바 글자 10.2:1, 사이드바 보조 글자 6.0:1. 본문 4.5:1, UI 요소 3:1 기준을 모두 넘는다.

규칙:
- 화면당 `primary`로 채운 버튼은 하나(그 화면의 주 행동). 나머지는 보조·고스트 버튼.
- 지표 카드의 아이콘 칩은 의미에 맞는 `*-tint` 배경 + 같은 계열 글자색.
- 차트 색은 `primary` → `chart-pending` → `success` → `danger` 순으로 쓴다. 계열이 더 필요하면 이 문서에 먼저 추가한다.
  - 근거(색약 검사, OKLab ΔE): 예전 순서(`primary`→`success`→`warning`→`danger`)는 `warning`↔`danger`가 적록 색약 3.2·정상 11.8로 **불합격**. 새 순서는 모든 이웃이 정상 15 이상이고, `success`↔`danger` 적록 색약 7.7은 하한 구간이라 막대 사이 2px 틈·범례·값 표시를 반드시 함께 둔다.
  - `chart-pending`은 배경 대비 2.86:1(3:1 미만)이라 범례와 값 표시(또는 표로 보기)를 함께 둔다.
  - 상태(대기·완료)를 칠할 때도 같은 규칙: 대기 `chart-pending`, 완료는 프로젝트가 정한 상태색, 둘 다 글자(범례·툴팁)를 붙인다.

## Typography

**글꼴: Pretendard Variable 하나.** 한글 업무 화면에서 가장 널리 쓰이고 고정폭 숫자(tnum)를 지원한다. 글꼴 파일은 프로젝트에 포함한다(CDN 의존 금지).

| 토큰 | 크기/굵기 | 용도 |
|---|---|---|
| `display` | 22 / 700 | 페이지 제목 (`h1`, 화면당 하나) |
| `title` | 18 / 600 | 서랍·모달 제목 |
| `heading` | 15 / 600 | 카드 제목 |
| `body` | 14 / 400 | 본문, 입력, 버튼 |
| `table` | 13 / 400 | 표 셀, 라벨, 보조 설명 |
| `caption` | 12 / 500 | 표 머리행, 힌트, 배지 |
| `figure` | 28 / 700 | 지표 숫자 |
| `hero` | 34 / 700 | 로그인 화면 왼쪽 패널의 시스템 이름 (다른 화면에서는 쓰지 않음) |

규칙:
- 숫자(금액·수량·날짜·건수)는 `tabular-nums`, 표에서는 오른쪽 정렬.
- 날짜·숫자 형식은 직접 만들지 않고 언어의 표준 로캘 기능(`Intl` 등, Implementation의 스택별 표 참고)으로 만든다. 날짜 입력값은 `YYYY-MM-DD`.
- 강조는 600, 700은 페이지 제목과 지표 숫자에만.
- 줄임표는 `…`, 로딩 문구는 `저장 중…`.

## Layout

```
┌──────────────┬───────────────────────────────────────────────────────────┐
│ ▣ 시스템명     │ ≡  홈 › 업무 메뉴              📅 2026. 10. 22. (목) | ⓐ 이름  ⏻ │ 상단바 56px
│   부제        ├───────────────────────────────────────────────────────────┤
│ 업무          │ 페이지 제목                                   [보조] [주 행동] │
│ ▦ 대시보드     │ 한 줄 설명                                                  │
│ ▤ 업무 메뉴    │ ┌ 지표 카드 ┐┌ 지표 카드 ┐┌ 지표 카드 ┐┌ 지표 카드 ┐              │
│ 관리          │ └──────────┘└──────────┘└──────────┘└──────────┘              │
│ ☺ 사용자 관리  │ ┌ ⌸ 카드 제목  [12건]                 [상태 탭: 전체|대기|완료] ┐│
│ ◷ 변경 이력    │ │ [🔍 검색…                     ] [검색]                      ││
│              │ │ 표 (머리행 고정, 첫 열 왼쪽 고정, 입력·동작 열 오른쪽 고정)        ││
│ 도움말        │ │ 25건 중 1–25                                    ‹ 1 2 3 › ││
│ ▤ 패치노트     │ └───────────────────────────────────────────────────────────┘│
│ </> API 문서   │                                                             │
└──────────────┴───────────────────────────────────────────────────────────┘
  248px 남색 (1024~1279px: 68px 아이콘만, ~1023px: 서랍)
```

- **사이드바**: 맨 위 시스템 로고 칩(`primary` 정사각형 + 흰 아이콘) + 이름·부제. 메뉴는 `업무 / 관리 / 도움말` 묶음이다. 현재 메뉴는 `nav-active` 면 + 왼쪽 3px `nav-accent` 막대 + 아이콘 강조.
  - `업무`: 대시보드(홈) + 프로젝트 업무 메뉴.
  - `관리`(관리자에게만 보임): 사용자 관리, 변경 이력.
  - `도움말`(**모든 프로젝트 기본 포함**, 사이드바 맨 아래 고정): 이슈(처리 대기 건수 배지) → 패치노트 → API 문서. 새 탭이 아니라 대시보드 레이아웃 안에서 연다(Swagger 같은 외부 도구 화면도 레이아웃 안에 넣는다).
- **상단바**: 흰 바탕 + 아래 선. 왼쪽 경로(breadcrumb), 오른쪽 오늘 날짜·사용자(아바타 이니셜 + 이름 + 권한)·로그아웃 아이콘 버튼.
- **본문**: 넓은 모니터에서도 **폭 100%, 왼쪽 정렬**(최대 폭 제한·가운데 정렬 없음 — 표를 최대한 넓게 본다). 바깥 여백 24px(모바일 16px), 카드 사이 20px.
- **페이지 머리**: 제목(`display`) + 설명(`fg-muted`) 왼쪽, 보조·주 행동 버튼 오른쪽(주 행동이 가장 오른쪽).
- **지표 카드**: 라벨 + 오른쪽 아이콘 칩 / 큰 숫자 + 단위 / 아래 이동 안내. 카드 전체가 해당 목록으로 가는 링크.
- **입력 폼 카드**: 넓은 화면 5열, 태블릿 2열, 모바일 1열. 아래 선 위에 "필수 표시 안내"는 왼쪽, 주 버튼은 오른쪽.
- **목록 카드**: 머리(제목·건수·상태 탭) → 검색 줄 → 표 → 바닥(건수 범위·페이지).

반응형: 1280px 이상 기본, 1024~1279px 사이드바 아이콘만, 1023px 이하 사이드바는 메뉴 버튼으로 여는 서랍, 767px 이하 폼 1열·표 가로 스크롤(페이지 전체는 넘치지 않음).

## Default Screens

모든 프로젝트가 업무 화면과 별개로 기본으로 갖추는 화면이다. 이름·순서·아이콘(Lucide)을 바꾸지 않는다.

| 묶음 | 화면 | 아이콘 | 핵심 |
|---|---|---|---|
| (레이아웃 밖) | 로그인 | `lock` | 가운데 폼 1개(최대 폭 380px), 위에 로고 칩 + 시스템 이름. ID·비밀번호 칸은 왼쪽 아이콘이 있는 큰 입력(`control-lg`). 실패 이유는 "ID 또는 비밀번호가 맞지 않아요" 하나로만 알린다 |
| (레이아웃 밖) | 첫 관리자 만들기 | `shield-check` | 사용자가 한 명도 없을 때만 열리는 로그인과 같은 틀 |
| 업무 | 대시보드 | `layout-dashboard` | 지표 카드 4개(각각 해당 목록 링크) → 최근 항목 표 카드 |
| 관리 | 사용자 관리 | `users` | 목록 카드 + 오른쪽 서랍(추가·수정·비밀번호 초기화). 권한·사용 여부는 배지 |
| 관리 | 변경 이력 | `history` | 데이터 변경(등록·수정·삭제)과 활동(로그인·로그인 실패·로그아웃·다운로드·초기 설정)을 한 표에서 본다. 조회 조건: 대상·사용자·동작·항목·기간. 머리 오른쪽에 `segmented` 빠른 조회(전체 / 활동만 / 로그인 실패) |
| 도움말 | 이슈 | `message-square-warning` | 버그 제보·기능 요청. 상태 `segmented`(전체·접수·진행 중·완료·거절 + 건수). 등록은 서랍, 이미지 끌어 놓기·Ctrl+V 붙여 넣기. 상세는 본문 + 첨부 + 관리자 답변 + 처리 이력(`timeline`) |
| 도움말 | 패치노트 | `scroll-text` | 날짜별 아코디온(`<details>`). 최신 날짜만 펼치고, 접힌 날짜는 항목 제목만 보인다 |
| 도움말 | API 문서 | `code-xml` | 레이아웃 안에 Swagger UI. 명세 파일 내려받기 버튼 |
| 상단바 | 내 정보 | 아바타 | 이름·이메일·비밀번호 변경 |
| (오류) | 403 / 404 | `lock` / `search-x` | 빈 화면 패턴 + "대시보드로 이동" 버튼 |

상태 배지 매핑 (프로젝트가 바꾸지 않는다):

| 대상 | 값 → 배지 |
|---|---|
| 이슈 상태 | 접수 `warning` · 진행 중 `primary` · 완료 `success` · 거절 `neutral` |
| 이슈 유형 | 아이콘 칩: 버그 제보 `bug` + `danger-tint` · 기능 요청 `lightbulb` + `primary-tint` |
| 이력 동작 | 등록 `success` · 수정 `primary` · 삭제 `danger` · 로그인/로그아웃 `neutral` · 로그인 실패 `danger` · 다운로드 `primary` · 초기 설정 `warning` |
| 사용자 | 권한: 관리자 `primary` · 일반 `neutral` · 게스트(읽기 전용) `warning` / 상태: 사용 중 `success` · 비활성 `neutral` |

## Page Patterns

**목록 화면** (업무 화면의 기본형)

```
페이지 제목 + 설명                               [양식 받기] [올리기] [내려받기] [＋ 추가]
┌ ⌕ 조회 조건 ─────────────────────────────── [↺ 조건 초기화] ┐   ← 조건이 있을 때만 초기화 표시
│ [대상 ▾] [사용자 ▾] [동작 ▾] [항목 ▾] [시작일 📅] [종료일 📅] [조회] │   ← xl 6열+버튼, lg 3열, sm 2열, 모바일 1열
└─────────────────────────────────────────────────────────────┘
┌ ▤ 목록 [128건]                            [전체 | 대기 | 완료] ┐
│ 표 …                                                         │
│ 128건 중 1–25                                    ‹ 1 2 3 › │
└─────────────────────────────────────────────────────────────┘
```

- 조회 조건·탭·페이지는 모두 GET 쿼리(새로 고침·링크 공유해도 같은 화면).
- 표 머리행 고정, 표 영역 최대 높이 `calc(100vh - 180px)`, 긴 글은 `cell-text`로 한 줄 줄임 + `title`에 전체 값.
- 결과가 없으면 `table-empty`: "조건에 맞는 ○○이 없어요." + 가능하면 조건 초기화 링크.

**표 안 바로 수정** (한 칸만 고치는 업무)

- 고칠 수 있는 칸만 입력칸으로 보이고 `sticky-right`로 고정한다. 바뀌면 바로 저장, 저장 중에는 `cell-saving`(흐리게) + 입력 잠금.
- 성공은 토스트 "저장했어요", 다른 사람이 먼저 바꿨으면(409) 최신 값으로 되돌리고 오류 토스트로 알린다.
- 완료 같은 행 상태는 행 전체 색 + 글자 배지를 함께 쓴다(색만 쓰지 않는다).

**서랍** (추가·상세·수정)

- 머리(제목 + 닫기) / 본문(스크롤) / 바닥(보조 버튼 왼쪽, 주 버튼 오른쪽) 3단. 상세 서랍 아래에는 해당 항목의 변경 이력 `timeline`.
- 저장 버튼은 누르면 "저장 중…"으로 바뀌고 잠긴다. 검증 오류는 칸 아래 `field-error`, 첫 오류 칸으로 포커스.

**일괄 업로드·다운로드**

- 순서: 양식 받기(보조) → 올리기(보조, 파일 선택 모달) → 내려받기(보조, 현재 조회 조건 그대로) → 추가(주).
- 업로드 결과는 페이지 위 `alert`: "N건 등록, M줄 건너뜀(이유)". 실패 시 한 건도 넣지 않는다고 알린다.
- 다운로드·업로드는 변경 이력의 활동으로 남긴다.

**대시보드**

- 지표 카드는 업무 상태별 건수(예: 전체·대기·완료·최근 7일 변경). 각 카드는 해당 목록의 필터가 걸린 주소로 간다.
- 아래에 "최근 항목" 카드 하나. 차트는 실제로 판단에 쓰일 때만 넣는다.

**빈 화면·오류 화면**

- 원형 아이콘 칩(`*-tint`) + 굵은 한 줄 + 설명 한 줄 + 행동 버튼 하나. 사과하지 않고 다음 행동을 알려 준다.

## Elevation & Depth

| 단계 | 대상 | 그림자 |
|---|---|---|
| 0 | 바탕, 표 | 없음 |
| 1 | 카드, 선택된 탭 | `shadow-card`: `0 1px 2px rgb(16 24 40/.05), 0 1px 3px rgb(16 24 40/.06)` |
| 2 | 지표 카드 마우스 오버, 드롭다운, 달력 | `shadow-pop`: `0 6px 16px rgb(16 24 40/.12), 0 2px 4px rgb(16 24 40/.06)` |
| 3 | 서랍, 모달, 토스트 | `shadow-overlay`: `0 20px 40px rgb(16 24 40/.18)` + 뒤 화면 `nav` 40% 덮개 |

## Shapes

| 토큰 | 값 | 대상 |
|---|---|---|
| `control` | 6px | 버튼, 입력, 탭, 페이지 번호 |
| `card` | 10px | 카드, 알림, 토스트 |
| `modal` | 12px | 모달 |
| `pill` | 9999px | 배지, 아바타 |

아이콘: **Lucide** (선형, ISC 라이선스). 쓰는 아이콘만 프로젝트에 포함하고 SVG를 HTML 안에 인라인으로 렌더링한다(아이콘 폰트·CDN 금지, 스택별 방법은 Implementation 참고). 선 굵기 1.75, 크기 16px(버튼·표·입력), 18px(메뉴·카드 제목·지표 칩), 20px(서랍 닫기·모바일 메뉴). 장식 아이콘은 `aria-hidden`.

## Components

Tailwind `@layer components`에 정의하고 화면에서는 클래스 이름으로 쓴다.

| 클래스 | 설명 |
|---|---|
| `btn` / `btn-primary` / `btn-danger` / `btn-ghost` / `btn-link` | 버튼. 높이 36px(`btn-sm` 30, `btn-lg` 42), 아이콘 + 글자. 아이콘만 있는 `btn-icon`은 `aria-label` 필수 |
| `input`, `input-with-icon` | 입력. 포커스 시 `primary` 테두리 + 3px 연한 링. 검색칸은 왼쪽 돋보기 아이콘 |
| `field` / `label` / `hint` / `field-error` | 라벨은 항상 보이고 입력 위에. 오류는 아이콘 + 문구를 칸 바로 아래 |
| `date-input` | 직접 입력 + 달력 버튼(flatpickr). 형식 `YYYY-MM-DD` |
| `card` / `card-header` / `card-title` / `card-body` / `card-footer` | 모든 내용 묶음의 기본 틀 |
| `kpi` | 지표 카드 (아이콘 칩·큰 숫자·이동 안내) |
| `segmented` | 상태 탭 (전체/대기/완료 + 건수). 선택은 흰 면 + 그림자 1단계 |
| `table` / `sticky-col` / `sticky-right` | 표. 머리행 고정, 첫 열 왼쪽 고정, 자주 쓰는 입력·동작 열 오른쪽 고정 |
| `badge-*` | 점 + 글자 배지 (`neutral` `primary` `success` `warning` `danger`) |
| `alert-*` | 아이콘 + 문구 알림 (`success` `danger` `info`) |
| `drawer` / `modal` / `scrim` | 상세·수정은 오른쪽 서랍(480px), 되돌릴 수 없는 행동 확인은 모달(440px) |
| `timeline` | 변경 이력 (점 색: 등록 초록, 수정 파랑, 삭제 빨강) |
| `avatar` | 이름 첫 글자 원형 |
| `toast` | 오른쪽 아래. 알림은 4초 뒤 사라지고 오류는 닫을 때까지 유지 |
| `app-shell` / `sidebar` / `sidebar-brand` / `sidebar-section` / `nav-link` / `topbar` / `breadcrumb` / `menu-button` | 레이아웃 틀. `nav-link`에는 건수 배지를 붙일 수 있다 |
| `page` / `page-header` / `page-title` / `page-desc` | 본문 머리 |
| `table-wrap` / `table-empty` / `cell-text` / `cell-text-wide` / `cell-saving` / `pager` | 표 보조: 스크롤 틀, 빈 결과, 한 줄 줄임, 저장 중, 페이지 이동 |
| `kpi-head` / `kpi-label` / `kpi-icon` / `kpi-value` / `kpi-unit` / `kpi-foot` | 지표 카드 부품 |
| `drawer-header` / `drawer-title` / `drawer-body` / `drawer-footer` | 서랍 3단 |
| `timeline-item` / `timeline-dot`(`is-create` `is-update` `is-delete`) / `timeline-meta` / `timeline-body` / `change-old` | 이력. 이전 값은 취소선 |
| `prose-notes` | 패치노트·이슈 본문 같은 긴 글 (최대 46em) |
| `skip-link` | 본문 바로가기 |

빈 화면: 원형 아이콘 칩 + 굵은 한 줄 + 할 수 있는 행동 버튼.

## Do's and Don'ts

**하기**
- 모든 화면에 경로 → 제목·설명·주 행동 → 카드 순서.
- 카드 제목에는 아이콘, 목록 카드에는 건수 배지.
- 상태는 배지(점 + 글자)로, 색과 글자를 함께.
- 숫자는 tabular-nums·오른쪽 정렬, 날짜·숫자는 `Intl` 형식.
- 필터·탭·페이지는 URL 쿼리에 남긴다.
- 모든 상호작용 요소에 보이는 포커스 링.

**하지 않기**
- 토큰에 없는 색·크기를 화면에서 바로 쓰기 (필요하면 이 문서와 `@theme`에 먼저 추가).
- 아이콘 폰트·외부 CDN, 이모지 아이콘.
- 색만으로 상태 구분, `outline: none`만 쓰고 포커스 대체 없음, `transition: all`.
- `<div onclick>`으로 버튼·링크 흉내.

## Motion

사용자 행동에 답하는 움직임만: 서랍·모달 180ms, 호버 120ms, 곡선 `cubic-bezier(0.2, 0, 0, 1)`. `transform`·`opacity`·색만 움직인다. `prefers-reduced-motion`이면 즉시 바꾼다.

예외: 로그인 화면 왼쪽 패널의 소개는 처음 열 때 한 번, 제목부터 차례로 왼쪽에서 밀려 들어온다(900ms, 항목 사이 140ms, 같은 곡선, `opacity`+`translateX(-40px)`). `prefers-reduced-motion`이면 움직이지 않는다.

## Writing

- 한국어, 짧은 해요체. 메뉴·열 이름은 명사, 버튼은 동사("내역 추가", "변경 내용 저장").
- 페이지 설명은 해요체 없이 명사형 요약("현장별 자재 선발 내역 관리"). 덧붙일 말은 " · "로 잇는다.
- 같은 행동은 끝까지 같은 이름(버튼 "삭제" → 토스트 "삭제했어요").
- 오류는 무엇이 잘못됐고 어떻게 고치는지. 사과·모호한 말 금지.

## Implementation (Tailwind CSS v4)

이 디자인 시스템은 개발 언어·프레임워크와 상관없다. 아래 공통 규칙을 지키면 어떤 스택이든 같은 화면이 나온다.

공통 규칙:
- 원본 CSS 한 파일(예: `app.css`)에 `@import "tailwindcss"` + `@theme`(이 문서의 토큰) + `@layer components`(위 컴포넌트)를 둔다. 토큰·컴포넌트를 화면 코드에 다시 정의하지 않는다.
- 토큰 이름이 곧 유틸리티 이름이다: `bg-canvas`, `text-fg-muted`, `border-line`, `rounded-card`, `shadow-card`, `h-control`, `text-table` 등.
- 클래스 이름을 동적으로 이어 붙이지 않는다(`grid-cols-${n}`, `grid-cols-<?= $n ?>` 금지). 빌드가 찾지 못한다. 완성된 클래스 이름을 조건으로 고른다.
- 배포 후 브라우저가 예전 CSS·JS를 쓰지 않게 한다(파일 이름에 해시, 또는 주소에 `?v=수정 시각`).
- 아이콘은 Lucide SVG를 HTML 안에 인라인으로 렌더링한다(아이콘 폰트·`<img>`·CDN 금지). 쓰는 아이콘만 프로젝트에 포함한다.
- 글꼴 Pretendard Variable 파일은 프로젝트에 포함한다.
- Tailwind CDN(브라우저에서 실행하는 방식)은 쓰지 않는다.

스택별 구현:

| 스택 | CSS 빌드 | 아이콘 | 캐시 무효화 | 날짜·숫자 형식 |
|---|---|---|---|---|
| 서버 렌더링 + 웹호스팅 (PHP: CodeIgniter·Laravel 등) | Tailwind **단독 실행 파일**(Node 불필요)로 빌드하고 결과 CSS를 커밋. 호스팅에서는 빌드하지 않음 | `lucide-static`의 SVG 파일만 복사해 두고 `icon('이름')` 같은 도우미로 인라인 출력 | 도우미가 `?v=파일 수정 시각`을 붙임 | `IntlDateFormatter` / `NumberFormatter` |
| 서버 렌더링 (Python: Django·FastAPI + Jinja, Java: Spring + Thymeleaf 등) | 단독 실행 파일 또는 npm `@tailwindcss/cli`. 배포 단계에서 빌드하면 결과 CSS는 커밋하지 않아도 됨 | 위와 같이 SVG 복사 + 템플릿 도우미(매크로·프래그먼트) | 정적 파일 매니페스트(Django `ManifestStaticFilesStorage` 등) 또는 `?v=` | 서버: 언어 표준 로캘 기능 / 화면: `Intl` |
| SPA·Node 계열 (React·Next.js·Vue·Nuxt·Svelte) | npm `tailwindcss` + `@tailwindcss/vite`(또는 `@tailwindcss/postcss`). 결과 CSS는 커밋하지 않음 | `lucide-react` / `lucide-vue-next` / `lucide-svelte` 컴포넌트(트리 셰이킹으로 쓰는 것만 포함) | 번들러의 파일 이름 해시 | `Intl.DateTimeFormat` / `Intl.NumberFormat` |

프로젝트가 어느 스택인지, 빌드 결과를 커밋하는지는 결과물 저장소의 CLAUDE.md에 적는다.
- Tailwind v4 기본 스타일은 버튼 커서를 `default`로 둔다. 기본 레이어에서 누를 수 있는 요소(`button`, `label[for]`, `select`, 체크박스 등)에 `cursor: pointer`, 비활성 요소에 `cursor: not-allowed`를 지정한다.

## Accessibility & Review Checklist

화면을 만든 뒤 `web-design-guidelines` 스킬과 gstack `/design-review`로 점검한다.

- [ ] 의미에 맞는 HTML, 제목 순서(`h1` 하나), 본문 바로가기 링크.
- [ ] Default Screens가 모두 있고 도움말 묶음(이슈·패치노트·API 문서)이 사이드바 맨 아래에 있다.
- [ ] 빈 결과·저장 중·저장 실패(충돌 포함)·권한 없음 상태를 모두 화면으로 확인했다.
- [ ] 모든 입력에 보이는 라벨, 표 안 입력칸은 `aria-label`.
- [ ] 아이콘만 있는 버튼에 `aria-label`, 장식 아이콘 `aria-hidden`.
- [ ] 서랍·모바일 메뉴가 열리면 뒤 화면 `inert`, 닫으면 연 버튼으로 포커스 복귀.
- [ ] 텍스트 4.5:1, UI 요소 3:1, 상태는 글자로도 구분.
- [ ] 토스트·검증 메시지 `aria-live`, 오류 토스트는 자동으로 사라지지 않음.
- [ ] 375px에서 페이지 전체 가로 넘침 없음, 터치 영역 40px 이상.
- [ ] `prefers-reduced-motion` 지원, 화면 확대를 막지 않음.