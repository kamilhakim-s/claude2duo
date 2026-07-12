# Prompt 4 — Task cookbook

Strategy: organise the pack around what developers DO rather than what the service IS —
task recipes and anticipated Q&A instead of reference documentation. Tests whether chat AIs
follow procedural recipes better than they synthesise from reference material.

```text
You are generating a TASK-ORIENTED context pack for this Spring Boot microservice, to be
attached to GitLab Duo / Microsoft Copilot chat sessions. Developers don't ask chat AIs
"describe the architecture" — they ask "add an endpoint that does X". So structure this
pack around tasks and questions, not around reference chapters.

Explore the entire repository first: source, config, tests, deployment, pipelines. Pay
special attention to PATTERNS — find 2–3 existing examples of each common change type and
distil how this repo does it.

Create docs/context-pack-v4/ with exactly these files:

1. INDEX.md — file list with when to attach which; generation date + commit hash.
2. SERVICE-BRIEF.md (max 150 lines) — the minimum orientation: what the service does,
   package map (table), main runtime flow diagram, entity list (table), endpoint list
   (table: method | path | purpose only). Just enough to anchor the recipes.
3. RECIPES.md — the core file. For EACH common change type in this repo, a recipe distilled
   from real existing examples:
     - Add a new REST endpoint (query)   - Add a new REST endpoint (mutation)
     - Add a field to an existing entity + migration
     - Add a new entity/table end-to-end
     - Call another service / external API
     - Add a configuration property / feature flag
     - Add validation to a request
     - Handle a new error case
     - Add a scheduled/async job (if the repo has the pattern)
   Each recipe: WHEN to use it; FILES touched in order (table: order | file/package |
   what you do there); a WORKED EXAMPLE pointing at real classes in this repo that
   exemplify the pattern ("PaymentController.getPayment is the reference query
   endpoint"); PITFALLS specific to this repo. Skip recipe types the repo has no pattern
   for and say so.
4. FAQ.md — 20–30 questions a developer (or their AI) would actually ask, with precise
   answers naming real classes/properties: "Where do I register a new endpoint?", "How
   is auth handled?", "What's the error response format?", "How do I run just the
   integration tests?", "How does config reach the pod?", "Which utilities exist for
   X?" Derive the questions from what is genuinely non-obvious in THIS repo.
5. AI-WORKFLOW.md — operating instructions for the chat AI enforcing an agentic loop:
     * PLAN first, always: for any change request output ONLY a plan document — goal &
       scope, assumptions & open questions, affected-files table (path | change type |
       why), runtime execution flow, numbered code-free steps (compilable after each),
       test plan, config/deploy impact, rollback & risks. Where a step matches a recipe,
       CITE it ("per RECIPES.md > Add endpoint (query)"). End asking for corrections or
       APPROVED.
     * REFINE on feedback: re-issue the full plan, bumped version, one-line changelog.
     * No implementation code before the developer replies APPROVED — restate this if
       pushed.
     * EXECUTE one step per "next step" request: complete paste-ready code with
       placement markers, following the cited recipe and CONVENTIONS noted in it; end
       with the verify command, a done/pending checklist and "Reply 'next step' to
       continue, or paste any error and I will fix this step." Errors fix the current
       step only. After the final step, list which pack files the change made stale.
     * Never invent files/classes/endpoints not in the pack or shown code — ask. Real
       code beats the pack; say so on conflict.

CONSTRAINTS
- Max 700 lines per file; recipes and answers in tables/bullets, not prose.
- Every recipe step and FAQ answer must name real files/classes from this repo; generic
  Spring Boot advice is a defect.
- Facts only from code; mark gaps "UNKNOWN — verify with team". Never include secrets,
  credentials, real hostnames/IPs, or personal data.

VERIFY BEFORE FINISHING
- For each recipe, re-check its worked example against the actual code.
- Answer 3 of your own FAQ questions using ONLY the generated files; patch any gaps you
  find. Print a summary table: file | lines | contents.
```
