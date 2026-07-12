# Context pack — transfer-service

Generated: 2026-07-12 · commit `b225393` · generator prompt: prompt-5-self-critique (Phase B identical to prompt-1 spec)

## How to use this pack
Attach `MANIFEST.md` + `AI-WORKFLOW.md` + the files relevant to your task to a **fresh**
GitLab Duo or Copilot chat session. For code changes always include `CONVENTIONS.md` and
`ARCHITECTURE.md`.

## Files

| File | Contents |
|---|---|
| SERVICE-OVERVIEW.md | Purpose, business flow, rules the service enforces |
| ARCHITECTURE.md | Package roles, dependency map, request flow diagram |
| API-CONTRACTS.md | The REST endpoint, request/response shapes, error behaviour |
| DATA-MODEL.md | Account and Transfer entities, relationships, schema management |
| CONVENTIONS.md | Layering, naming, error handling, validation, transaction rules |
| CONFIG-PROFILES.md | Spring configuration (no profiles exist), datasource |
| DEPLOYMENT.md | Build; deployment is not defined in this repo (marked UNKNOWN) |
| TESTING.md | Test approach, base setup, how to run |
| GOTCHAS.md | Pitfalls: concurrency, ddl-auto, 404-vs-REJECTED semantics |
| AI-WORKFLOW.md | Mandatory 4-phase workflow for the chat AI (plan → refine → approve → execute) |
| SELF-TEST-REPORT.md | Phase C adversarial self-test: defects found in the pack and the patches applied (not needed in chat sessions) |
