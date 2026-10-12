---
name: writing-clearly-and-concisely
description: >-
  Copyedits drafts a person will read (Slack or email messages, PR and Jira
  text, docs, commit message bodies, error and UI text) using Strunk's
  Elements of Style (1918). Use when asked to tighten, copyedit, proofread, or
  "Strunk" a draft, and before finalizing such prose. Cuts needless words,
  prefers active voice and concrete terms, and fixes punctuation and word
  misuse. Not for code, routine chat replies, or text that must stay verbatim.
---

# Writing Clearly and Concisely

Edit for the reader with Strunk's rules. Treat them as defaults: meaning, accuracy, house style and the writer's voice outrank them, and the 1918 usage preferences are advice, not proof that accepted modern English is wrong.

## Procedure

1. **Target.** Identify the text to edit. Quotation marks or a fence around the draft don't make it verbatim. Note the audience, purpose, genre (Slack DM, PR description, README, error text), any voice or format the user gave, and the requested depth: proofreading fixes mechanics; copyediting may restructure without changing meaning.
2. **Protect.** Never change code, commands, paths, identifiers, placeholders, attributed quotations or other spans the user marks as verbatim, numbers, units, dates, names, links, required templates, or the wording that sets a claim's strength or a requirement's level ("may", "about", "not yet", "in 3 of 12 runs", "must", "MUST NOT").
3. **Structure.** Lead with the point or the ask. One topic per paragraph or bullet (R8, R9). Parallel form for list items and headings (R15).
4. **Sentences.** Cut needless words (R13). Make the actor the subject when the actor matters (R10). Prefer positive statements without changing what is claimed (R11). Use specific words you can support (R12). Keep modifiers beside what they modify (R16). End on the word that matters (R18). Break up runs of "X, and Y" sentences (R14).
5. **Mechanics.** Fix comma splices (R5), dangling openers (R7), serial and paired commas (R2, R3) and misused words.
6. **Verify.** Every protected item survives. No claim got stronger, weaker or newly invented. The result is clearer or shorter, not just different. If a fix needs a fact you don't have, keep the original wording or ask.
7. **Output.** Return the revised text, or the original if no change improves it. Flag an unresolved meaning question rather than silently choosing an interpretation. List changes only when asked, or when you changed meaning-bearing wording on purpose.

For a short message, do these checks in one pass, but keep the audience, protect, mechanics and verify checks.

## Gotchas: where the 1918 text misleads modern technical prose

- Use singular *they*; ignore the guide's generic *he*.
- *Data* follows house style (singular is common in tech writing), not the guide's plural-only rule.
- Preserve requirement levels, negation and modal wording (*must*, *shall*, *should*, *may*, including uppercase RFC 2119 forms) unless the user asks to change the requirement. Ignore the 1918 shall/will person rules.
- Keep *fix*, *feature*, *factor*, *system*, *state*, *phase* and *case* when they name a technical thing (bug fix, feature flag, state machine, test case).
- Keep *respectively* when it maps items between two lists.
- Opening a sentence with *However* and splitting an infinitive are both fine.
- Not every "there were" or "became X" sentence is passive. Edit for directness, but don't call it passive.
- Positive form must not change claim strength: "not verified" is not "failed". Strunk calls one of his own rewrites "simply a guess at the writer's intention"; don't guess.
- Rule 13 means "make every word tell", not "make every sentence short". Keep necessary detail.
- Rule 17 is about the narrative frame of a summary. Keep tense changes that separate past events, current state and future plans ("we deployed yesterday; errors are falling; we'll review tomorrow").
- Use the document's current variety of English (US or UK); don't import historical spellings such as *to-day*.

## Rules (Strunk's numbering)

Apply the rules that are relevant; not every sentence needs changing.

- R1. Possessive singular adds 's (Charles's).
- R2. Serial comma in a series of three or more.
- R3. Commas on both sides of a parenthetic expression, or neither.
- R4. Comma before a conjunction joining two independent clauses.
- R5. No comma splice; use a semicolon or a period.
- R6. Don't break a sentence in two (an emphatic fragment is allowed).
- R7. An opening participial phrase refers to the grammatical subject.
- R8. One topic per paragraph.
- R9. Open a paragraph with its topic sentence.
- R10. Prefer active voice; passive fits when the actor is unknown, unimportant or not the topic.
- R11. Put statements in positive form.
- R12. Use definite, specific, concrete language.
- R13. Omit needless words.
- R14. Avoid a run of loose compound sentences.
- R15. Express parallel ideas in parallel form.
- R16. Keep related words together.
- R17. Keep one tense in a summary's narrative.
- R18. Put the emphatic words at the end.

## Common cuts

- "due to the fact that the cache is cold" → "because the cache is cold"
- "in order to" → "to"; "make a change to" → "change"
- "It is important to note that X" → "X"
- "Postgres, which is our primary store," → "Postgres, our primary store,"
- "there are three jobs that fail" → "three jobs fail"
- Cut empty intensifiers, but keep words that express probability, degree, contrast or deliberate emphasis ("very likely" is not "likely"). Don't strengthen a claim to make it punchier.

## Examples

Slack request (keep the politeness and the uncertainty)
- Before: "I wanted to ask if you could take a look at the rerun when you have a chance. It may still fail in production."
- After: "Could you review the rerun when you have a chance? It may still fail in production."

Commit body
- Before: "This commit makes changes to the retry logic in order to stop retrying requests in cases where the server returned a 400."
- After: "Stop retrying requests that fail with HTTP 400."

Docs (the context establishes that the reader rotates the token)
- Before: "The token must be rotated every 90 days."
- After: "You must rotate the token every 90 days."

Keep the passive (the actor is unimportant): "Logs are deleted after 30 days."

Don't do this (it changes the claim)
- Before: "The fix has not been verified in production."
- Bad: "The fix fails in production."
- OK: unchanged.

## References

Paths are relative to this skill's directory. Read only the part you need; a routine edit needs none. To read one rule or entry, search the file for its heading and read up to the next heading of the same level.

- [references/usage-rules.md](references/usage-rules.md): Rules 1–7 with Strunk's examples (~2.8k tokens). Find the `### Rule N.` heading.
- [references/composition-rules.md](references/composition-rules.md): Rules 8–18 (~7.4k tokens). Find the `### Rule N.` heading.
- [references/misused-words.md](references/misused-words.md): 65 entries, one `### Word` heading each (~5.4k tokens). Find the entry's heading, for example `### Data`.

## Long documents

Edit inline by default, a coherent section at a time, then make one consistency pass over the whole. A long document doesn't by itself justify reading a whole reference file. If the harness supports subagents and the size justifies one, give it a single bounded editing assignment: the draft, relevant context, audience, voice and house style, requested depth, protected spans, the output you want, and absolute paths to this file and the reference files (a subagent may not be able to load skills by name). Tell it not to delegate further. Check its revision against the original before delivering it.
