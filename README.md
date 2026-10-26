# skills-cheatsheet

> 기본 스킬(ppt-master, frontend-design 등) 위에 **팀 표준을 덮어씌운 오버레이 스킬** 모음
> 스킬 이름만 부르면 표준대로 결과가 나오게 하는 것이 목표

## 치트시트

| 하고 싶은 것 | 스킬 | 이렇게 요청 | 결과 |
| --- | --- | --- | --- |
| 고객 제안서 덱 | `om-ppt-proposal` | `om-ppt-proposal로 첨부한 구성 문서 기준 제안서 만들어줘` | 겸용 PPTX + 발표자 노트, 8~15장 |
| 설치·점검·PoC 결과 보고 | `om-ppt-report` | `om-ppt-report로 첨부한 점검 결과 보고서 만들어줘` | 정보 전달용 PPTX, 요약 장 필수 |
| 팀장·임원 내부 보고 | `om-ppt-briefing` | `om-ppt-briefing으로 이 내용 3장 브리핑 만들어줘` | 1~5장 PPTX, 첫 장 결론·요청 |
| 업무 시스템 관리자 화면 | `om-web-admin` | `om-web-admin으로 자재 입고 목록 화면 만들어줘` | Tailwind v4 토큰 기반 화면 + 기본 화면 + 점검 결과 |

- PPT 공통: 결과와 함께 **스토리라인 표**, `[자료 필요]`·`[확인 필요]` 목록, 점검 결과 요약 제출
- 구성 문서가 없으면 스킬이 필수 항목 몇 가지만 묻고 초안부터 작성
- 요청 문구 더 보기: [guides/ppt-master-prompts.md](guides/ppt-master-prompts.md) (스킬명만 바꿔서 사용)

## 여러 스킬 함께 쓰기

- 오버레이 스킬끼리 **동시에 설치·사용 가능** — 요청 문구에 맞는 스킬을 Claude가 골라 불러 씀
- 한 작업에서 이어 쓰기도 가능: `om-web-admin으로 화면 만들고, 그 화면 캡처로 om-ppt-proposal 제안서 3장 추가해줘`
- 하나의 오버레이가 **엔진 여러 개**를 단계별로 사용 가능 (예: `om-web-admin` = 구현 `frontend-design` + 점검 `web-design-guidelines`)
- 호출이 겹치지 않게 각 `description`에 용도·호출 문구를 분명히 구분

## 오버레이 구조

```text
              PPT 계열                                         웹 계열
[오버레이]    om-ppt-proposal | -report | -briefing (profile.md)  om-web-admin
                     ▼ 덮어씀                                          ▼ 덮어씀
[공통 표준]   shared/ppt/PPT-MASTER_생성표준.md                    shared/web/WEB-DESIGN.md
                     ▼ 덮어씀                                          ▼ 덮어씀
[엔진]        ppt-master                                          frontend-design (구현) + web-design-guidelines (점검)
```

| 계층 | 담당 | 바뀌는 주기 |
| --- | --- | --- |
| 엔진 | 생성 절차, 도구, 렌더링 | 원본 저장소 업데이트 |
| 공통 표준 | 회사 공통 디자인·문장·사실 원칙 | 팀 합의로 개정 |
| 프로필 (선택) | 같은 표준 안에서 용도별 차이 (청중, 흐름, 장수 등) — 용도가 하나면 생략 | 용도 추가 시 |
| 구성 문서 | 업무별 내용 (고객, 메시지, 장표 구성) | 업무마다 |

**규칙 우선순위**: 이번 요청 > 구성 문서 > 프로필 > 공통 표준 > 엔진 기본값

- 표준을 고치면 → 모든 오버레이 스킬에 반영 (다시 빌드·업로드)
- 새 용도가 생기면 → 프로필만 새로 써서 스킬 하나 추가

## 폴더 구조

```text
skills-cheatsheet/
├── README.md                    # 치트시트 (이 문서)
├── CONTRIBUTING.md              # 새 오버레이 스킬 만드는 법, 업로드 규칙
├── shared/                      # 여러 스킬이 공유하는 표준·양식 (원본은 여기 한 곳)
│   ├── ppt/
│   │   ├── PPT-MASTER_생성표준.md
│   │   └── 구성문서_양식.md
│   └── web/
│       └── WEB-DESIGN.md        # 업무 시스템 디자인 시스템 (토큰 + 규칙)
├── skills/                      # 오버레이 스킬 (폴더명 = 스킬명)
│   ├── om-ppt-proposal/
│   │   ├── SKILL.md             # 호출 조건(description) + 실행 절차
│   │   ├── profile.md           # 용도별 덮어쓰기 값
│   │   └── bundle.txt           # 빌드 때 references/로 넣을 shared 파일 목록
│   ├── om-ppt-report/
│   ├── om-ppt-briefing/
│   └── om-web-admin/            # profile 없음 (디자인 시스템이 곧 표준)
├── guides/                      # 엔진 스킬 사용 가이드 (사람이 읽는 문서)
│   ├── ppt-master.md
│   └── ppt-master-prompts.md
├── _template/overlay-skill/     # 새 오버레이 스킬 양식
└── scripts/build.sh             # skills/* → dist/*.zip (claude.ai 업로드용)
```

## 설치 (claude.ai)

1. 엔진 스킬 활성화 확인 — PPT 계열: `ppt-master` / 웹 계열: `frontend-design`, `web-design-guidelines`(선택)
2. 빌드: `scripts/build.sh` → `dist/om-*.zip` 생성
3. claude.ai 설정의 Skills 항목에서 zip 업로드 (조직 배포는 관리자)
4. 테스트: `om-ppt-briefing으로 첨부 내용 1장 요약 만들어줘`

## 로드맵

| 스킬 | 엔진 | 상태 |
| --- | --- | --- |
| `om-ppt-proposal` | ppt-master | v1.0 (표준 그대로) |
| `om-ppt-report` | ppt-master | v0.1 초안 |
| `om-ppt-briefing` | ppt-master | v0.1 초안 |
| `om-web-admin` | frontend-design + web-design-guidelines | v1.0 (WEB-DESIGN.md 그대로) |
| `om-diagram-arch` (구성도 표준) | drawio | 예정 |
| `om-docx-report` (Word 보고서 표준) | docx | 예정 |
