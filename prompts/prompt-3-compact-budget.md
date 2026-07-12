# Prompt 3 — Compact token budget

Strategy: optimise for the chat tools' real bottleneck — the context cap. Three files only,
hard token budget, density over completeness. Tests whether a small pack that always fits
(with headroom for conversation) beats bigger, more complete packs.

```text
You are generating a MINIMAL context pack for this Spring Boot microservice, optimised
for AI chat tools with tight context windows (GitLab Duo, Microsoft Copilot). The whole
pack must be attachable to one fresh chat session while leaving most of the context
window free for the actual conversation.

HARD BUDGET: the entire pack must total under 2,500 lines-equivalent of ~8k tokens —
target ~6k. Density is the design goal: every line must earn its place. Use tables,
compressed notation and abbreviations defined once in the header. No prose paragraphs
where a table row will do. No generic Spring Boot explanations — the reader AI already
knows Spring Boot; document only what is specific to THIS service.

Explore the full repository first. Then create docs/context-pack-v3/ with exactly 3 files:

1. SERVICE-MAP.md — the single dense knowledge file:
   - Header: service purpose in 2 lines; generation date + commit hash; notation legend.
   - PACKAGES: table of package -> role (one line each).
   - FLOW: text diagram(s) of the main runtime flows through the layers.
   - API: table of every endpoint — method | path | purpose | key request fields | key
     response fields | errors. Compress field lists (name:type).
   - DATA: table of entities — name | table | key fields | relations | notes.
   - CONVENTIONS: bullet list of the rules that actually matter here (layering, DTO
     mapping, error handling, logging, validation, transactions) + a table of reusable
     utility classes (class | package | use it for).
   - CONFIG: profiles table; properties that matter (property | effect); secret-injection
     mechanism in one line (never values).
   - DEPLOY: build->deploy pipeline in <=10 bullets; what to touch for a new endpoint or
     config value.
   - TESTS: layers table (layer | tooling | run command | base classes).
   - GOTCHAS: numbered list, one line each, most dangerous first.
2. AI-WORKFLOW.md — chat-AI operating instructions, compressed but complete:
   - Preamble: the attached files are the source of truth; four-phase workflow is
     mandatory; no implementation code before the plan is APPROVED.
   - PLAN: reply to any change request with only a plan doc — goal/scope, assumptions &
     open questions, affected-files table (path | create/modify/delete | why), runtime
     execution flow of the change, numbered no-code steps (app compiles after each),
     test plan, config/deploy impact, rollback & risks — ending "Reply with corrections,
     or APPROVED to start."
   - REFINE: on feedback re-issue the FULL plan, bump DRAFT version, one-line changelog.
   - EXECUTE: after APPROVED, one step per "next step": restate step + files, complete
     paste-ready code with placement markers, verify command, done/pending checklist.
     Pasted error => fix current step only.
   - Rules: never invent files/classes/endpoints — ask; real code beats the pack, say so
     when they conflict; one step per response unless told "implement remaining steps".
3. INDEX.md — max 20 lines: what the two files above are, how to attach them, date +
   commit hash.

QUALITY RULES
- Exact class/package/endpoint/property names only; a statement that could describe any
  Spring Boot service is a defect.
- Facts only from the code; mark gaps "UNKNOWN — verify with team".
- Never include secrets, credentials, real hostnames/IPs or personal data.

VERIFY BEFORE FINISHING
- Confirm every named class/endpoint/property exists in the repo.
- Print total line count and estimated token count per file; if over budget, cut the
  least load-bearing content and say what you cut.
```
