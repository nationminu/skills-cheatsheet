#!/usr/bin/env bash
# 오버레이 스킬을 Claude Code 스킬 폴더에 설치
# 사용: scripts/install-claude-code.sh --personal [스킬...]      # ~/.claude/skills/ (내 모든 프로젝트)
#       scripts/install-claude-code.sh <프로젝트 경로> [스킬...]  # <프로젝트>/.claude/skills/ (커밋해서 팀 공유)
# 스킬을 지정하지 않으면 skills/ 아래 전부 설치
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
[[ $# -ge 1 ]] || { sed -n '2,5p' "$0"; exit 1; }

if [[ "$1" == "--personal" ]]; then DEST="$HOME/.claude/skills"
else [[ -d "$1" ]] || { echo "error: 프로젝트 경로 없음: $1"; exit 1; }; DEST="$(cd "$1" && pwd)/.claude/skills"; fi
shift

if [[ $# -gt 0 ]]; then names=("$@"); else names=(); for d in "$ROOT"/skills/*/; do names+=("$(basename "$d")"); done; fi

mkdir -p "$DEST"
for n in "${names[@]}"; do
  "$ROOT/scripts/build.sh" "$n" >/dev/null
  rm -rf "${DEST:?}/$n"
  cp -R "$ROOT/dist/$n" "$DEST/$n"
  echo "installed: $DEST/$n"
done
