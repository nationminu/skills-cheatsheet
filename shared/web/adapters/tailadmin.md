# 어댑터: TailAdmin (무료 HTML 버전)

> [TailAdmin free Tailwind dashboard template](https://github.com/TailAdmin/tailadmin-free-tailwind-dashboard-template)에서 **부품을 가져올 때** 우리 토큰으로 바꾸는 치환표
> 원칙: TailAdmin은 부품 공급원, 레이아웃·화면 패턴·문구·테마는 `DASHBOARD-DESIGN.md`·`themes/*.md` 기준

## 1. 확인한 사실 (2026-10-26, 무료 HTML 버전 저장소 기준)

| 항목 | 내용 | 우리 표준과의 관계 |
| --- | --- | --- |
| 라이선스 | MIT | 사내·고객 납품 코드에 포함 가능 (저작권 고지 유지) |
| 스택 | HTML + Alpine.js + Tailwind CSS v4 + Webpack | 서버 렌더링 프로젝트에 부품 이식 쉬움 |
| 색 정의 | `@theme`에 `brand-*`·`gray-*`·`success-*`·`error-*`·`warning-*`·`blue-light-*`·`orange-*` 팔레트 | **팔레트 클래스 방식** — 우리 토큰 방식과 다름 |
| 다크 모드 | `@custom-variant dark (&:is(.dark *))` + 화면 코드의 `dark:` 클래스 (HTML 69개 파일에 1,495개) + Alpine `darkMode` 값을 `localStorage`에 저장 | **계약 위반** — 이식 시 `dark:` 전부 제거, 토큰으로 치환 |
| 글꼴 | Outfit | Pretendard Variable로 교체 |
| 주요 라이브러리 | ApexCharts, Flatpickr, FullCalendar, jsVectorMap, Dropzone, Swiper | Flatpickr는 우리 표준과 같음 |

> 버전이 바뀌면 이 표를 다시 확인 — `dark:` 개수 확인: 저장소에서 `grep -ro 'dark:' src --include=*.html | wc -l`

## 2. 가져올 것 / 가져오지 않을 것

| 가져올 것 (부품) | 가져오지 않을 것 (구조) |
| --- | --- |
| 차트 설정 (`src/js/components/charts/`) — 색만 토큰으로 교체 | 전체 레이아웃 (`sidebar.html`·`header.html`) — 흰 사이드바·검색창 구조가 우리와 다름 |
| 달력 (`calendar-init.js`, FullCalendar) | 페이지 머리·카드 배치 — `DASHBOARD-DESIGN.md` Page Patterns 사용 |
| 날짜 선택 (`datepicker.html`, Flatpickr) | 색 팔레트 `@theme` 블록 |
| 드롭다운·모달·알림 등 상호작용 부품의 **동작(Alpine 코드)** | `dark:` 클래스, `darkMode` 토글 방식 |
| 파일 끌어 놓기 (Dropzone) | 영문 문구 — Writing 규칙(해요체)으로 다시 작성 |

## 3. 클래스 치환표

라이트 클래스와 짝이 되는 `dark:` 클래스는 **함께 지우고** 오른쪽 토큰 하나로 바꿈

| TailAdmin (라이트 + 다크 짝) | 우리 토큰 | 용도 |
| --- | --- | --- |
| `bg-gray-50` + `dark:bg-gray-900` (body) | `bg-canvas` | 앱 바탕 |
| `bg-white` + `dark:bg-white/3`·`dark:bg-gray-900` | `bg-surface` | 카드·표·입력 |
| `bg-gray-50`·`bg-gray-100` + `dark:bg-gray-800`·`dark:bg-white/5` | `bg-surface-muted` | 표 머리행, 보조 면 |
| `hover:bg-gray-50`·`hover:bg-gray-100` + `dark:hover:bg-white/3`·`/5` | `hover:bg-surface-muted` | 행·메뉴 마우스 오버 |
| `text-gray-800`·`text-gray-700` + `dark:text-white/90`·`dark:text-white` | `text-fg` | 제목·본문 |
| `text-gray-500` + `dark:text-gray-400` | `text-fg-muted` | 설명·보조 글자 |
| `text-gray-400` | `text-fg-subtle` | 비활성·장식만 (읽는 글자 금지) |
| `border-gray-100`·`border-gray-200` + `dark:border-gray-800` | `border-line` | 카드·표 구분선 |
| `border-gray-300` + `dark:border-gray-700` | `border-line-strong` | 입력·보조 버튼 테두리 |
| `bg-brand-500` + `hover:bg-brand-600`, `text-white` | `bg-primary hover:bg-primary-hover text-surface` | 주 버튼 |
| `text-brand-500` + `dark:text-brand-400` | `text-primary` | 링크·선택 상태 |
| `bg-brand-50` + `dark:bg-brand-500/[0.12]` (`menu-item-active`) | `bg-primary-tint` (본문) / 사이드바는 `bg-nav-active` | 선택 면 |
| `focus:border-brand-300 focus:ring-brand-500/10` + `dark:focus:border-brand-800` | `focus:border-primary focus:ring-3 focus:ring-primary/20` | 입력 포커스 |
| `bg-success-50` + `dark:bg-success-500/15`, `text-success-600` + `dark:text-success-500` | `bg-success-tint text-success` | 완료 배지 |
| `error-*` (같은 패턴) | `danger-tint` / `danger` | 오류·위험 |
| `warning-*` (같은 패턴) | `warning-tint` / `warning` | 대기 |
| `orange-*` (차트) | `chart-pending` | 차트 "대기" 색 |
| `blue-light-*` | `primary` 계열 | 정보 |
| `shadow-theme-xs`·`sm` / `md`·`lg` / `xl` | `shadow-card` / `shadow-pop` / `shadow-overlay` | 그림자 3단계 |
| `rounded-2xl` (카드) / `rounded-lg` (버튼·입력) | `rounded-card` / `rounded-control` | 모서리 |
| `font-outfit` | (삭제 — 기본 글꼴 Pretendard) | |

**치환표에 없는 클래스**: 가장 가까운 토큰으로 바꾸고, 맞는 토큰이 없으면 `DASHBOARD-DESIGN.md`에 토큰 추가를 먼저 제안 (화면 코드에 팔레트 클래스 남기지 않음)

## 4. 다크 모드 토글 바꾸기

```html
<!-- TailAdmin: <body :class="{'dark bg-gray-900': darkMode === true}"> + localStorage 'darkMode' -->
<!-- 우리: <html data-theme="dark|light"> + localStorage 'theme' (THEME-CONTRACT.md 4장) -->
<script>
  try { document.documentElement.dataset.theme = localStorage.getItem('theme') || 'dark'; } catch (e) {}
</script>
```

## 5. 차트 색 (ApexCharts)

ApexCharts는 CSS 클래스가 아니라 JS 설정으로 색을 받음 → 하드코딩된 `#465FFF` 등을 지우고 토큰 값을 읽어서 전달

```js
const css = getComputedStyle(document.documentElement);
const token = (name) => css.getPropertyValue(`--color-${name}`).trim();
const options = {
  colors: ['primary', 'chart-pending', 'success', 'danger'].map(token),  // 테마 chart-order
  grid: { borderColor: token('line') },
  xaxis: { labels: { style: { colors: token('fg-muted') } } },
  yaxis: { labels: { style: { colors: token('fg-muted') } } },
  chart: { fontFamily: 'Pretendard Variable, sans-serif', foreColor: token('fg-muted') },
};
// 테마 전환 시: chart.updateOptions({ colors: … }) 로 다시 읽어서 반영
```

## 6. 점검

- [ ] 이식한 파일에 `dark:`, `brand-`, `gray-`, `success-`, `error-`, `shadow-theme`, `font-outfit` 문자열 없음
- [ ] 차트 설정에 `#` 색 값 하드코딩 없음
- [ ] 영문 UI 문구를 한국어 Writing 규칙으로 교체
- [ ] 라이트·다크 두 모드에서 화면 확인
- [ ] TailAdmin MIT 저작권 고지를 프로젝트 라이선스 목록(예: `THIRD-PARTY-NOTICES`)에 기재
