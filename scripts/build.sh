#!/usr/bin/env bash
# skills/<스킬>/ 을 claude.ai 업로드용 zip으로 패키징
# - bundle.txt 에 적힌 shared/ 파일을 references/ 로 복사 (업로드 스킬은 자기 폴더만 볼 수 있음)
# 사용: scripts/build.sh            # 전체
#       scripts/build.sh ppt-report   # 하나만
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
    # shared/<계열>/ 아래 경로를 유지해 references/ 로 복사 (glob 허용: shared/web/themes/*.md)
    while IFS= read -r pat; do
      [[ -z "$pat" || "$pat" == \#* ]] && continue
      local matched=0
      for f in $ROOT/$pat; do
        [[ -f "$f" ]] || continue
        matched=1
        local rel="${f#$ROOT/shared/*/}"
        mkdir -p "$out/references/$(dirname "$rel")"
        cp "$f" "$out/references/$rel"
      done
      [[ $matched == 1 ]] || { echo "error: $name — bundle 경로 없음: $pat"; exit 1; }
    done < "$src/bundle.txt"
  fi
  (cd "$DIST" && zip -qr "$name.zip" "$name")
  echo "built: dist/$name.zip"
}

if [[ $# -gt 0 ]]; then build "$1"; else
  for d in "$ROOT"/skills/*/; do build "$(basename "$d")"; done
fi
