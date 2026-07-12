# Prompt 1 — Structured specification

Strategy: prescribe the exact file set and the contents of every file. Maximum predictability
and completeness; the AI has no freedom over structure.

```text
You are generating an "AI context pack" for this repository — a Spring Boot microservice.
The pack will be attached to fresh GitLab Duo or Microsoft Copilot CHAT sessions
(context-capped, non-agentic tools). Write for an AI reader that has NEVER seen this
codebase and will NOT be able to browse it.

Explore the entire repository systematically before writing anything: build files, source
tree, resources/configuration, tests, deployment manifests, pipelines, existing docs.

OUTPUT — create docs/context-pack-v1/ containing exactly these files:

1. MANIFEST.md — generation date, git commit hash, one-line description of each file, and
   a "how to use this pack" note (attach MANIFEST.md + AI-WORKFLOW.md + files relevant to
   your task to a fresh chat session).
2. SERVICE-OVERVIEW.md — purpose, business responsibilities, key business flows
   end-to-end, main consumers/producers.
3. ARCHITECTURE.md — package layout with each package's role, internal dependency map,
   upstream/downstream services and how they are called, and a text diagram of the main
   request flow through the layers (controller -> service -> repository -> external).
4. API-CONTRACTS.md — every REST endpoint: method, path, purpose, condensed
   request/response shape (field names + types), error responses and error-handling
   conventions. Include message/event contracts if any.
5. DATA-MODEL.md — entities/tables, key fields, relationships, migration mechanism,
   non-obvious persistence behaviour (caching, soft deletes, auditing).
6. CONVENTIONS.md — how code is written in THIS repo: layering rules, naming, DTO vs
   entity usage, error handling, logging, validation, transactions, and utility classes
   an AI should reuse instead of reinventing (exact names with packages).
7. CONFIG-PROFILES.md — Spring profiles and their purpose, important properties, feature
   flags, and HOW secrets are injected (mechanism only — never values).
8. DEPLOYMENT.md — build + deploy pipeline stages, image build, manifests, resources/
   probes, routes (pattern only, no real hostnames), what to touch when adding config or
   an endpoint.
9. TESTING.md — test layers, key test utilities/base classes, how to run each layer,
   conventions for new tests, fixture locations.
10. GOTCHAS.md — known pitfalls, surprising behaviour, tech debt, fragile areas. Honest
    and specific.
11. AI-WORKFLOW.md — operating instructions addressed to the chat AI, containing:
    a) Role preamble: "You are assisting a developer on this Spring Boot microservice.
       The attached context-pack files are your source of truth. Follow the four-phase
       workflow below for every code-change request. Never skip a phase. Never output
       implementation code before the plan is explicitly approved."
    b) PHASE 1 — PLAN: on receiving a task, respond ONLY with a plan document:
         ## Plan: <task title>   (status: DRAFT v1)
         1. Goal & scope (incl. explicit out-of-scope)
         2. Assumptions & open questions
         3. Affected files — table: file path | create/modify/delete | why
         4. Execution flow — how the change flows through the layers at runtime and how
            new code integrates with existing classes named in this pack
         5. Step-by-step changes — numbered, each independently implementable and
            verifiable, files named, 1–3 sentence description, NO code; the app must
            compile after every step
         6. Test plan per step
         7. Config & deployment impact
         8. Rollback & risks
       End with: "Review this plan. Reply with corrections to refine it, or reply
       APPROVED to begin implementation."
    c) PHASE 2 — REFINE: on feedback, re-output the FULL plan, version bumped
       (DRAFT v2, v3…), one-line changelog at top. Repeat until approved.
    d) PHASE 3 — APPROVE: code only after the developer replies APPROVED. If asked for
       code earlier, restate that approval is needed and ask what to refine.
    e) PHASE 4 — EXECUTE step by step: on "implement step N" / "next step": restate the
       step and its files; output complete paste-ready code with placement markers ("add
       after method X", "replace method Y") — never fragments; follow CONVENTIONS.md and
       reuse the utilities it names; end with how to verify the step, a done/pending
       checklist of all steps, and "Reply 'next step' to continue, or paste any error
       output and I will fix this step." On a pasted error, fix ONLY the current step.
    f) General rules: never invent files/classes/endpoints not in the pack or shown code
       — ask instead; if the pack contradicts code the developer shows, trust the code
       and say so; never combine multiple steps into one response unless told
       "implement remaining steps".

HARD CONSTRAINTS
- Max 800 lines per file, aim well under; split into e.g. API-CONTRACTS-2.md if truly
  needed and note it in MANIFEST.md.
- Markdown only. Prefer tables and short bullets over prose.
- Everything derived from actual code; write "UNKNOWN — verify with the team" rather
  than guess.
- NEVER include secrets, credentials, tokens, real hostnames/IPs, or personal data —
  describe mechanisms only.
- Use exact class/package/file names throughout.

VERIFY BEFORE FINISHING
- Re-read each file; confirm every class/endpoint/property it mentions exists in the repo.
- Check sizes against the limit; scan for secrets/hostnames one final time.
- Print a summary table: file | line count | topics covered.
```
