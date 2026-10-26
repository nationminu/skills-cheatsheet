---
name: admin-navy
description: 기본 테마 — 밝은 회청색 작업 영역 + 짙은 남색 사이드바 (WEB-DESIGN.md 기본값)
modes: [light]
default-mode: light
colors:
  light:
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
chart-order: [primary, chart-pending, success, danger]
---

# admin-navy 테마 (기본)

`WEB-DESIGN.md`의 YAML `colors`와 같은 값. 테마를 지정하지 않으면 이 테마 적용.

- 라이트 모드만 정의 — "다크 모드 지원" 요청 시 `dark` 블록을 `THEME-CONTRACT.md` 기준으로 추가하거나 `slate` 테마 사용
- 대비 측정값·색약 검사 결과는 `WEB-DESIGN.md` Colors 섹션 참고 (차트 순서 근거 포함)
- 값을 바꿀 때는 `WEB-DESIGN.md` YAML과 이 파일을 함께 수정
