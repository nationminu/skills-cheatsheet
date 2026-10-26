---
name: web-admin
description: 오픈마루 표준 업무 시스템(관리자 대시보드) 화면 제작·수정. "관리자 화면", "어드민 대시보드", "업무 시스템 UI", "web-admin"으로 요청하거나 사내 업무 시스템의 목록·입력·서랍·대시보드 화면을 만들 때 사용. 업무 시스템 디자인 시스템(Tailwind CSS v4 토큰 + Lucide)을 frontend-design·web-design-guidelines 스킬 위에 덮어씌워 같은 밀도·위계의 화면을 만든다.
---

# web-admin — 오픈마루 표준 업무 시스템 화면

여러 엔진 스킬을 단계별로 쓰고, 이 스킬의 디자인 시스템을 **규칙**으로 적용하는 오버레이 스킬.

## 파일

| 파일 | 역할 |
| --- | --- |
| `references/WEB-DESIGN.md` | 업무 시스템 디자인 시스템 — YAML 토큰이 값의 원본, 본문이 사용 규칙 |

## 엔진

| 단계 | 엔진 스킬 | 쓰는 범위 |
| --- | --- | --- |
| 구현 | `frontend-design` | 구현 품질·마감 요령만 참고 (미적 방향 제안은 쓰지 않음) |
| 점검 | `web-design-guidelines` | 접근성·인터랙션 점검 (설치된 경우) |

엔진 스킬이 없으면 이 문서와 `references/WEB-DESIGN.md`만으로 진행.

## 규칙 우선순위

1. 사용자의 이번 요청
2. 결과물 저장소의 CLAUDE.md·설계 문서 (스택, 빌드 결과 커밋 여부, 업무 메뉴·상태)
3. `references/WEB-DESIGN.md`
4. 엔진 스킬 기본값 — 색·글꼴·레이아웃·모서리·그림자는 **항상 3번을 따름**. frontend-design의 "독특한 미적 방향" 제안은 적용하지 않음

## 실행 절차

1. **규칙 로드**: `references/WEB-DESIGN.md` 끝까지 읽음 (토큰, Default Screens, Page Patterns, Writing, Checklist)
2. **프로젝트 확인**: CLAUDE.md에서 스택(PHP / Python·Java 서버 렌더링 / SPA) 확인 → WEB-DESIGN.md Implementation 표의 해당 행 적용. 없으면 사용자에게 스택 한 가지만 물음
3. **토대 먼저**
   - `app.css`에 `@import "tailwindcss"` + `@theme`(YAML 토큰 그대로) + `@layer components`
   - 토큰에 없는 색·크기는 화면 코드에 쓰지 않음 — 필요하면 사용자에게 토큰 추가 제안
4. **Default Screens 확인**: 로그인·첫 관리자·대시보드·사용자 관리·변경 이력·도움말(이슈·패치노트·API 문서)·내 정보·403/404가 없으면 업무 화면보다 먼저 만듦 (사용자가 범위를 한 화면으로 지정한 경우 제외, 누락 목록만 보고)
5. **업무 화면**: Page Patterns(목록·표 안 수정·서랍·일괄 업로드·대시보드·빈 화면) 중 맞는 패턴으로 작성, 문구는 Writing 규칙(해요체, 버튼은 동사)
6. **상태 확인**: 빈 결과·저장 중·저장 실패(409 포함)·권한 없음·375px 모바일 화면을 실제로 띄워 확인 (브라우저 도구가 있으면 스크린샷)
7. **점검**: `web-design-guidelines` 스킬이 있으면 실행 + WEB-DESIGN.md "Accessibility & Review Checklist" 전 항목 확인, 위반 수정
8. **보고**: 만든 화면 목록, 추가·변경한 토큰, 점검 결과(통과/수정), 미확인 상태
