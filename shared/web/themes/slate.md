---
name: slate
description: 모던하고 깔끔한 딥 블루(slate) 대시보드 테마 — 다크 모드 기본, 라이트 모드 지원
modes: [light, dark]
default-mode: dark
colors:
  light:
    canvas: "#F8FAFC"
    surface: "#FFFFFF"
    surface-muted: "#F1F5F9"
    line: "#E2E8F0"
    line-strong: "#64748B"
    fg: "#0F172A"
    fg-muted: "#475569"
    fg-subtle: "#94A3B8"
    primary: "#2563EB"
    primary-hover: "#1D4ED8"
    primary-tint: "#EFF6FF"
    focus: "#2563EB"
    success: "#047857"
    success-tint: "#ECFDF5"
    warning: "#B45309"
    warning-tint: "#FFFBEB"
    chart-pending: "#D97706"
    danger: "#B91C1C"
    danger-hover: "#991B1B"
    danger-tint: "#FEF2F2"
    nav: "#0F172A"
    nav-raised: "#16233B"
    nav-active: "#1E293B"
    nav-fg: "#CBD5E1"
    nav-muted: "#94A3B8"
    nav-accent: "#60A5FA"
  dark:
    canvas: "#0F172A"
    surface: "#1E293B"
    surface-muted: "#172236"
    line: "#334155"
    line-strong: "#7C8BA1"
    fg: "#F1F5F9"
    fg-muted: "#A3B1C6"
    fg-subtle: "#64748B"
    primary: "#60A5FA"
    primary-hover: "#93C5FD"
    primary-tint: "#1B3358"
    focus: "#60A5FA"
    success: "#34D399"
    success-tint: "#0F3A31"
    warning: "#FBBF24"
    warning-tint: "#3A2E0D"
    chart-pending: "#F59E0B"
    danger: "#F87171"
    danger-hover: "#FCA5A5"
    danger-tint: "#3F1F25"
    nav: "#020617"
    nav-raised: "#0B1220"
    nav-active: "#1E293B"
    nav-fg: "#CBD5E1"
    nav-muted: "#94A3B8"
    nav-accent: "#60A5FA"
chart-order: [primary, chart-pending, success, danger]
---

# slate 테마

딥 블루(Tailwind slate 계열) 기반의 모던 대시보드 테마. 다크 모드가 기본이고, 헤더 버튼으로 라이트 모드 전환.

- **다크**: 바탕 `canvas` #0F172A(slate-900), 카드 `surface` #1E293B(slate-800), 사이드바 `nav` #020617(slate-950)로 한 단계 더 어둡게 — 크롬은 어둡게, 작업 영역은 한 단계 밝게
- **라이트**: 바탕 slate-50, 흰 카드, 사이드바는 다크와 같은 slate-900 유지 (모드가 바뀌어도 탐색 위치 인지 유지)
- **행동색**: 다크에서는 밝은 파랑 `#60A5FA` + 버튼 글자 `surface`(어두운 색), 라이트에서는 `#2563EB` + 흰 글자
- 구조·크기·컴포넌트는 `WEB-DESIGN.md` 그대로, 이 파일은 색만 담당 (`THEME-CONTRACT.md`)

## 대비 측정 (WCAG 2.x)

| 조합 | 라이트 | 다크 | 기준 |
| --- | --- | --- | --- |
| `fg` / `surface` | 17.85 | 13.35 | 4.5 |
| `fg-muted` / `surface` | 7.58 | 6.73 | 4.5 |
| `fg-muted` / `surface-muted` | 6.92 | 7.33 | 4.5 |
| `primary` / `surface` (링크) | 5.17 | 5.75 | 4.5 |
| `surface` / `primary` (주 버튼 글자) | 5.17 | 5.75 | 4.5 |
| `surface` / `primary-hover` | 6.70 | 8.11 | 4.5 |
| `primary` / `primary-tint` | 4.75 | 4.97 | 4.5 |
| `success` / `success-tint` | 5.21 | 6.54 | 4.5 |
| `warning` / `warning-tint` | 4.84 | 7.98 | 4.5 |
| `danger` / `danger-tint` | 5.91 | 5.29 | 4.5 |
| `surface` / `danger` (위험 버튼 글자) | 6.47 | 5.29 | 4.5 |
| `line-strong` / `surface` (입력 테두리) | 4.76 | 4.22 | 3.0 |
| `chart-pending` / `surface` | 3.19 | 6.81 | 3.0 |
| `nav-fg` / `nav` | 12.02 | 13.59 | 4.5 |
| `nav-muted` / `nav` | 6.96 | 7.87 | 4.5 |

## 차트 색

- 순서: `primary` → `chart-pending` → `success` → `danger`
- 색약 시뮬레이션 검사는 아직 하지 않음 → 범례·값 직접 표시·막대 사이 틈을 반드시 함께 사용 (검사 후 이 항목 갱신)
