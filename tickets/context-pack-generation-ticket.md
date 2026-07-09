# Jira ticket — Context pack generation (copy-paste into Jira)

---

## Summary

Generate AI context pack + agentic workflow guide for `<SERVICE-NAME>` using Claude Code

## Issue type / classification

- **Type:** Task (Enabler)
- **Labels:** `ai-enablement`, `context-pack`, `spike`
- **Component:** `<SERVICE-NAME>`

## Description

### Background

Most of the team uses GitLab Duo / Microsoft Copilot in chat mode. These tools have no
systematic knowledge of our services and a per-session context cap, so answers are generic
and every session starts from zero.

This ticket uses Claude Code (licensed developers only) to generate a **context pack** for
`<SERVICE-NAME>`: a small set of Markdown files that any developer can attach to a fresh
Duo or Copilot session so the AI understands the service immediately. The pack also
includes an **AI workflow guide** (`AI-WORKFLOW.md`) that instructs the chat AI to work
like an agentic tool: produce a **plan document** first (affected files, execution flow,
step-by-step changes), refine it with the developer, wait for **explicit approval**, and
then implement the plan **one step at a time** on request — never dumping the whole code
change at once.

### Instructions for the assignee (Claude Code licence holder)

1. Clone / open the `<SERVICE-NAME>` repository locally and check out the latest `main`.
2. Start Claude Code at the repository root.
3. Paste the full prompt from the **"Claude Code prompt"** section below and let it run to completion.
4. Review the generated files under `docs/context-pack/`:
   - spot-check factual accuracy (endpoints, entities, module names) against the code;
   - confirm **no secrets, credentials, tokens, internal hostnames/IPs, or personal data** appear anywhere;
   - confirm each file respects the size limit stated in the prompt.
5. Commit the `docs/context-pack/` folder to a branch and raise an MR for the service team to review.
6. Attach one generated file (e.g. `ARCHITECTURE.md`) to a fresh GitLab Duo session and a fresh Copilot session to confirm the files load without truncation. Note the result in a comment on this ticket.

### Acceptance criteria

- [ ] `docs/context-pack/` exists in the service repo and contains all files listed in the prompt (including `AI-WORKFLOW.md` and `MANIFEST.md`).
- [ ] `MANIFEST.md` records the generation date and the git commit hash the pack was generated from.
- [ ] Every file is within the size limit defined in the prompt.
- [ ] No secrets, credentials, internal hostnames/IPs, or personal data in any file (checked by assignee and by MR reviewer).
- [ ] Factual spot-check passed by a developer who knows the service.
- [ ] Pack files load successfully into a fresh GitLab Duo session and a fresh Copilot session (no truncation), evidence attached as a ticket comment.
- [ ] MR merged to `main`.

---

## Claude Code prompt

Paste everything between the lines below into Claude Code at the repository root.

```text
You are generating an "AI context pack" for this repository — a Spring Boot microservice
deployed to an on-premise OpenShift platform. The pack will be attached to fresh GitLab Duo
or Microsoft Copilot CHAT sessions (context-capped, non-agentic tools) so they can help
developers work on this service effectively. Write for an AI reader that has NEVER seen
this codebase and will NOT be able to browse it.

Explore the entire repository systematically before writing anything: build files, source
tree, resources/configuration, tests, OpenShift/deployment manifests, pipeline definitions,
and any existing documentation.

OUTPUT
Create the folder docs/context-pack/ containing exactly these files:

1. MANIFEST.md — generation date, git commit hash generated from, one-line description of
   each file in the pack, and a short "how to use this pack" note (attach MANIFEST.md +
   AI-WORKFLOW.md + the files relevant to your task to a fresh chat session).
2. SERVICE-OVERVIEW.md — purpose of the service, business responsibilities, key business
   flows end-to-end, owning team, main consumers and producers.
3. ARCHITECTURE.md — module/package layout with the role of each package, internal
   dependency map, upstream/downstream services and how they are called (REST, messaging,
   etc.), and a text-based diagram of the main request flow through the layers
   (e.g. controller -> service -> repository -> external calls).
4. API-CONTRACTS.md — every REST endpoint: method, path, purpose, request/response shape
   (field names and types, condensed — not full JSON schemas), error responses and the
   service's error-handling conventions. Include message/event contracts if the service
   consumes or publishes any.
5. DATA-MODEL.md — entities/tables, their key fields and relationships, how migrations are
   managed, and any non-obvious persistence behaviour (caching, soft deletes, auditing).
6. CONVENTIONS.md — how code is written in THIS repo: layering rules, naming patterns, DTO
   vs entity usage, error handling, logging, validation, transaction boundaries, common
   utility classes an AI should reuse instead of reinventing (name them with their
   packages).
7. CONFIG-PROFILES.md — Spring profiles and what each is for, the important configuration
   properties and what they control, feature flags, and HOW secrets are injected (mechanism
   only — never values or locations).
8. DEPLOYMENT.md — how the service is built and deployed to OpenShift: pipeline stages,
   image build, manifests/templates used, resources/probes/scaling, routes (pattern only,
   no real hostnames), and what a developer must touch when adding config or a new
   endpoint.
9. TESTING.md — test layers present (unit/integration/contract/etc.), key test utilities
   and base classes, how to run each layer, conventions for writing new tests, and where
   test fixtures live.
10. GOTCHAS.md — known pitfalls, surprising behaviour, tech debt, fragile areas, and things
    a newcomer (human or AI) would get wrong. Be honest and specific.
11. AI-WORKFLOW.md — the operating instructions for the chat AI. Write this file EXACTLY as
    specified in the "AI-WORKFLOW.md SPECIFICATION" section below, adapting the examples to
    this service.

HARD CONSTRAINTS
- Each file must be at most 800 lines and aim for well under that; if a topic genuinely
  needs more, split into a second file named e.g. API-CONTRACTS-2.md and note the split in
  MANIFEST.md. Small enough to attach to a context-capped chat session is the priority.
- Markdown only. Prefer tables and short bullet lists over prose. No decorative content.
- Every statement must be derived from the actual code. If something cannot be determined
  from the repo, write "UNKNOWN — verify with the team" rather than guessing.
- NEVER include: secrets, credentials, tokens, API keys, real internal hostnames or IPs,
  certificate contents, or personal data. Refer to such values by mechanism ("injected via
  OpenShift secret") only.
- Use exact class/package/file names so a chat AI can tell the developer precisely where
  to make changes.

AI-WORKFLOW.md SPECIFICATION
This file is addressed to the chat AI (Duo/Copilot) and instructs it to behave like an
agentic assistant with distinct PLAN -> REFINE -> APPROVE -> EXECUTE phases. It must
contain:

  a) Role preamble: "You are assisting a developer on the <service> Spring Boot
     microservice. The attached context-pack files are your source of truth about this
     codebase. You must follow the four-phase workflow below for every code-change
     request. Never skip a phase. Never output implementation code before the plan is
     explicitly approved."

  b) PHASE 1 — PLAN: when the developer describes a task, respond ONLY with a plan
     document using exactly this structure:
       ## Plan: <task title>            (status: DRAFT v1)
       1. Goal & scope — what changes, and explicitly what is out of scope
       2. Assumptions & open questions — anything uncertain the developer must confirm
       3. Affected files — a table: file path | change type (create/modify/delete) | why
       4. Execution flow — how the change flows through the layers at runtime
          (e.g. Controller -> Service -> Repository -> external call), and how the new
          code integrates with existing classes named in the context pack
       5. Step-by-step changes — numbered steps, each small enough to implement and
          verify independently; each step names its files and describes the change in
          1-3 sentences (NO code yet); the application must compile after every step
       6. Test plan — tests to add/update per step and how to run them
       7. Config & deployment impact — Spring profiles/properties, OpenShift manifests
       8. Rollback & risks — how to revert; what could break
     End every plan with: "Review this plan. Reply with corrections to refine it, or
     reply APPROVED to begin implementation."

  c) PHASE 2 — REFINE: when the developer replies with feedback, output the FULL updated
     plan (not a diff of it) with the version bumped (DRAFT v2, v3 ...) and a one-line
     changelog at the top. Repeat until approved.

  d) PHASE 3 — APPROVE: implementation may begin ONLY after the developer replies
     APPROVED. If the developer asks for code before approval, restate that the plan
     needs approval first and ask what to refine.

  e) PHASE 4 — EXECUTE, step by step: after approval, implement ONE step at a time.
     When the developer says "implement step N" (or "next step"):
       - restate the step title and its files;
       - output the complete new content of each affected file section — full method/class
         bodies ready to paste, with clear markers for WHERE in the file the code goes
         (e.g. "add after method X", "replace method Y") — never fragments the developer
         has to guess about;
       - follow the conventions in CONVENTIONS.md and reuse the utilities it names;
       - end with: how to verify this step (compile/test/run command), a progress
         checklist of all steps marked done/pending, and "Reply 'next step' to continue,
         or paste any error output and I will fix this step."
     If the developer pastes an error, fix ONLY the current step and re-output it.

  f) General rules for the AI: never invent files, classes or endpoints not present in
     the context pack or the attached code — ask instead; if the context pack seems to
     contradict the actual code the developer shows you, trust the code and say so; keep
     answers scoped to the current step; never combine multiple steps into one response
     even if asked to hurry, unless the developer explicitly says "implement remaining
     steps".

VERIFY BEFORE FINISHING
- Re-read each generated file and check every class/endpoint/property it mentions exists
  in the repo.
- Check file sizes against the limit.
- Scan all files for secrets/hostnames/credentials one final time.
- Print a summary table: file name | line count | topics covered.
```

---

## Notes for the reporter (not part of the ticket)

- Replace `<SERVICE-NAME>` in the summary/description before creating the ticket.
- Create one ticket per service; the prompt is service-agnostic and unchanged each time.
- Estimated effort: ~1–2 h including review and the Duo/Copilot load check.
