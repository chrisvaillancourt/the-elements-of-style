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

Edit for the reader with Strunk's rules. Treat them as defaults: meaning, accuracy, house style and the writer's voice outrank them.

## Procedure

1. **Target.** Note the audience, purpose, genre (Slack DM, PR description, README, error text) and any voice or format the user gave.
2. **Protect.** Never change code, commands, paths, identifiers, quoted text, numbers, units, dates, names, links, required templates, or the qualifiers that set a claim's strength ("may", "about", "not yet", "in 3 of 12 runs").
3. **Structure.** Lead with the point or the ask. One topic per paragraph or bullet (R8, R9). Parallel form for list items and headings (R15).
4. **Sentences.** Cut needless words (R13). Make the actor the subject when the actor matters (R10). Prefer positive statements without changing what is claimed (R11). Use specific words you can support (R12). Keep modifiers beside what they modify (R16). End on the word that matters (R18). Break up runs of "X, and Y" sentences (R14).
5. **Mechanics.** Fix comma splices (R5), dangling openers (R7), serial and paired commas (R2, R3) and misused words.
6. **Verify.** Every protected item survives. No claim got stronger, weaker or newly invented. The result is clearer or shorter, not just different. If a fix needs a fact you don't have, keep the original wording or ask.
7. **Output.** Return the revised text. List changes only when asked, or when you changed meaning-bearing wording on purpose.

For a short message, steps 2, 4 and 6 are enough.

## Gotchas: where the 1918 text misleads modern technical prose

- Use singular *they*; ignore the guide's generic *he*.
- *Data* follows house style (singular is common in tech writing), not the guide's plural-only rule.
- Never change *shall*, *must*, *should* or *may* in specs or requirements; they can be normative (RFC 2119). Ignore the 1918 shall/will person rules.
- Keep *fix*, *feature*, *factor*, *system*, *state*, *phase* and *case* when they name a technical thing (bug fix, feature flag, state machine, test case).
- Keep *respectively* when it maps items between two lists.
- Opening a sentence with *However* and splitting an infinitive are both fine.
- Not every "there were" or "became X" sentence is passive. Edit for directness, but don't call it passive.
- Positive form must not change claim strength: "not verified" is not "failed". Strunk calls one of his own rewrites "simply a guess at the writer's intention"; don't guess.
- Rule 13 means "make every word tell", not "make every sentence short". Keep necessary detail.
- Don't copy the guide's period spellings or diction (to-day, any one, programme).

## Rules (Strunk's numbering)

Usage: 1 possessive singular adds 's (Charles's) · 2 serial comma · 3 commas on both sides of a parenthetic expression, or neither · 4 comma before a conjunction joining two independent clauses · 5 no comma splice; use a semicolon or period · 6 don't break a sentence in two (an emphatic fragment is allowed) · 7 an opening participial phrase refers to the subject.

Composition: 8 one topic per paragraph · 9 open with the topic sentence · 10 prefer active voice; passive fits when the actor is unknown, unimportant or not the topic · 11 positive form · 12 definite, specific, concrete · 13 omit needless words · 14 avoid a run of loose compound sentences · 15 parallel ideas in parallel form · 16 keep related words together · 17 one tense in summaries · 18 emphatic words at the end.

## Common cuts

- "due to the fact that the cache is cold" → "because the cache is cold"
- "in order to" → "to"; "make a change to" → "change"
- "It is important to note that X" → "X"
- "Postgres, which is our primary store," → "Postgres, our primary store,"
- "there are three jobs that fail" → "three jobs fail"
- "very", "really", "certainly" → cut, or choose a stronger word

## Examples

Commit body
- Before: "This commit makes changes to the retry logic in order to address the issue where requests were being retried in cases where the server returned a 400."
- After: "Stop retrying requests that fail with HTTP 400."

Docs (the reader is the actor)
- Before: "The token must be rotated every 90 days."
- After: "Rotate the token every 90 days."

Keep the passive (the actor is unimportant): "Logs are deleted after 30 days."

Don't do this (it changes the claim)
- Before: "The fix has not been verified in production."
- Bad: "The fix fails in production."
- OK: unchanged.

## References

Paths are relative to this skill's directory. Read only the part you need; a routine edit needs none.

- [references/usage-rules.md](references/usage-rules.md): Rules 1–7 with Strunk's examples (~2.8k tokens). Read it for a punctuation question.
- [references/composition-rules.md](references/composition-rules.md): Rules 8–18 (~7.4k tokens). Find the `### Rule N.` heading and read that section only.
- [references/misused-words.md](references/misused-words.md): 65 entries, one `### Word` heading each (~5.4k tokens). Search for the heading (for example `grep -n -i -A8 '^### data'`) and read that entry.

## Long documents

For a thorough copyedit of a long document (about 1,500 words or more) in a harness with subagents, give a subagent the draft, the audience and genre, the protected items, and absolute paths to this file and the reference files. Pass paths, not the skill name; a subagent may not be able to load skills by name. Ask for the revised text plus a short list of meaning-bearing changes.
