# Fork changes and decisions

This fork of [obra/the-elements-of-style](https://github.com/obra/the-elements-of-style) reworks the `writing-clearly-and-concisely` skill. This file records what changed, why, and how, so later edits don't have to rediscover it.

Baseline: upstream `05fc4f0` (2026-08-12). Fork commits: `e59690b` (rework), `bbc7f20` (description order), then this record and the follow-up fixes from an independent review (see [Review follow-up](#review-follow-up-2026-10-12)).

## Why fork instead of using upstream

- **The skill's default behavior was the problem, not its content.** Upstream's description said to apply Strunk to "ANY prose humans will read", and `SKILL.md` ended with "Read `elements-of-style.md` and apply the rules". Every activation therefore loaded a ~15.8k-token file (o200k) with no editing procedure and no guidance on where 1918 usage misleads modern technical prose.
- **Observed cost.** In a 2026-09 Codex pilot (codex-cli 0.152.0), runs that activated the skill read the whole reference, then re-read overlapping chunks, for a 500-word draft: about 12× the input tokens and several times the latency of runs that didn't activate.
- **Upstream is effectively frozen.** No pull request has been merged or answered, every closed PR was closed by its own author, and the last push was 2026-08-12 (checked 2026-10-12). Open PRs #9 (description) and #6 (procedure) point in the right direction but weren't merged, and #9's description doesn't parse as YAML (an unquoted `read: documentation` makes PyYAML raise a ScannerError).
- **Guidance agrees on the shape.** Anthropic's skill authoring best practices, the Agent Skills spec and guides (agentskills.io) and OpenAI's Codex skills docs all recommend a lean, procedural `SKILL.md`, reference files loaded on demand with stated triggers, gotchas inline in `SKILL.md`, and a third-person description that says when to use the skill and when not to.

Strunk's text stays unchanged. All changes are in the wrapper.

## What changed

### `SKILL.md`: from a reading assignment to a working checklist

- **Description (frontmatter).** Third person, with explicit "Use when" and "Not for" clauses, written as a YAML folded block scalar (`>-`) so colons are safe. Its scope is drafts a person will read: messages, PR and Jira text, docs, commit message bodies, error and UI text. It excludes code, routine chat replies and text that must stay verbatim. Model invocation stays on.
- **Body (~1.9k o200k tokens, was ~490).**
  - a 7-step procedure: target, protect, structure, sentences, mechanics, verify, output. Target also settles the edit depth (proofread fixes mechanics; copyedit may restructure) and makes clear that quotation marks around a draft don't make it verbatim. Output may return the original unchanged and should flag unresolved meaning questions.
  - a protected-content rule: never change code, commands, paths, placeholders, attributed quotations, numbers, dates, names, links, required templates, or wording that sets a claim's strength or a requirement's level
  - modern-usage gotchas (below)
  - all 18 rules, one per line, summarized with selected caveats
  - common cuts (intensifiers are cut only when empty; "very likely" is not "likely"), before/after examples including a Slack request, and one "don't do this" example
  - pointers to the reference files, with when to read each
  - long documents: edit inline by default; delegate only when the harness and size justify it, as one bounded assignment with absolute file paths (subagents may not be able to load skills by name), no further delegation, and a parent check of the result
- **Order matters.** Procedure and gotchas come first. Claude Code re-attaches only the first 5,000 tokens of an invoked skill after compaction.

### Gotchas: where the 1918 text misleads modern technical prose

Each one overrides advice the reference gives, and each was checked against the text:

| Reference says | Override | Why |
|---|---|---|
| Generic *he* (misused-words: "They") | Singular *they* | Modern style guides, e.g. Google's developer style guide |
| *Data* is plural only | Follow house style | Singular is common in technical writing |
| 1918 *shall/will* person rules | Preserve requirement levels, negation and modal wording unless the user asks to change the requirement | Requirement wording can be normative (uppercase forms per RFC 2119/8174; lowercase can still state a requirement) |
| *fix, feature, factor, system, state, phase, case* are hackneyed or colloquial | Keep them when they name a technical thing | bug fix, feature flag, state machine, test case |
| *respectively* "may usually be omitted" | Keep it when it maps two lists | Removing it loses the mapping |
| No opening *However*; no split infinitives | Both are fine | Pullum, "50 Years of Stupid Grammar Advice" (2009) |
| Rule 10's examples treat "there were…" and "became…" as passive | Edit for directness, but don't call it passive | Most of those examples aren't passive constructions |
| Rule 11's rewrites change claim strength | Positive form must not change what is claimed | Strunk calls one of his own rewrites "simply a guess at the writer's intention" |
| Rule 13 read as "make sentences short" | "Make every word tell" | Strunk's own qualifier |
| Rule 17: one tense in summaries | Applies to the narrative frame; keep tense changes that separate past events, current state and future plans | Status and incident summaries need them |
| Historical spellings (to-day) | Use the document's current variety of English | *programme* is current UK English, not archaic |

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

### Description order (`bbc7f20`, then shortened)

- **How omp displays descriptions.** omp never shows the full description. It asks its small model (the `smol` role) for a routing hint of at most 12 words and caches it, keyed by the exact description text. Until a hint passes validation, it shows a preview: the first sentence if that ends within 99 characters, otherwise the first 100 characters. Hint generation often fails validation (77 failures for this skill in October's logs), so some sessions after each description change see the preview, until one attempt succeeds and is cached.
- **Codex** also shortens descriptions when many skills are installed.
- **So the description leads with what the skill edits.** `bbc7f20` moved the genres to the front. A later commit shortened the first sentence to 98 characters so the preview shows it whole: "Copyedits prose people will read: Slack, email, PRs, Jira, docs, commit bodies, error and UI text." The re-run trigger test showed no measurable difference (see below). It was kept because it carries the genres to every display, at no cost.
- **Cached hints as of 2026-10-12:**
  - upstream: "Use when drafting or editing human-readable prose, documentation, messages, or explanations."
  - `bbc7f20`: "Tighten, copyedit, proofread, or "Strunk" reader-facing drafts before finalizing."
  - current: "Use to tighten, copyedit, or proofread prose; not code or verbatim text."

  Once cached, the hint is what omp's model routes on.

### Packaging and docs

- **Self-references.** Upstream's manifests and install docs pointed at `obra/elements-of-style`, which returns 404 (upstream issues #14 and #18). They now point at this fork, edited in `everyharness.yaml` and in every generated file.
- **Manifest hashes.** `.everyharness/manifest.json` stores plain sha256 hashes of generated files. Those were recomputed by hand instead of running `everyharness generate`, because `everyharness@1.0.0` (the only published version) was four days old and the edit was a pure URL substitution. A later `generate` produces the same URLs from `everyharness.yaml`. **Caveat learned in review:** matching hashes prove only that files match the manifest, not that they match what the generator would emit. The hand edit missed that the Droid install ID derives from the repository name (`elements-of-style@the-elements-of-style`), now fixed. Next time, regenerate with a pinned, reviewed everyharness version instead.
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
- **Blind quality ranking** of the meaning-check outputs (first run of each condition) by the user, to judge clarity and voice beyond the protected-content checks.
- **Version metadata** still says `1.0.0`. It doesn't matter for skills-CLI installs; bump it before distributing through Claude plugins.

## Review follow-up (2026-10-12)

An independent review (GPT-6 Astra via omp, high reasoning) of `e59690b`/`bbc7f20` found no blockers and confirmed the split, YAML parsing, links, sizes and manifest hashes. It found contradictions in the new instructions, all fixed in the follow-up commit:

- **Example contradicted a gotcha:** "The token must be rotated" → "Rotate the token" dropped the *must* the gotcha protects. The example now keeps it ("You must rotate…").
- **"Never change quoted text" was ambiguous** when the draft itself is quoted. Protection now covers attributed quotations and marked verbatim spans, and Target says delimiters don't make the draft verbatim.
- **Blanket cut of "very/really/certainly"** conflicted with protecting claim strength. Now only empty intensifiers are cut.
- **Droid install ID** in the generated install doc was wrong (see Packaging).
- **Nits:** *programme* isn't archaic; the sample `grep` had no filename and a fixed line window (now: read from the heading to the next same-level heading); "all 18 rules with Strunk's qualifiers" overstated the summary.
- **Improvements adopted:** edit depth and an unchanged-output option, a short-message rule that keeps the audience and mechanics checks, a Rule 17 chronology gotcha, a general "1918 preferences are advice" principle, one rule per line, a Slack example, delegation made optional and bounded, and a skills-CLI install route in the README.
- **Not adopted yet:** a revised description (keep the current one unless trigger evidence shows a need), license and provenance changes (an owner decision), and the meaning-preservation cases (open item).

## Trigger test (2026-10-12)

Harness: [`evals/omp-trigger/`](../evals/omp-trigger/). `setup.sh` builds two isolated `HOME` directories that link the real omp config and every installed skill except this one, then add either the upstream skill (`05fc4f0`) or this fork's. `run_trigger.py` runs each prompt through `omp -p --mode json` and counts the skill as activated when the agent reads `skill://writing-clearly-and-concisely`. Raw results: `results-2026-10-12.jsonl`.

Setup: 10 should-trigger prompts (Slack, email, PR, Jira, commit body, error text, README, release note, concision, status update) and 10 near misses (regex explanation, variable renames, diff summary, plain-language rewrite, translation, Markdown lint, a concept question, "thanks", a docstring, a Python function). Each ran on `openai-codex/gpt-6.1-sol` at low and medium effort, 2 runs each: 160 calls, no failures, $4.46.

| Skill | Effort | Should trigger: caught | Shouldn't: stayed quiet | Balanced accuracy | Read the reference when triggered |
|---|---|---|---|---|---|
| upstream | low | 90% | 70% | 0.80 | 67% |
| upstream | medium | 100% | 45% | 0.72 | 84% |
| fork | low | 85% | 100% | 0.93 | 0% |
| fork | medium | 95% | 95% | 0.95 | 0% |

- **Over-firing is gone.** The upstream skill fired on the regex explanation, the diff summary and the Markdown lint fix every time, and at medium effort also on the concept question, the plain-language rewrite and the docstring. In omp, upstream is shown through its cached routing hint, "Use when drafting or editing human-readable prose, documentation, messages, or explanations"; "explanations" plausibly pulls in the explanation prompts.
- **Cheaper when it fires.** Activated runs averaged ~31k input tokens (including cache reads) and 10.8 s, against ~48k and 16.0 s for upstream, because the fork never read a reference file.
- **Misses.** The fork missed the error-text prompt 3 of 4 times and the Jira comment once at low effort. The outputs were still good: the model handled those short edits without the skill. One false positive (the plain-language rewrite, once at medium) is a reasonable composition with a copyedit.
- **Limits.** Two runs per cell, one model, omp only. The two skills reach the model through different omp displays: upstream through its cached 12-word hint, the fork through the 100-character preview, because omp's hint generation failed validation for it. The test measures what omp users actually see, not the descriptions in isolation. The test used the `bbc7f20` body; the later body edits don't change the description. **Confound found afterwards:** the fork's hint was cached at some point during or after this run, so some fork runs may have seen the hint rather than the preview.

### Re-run with the shortened first sentence

Same 20 prompts, fork only, low and medium effort, 2 runs each (80 calls, `results-2026-10-12-v2.jsonl`).

| Description | Effort | Should trigger: caught | Shouldn't: stayed quiet | Balanced accuracy |
|---|---|---|---|---|
| `bbc7f20` | low | 85% | 100% | 0.93 |
| `bbc7f20` | medium | 95% | 95% | 0.95 |
| shortened | low | 85% | 100% | 0.93 |
| shortened | medium | 95% | 95% | 0.95 |

- The error-text prompt improved from 1 of 4 caught to 3 of 4. The Jira and release-note prompts each lost a catch, and "summarize this diff" triggered once. At two runs per cell this is noise: **no measurable difference.**
- **Confound:** omp cached the shortened description's hint partway through this run, so runs mixed the preview and the hint. A clean steady-state comparison would re-run now that every version has a cached hint.

## Meaning-preservation check (2026-10-12)

Harness: [`evals/meaning/`](../evals/meaning/). Three drafts built to tempt an editor into changing meaning:
- **Slack:** a quoted draft containing an attributed quotation, "not yet", "might" and a hedged date
- **API docs:** `MUST NOT`, `SHOULD`, 500 ms, HTTP 400/503, a retry limit of 3 and a link
- **Jira:** past, present and future tenses, "very likely", "haven't confirmed", an @mention and a polite ask

Each ran with no skill, the upstream skill and the fork's skill, in Claude Code (Opus 5.5) and omp (`gpt-6.1-sol`, medium), 2 runs each (36 runs). In Claude Code, no skill means `--disable-slash-commands`, and the upstream and fork skills were loaded as plugins with distinct names. In omp, each condition ran with its own isolated `HOME`. Every run's trace confirmed it loaded the intended skill or none.

| Harness | No skill | Upstream skill | Fork skill |
|---|---|---|---|
| Claude Code | 31/34 checks | 31/34 | **34/34** |
| omp | 34/34 | 30/34 | **34/34** |

- **Upstream failures:** it paraphrased away the attributed quotation (3 of 4 Slack runs), cut "very likely" to "likely" (3 of 4 Jira runs), and once dropped the hedge on Thursday.
- **No-skill Claude failures:** it dropped the quotation (both Slack runs) and once turned "very likely" into "We think".
- **The fork's skill never lost a protected item.** It also never read a reference file; upstream read its full reference in every omp run.
- **Limits:** three cases and two runs per cell. The checks are string matches; every failure was confirmed by reading the output. They test what must not change, not whether the edit is good. A blind quality ranking by the user is pending.
