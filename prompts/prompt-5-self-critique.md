# Prompt 5 — Generate, self-test, patch

Strategy: same content goals as the structured spec, but with an explicit adversarial
self-review phase — the generator must answer realistic developer questions and plan a real
change using ONLY its generated files, then patch every gap it finds. Tests whether a
verification loop measurably improves pack quality over a single pass.

```text
You are generating an AI context pack for this Spring Boot microservice in THREE explicit
phases. Do not merge the phases. The pack will be attached to context-capped chat AIs
(GitLab Duo / Microsoft Copilot) that cannot browse the repo.

PHASE A — INVENTORY (do not write pack files yet)
Explore the repository completely. Produce (to the console, not files) an inventory:
packages and roles; every REST endpoint; entities and relations; external integrations;
profiles and key properties; test layers; deployment mechanism; utility classes;
surprising/fragile areas. This inventory is your completeness checklist for Phase B.

PHASE B — GENERATE
Create docs/context-pack-v5/ with:
1. MANIFEST.md — file list + purpose, generation date, git commit hash, how to use the
   pack (attach MANIFEST + AI-WORKFLOW + task-relevant files to a fresh session).
2. SERVICE-OVERVIEW.md — purpose, responsibilities, key business flows, consumers/
   producers.
3. ARCHITECTURE.md — package roles, dependency map, upstream/downstream calls, text
   diagram of main runtime flows.
4. API-CONTRACTS.md — all endpoints (method | path | purpose | condensed req/resp
   fields | errors) + messaging contracts if any + error-handling conventions.
5. DATA-MODEL.md — entities, key fields, relations, migrations, non-obvious persistence
   behaviour.
6. CONVENTIONS.md — this repo's layering, naming, DTO/entity rules, error handling,
   logging, validation, transactions; reusable utilities (exact class + package).
7. CONFIG-PROFILES.md — profiles, important properties, flags, secret-injection
   mechanism only.
8. DEPLOYMENT.md — pipeline, image build, manifests, probes/resources, route patterns,
   what to touch for new config/endpoints.
9. TESTING.md — layers, base classes/utilities, run commands, conventions, fixtures.
10. GOTCHAS.md — pitfalls, fragile areas, tech debt; specific and honest.
11. AI-WORKFLOW.md — chat-AI operating instructions enforcing:
    PLAN (only a plan document for any change request: goal & scope, assumptions & open
    questions, affected-files table with change type and reason, runtime execution flow,
    numbered code-free steps compilable after each, test plan, config/deploy impact,
    rollback & risks; ends asking for corrections or APPROVED) ->
    REFINE (full re-issued plan, bumped DRAFT version, one-line changelog) ->
    APPROVE (no implementation code before the literal reply APPROVED) ->
    EXECUTE (one step per "next step": complete paste-ready code with placement markers,
    verify command, done/pending checklist; pasted errors fix the current step only).
    Rules: never invent files/classes/endpoints — ask; real code beats the pack, say so
    on conflict; one step per response unless told "implement remaining steps".
Constraints: max 800 lines/file (aim well under); tables/bullets over prose; exact names
only; facts only from code, gaps marked "UNKNOWN — verify with team"; never include
secrets, credentials, real hostnames/IPs, or personal data.

PHASE C — ADVERSARIAL SELF-TEST, THEN PATCH
Now simulate being GitLab Duo: you may use ONLY the files in docs/context-pack-v5/ (no
other repository knowledge) to do the following. Be honest — the goal is to find gaps.
1. Answer these 8 developer questions from the pack alone:
   - What does this service do and who calls it?
   - What is the full list of endpoints and where is <pick one> implemented?
   - How do I add a field to <pick a real entity> including migration?
   - What is the error response format and where is it produced?
   - How do I add and inject a new config property for one environment only?
   - How do I run the integration tests?
   - Which utility should I use for <pick something CONVENTIONS.md covers>?
   - What's the riskiest area of this codebase?
2. Produce a full PLAN document (per AI-WORKFLOW.md) for one realistic feature: pick a
   plausible small feature for this service and plan it from the pack alone.
3. Grade yourself: for every question or plan section where the pack was insufficient,
   ambiguous, or wrong versus the real code, list the defect.
4. PATCH the pack files to fix every defect found. Re-run the check on patched areas.
5. Print a final report: defects found and fixed | file sizes | confirmation that no
   secrets/hostnames are present and every named symbol exists in the repo.
```
