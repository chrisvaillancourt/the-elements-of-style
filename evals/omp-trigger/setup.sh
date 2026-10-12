#!/usr/bin/env bash
# Build isolated HOME dirs for the omp trigger test (see docs/fork-changes.md).
# Usage: evals/omp-trigger/setup.sh [old-ref]   (default: upstream baseline 05fc4f0)
# home-old gets the skill at <old-ref>; home-new gets the working tree's skill.
# Each home links the real ~/.omp (config, auth) and ~/.codex, and every skill
# in ~/.agents/skills except writing-clearly-and-concisely, so omp sees the
# same skill portfolio with only the variant under test swapped in.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
repo="$(git -C "$here" rev-parse --show-toplevel)"
old_ref="${1:-05fc4f0}"
skill=writing-clearly-and-concisely

rm -rf "$here/variants" "$here/home-old" "$here/home-new"
mkdir -p "$here/variants/old" "$here/variants/new"
git -C "$repo" archive "$old_ref" "skills/$skill" | tar -x -C "$here/variants/old" --strip-components=1
cp -R "$repo/skills/$skill" "$here/variants/new/"

for v in old new; do
  h="$here/home-$v"
  mkdir -p "$h/.agents/skills"
  ln -sfn "$HOME/.omp" "$h/.omp"
  ln -sfn "$HOME/.codex" "$h/.codex"
  for d in "$HOME"/.agents/skills/*; do
    n="$(basename "$d")"
    [ "$n" = "$skill" ] && continue
    ln -sfn "$(readlink -f "$d")" "$h/.agents/skills/$n"
  done
  cp -R "$here/variants/$v/$skill" "$h/.agents/skills/"
done
echo "ready: $here/home-old $here/home-new"
