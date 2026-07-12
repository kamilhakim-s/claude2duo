# Prompt v1 — Context File Generation for GitLab Duo / Copilot

**Usage:** Paste everything below the line into a fresh Claude Code session opened at the repo root.
**Tracking:** Record results in `prompts/results-log.md` (which prompt version, which tool tested, pass/fail per test).

---

You are preparing this repository so that weaker AI coding assistants (GitLab Duo in IntelliJ, and Microsoft Copilot which can only receive file attachments) can work on it effectively without your reasoning ability or repo-wide context retrieval.

## Your task

Explore this repository fully, then generate the following files. Do NOT modify any existing source code.

### 1. `docs/ai-context/ARCHITECTURE.md`
A map of the codebase that fits in ~600 words. Must contain:
- One-paragraph purpose of the application
- Module/package structure as a tree with a one-line description per package
- The main runtime flow(s) described step by step (HTTP request → controller → service → repository → DB, plus any async/messaging flows), naming the actual classes involved
- Key domain concepts and invariants (business rules the code enforces)
- Technology stack with versions taken from the build file

### 2. `docs/ai-context/CONVENTIONS.md`
Coding conventions **derived from the actual code, not generic best practice**. Must contain:
- Layering rules (what may call what)
- Naming patterns observed (suffixes, DTO vs entity handling)
- Error handling pattern used, with one short real example referenced by class name
- Testing pattern used (framework, structure, naming, what gets mocked vs real)
- Validation approach

### 3. `docs/ai-context/API-SIGNATURES.md`
A compressed "repo digest": for every public class, list its public method signatures only (no bodies). Group by package. This substitutes for repo-wide retrieval when a tool can only see attached files.

### 4. `docs/ai-context/TASK-TEMPLATE.md`
A fill-in-the-blank prompt template a human will paste into Duo or Copilot to start a task. It must instruct the assistant to:
- Read the attached/open context files first
- Restate its understanding of the relevant flow before writing code
- Propose a plan and wait for approval
- Implement one step at a time
- Finish by listing which context files are now stale
Include placeholders like `{TASK_DESCRIPTION}`, `{FILES_IN_SCOPE}`, `{ACCEPTANCE_CRITERIA}`.

### 5. `docs/ai-context/HANDOVER.md`
An initially near-empty session log with a defined structure (Date / Task / Decisions / Changes / Open questions / Stale docs) and one example entry marked as EXAMPLE.

## Constraints

- Every claim in ARCHITECTURE.md and CONVENTIONS.md must be verifiable against the code. If something is ambiguous, write "UNVERIFIED:" before it.
- Optimise for a model with a SMALL context window: front-load the most important facts, use terse bullet style, no filler prose, no marketing language.
- Each file must be independently useful when attached alone (repeat critical facts like tech stack in a one-line header on each file).
- Use only plain Markdown — no HTML, no mermaid (Copilot attachment rendering is unreliable).
- After generating, print a summary table: file, word count, and the single most important fact it contains.

## Self-check before finishing

Re-read each generated file and answer in your final message:
1. Could a developer who has never seen this repo implement a small change using only these files plus the 2-3 source files in scope?
2. Is anything stated that the code does not support?
3. What is the weakest file and why?
