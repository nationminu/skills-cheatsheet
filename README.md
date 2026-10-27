# Skill Presets

> Claude 기본 스킬에 팀 표준을 입혀, **이름만 부르면 같은 품질의 결과가 나오게 하는 프리셋** 모음
> 내부 명칭: 치트시트 (`skills-cheatsheet`)
> **Claude 전용** — claude.ai와 Claude Code에서 같은 프리셋 사용 ([Claude Code 가이드](guides/claude-code.md))

## 빠른 사용표

| 하고 싶은 것 | 프리셋 | 이렇게 요청 | 결과 |
| --- | --- | --- | --- |
| 고객 제안서 덱 | `ppt-proposal` | `ppt-proposal로 첨부한 구성 문서 기준 제안서 만들어줘` | 겸용 PPTX + 발표자 노트, 8~15장 |
| 설치·점검·PoC 결과 보고 | `ppt-report` | `ppt-report로 첨부한 점검 결과 보고서 만들어줘` | 정보 전달용 PPTX, 요약 장 필수 |
| 팀장·임원 내부 보고 | `ppt-briefing` | `ppt-briefing으로 이 내용 3장 브리핑 만들어줘` | 1~5장 PPTX, 첫 장 결론·요청 |
| 업무 시스템 관리자 화면 | `web-admin` | `web-admin으로 자재 입고 목록 화면 만들어줘` | Tailwind v4 토큰 기반 화면 + 기본 화면 + 점검 결과 |
| 테마를 지정한 대시보드 | `web-admin` + 테마 | `web-admin으로 slate 테마, 다크 모드 기본 대시보드 만들어줘` | 같은 구조 + 테마 색상, 라이트/다크 전환 ([예시](examples/web/slate-dashboard.html)) |

- PPT 공통: 결과와 함께 **스토리라인 표**, `[자료 필요]`·`[확인 필요]` 목록, 점검 결과 요약 제출
- 구성 문서가 없으면 스킬이 필수 항목 몇 가지만 묻고 초안부터 작성
- 요청 문구 더 보기: [guides/ppt-master-prompts.md](guides/ppt-master-prompts.md) (스킬명만 바꿔서 사용)
- **설치 없이 쓰기**: 기본 스킬(`ppt-master` 등)만 있으면 md 파일 첨부로 같은 결과 → [guides/no-install.md](guides/no-install.md)

## 웹 테마

- 웹 디자인 표준은 용도별로 분리: `DASHBOARD-DESIGN.md`(관리자·업무 시스템 대시보드) / `FRONT-DESIGN.md`(서비스 프론트, 예정)
- **구조**(`DASHBOARD-DESIGN.md`)와 **색상**(`themes/*.md`) 분리 → 같은 토큰 이름에 값만 교체, 화면 코드는 그대로
- 요청에서 테마 이름을 부르거나(`slate 테마로`), 분위기를 설명하면(`딥 블루 다크 톤`) 맞는 테마 적용, 없으면 새 테마 파일을 계약대로 만들어 함께 제출
- 외부 부품은 어댑터로 연결: [shadcn/ui](shared/web/adapters/shadcn.md) (React·Next.js, 대응표로 테마 그대로 적용) · [TailAdmin](shared/web/adapters/tailadmin.md) (MIT, 차트·달력 등 부품만 가져와 토큰으로 치환)
- 새 테마 추가: `shared/web/themes/{이름}.md` 작성 ([THEME-CONTRACT.md](shared/web/THEME-CONTRACT.md) 6장 형식, 대비 측정표 포함) → `python3 scripts/theme-to-css.py shared/web/themes/{이름}.md`로 검증 → 빌드

| 테마 | 모드 | 분위기 |
| --- | --- | --- |
| `admin-navy` (기본) | 라이트 | 밝은 회청색 작업 영역 + 짙은 남색 사이드바 |
| `slate` | 다크(기본)·라이트 | 딥 블루 slate-900 바탕의 모던 대시보드 |

## 여러 스킬 함께 쓰기

- 프리셋끼리 **동시에 설치·사용 가능** — 요청 문구에 맞는 프리셋을 Claude가 골라 불러 씀
- 한 작업에서 이어 쓰기도 가능: `web-admin으로 화면 만들고, 그 화면 캡처로 ppt-proposal 제안서 3장 추가해줘`
- 하나의 프리셋이 **엔진 여러 개**를 단계별로 사용 가능 (예: `web-admin` = 구현 `frontend-design` + 점검 `web-design-guidelines`)
- 호출이 겹치지 않게 각 `description`에 용도·호출 문구를 분명히 구분

## 동작 방식 (오버레이 구조)

프리셋은 기본 스킬(엔진)을 고치지 않고 **위에 덮어씌우는(오버레이)** 방식 — 엔진은 생성 절차를, 프리셋은 표준·테마·용도별 규칙을 담당

```text
              PPT 계열                                  웹 계열
[프리셋]      ppt-proposal | -report | -briefing          web-admin
              (+ 용도별 profile.md)
[테마]        -                                           shared/web/themes/*.md  ← 색상만, 교체 가능
[공통 표준]   shared/ppt/PPT-MASTER.md                    shared/web/DASHBOARD-DESIGN.md
              shared/diagram/ARCH-DIAGRAM.md (구성도)
[엔진]        ppt-master                                  frontend-design(구현) + web-design-guidelines(점검)

위 계층이 아래 계층을 덮어씀 (같은 항목이면 위가 우선)
```

| 계층 | 담당 | 바뀌는 주기 |
| --- | --- | --- |
| 엔진 | 생성 절차, 도구, 렌더링 | 원본 저장소 업데이트 |
| 공통 표준 | 회사 공통 디자인·문장·사실 원칙 | 팀 합의로 개정 |
| 프로필 (선택) | 같은 표준 안에서 용도별 차이 (청중, 흐름, 장수 등) — 용도가 하나면 생략 | 용도 추가 시 |
| 구성 문서 | 업무별 내용 (고객, 메시지, 장표 구성) | 업무마다 |

**규칙 우선순위**: 이번 요청 > 구성 문서 > 프로필 > 공통 표준 > 엔진 기본값

- 표준을 고치면 → 모든 프리셋에 반영 (다시 빌드·업로드)
- 새 용도가 생기면 → 프로필만 새로 써서 스킬 하나 추가

## 폴더 구조

```text
skills-cheatsheet/
├── README.md                    # 프리셋 목록·사용법 (이 문서)
├── CONTRIBUTING.md              # 새 프리셋 만드는 법, 업로드 규칙
├── shared/                      # 여러 스킬이 공유하는 표준·양식 (원본은 여기 한 곳)
│   ├── ppt/
│   │   ├── PPT-MASTER.md
│   │   └── PPT-OUTLINE-TEMPLATE.md
│   ├── diagram/
│   │   ├── ARCH-DIAGRAM.md      # 논리 구성도 디자인 표준 (디자인 고정, 내용은 YAML)
│   │   └── arch-diagram-template.yaml  # 구성도 내용 양식 (scripts/arch-diagram.py 로 생성)
│   └── web/
│       ├── DASHBOARD-DESIGN.md  # 대시보드(관리자·업무 시스템) 구조: 레이아웃·컴포넌트·패턴·문구
│       ├── THEME-CONTRACT.md    # 테마 규칙: 필수 토큰, 대비 기준, 라이트/다크 구현
│       ├── themes/              # 테마 = 색상 토큰만 (admin-navy 기본, slate 딥 블루 다크)
│       └── adapters/            # 외부 부품 연결: shadcn.md, tailadmin.md
├── skills/                      # 프리셋 (폴더명 = 스킬명)
│   ├── ppt-proposal/
│   │   ├── SKILL.md             # 호출 조건(description) + 실행 절차
│   │   ├── profile.md           # 용도별 덮어쓰기 값
│   │   └── bundle.txt           # 빌드 때 references/로 넣을 shared 파일 목록
│   ├── ppt-report/
│   ├── ppt-briefing/
│   └── web-admin/            # profile 없음 (디자인 시스템이 곧 표준)
├── guides/                      # 엔진 스킬 사용 가이드 (사람이 읽는 문서)
│   ├── no-install.md            # 설치 없이 파일 첨부로 쓰는 방법
│   ├── claude-code.md           # Claude Code에 설치·사용
│   ├── ppt-master.md
│   └── ppt-master-prompts.md
├── examples/web/                # 테마 적용 예시 화면 (가상 데이터)
├── _template/preset/            # 새 프리셋 양식
├── scripts/build.sh             # skills/* → dist/*.zip (claude.ai 업로드용)
├── scripts/install-claude-code.sh  # 스킬을 ~/.claude/skills 또는 프로젝트 .claude/skills에 설치
└── scripts/theme-to-css.py      # 테마 파일 → CSS 변수 (Tailwind v4 / 순수 CSS / shadcn)
```

## 설치 (claude.ai)

> Claude Code는 `scripts/install-claude-code.sh` — [Claude Code 가이드](guides/claude-code.md)

> 업로드 없이 쓰려면 [설치 없이 사용하기](guides/no-install.md)

1. 엔진 스킬 활성화 확인 — PPT 계열: `ppt-master` / 웹 계열: `frontend-design`, `web-design-guidelines`(선택)
2. 빌드: `scripts/build.sh` → `dist/*.zip` 생성
3. claude.ai 설정의 Skills 항목에서 zip 업로드 (조직 배포는 관리자)
4. 테스트: `ppt-briefing으로 첨부 내용 1장 요약 만들어줘`

## 로드맵

| 프리셋 | 엔진 | 상태 |
| --- | --- | --- |
| `ppt-proposal` | ppt-master | v1.0 (표준 그대로) |
| `ppt-report` | ppt-master | v0.1 초안 |
| `ppt-briefing` | ppt-master | v0.1 초안 |
| `web-admin` | frontend-design + web-design-guidelines | v1.0 (DASHBOARD-DESIGN.md 그대로) |
| `web-front` (서비스 프론트, `FRONT-DESIGN.md`) | frontend-design + web-design-guidelines | 예정 |
| `diagram-arch` (구성도 표준) | drawio | 예정 |
| `docx-report` (Word 보고서 표준) | docx | 예정 |
