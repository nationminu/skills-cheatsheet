# 웹 테마 계약 (Theme Contract)

> 적용 범위: **대시보드 디자인(`DASHBOARD-DESIGN.md`)** 테마 — 사이드바(`nav*`) 등 대시보드 전용 토큰 포함
> 이후 작성할 서비스 프론트 디자인(`FRONT-DESIGN.md`)은 별도 토큰 체계, 공통 토큰을 나눌 경우 이 문서를 개정

> `DASHBOARD-DESIGN.md`는 **구조**(레이아웃·컴포넌트·화면 패턴·문구·접근성), `themes/*.md`는 **색상 값**을 담당
> 테마를 바꿔도 화면 코드는 그대로 — 같은 토큰 이름에 다른 값만 넣는 방식

## 1. 계층

```text
[이번 요청의 화면 사양]   사이드바·헤더·카드 3개·차트·표 …      ← 무엇을 그릴지
[themes/{테마}.md]        colors (light / dark)                 ← 무슨 색으로
[DASHBOARD-DESIGN.md]           typography · spacing · rounded · components · 패턴 · 규칙  ← 어떻게
```

- 테마가 바꾸는 것: `colors` 토큰 값 (모드별), 테마별 차트 색 순서
- 테마가 바꾸지 않는 것: 토큰 **이름**, 글꼴·크기, 간격, 모서리, 컴포넌트 구조, 레이아웃, 문구 규칙
- 모서리·그림자 강도까지 바꾸고 싶으면 테마 파일에 `rounded` / `elevation` 블록 추가 (선택, 같은 키 이름만)

## 2. 필수 토큰

모든 테마는 아래 이름을 **빠짐없이** 정의 (다크 모드 지원 테마는 `light`·`dark` 둘 다)

| 묶음 | 토큰 |
| --- | --- |
| 면 | `canvas` `surface` `surface-muted` |
| 선 | `line` `line-strong` |
| 글자 | `fg` `fg-muted` `fg-subtle` |
| 행동 | `primary` `primary-hover` `primary-tint` `focus` |
| 상태 | `success` `success-tint` `warning` `warning-tint` `danger` `danger-hover` `danger-tint` `chart-pending` |
| 사이드바 | `nav` `nav-raised` `nav-active` `nav-fg` `nav-muted` `nav-accent` |

**주의**: 컴포넌트는 주 버튼·위험 버튼 글자색으로 `surface`를 씀 → `surface`와 `primary`·`danger` 사이 대비 4.5:1 필요 (다크 테마는 밝은 `primary` + 어두운 `surface` 조합)

## 3. 통과 기준 (테마 파일에 측정값 기재)

| 조합 | 기준 |
| --- | --- |
| `fg`·`fg-muted` / `surface`·`surface-muted`·`canvas` | 4.5:1 이상 |
| `primary`·`success`·`warning`·`danger` 글자 / `surface` 및 각자 `*-tint` | 4.5:1 이상 |
| `surface`(버튼 글자) / `primary`·`primary-hover`·`danger` | 4.5:1 이상 |
| `line-strong` / `surface` (입력 테두리) | 3:1 이상 |
| `chart-pending` / `surface` | 3:1 이상 (미달 시 범례·값 표시 필수) |
| `nav-fg`·`nav-muted` / `nav`·`nav-active` | 4.5:1 이상 |
| `fg-subtle` | 장식·비활성 전용, 기준 없음 |

## 4. 구현 (Tailwind CSS v4)

```css
@import "tailwindcss";

/* 기본(light) 값 = 테마 파일 light 블록 */
@theme {
  --color-canvas: #F8FAFC;
  --color-surface: #FFFFFF;
  /* … 필수 토큰 전부 */
}

/* 다크 값 = 테마 파일 dark 블록 — 같은 변수만 다시 정의 */
@layer base {
  [data-theme="dark"] {
    --color-canvas: #0F172A;
    --color-surface: #1E293B;
    /* … */
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --color-canvas: #0F172A;
      /* … 위와 같은 값 */
    }
  }
}
```

- 화면 코드는 `bg-canvas`, `text-fg-muted`처럼 **토큰 유틸리티만** 사용 → 테마·모드 전환 시 코드 수정 없음
- 화면 코드에 `dark:` 접두어, `bg-slate-900` 같은 팔레트 클래스 직접 사용 금지
- 모드 선택: 기본은 OS 설정 따름, 헤더의 테마 버튼으로 `data-theme` 전환, 선택값은 `localStorage`에 저장(읽기·쓰기 실패해도 동작)
- 다크 모드에서는 그림자 대신 `line` 테두리로 면 구분 (그림자는 어두운 바탕에서 보이지 않음)

## 5. 요청 문구 → 테마 해석

| 요청 표현 | 처리 |
| --- | --- |
| `slate 테마로`, `admin-navy 테마로` | 해당 `themes/*.md` 적용 |
| `다크 모드 지원` | 선택 테마의 `dark` 블록 사용 + 테마 전환 버튼 (dark 블록 없는 테마면 새로 정의) |
| `딥 블루(bg-slate-900) 톤` 같은 팔레트 클래스 | 클래스를 코드에 쓰지 않고 **토큰 값으로 변환** (`canvas: #0F172A`) — 기존 테마 중 맞는 것이 있으면 그것을 사용 |
| 새로운 색 분위기 설명 | 새 테마 파일 작성 → 3장 기준 측정 → 결과와 함께 제출 (팀 레포 `shared/web/themes/`에 추가 제안) |

## 6. 새 테마 파일 형식

```yaml
---
name: {테마명}            # 소문자·하이픈
description: {한 줄 분위기}
modes: [light, dark]      # 지원 모드
default-mode: dark        # 첫 화면 모드 (system이면 OS 설정)
colors:
  light: { canvas: "#…", … 필수 토큰 전부 }
  dark:  { canvas: "#…", … 필수 토큰 전부 }
chart-order: [primary, chart-pending, success, danger]
---
```

본문: 분위기·사용처, 대비 측정표(3장 기준), 차트 색 주의사항
