# Test Protocol — Evaluating Generated Context Files in Duo / Copilot

Run this after Claude Code has generated `docs/ai-context/` from a prompt version. Always use a **fresh session** in the tool under test.

## Setup per run

1. Note the prompt version used (v1, v2, ...).
2. GitLab Duo: open the repo in IntelliJ, open only the context files + the task's in-scope source files as tabs.
3. Copilot: attach the context files (and in-scope source files) to a fresh chat.

## Standard test tasks (run all three per tool)

**T1 — Comprehension (no code)**
Paste TASK-TEMPLATE.md filled with: "Explain how a transfer request flows through this application and which business rules can reject it. Do not write code."
Pass = names the correct classes in order and lists all rejection rules without hallucinating classes.

**T2 — Small change**
Task: "Add a `description` field (max 140 chars, optional) to transfers. It must be persisted and returned in the response."
Pass = correct files identified from API-SIGNATURES.md alone, validation follows the pattern in CONVENTIONS.md, a test is proposed matching the existing test style.

**T3 — Rule change with a trap**
Task: "Reject transfers over 10,000. Where does this belong?"
Pass = puts the rule in the service layer (per CONVENTIONS.md layering), not in the controller, and mentions updating the context docs afterwards.

## Scoring

| Run | Prompt ver | Tool | T1 | T2 | T3 | Hallucinated class/file? | Notes |
|-----|-----------|------|----|----|----|--------------------------|-------|
|     |           |      |    |    |    |                          |       |

Score each T as 0 (fail), 1 (partial), 2 (pass). A prompt version "wins" when its files produce ≥10/12 across both tools with zero hallucinated classes.

## What to tweak between prompt versions

- If T1 fails → ARCHITECTURE.md flow section too vague; demand class-by-class flow.
- If T2 picks wrong files → API-SIGNATURES.md too long or unstructured; tighten grouping.
- If T3 puts logic in the controller → CONVENTIONS.md layering rules not explicit enough.
- If the tool ignores the docs entirely → strengthen TASK-TEMPLATE.md's "read context first, restate understanding" step.
