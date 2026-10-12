"""Split elements-of-style.md into three reference files, text verbatim.

Usage:
    git show 05fc4f0:skills/writing-clearly-and-concisely/elements-of-style.md > eos.md
    uv run python scripts/split-reference.py eos.md skills/writing-clearly-and-concisely/references

Sections II, III and V go to usage-rules.md, composition-rules.md and
misused-words.md. Section V entries change from "**Word.** text" to
"### Word" + text so one grep finds one entry. Everything before Section II
(title, contents block, paraphrased introduction) is dropped. After writing,
the script re-reads the files and checks that the bodies rebuild the original
sections exactly. See docs/fork-changes.md.
"""

import re
import sys
from pathlib import Path

src, out = Path(sys.argv[1]), Path(sys.argv[2])
lines = src.read_text().splitlines()

def find(prefix):
    return next(i for i, l in enumerate(lines) if l.startswith(prefix))

usage_start = find("## II. ")
comp_start = find("## III. ")
words_start = find("## V. ")

usage = lines[usage_start:comp_start]
comp = lines[comp_start:words_start]
words = lines[words_start:]

ENTRY = re.compile(r"^\*\*([^*]+)\.\*\*(?: (.*))?$")

def to_headings(block):
    result = []
    for line in block:
        m = ENTRY.match(line)
        if m:
            result.append(f"### {m.group(1)}")
            if m.group(2) is not None:
                result += ["", m.group(2)]
        else:
            result.append(line)
    return result

def from_headings(block):
    result, i = [], 0
    while i < len(block):
        line = block[i]
        if line.startswith("### "):
            name = line[4:]
            if i + 2 < len(block) and block[i + 1] == "" and block[i + 2] and not block[i + 2].startswith(("|", "### ")):
                result.append(f"**{name}.** {block[i + 2]}")
                i += 3
                continue
            result.append(f"**{name}.**")
        else:
            result.append(line)
        i += 1
    return result

PROVENANCE = (
    "_From William Strunk Jr., *The Elements of Style* (1918), public domain "
    "(Project Gutenberg #37134). Text unchanged; this edition is abridged. "
    "Where 1918 usage misleads modern technical prose, the Gotchas in "
    "SKILL.md take precedence._"
)

rule_heads = lambda block: [l[4:] for l in block if l.startswith("### Rule ")]

def write(name, title, contents, body):
    text = [f"# {title}", "", PROVENANCE, "", "## Contents", "", *contents, "", *body]
    (out / name).write_text("\n".join(text).rstrip("\n") + "\n")
    return text

out.mkdir(parents=True, exist_ok=True)
header_len = {}
for name, title, block in [
    ("usage-rules.md", "Elementary Rules of Usage (Rules 1–7)", usage),
    ("composition-rules.md", "Elementary Principles of Composition (Rules 8–18)", comp),
]:
    contents = [f"- {h}" for h in rule_heads(block)]
    write(name, title, contents, block)
    header_len[name] = 6 + len(contents) + 1

word_body = to_headings(words)
entries = [l[4:] for l in word_body if l.startswith("### ")]
write("misused-words.md", "Words and Expressions Commonly Misused",
      [" · ".join(entries)], word_body)
header_len["misused-words.md"] = 8

# Round-trip check: the three bodies rebuild the original sections II-V.
def body(name):
    return (out / name).read_text().splitlines()[header_len[name]:]

rebuilt = body("usage-rules.md") + [""] + body("composition-rules.md") + [""] + from_headings(body("misused-words.md"))
original = lines[usage_start:]
while original and original[-1] == "":
    original.pop()
assert rebuilt == original, next(
    (i, a, b) for i, (a, b) in enumerate(zip(rebuilt, original)) if a != b
) if len(rebuilt) == len(original) else (len(rebuilt), len(original))
print(f"ok: {len(entries)} entries, {len(rule_heads(usage))} usage rules, "
      f"{len(rule_heads(comp))} composition rules; round-trip exact")
