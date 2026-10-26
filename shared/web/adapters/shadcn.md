# 어댑터: shadcn/ui

> React·Next.js 프로젝트에서 **shadcn/ui 컴포넌트**를 쓸 때 우리 테마(`themes/*.md`)를 그대로 입히는 대응표
> shadcn/ui도 테마를 CSS 변수(`--background`, `--primary` …)로 두고 `.dark`에서 값만 바꾸는 방식 → 우리 `THEME-CONTRACT.md`와 같은 원리, 대응표만으로 연결

## 1. 생성

```bash
python3 scripts/theme-to-css.py shared/web/themes/slate.md --shadcn > src/app/globals.css
```

- 출력: `:root`(라이트) + `.dark, [data-theme="dark"]`(다크) + `@theme inline` 연결 + `@custom-variant dark`
- shadcn 변수와 우리 토큰(`bg-canvas`, `text-fg-muted`, `bg-success-tint` 등)을 **둘 다** 쓸 수 있게 생성
- 테마의 `default-mode: dark`면 `<html class="dark">`로 시작
- 생성 파일은 직접 고치지 않음 — 색을 바꿀 때는 테마 파일 수정 후 다시 생성

## 2. 대응표

| shadcn 변수 | 우리 토큰 | 비고 |
| --- | --- | --- |
| `background` / `foreground` | `canvas` / `fg` | 앱 바탕 |
| `card` / `card-foreground` | `surface` / `fg` | |
| `popover` / `popover-foreground` | `surface` / `fg` | 드롭다운·달력 (그림자 2단계) |
| `primary` / `primary-foreground` | `primary` / `surface` | 버튼 글자 = `surface` (계약 2장 대비 조건) |
| `secondary` / `secondary-foreground` | `surface-muted` / `fg` | 보조 버튼 면 |
| `muted` / `muted-foreground` | `surface-muted` / `fg-muted` | 표 머리행, 설명 글자 |
| `accent` / `accent-foreground` | `surface-muted` / `fg` | 메뉴 항목 마우스 오버 |
| `destructive` / `destructive-foreground` | `danger` / `surface` | |
| `border` / `input` / `ring` | `line` / `line-strong` / `focus` | 입력 테두리는 3:1 이상인 `line-strong` |
| `chart-1` ~ `chart-4` | 테마 `chart-order` 순서 | 기본: `primary` → `chart-pending` → `success` → `danger` |
| `chart-5` | `fg-muted` | 기타·비교값 |
| `sidebar` / `sidebar-foreground` | `nav` / `nav-fg` | |
| `sidebar-primary` / `sidebar-primary-foreground` | `nav-accent` / `nav` | 로고 칩·현재 표시 |
| `sidebar-accent` / `sidebar-accent-foreground` | `nav-active` / `nav-fg` | 현재 메뉴 면 |
| `sidebar-border` / `sidebar-ring` | `nav-raised` / `nav-accent` | |
| `radius` | `0.625rem` (10 px) | `rounded-lg` = 카드 10 px, `rounded-sm` = 6 px |

## 3. 차이 보정

| 항목 | shadcn 기본 | 우리 표준 | 처리 |
| --- | --- | --- | --- |
| 상태색 | `destructive` 하나 | `success`·`warning`·`danger` + `*-tint` | `--shadcn` 출력이 우리 토큰도 함께 정의(`--t-*` → `--color-*`) → 배지·알림은 `bg-success-tint text-success`처럼 사용 |
| 버튼 모서리 | `rounded-md` (8 px) | `control` 6 px | `components/ui/button.tsx`의 `rounded-md` → `rounded-sm` |
| 버튼 높이 | `h-9` (36 px) | `control` 36 px | 그대로 |
| 표 행 높이 | 컴포넌트 기본 | 44 px | `TableRow`에 `h-11` |
| 글꼴 | Geist 등 | Pretendard Variable | `layout.tsx` 글꼴 교체, 파일 내장 |
| 아이콘 | lucide-react | Lucide | 그대로 (선 굵기 1.75, 16/18/20 px) |
| `dark:` 클래스 | 일부 컴포넌트에 포함 | 화면 코드에서 금지 | 컴포넌트 내부(`components/ui/*`)의 것은 허용, 우리가 쓰는 화면 코드에는 추가 금지 |

## 4. 적용 범위

- React·Next.js 프로젝트에서만 사용 — 서버 렌더링(PHP·Java·Python) 프로젝트는 `DASHBOARD-DESIGN.md` 컴포넌트 클래스 그대로
- 레이아웃·화면 패턴·문구·기본 화면은 `DASHBOARD-DESIGN.md` 기준, shadcn은 **부품**만 제공
