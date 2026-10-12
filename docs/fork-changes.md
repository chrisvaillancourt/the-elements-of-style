# Fork changes and decisions

This fork of [obra/the-elements-of-style](https://github.com/obra/the-elements-of-style) reworks the `writing-clearly-and-concisely` skill. This file records what changed, why, and how, so later edits don't have to rediscover it.

Baseline: upstream `05fc4f0` (2026-08-12). Fork commits: `e59690b` (rework), `bbc7f20` (description order), plus this record.

## Why fork instead of using upstream

- **The skill's default behavior was the problem, not its content.** Upstream's description said to apply Strunk to "ANY prose humans will read", and `SKILL.md` ended with "Read `elements-of-style.md` and apply the rules". Every activation therefore loaded a ~15.8k-token file (o200k) with no editing procedure and no guidance on where 1918 usage misleads modern technical prose.
- **Observed cost.** In a 2026-09 Codex pilot (codex-cli 0.152.0), runs that activated the skill read the whole reference, then re-read overlapping chunks, for a 500-word draft: about 12× the input tokens and several times the latency of runs that didn't activate.
- **Upstream is effectively frozen.** No pull request has been merged or answered, every closed PR was closed by its own author, and the last push was 2026-08-12 (checked 2026-10-12). Open PRs #9 (description) and #6 (procedure) point in the right direction but weren't merged, and #9's description doesn't parse as YAML (an unquoted `read: documentation` makes PyYAML raise a ScannerError).
- **Guidance agrees on the shape.** Anthropic's skill authoring best practices, the Agent Skills spec and guides (agentskills.io) and OpenAI's Codex skills docs all recommend a lean, procedural `SKILL.md`, reference files loaded on demand with stated triggers, gotchas inline in `SKILL.md`, and a third-person description that says when to use the skill and when not to.

Strunk's text stays unchanged. All changes are in the wrapper.

## What changed

### `SKILL.md`: from a reading assignment to a working checklist

- **Description (frontmatter).** Third person, with explicit "Use when" and "Not for" clauses, written as a YAML folded block scalar (`>-`) so colons are safe. Its scope is drafts a person will read: messages, PR and Jira text, docs, commit message bodies, error and UI text. It excludes code, routine chat replies and text that must stay verbatim. Model invocation stays on.
- **Body (~1.5k o200k tokens, was ~490).**
  - a 7-step procedure: target, protect, structure, sentences, mechanics, verify, output
  - a protected-content rule: never change code, commands, paths, quotes, numbers, dates, names, links, required templates, or qualifiers that set a claim's strength
  - modern-usage gotchas (below)
  - all 18 rules on two lines, with Strunk's own qualifiers
  - common cuts, before/after examples and one "don't do this" example
  - pointers to the reference files, with when to read each
  - delegation for long documents: pass the subagent absolute file paths, because subagents may not be able to load skills by name
- **Order matters.** Procedure and gotchas come first. Claude Code re-attaches only the first 5,000 tokens of an invoked skill after compaction.

### Gotchas: where the 1918 text misleads modern technical prose

Each one overrides advice the reference gives, and each was checked against the text:

| Reference says | Override | Why |
|---|---|---|
| Generic *he* (misused-words: "They") | Singular *they* | Modern style guides, e.g. Google's developer style guide |
| *Data* is plural only | Follow house style | Singular is common in technical writing |
| 1918 *shall/will* person rules | Never change *shall/must/should/may* in specs | They can be normative (RFC 2119) |
| *fix, feature, factor, system, state, phase, case* are hackneyed or colloquial | Keep them when they name a technical thing | bug fix, feature flag, state machine, test case |
| *respectively* "may usually be omitted" | Keep it when it maps two lists | Removing it loses the mapping |
| No opening *However*; no split infinitives | Both are fine | Pullum, "50 Years of Stupid Grammar Advice" (2009) |
| Rule 10's examples treat "there were…" and "became…" as passive | Edit for directness, but don't call it passive | Most of those examples aren't passive constructions |
| Rule 11's rewrites change claim strength | Positive form must not change what is claimed | Strunk calls one of his own rewrites "simply a guess at the writer's intention" |
| Rule 13 read as "make sentences short" | "Make every word tell" | Strunk's own qualifier |
| Period spellings (to-day, any one, programme) | Don't copy them | Archaic |

### Reference split into `references/`

| File | Content | Size (o200k) |
|---|---|---|
| `usage-rules.md` | Section II, Rules 1–7 | ~2.8k |
| `composition-rules.md` | Section III, Rules 8–18 | ~7.4k |
| `misused-words.md` | Section V, 65 entries, one `### Word` heading each | ~5.4k |

- Why: an agent can read one rule or one word entry (hundreds of tokens) instead of 15.8k. Each file also fits under Codex's 10k-token default output cap for a single command; a whole-file read of the old reference got truncated, which likely explains the chunked re-reads in the pilot.
- Each file starts with a provenance line and a short contents list with no anchor links. The old 734-token anchor-link contents block is gone.
- **Dropped:** upstream's one-paragraph "Introductory", which paraphrased Strunk rather than quoting him. Upstream had already removed Sections IV (form), VI (spelling) and VII (exercises) in `58aa887` and `b94a6e8`.
- **Links** are relative Markdown links, and `SKILL.md` says paths resolve from the skill directory. This addresses upstream issue #2 portably. `${CLAUDE_SKILL_DIR}` was rejected because only Claude Code expands it.

### Description order (`bbc7f20`)

omp shows a skill's description as its first sentence, if under 100 characters, or else the first 100 characters. It replaces that with a 12-word routing hint only after a small model's summary passes validation, and for this skill that validation failed in practice. Codex also shortens descriptions when many skills are installed. The description therefore leads with what the skill edits, so the first 100 characters carry the trigger: "Copyedits drafts a person will read (Slack or email messages, PR and Jira text, docs, commit…"

### Packaging and docs

- **Self-references.** Upstream's manifests and install docs pointed at `obra/elements-of-style`, which returns 404 (upstream issues #14 and #18). They now point at this fork, edited in `everyharness.yaml` and in every generated file.
- **Manifest hashes.** `.everyharness/manifest.json` stores plain sha256 hashes of generated files. Those were recomputed by hand instead of running `everyharness generate`, because `everyharness@1.0.0` (the only published version) was four days old and the edit was a pure URL substitution. A later `generate` produces the same URLs from `everyharness.yaml`.
- **README.** It claimed "the complete 1918 text, roughly 12,000 tokens". It now says the text is abridged and gives per-file sizes (12,000 was the word count).
- **Research doc.** Its links to the old single file now point at upstream's copy at `05fc4f0`.

## Implementation notes

- **Split script:** [`scripts/split-reference.py`](../scripts/split-reference.py). Run against upstream's `elements-of-style.md` at `05fc4f0`, it rebuilds the three reference files byte for byte. It also re-reads its output and checks that the bodies rebuild the original Sections II–V exactly. If the source text ever changes, rerun it rather than hand-editing the references.
- **Install.** The skill is installed with the vercel-labs `skills` CLI from this fork's `main`. It goes into `~/.agents/skills/`, which Codex and omp read directly; `~/.claude/skills/` symlinks to it for Claude Code. `skills update` follows this fork, so upstream changes arrive only when merged here.
- **Token counts** come from `tiktoken` (o200k_base, cl100k_base). Claude's tokenizer wasn't measured.

## Verification

- **Reference split:** the round-trip check passed (65 entries, 7 usage rules, 11 composition rules), and every quote in the Gotchas matches the reference text.
- **Frontmatter:** parses with PyYAML. Claude Code, Codex (`codex debug prompt-input`) and omp all list the new description.
- **Smoke test (2026-10-12, Claude Code, Sonnet):** "tighten this slack reply…" invoked the skill automatically, read no reference file, and kept the "may" qualifier. One run, not a measurement.

## Considered and not done

- **Light edits only (PR #9's description plus a path note).** This leaves the full-reference default in place, and #9's YAML doesn't parse.
- **A paraphrased "distilled" Strunk (issue #1).** It would drift from the source. The distillation lives in `SKILL.md` instead, and the text stays verbatim.
- **`when_to_use`, `agents/openai.yaml`, `${CLAUDE_SKILL_DIR}`.** Each is specific to one harness, and Codex's implicit invocation is already on by default.
- **The preregistered Codex eval** (routing and quality suites, 2026-08/09). Dropped on 2026-10-12. Its routing negatives were trivia, so it couldn't measure under-triggering in mixed coding and prose work. Its harness was tied to one Codex CLI version, and the human review cost was high. The branch was local only and was deleted.

## Open items

- **License for the wrapper** (upstream issue #7, PR #10). The Strunk text is public domain, but the repository has no license file, and "Public Domain" isn't an SPDX identifier. Undecided.
- **Trigger evaluation.** An omp trigger test (old vs. new skill, gpt-6.1-sol at low and medium effort) and an independent GPT-6 Astra review are in progress. Results will be added here.
