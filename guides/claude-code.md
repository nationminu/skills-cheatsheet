# Claude Code에서 사용하기

> 같은 오버레이 스킬을 claude.ai(채팅)와 Claude Code(개발 환경) 양쪽에서 사용
> 이 레포는 **Claude 전용** — 다른 AI 도구용 규칙 파일은 만들지 않음

## 1. 어디에 쓰나

| 작업 | 권장 위치 | 이유 |
| --- | --- | --- |
| 제안서·보고서·브리핑 PPT (`ppt-*`) | claude.ai | 첨부 자료 중심, 결과 파일 다운로드 |
| 대시보드 화면 시안 (`web-admin`) | claude.ai | 단독 HTML로 빠르게 확인 |
| 실제 프로젝트 화면 구현 (`web-admin`) | **Claude Code** | 프로젝트 코드·CLAUDE.md·빌드를 보면서 표준대로 확장 |

## 2. 설치

Claude Code는 스킬 폴더(`SKILL.md`가 든 폴더)를 아래 위치에서 읽음 ([공식 문서](https://code.claude.com/docs/en/skills))

| 범위 | 위치 | 용도 |
| --- | --- | --- |
| 개인 | `~/.claude/skills/<스킬>/` | 내 모든 프로젝트 |
| 프로젝트 | `<프로젝트>/.claude/skills/<스킬>/` | 저장소에 커밋해서 팀 공유 |

```bash
git clone https://github.com/nationminu/skills-cheatsheet
cd skills-cheatsheet

scripts/install-claude-code.sh --personal                  # 전체 스킬 → ~/.claude/skills/
scripts/install-claude-code.sh ~/work/my-admin web-admin   # 한 프로젝트에 web-admin만
```

- 스크립트가 `scripts/build.sh`로 빌드한 폴더(`dist/<스킬>/`)를 복사 — 표준·테마·어댑터·생성 스크립트가 스킬 폴더 안에 함께 들어감
- 표준을 고친 뒤에는 같은 명령을 다시 실행 (기존 스킬 폴더 교체)

## 3. 엔진 스킬

| 오버레이 | 엔진 | Claude Code에서 |
| --- | --- | --- |
| `ppt-*` | `ppt-master` | [원본 저장소](https://github.com/hugohe3/ppt-master)의 `skills/ppt-master/` 폴더를 `~/.claude/skills/ppt-master/`로 복사 (원본 의존성·설정은 저장소 README 확인) — 오버레이가 `~/.claude/skills`, `.claude/skills`에서 자동으로 찾음 |
| `web-admin` | `frontend-design`, `web-design-guidelines` (선택) | 없어도 동작 — 오버레이 스킬의 표준과 체크리스트만으로 진행 |

## 4. 사용

```text
# 자동 호출: 요청 문구가 스킬 description과 맞으면 Claude가 불러 씀
web-admin으로 주문 관리 목록 화면 추가해줘. slate 테마, 다크 모드 기본

# 직접 호출: 슬래시 명령
/web-admin 주문 관리 목록 화면 추가
```

**프로젝트 CLAUDE.md에 한 번 적어 두기** (스킬이 2단계에서 읽음)

```markdown
## 화면 표준
- 화면 작업은 web-admin 스킬 기준
- 스택: Laravel + Blade, Tailwind 단독 실행 파일로 빌드, 결과 CSS 커밋
- 테마: slate (다크 기본)
- 외부 부품: 차트는 TailAdmin에서 가져옴 (adapters/tailadmin.md 치환 필수)
```

## 5. 테마 CSS 생성 (프로젝트 안에서)

```bash
# Tailwind v4 (서버 렌더링 프로젝트)
python3 .claude/skills/web-admin/scripts/theme-to-css.py \
  .claude/skills/web-admin/references/themes/slate.md > resources/css/theme.css

# shadcn/ui (React·Next.js 프로젝트)
python3 .claude/skills/web-admin/scripts/theme-to-css.py \
  .claude/skills/web-admin/references/themes/slate.md --shadcn > src/app/globals.css
```

- 새 테마는 레포 `shared/web/themes/`에 추가 → 다시 설치하면 모든 프로젝트에서 사용 가능
