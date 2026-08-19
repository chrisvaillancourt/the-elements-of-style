# Writing-skill alternatives and effectiveness

Research snapshot: 2026-08-19. Install counts, stars, releases, and repository activity are point-in-time observations and will drift.

## Executive verdict

This project is a well-packaged, portable reminder of a useful editorial tradition. It is not yet an evidence-backed writing intervention.

The short skill can plausibly nudge a model toward active, concrete, concise prose. Nothing in the repository, the surrounding skill ecosystem, or the research reviewed here shows that loading its long reference consistently improves human-facing prose over a capable model's ordinary judgment. The repository has no trigger tests, output evals, benchmarks, or before/after examples. A small local smoke test conducted for this review found no overall advantage from explicit use of the full skill and reference.

The best current approach is layered:

1. Put a compact, audience-aware style contract in project instructions for rules that should always apply.
2. Invoke a focused editing skill only for a substantial draft or review pass.
3. Route specialized work to specialized guidance: technical documentation, UI copy, and marketing copy have different success criteria.
4. Run a deterministic prose linter such as Vale on files where consistent mechanical rules matter.
5. Keep a blinded baseline-versus-intervention eval suite. Retain the Strunk skill only if it produces a meaningful gain relative to its token and latency cost.

The defensible effectiveness verdict today is **promising as an optional editorial cue, but unvalidated as a universal writing skill**.

## Scope and method

This review inspected the fork at `05fc4f0`, its upstream source, its history, its current issue reports, first-party skill listings and source repositories, official tool documentation, and primary research. It did not install candidates or modify external systems.

Candidate quality was checked against source rather than search summaries: current availability, first-party install listing, repository adoption and activity, license, trigger design, instruction content, and instruction footprint. Install and star counts indicate adoption, not output quality. No competing prose skill found here publishes a credible controlled outcome evaluation.

Facts, inferences, and recommendations are separated below. “Token” measurements for this project used the `o200k` and `cl100k` tokenizers. Candidate token figures are rough `UTF-8 characters / 4` estimates; exact word and character counts are reported alongside them when useful.

## What this project actually delivers

### Confirmed facts

| Dimension | Current state | Consequence |
|---|---|---|
| Core instruction | The [`SKILL.md`](../../skills/writing-clearly-and-concisely/SKILL.md) is 325 words and 487 `o200k` tokens. Its description says to apply Strunk to “ANY prose humans will read,” and its body says to use the skill whenever the agent writes prose. | Cheap after activation, but deliberately over-broad. It gives the agent few meaningful negative trigger cases. |
| Reference | [`elements-of-style.md`](../../skills/writing-clearly-and-concisely/elements-of-style.md) is 12,154 words: 15,783 `o200k` tokens or 15,856 `cl100k` tokens. Skill plus reference is about 16,270 `o200k` tokens. | Progressive disclosure avoids the full cost until the file is read. Once read, this is a material context and latency cost for generic knowledge that modern models may already possess. |
| Activation | The plugin sets [`bootstrap: none`](../../everyharness.yaml); compatible clients discover the skill and usually rely on model judgment to activate it. The Agent Skills specification confirms that model-driven activation is the common pattern and that the description carries the trigger decision. [Agent Skills activation model](https://agentskills.io/client-implementation/adding-skills-support) | Availability is not enforcement. A broad description can over-trigger, while a general writing request may still fail to trigger because the model believes it can handle the task itself. |
| Packaging | `everyharness` emits manifests and install instructions for many agent clients. The generated [support matrix](../support-matrix.md) reports full skill support across its named skill-capable targets. | Portability and maintenance are real strengths, independent of whether the writing guidance improves output. |
| Evidence in the repo | The 34 tracked files contain no tests, trigger cases, eval corpus, benchmark, or scored before/after examples. | The README's quality claims are mechanism claims, not measured results. |
| Adoption | The upstream repository had 527 stars and 76 forks on 2026-08-19, and its [skills.sh listing](https://skills.sh/obra/the-elements-of-style/writing-clearly-and-concisely) showed 1,460 installs. The fork is not currently listed on skills.sh. [Upstream repository](https://github.com/obra/the-elements-of-style) | There is meaningful interest, but popularity does not establish writing quality. |
| License metadata | Package and plugin metadata say “Public Domain,” while GitHub detects no repository license file. [Package metadata](../../package.json) | The source text's public-domain status and the licensing of the repository's packaging/instructions are not expressed as cleanly as they could be. This is a reuse concern, not evidence about effectiveness. |

The upstream skills.sh listing exposes `npx skills add https://github.com/obra/the-elements-of-style --skill writing-clearly-and-concisely`. The [corresponding direct page for this fork](https://skills.sh/chrisvaillancourt/the-elements-of-style/writing-clearly-and-concisely) currently says that the skill is unavailable in the repository, so the fork has no registry install count.

The README calls the Markdown reference the “complete 1918 text” and estimates roughly 12,000 tokens. The current reference is an abridged and edited edition: commit [`b94a6e8`](https://github.com/obra/the-elements-of-style/commit/b94a6e8) removed section VII, and [`58aa887`](https://github.com/obra/the-elements-of-style/commit/58aa887) removed sections IV and VI and replaced the original introduction. The retained reference is still substantial, but “complete” is inaccurate and the current measured footprint is about 15,800 reference tokens, not 12,000.

Several upstream reports match the design risks, although they are anecdotal rather than controlled evidence: [issue #5](https://github.com/obra/the-elements-of-style/issues/5) reports that implicit invocation rarely occurs, [issue #2](https://github.com/obra/the-elements-of-style/issues/2) reports relative-path lookup failures, and [issue #1](https://github.com/obra/the-elements-of-style/issues/1) asks for a distilled guide. These reports justify trigger and path tests; they do not establish population-wide failure rates.

Official Agent Skills guidance is especially relevant. It recommends putting into a skill what an agent would otherwise get wrong, testing whether the skill adds value at all, keeping instructions lean, and preferring focused procedures over exhaustive rules. It also warns that every loaded token competes for attention and that over-broad skills are hard to activate precisely. [Agent Skills best practices](https://agentskills.io/skill-creation/best-practices)

### Local explicit-invocation smoke test

A small test during this review compared ordinary model judgment with explicit loading of the current `SKILL.md` and full reference. Isolated generators used the same session-default Codex model with no override; the exact model identifier was not exposed. Two blind judges also used the session default. The four tasks required fact preservation and prohibited invention.

| Task | Observed result |
|---|---|
| User-facing troubleshooting explanation | Ordinary output was preferred for precision. |
| Actionable UI error copy | Outputs were identical. |
| Engineering status report with numbers and qualifiers | Guided output was preferred. |
| Git commit message | Ordinary output was preferred for precision. |

Nearly all outputs received 5/5 rubric scores. Across the four pairs, one judge's overall verdict was a tie and the other preferred ordinary judgment; both reported medium confidence.

This is useful negative evidence against assuming a large effect, but it is **not a benchmark**: `n=4`, one unknown session-default model, one sample per condition, only two judges, no measured natural trigger behavior, and explicit invocation that gives the skill its best chance. The result is “no clear signal,” not “the skill never helps.”

## Comparable agent skills and plugins

### Direct candidates

The table ranks fit, not popularity. A specialist can be better for its genre while being a poor universal replacement.

| Candidate | Verified availability and health (2026-08-19) | Content and trigger design | Footprint | Material difference from this project |
|---|---|---|---:|---|
| **[Blader Humanizer](https://skills.sh/blader/humanizer/humanizer)** | 4,541 installs; [36,590-star MIT repository](https://github.com/blader/humanizer), pushed 2026-08-19. [Exact skill source](https://github.com/blader/humanizer/blob/38b88903a5080c72a8c0472e79dcc9ffbf07938b/SKILL.md) | Activates for AI-sounding prose. Covers 35 observed AI-pattern families, prioritizes a supplied voice sample, preserves every claim, forbids invented facts, distinguishes neutral from personal prose, and includes false-positive checks. | 4,734 words; 30,409 chars; ~7,602 tokens | Best verified alternative for the narrower goal “remove AI tells while preserving voice.” More LLM-specific and guarded than Strunk, but not a general grammar guide. Its Wikipedia-derived checklist has no published outcome eval and may overfit today's surface tells. |
| **[Vercel writing-guidelines](https://skills.sh/vercel-labs/agent-skills/writing-guidelines)** | 47,172 installs; wrapper repository had 30,216 stars and was pushed 2026-08-18. Wrapper repo has no detected root license; the fetched-rules repo is MIT. [Wrapper source](https://github.com/vercel-labs/agent-skills/blob/2f423a2f30bcd6fd1a687e2cd52c569ada179e88/skills/writing-guidelines/SKILL.md) · [fetched rules](https://github.com/vercel-labs/writing-guidelines/blob/11483f8b60f3a90aa396b07a3cfbc32d42741162/command.md) | Activates for review/audit requests, fetches current rules, and returns terse `file:line` findings. Covers technical docs, headings, code blocks, voice, and AI tells. | 177-word wrapper plus 2,063-word fetched rules; ~3,865 tokens | Strong audit contract and modern technical rules. It has a mutable network dependency, Vercel-specific prescriptions, and licensing ambiguity, so it is not a clean generic drop-in. |
| **[MarketingSkills copy-editing](https://skills.sh/coreyhaines31/marketingskills/copy-editing)** | 112,009 installs; [44,910-star active MIT repository](https://github.com/coreyhaines31/marketingskills). [Exact skill source](https://github.com/coreyhaines31/marketingskills/blob/30f9b9a729bbbe3da562fc1108c31f3a35afcca1/skills/copy-editing/SKILL.md) | Activates on existing marketing copy and performs seven sequential sweeps: clarity, voice, benefit, proof, specificity, emotion, and risk. | 2,296 words; 15,000 chars; ~3,750 tokens before optional references | Well-adopted and process-oriented. Conversion goals can distort neutral documentation, reports, and error text. Its multi-pass, preserve-voice workflow is worth borrowing even when the skill itself is not. |
| **[UX Writing](https://skills.sh/content-designer/ux-writing-skill/ux-writing)** | 1,481 installs; [152-star active MIT repository](https://github.com/content-designer/ux-writing-skill). [Exact skill source](https://github.com/content-designer/ux-writing-skill/blob/a9fba5244645fba26361e15eddb65fd1fec2c87f/SKILL.md) | Targets UI strings, errors, forms, onboarding, voice/tone, and copy audits. Supplies UI patterns, accessibility guidance, tone-by-state rules, four editing passes, and templates. | 2,156 words; 15,341 chars; ~3,835 tokens before references | Better than a general Strunk pass for UI and error copy because it encodes interaction context. Some numerical “research-backed” claims lack inline sources and should be validated before adoption. |
| **[Cursor pstack technical-writing](https://skills.sh/cursor/plugins/technical-writing)** | 249 installs; hosted in the [3,662-star Cursor plugins repo](https://github.com/cursor/plugins); the pstack subtree is MIT and active. [Exact skill source](https://github.com/cursor/plugins/blob/b047069f4f3a73e87dd1f11f7913386d25876b91/pstack/skills/technical-writing/SKILL.md) | Manual-only (`disable-model-invocation: true`). Combines Diátaxis, Google developer style, Simplified Technical English, and Global English for docs, RFCs, READMEs, PRs, and commits; explicitly excludes product UI. | 1,910 words; 11,522 chars; ~2,881 tokens | Strongest technical-document framework reviewed and careful about legitimate exceptions and rhythm. It references a separate `unslop` skill without declaring an install dependency. Adoption is modest. |
| **[Orwell Writing](https://skills.sh/tamdogood/builder-essential-skills/orwell-writing)** | 121 installs; [166-star active MIT repository](https://github.com/tamdogood/builder-essential-skills). [Exact skill source](https://github.com/tamdogood/builder-essential-skills/blob/80c04a321ff252ade938ff3ed616eec436ddfe44/skills/orwell-writing/SKILL.md) | Broad drafting/revision trigger. Uses Orwell's six rules plus high-level Simplified Technical English, while preserving meaning, audience, tone, necessary jargon, and creative rhythm. | 708 words; 4,530 chars; ~1,133 tokens | Best compact general substitute found. More explicit than Strunk about voice and exceptions, but low adoption and no eval evidence. |

First-party skills.sh install commands, for reproducibility only:

```text
npx skills add https://github.com/blader/humanizer --skill humanizer
npx skills add https://github.com/vercel-labs/agent-skills --skill writing-guidelines
npx skills add https://github.com/coreyhaines31/marketingskills --skill copy-editing
npx skills add https://github.com/content-designer/ux-writing-skill --skill ux-writing
npx skills add https://github.com/cursor/plugins --skill technical-writing
npx skills add https://github.com/tamdogood/builder-essential-skills --skill orwell-writing
```

No installation was performed during this review.

### Lower-confidence and negative controls

- [different-ai/writing-style](https://skills.sh/different-ai/agent-bank/writing-style) is a useful 199-word, voice-preserving minimal-edit prompt, but it had only 369 installs and declares OpenCode compatibility; Codex fit was not confirmed from source.
- [tw93/Waza write](https://skills.sh/tw93/waza/write) is active, MIT licensed, and well adopted (12,761 installs), but its roughly 4,482-token core is a much broader bilingual localization, social, and document workflow rather than a clean English prose editor. [Source](https://github.com/tw93/Waza/blob/30bf563ccba94652081b53a0d574ef91c32516ee/skills/write/SKILL.md)
- [NeoLab write-concisely](https://skills.sh/neolabhq/context-engineering-kit/write-concisely) embeds roughly the whole Strunk text directly in `SKILL.md` (12,389 words; about 18,200 estimated tokens). It has the same central idea with worse progressive disclosure.
- Anthropic's `plain-language-letters` remains indexed but its source marks it deprecated and redirects to legal-specific skills. An install count can outlive a useful artifact.
- `openprose/open-prose` is a prose workflow/programming system, not a copyediting skill.

### Inference

There is no universally “better writing skill” because these candidates optimize different outcomes. Humanizer is a serious conditional replacement for de-AI editing; technical-writing and UX Writing are better genre tools; MarketingSkills is appropriate only when conversion is the goal; Orwell is the closest compact general alternative. Composing a small general core with specialist routing is less likely to flatten every genre into the same voice.

## Alternatives outside agent skills

### Always-on instructions

A short project style contract is the lowest-complexity option when a rule truly applies to every output. Codex reads layered `AGENTS.md` files with a 32 KiB default combined limit, making them suitable for a concise project contract. [Official Codex `AGENTS.md` documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md) Claude Code similarly loads `CLAUDE.md` as context and recommends concise, specific instructions; it can import `AGENTS.md`. [Official Claude Code memory documentation](https://code.claude.com/docs/en/memory)

This mechanism is more reliable than hoping a universal skill triggers, but it consumes context on every task. Keep it to high-value invariants such as:

- Preserve facts, numbers, qualifiers, links, and the writer's intended meaning.
- Match the audience, genre, and supplied voice before applying generic style preferences.
- Prefer direct, concrete language; remove needless words without deleting necessary nuance.
- Treat active voice as a default, not a ban on useful passive constructions.
- For substantial prose, draft first and run a separate editing pass.

Harness-specific output styles are another option. Claude output styles modify the system prompt, can be scoped to a project/user/plugin, and add input tokens; they affect the main conversation rather than ordinary subagents. [Claude output-style documentation](https://code.claude.com/docs/en/output-styles) They are appropriate for a persistent personal voice, less so for a repository that aims to remain portable.

### Deterministic prose tooling

| Tool | Current health (2026-08-19) | What it enforces | Best fit and limitation |
|---|---|---|---|
| **[Vale](https://github.com/vale-cli/vale)** | 5,971 stars, MIT, [v3.17.1](https://github.com/vale-cli/vale/releases/tag/v3.17.1) released 2026-08-05, [default branch active 2026-08-14](https://github.com/vale-cli/vale/commit/e58732900ce0f94b85e46f3093cfd6facbb9e3cd) | Offline, markup-aware YAML rules, structural scopes, JSON output, and CI support. Its [package explorer](https://vale.sh/explorer) includes Microsoft, Google, write-good, proselint, alex, and other styles. | Best general local/CI gate. Repeatable and zero model tokens, but cannot judge argument quality, audience fit, factuality, or perform a holistic rewrite. |
| **[proselint](https://github.com/amperser/proselint)** | 4,563 stars, BSD-3-Clause, [v0.16.0](https://github.com/amperser/proselint/releases/tag/v0.16.0), [active 2026-06-22](https://github.com/amperser/proselint/commit/dbed789caae662d06c7c8a5a13dd31f1acd36f5c) | Curated usage checks, granular selection, pre-commit support, nonzero findings status, JSON output. | Broad built-in advice, but its raw-text treatment can create code/markup false positives. Vale's proselint package is usually a cleaner Markdown deployment. |
| **[write-good](https://github.com/btford/write-good)** | 5,081 stars, MIT; [npm 1.0.8](https://registry.npmjs.org/write-good/latest) dates to 2021, [repository last active 2025-03-10](https://github.com/btford/write-good/commit/6940b034c6f5a7e101c01a24d651a778fc3fe435) | Passive voice, repetition, weasel words, adverbs, wordiness, clichés, optional E-Prime. It describes itself as naive. | Closest mechanical overlap with “active voice” and “omit needless words”; narrow and materially stale at the package level. |
| **[alex](https://github.com/get-alex/alex)** | 5,098 stars, MIT; [npm 11.0.1](https://registry.npmjs.org/alex/latest) from 2023, [repository last active 2024-11-27](https://github.com/get-alex/alex/commit/9a57595d1050d8fff99dc073670ee2bb41c925f6) | Inclusive-language checks for plain text, Markdown, MDX, and HTML, with suggestions and allow/deny controls. | Covers a modern concern absent from a 1918 guide. Complementary rather than a general clarity system; maintenance is limited. |
| **[textlint](https://github.com/textlint/textlint)** | 3,169 stars, MIT, [v15.8.0](https://github.com/textlint/textlint/releases/tag/v15.8.0), [active 2026-08-12](https://github.com/textlint/textlint/commit/3bb00451d4890b7b45777676980c4d7806b1eb7a) | ESLint-like pluggable framework, parsers, auto-fix/dry-run, cache, CI formats, and MCP-server mode. | Best when Node extensibility, auto-fix, or MCP integration matters. More setup than Vale, and quality depends on chosen rule packages. |

Deterministic tools use local runtime rather than model context. Their cost is configuration, false-positive triage, and CI time. They should flag or gate rules that are genuinely mechanical; they should not be treated as proof that a document communicates well.

### Eval-driven workflow

[Promptfoo](https://github.com/promptfoo/promptfoo) is an active MIT evaluation harness (24,379 stars, [v0.122.0 on 2026-08-04](https://github.com/promptfoo/promptfoo/releases/tag/0.122.0), [active 2026-08-19](https://github.com/promptfoo/promptfoo/commit/7d26d8f3cccb35dc6df53b18af32f0082cef2197)). It supports deterministic assertions, pairwise `select-best`, `llm-rubric`, and G-Eval. Its own guidance recommends cheap deterministic checks before model judges. [Assertions documentation](https://www.promptfoo.dev/docs/configuration/expected-outputs/) · [LLM-as-judge guidance](https://www.promptfoo.dev/docs/guides/llm-as-a-judge/)

Promptfoo is not required; a small local harness can do the same job. Its value is methodological: compare interventions rather than assuming a respected guide helps. Model judging adds tokens, latency, and variance, so it must be calibrated against human labels.

The official Agent Skills evaluation guide recommends clean-context with-skill/without-skill runs, saving token and duration data, objective assertions where possible, and human review for style and design. It explicitly advises removing rules that do not beat the baseline. [Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills)

## What primary evidence says about likely effectiveness

No identified study directly A/B-tests the complete 1918 *Elements of Style* as an LLM skill. The following evidence is indirect but decision-relevant.

| Primary source | Confirmed result | Limitation | Implication for this project |
|---|---|---|---|
| [OpenAI current model guidance](https://developers.openai.com/api/docs/guides/latest-model) | OpenAI reports internal coding-agent evals in which leaner system prompts improved scores by roughly 10–15%, reduced tokens 41–66%, and reduced cost 33–67%. It recommends stating instructions once and retaining style rules for requirements or measured gaps. | Directional internal results; tasks, sample, and uncertainty are not disclosed, and this is not a prose experiment. | Long reference loading is a hypothesis to test, not a safe default. |
| [EditEval, CoNLL 2024](https://aclanthology.org/2024.conll-1.7/) | Across ten English editing datasets, seven task types, several 3B–175B models, and 3–11 prompt variants per task, small wording changes produced substantial model-dependent variation. The highest-scoring prompt was not necessarily the most robust. | Older models and mostly task-specific automatic metrics; no Strunk condition. | Editing instructions can help, but a canonical prompt does not generalize automatically across models or tasks. |
| [Sclar et al., ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/file/6c0e99d736da621403018ca7b32b1a4d-Paper-Conference.pdf) | Across more than 50 tasks, meaning-preserving prompt-format changes shifted accuracy by about ten points on average and up to 76 points for one model. Good formats transferred weakly between models. | Mostly few-shot classification, not prose quality. | The plugin likely changes behavior, but neither direction nor magnitude can be assumed across harnesses and models. |
| [FollowBench, ACL 2024](https://aclanthology.org/2024.acl-long.257/) | In 820 instructions from more than 50 tasks, strict satisfaction declined as constraints accumulated. GPT-4-Preview fell from 84.7% with one constraint to 61.9% with five; GPT-3.5 fell from 80.3% to 53.2%. | 2023-era models; some scoring used an LLM judge. | Treating all 18 principles as simultaneous requirements risks partial compliance. Select the few relevant rules. |
| [Du et al., Findings EMNLP 2025](https://aclanthology.org/2025.findings-emnlp.1264/) | Five models lost 13.9–85% performance as otherwise controlled prompts grew toward 30K tokens, even with verified retrieval of the relevant fact. | Synthetic expansion and non-prose tasks. | Context capacity is not free. Finding a rule in the 15.8K-token reference does not guarantee the underlying task stays equally strong. |
| [Zheng et al., NeurIPS 2023](https://arxiv.org/abs/2306.05685) | GPT-4 judges had high aggregate agreement with humans after ties were removed, but exhibited position, verbosity, and about ten-point self-preference bias. | Older models, broad assistant tasks, and a headline agreement that excludes ties. | LLM judges are useful secondary evaluators, not sufficient proof of better writing. |
| [Liu et al., ACL 2023](https://aclanthology.org/2023.acl-long.228.pdf) | In about 50,000 summarization judgments, fine-grained binary content-unit checks reached Krippendorff's alpha around .75, while broad 1–5 ratings reached only .22–.35. Typical 50–100-item evals had power only for large effects. | Summarization salience rather than general prose style. | Check atomic meaning preservation and use enough examples; a holistic “better writing” score is unreliable. |
| [Cachola et al., EMNLP 2025](https://aclanthology.org/2025.emnlp-main.1225/) | Against human judgments of plain-language scientific summaries, six readability metrics correlated below .30; Flesch–Kincaid reached only `r=.16`, and the best LLM judge reached `r=.56`. | English scientific summaries only. | Word counts and readability grades are diagnostics, not evidence of clearer communication. |
| [Ferreira, Cognitive Psychology 2003](https://pubmed.ncbi.nlm.nih.gov/12948517/) | Controlled comprehension experiments found 96% accuracy for active versus 85% for passive nonreversible sentences, with faster processing for active sentences. | Isolated auditory sentences in laboratory tasks. | Active voice has support as a soft default, not as a universal ban on passive voice in coherent documents. |
| [Sayfi et al., 2024 randomized trial](https://www.sciencedirect.com/science/article/pii/S0895435623003037) | Among 488 adults, a plain-language redesign improved comprehension of one vaccine recommendation by 19.8 points but improved another by a nonsignificant 3.9 points. | Multi-component redesign and an online English-speaking sample. | Plain language can help substantially, but the same intervention's effect depends on the source and audience. |
| [Personalized Benchmarking, ACL 2026](https://aclanthology.org/2026.findings-acl.31/) | Personalized rankings for 115 active Chatbot Arena users correlated only `rho=.04` on average with aggregate rankings; 57% were near-zero or negative. | Small, self-selected power-user population and model-level rankings rather than sentence edits. | There is no single universal prose preference. Explicit audience and user voice should outrank generic rules. |

### Confirmed synthesis

- Prompt instructions and formatting can materially change model behavior.
- The effect varies with model, prompt, task, and number of simultaneous constraints.
- More context can reduce task performance even when the relevant material is retrievable.
- Some Strunk principles, such as preferring active constructions when they aid comprehension, have empirical support as defaults.
- Plain-language redesign can improve comprehension, but benefits vary by document and audience.
- Holistic ratings, readability formulas, and LLM judges are biased or noisy unless decomposed and human-calibrated.
- Neither installs, stars, token count, nor adherence to a famous style manual demonstrates reader benefit.

### Inference

The project has a plausible mechanism: a reminder may shift model prose. Its incremental value is unknown, and the full-reference path is likely over-scoped for routine use. The broad trigger also conflicts with the central fact that useful style depends on audience and genre.

The short 18-rule card is the part most likely to offer a favorable cost/benefit ratio. The long reference is better treated as an optional lookup source for a detected editorial problem, not as standard generation context. A separate revision pass is more defensible than asking the generation pass to satisfy the task plus dozens of style constraints at once.

## Recommended decision and test plan

### Recommendation

Keep the fork if the goal is a portable, optional Strunk reference. Do not rely on it as the sole or universal writing-quality mechanism.

For a stronger system:

1. Narrow the skill to explicit drafting, copyediting, or review of substantial human-facing prose. Ordinary conversational answers should not automatically load a handbook.
2. Replace universal rhetoric with a compact operational core: preserve facts; establish audience and genre; prefer concrete, direct language; cut redundancy; retain useful qualifiers; preserve the writer's voice; use passive voice when the actor is unknown or irrelevant.
3. Give user, project, audience, factual, accessibility, and genre requirements explicit precedence over Strunk.
4. Retrieve only the relevant reference section for a detected problem. Accurately label the bundled text as abridged and edited.
5. Route UI copy, technical documentation, marketing, and anti-AI cleanup to specialist guidance rather than forcing one manual across all four.
6. Add Vale for deterministic repository prose rules, with a small reviewed rule set and inline suppression for legitimate exceptions.
7. Add trigger and output evals before making stronger effectiveness claims.

### Minimum credible eval

Build 30–50 representative tasks spanning documentation, PR and commit text, error/UI copy, technical explanations, reports with numbers and qualifiers, and revision requests. Include hard negative trigger cases such as code generation, terse factual answers, and content where a generic style pass would be harmful.

Compare at least:

1. No style intervention.
2. Current short skill only.
3. Current short skill plus full reference.
4. A compact audience/voice-preserving instruction.
5. Compact instruction plus a Vale-informed revision pass.
6. Relevant specialist skill for the genre.

Run natural-trigger and explicit-invocation tests separately. Hold the model, reasoning effort, inputs, and tools constant; run multiple samples per condition. The Agent Skills trigger guide suggests about 20 balanced should-trigger/should-not-trigger prompts and three runs per query as a starting point. [Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)

Use blinded, randomized human pairwise review for:

- factual and numerical preservation;
- required-content retention;
- clarity and actionability for the intended reader;
- concision without lost nuance;
- voice and genre fit;
- overall preference.

Add deterministic measurements such as severe Vale findings per 1,000 words, output tokens, latency, cost, and atomic fact/qualifier retention. Calibrate any LLM judge against human labels, report ties, and test for position and verbosity bias.

Predeclare a practical threshold. If the full reference does not produce a reproducible reader-preference or task-success gain over the compact condition, keep it as optional source material and stop loading it during normal writing. That result would still leave the project useful as a portable edition; it would simply avoid claiming an unmeasured capability.
