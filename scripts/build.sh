#!/usr/bin/env bash
# skills/<스킬>/ 을 claude.ai 업로드용 zip으로 패키징
# - bundle.txt 에 적힌 shared/ 파일을 references/ 로 복사 (업로드 스킬은 자기 폴더만 볼 수 있음)
# 사용: scripts/build.sh            # 전체
#       scripts/build.sh om-ppt-report   # 하나만
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIST="$ROOT/dist"
mkdir -p "$DIST"

build() {
  local name="$1" src="$ROOT/skills/$1" out="$DIST/$1"
  [[ -f "$src/SKILL.md" ]] || { echo "skip: $name (SKILL.md 없음)"; return; }
  grep -q "^name: $name$" "$src/SKILL.md" || { echo "error: $name — SKILL.md name 과 폴더명 불일치"; exit 1; }
  rm -rf "$out" "$DIST/$name.zip"
  mkdir -p "$out/references"
  cp -R "$src/." "$out/" && rm -f "$out/bundle.txt"
  if [[ -f "$src/bundle.txt" ]]; then
    while IFS= read -r f; do
      [[ -z "$f" || "$f" == \#* ]] && continue
      cp "$ROOT/$f" "$out/references/"
    done < "$src/bundle.txt"
  fi
  (cd "$DIST" && zip -qr "$name.zip" "$name")
  echo "built: dist/$name.zip"
}

if [[ $# -gt 0 ]]; then build "$1"; else
  for d in "$ROOT"/skills/*/; do build "$(basename "$d")"; done
fi
