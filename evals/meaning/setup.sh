#!/usr/bin/env bash
# Build the variants for the meaning-preservation runs (see docs/fork-changes.md).
# Usage: evals/meaning/setup.sh [old-ref]   (default: upstream baseline 05fc4f0)
# Claude Code: plug-old / plug-new load each skill as a plugin (wcc-old:..., wcc-new:...);
#   the no-skill condition uses --disable-slash-commands.
# omp: home-none links the real ~/.omp, ~/.codex and every installed skill except
#   this one; the old/new omp homes come from evals/omp-trigger/setup.sh.
# Then: uv run python evals/meaning/meaning_run.py evals/meaning evals/omp-trigger <reps>
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
repo="$(git -C "$here" rev-parse --show-toplevel)"
old_ref="${1:-05fc4f0}"
skill=writing-clearly-and-concisely
rm -rf "$here/plug-old" "$here/plug-new" "$here/home-none"
for v in old new; do
  mkdir -p "$here/plug-$v/.claude-plugin" "$here/plug-$v/skills"
  printf '{"name":"wcc-%s","version":"0.0.1","description":"test variant"}\n' "$v" > "$here/plug-$v/.claude-plugin/plugin.json"
done
git -C "$repo" archive "$old_ref" "skills/$skill" | tar -x -C "$here/plug-old" --strip-components=0
cp -R "$repo/skills/$skill" "$here/plug-new/skills/"
h="$here/home-none"
mkdir -p "$h/.agents/skills"
ln -sfn "$HOME/.omp" "$h/.omp"
ln -sfn "$HOME/.codex" "$h/.codex"
for d in "$HOME"/.agents/skills/*; do
  n="$(basename "$d")"
  [ "$n" = "$skill" ] && continue
  ln -sfn "$(readlink -f "$d")" "$h/.agents/skills/$n"
done
"$here/../omp-trigger/setup.sh" "$old_ref" >/dev/null
echo "ready"
