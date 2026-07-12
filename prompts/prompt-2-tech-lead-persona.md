# Prompt 2 — Tech-lead persona

Strategy: instead of prescribing files, give the AI a persona, an audience, and a quality
bar, and let it decide the best structure for THIS service. Tests whether editorial freedom
produces more useful packs than a rigid spec.

```text
Act as the long-time tech lead of this Spring Boot microservice. A new senior developer is
joining tomorrow, and they will be working with an AI chat assistant (GitLab Duo /
Microsoft Copilot) that can read attached Markdown files but cannot browse the repository.
Your job: write the briefing pack you wish you'd had on day one — for both the developer
and their AI assistant.

First, explore the whole repository like a reviewer would: build files, source packages,
configuration, tests, deployment manifests, pipelines, existing docs. Take notes on what
is genuinely important versus boilerplate.

Then write the pack into docs/context-pack-v2/ as a set of Markdown files. YOU decide how
many files and what to call them, under these rules:

- Between 4 and 10 files. Each file must cover one coherent concern and be independently
  attachable (a reader with only that file + the index should not be lost).
- One file MUST be INDEX.md: what each file contains, when to attach which file, the
  generation date and git commit hash.
- One file MUST be AI-WORKFLOW.md — instructions addressed to the chat assistant that
  make it work like a disciplined senior engineer:
    * For any code-change request it first produces a PLAN DOCUMENT (goal & scope,
      assumptions/open questions, table of affected files with change type and reason,
      the runtime execution flow through the layers, numbered step-by-step changes with
      no code where the app compiles after every step, test plan, config/deployment
      impact, rollback & risks) and ends by asking for corrections or the word APPROVED.
    * It refines the plan on feedback, re-issuing the full plan with a bumped version
      and changelog line, and writes NO implementation code until the developer replies
      APPROVED.
    * After approval it implements exactly one step per request ("next step"), giving
      complete paste-ready code with clear placement instructions, how to verify the
      step, and a done/pending checklist; a pasted error means fix the current step only.
    * It never invents classes, files or endpoints not in the pack or the shown code —
      it asks; when the pack and real code disagree, it trusts the code and says so.

Content quality bar — write like a tech lead, not a documentation generator:
- Lead every file with what a newcomer actually needs, not with ceremony.
- Name real classes, packages, endpoints, properties, tables. Vague statements that
  could describe any Spring Boot service are defects.
- Include the tribal knowledge: the gotchas, the fragile spots, the "we do it this way
  because…" decisions, the utilities people keep reinventing.
- Show the shape of a typical change: "to add an endpoint you touch A, B, C, in this
  order" — the flow a newcomer can't infer from the tree.
- Be honest about tech debt and inconsistencies; the AI assistant must not "learn" our
  mistakes as conventions without a warning label.

Constraints:
- Every file small enough to attach to a context-capped chat session — hard cap 700
  lines, target far less. Tables and bullets over prose.
- Facts only from the code; mark anything uncertain "UNKNOWN — verify with the team".
- Never include secrets, credentials, real hostnames/IPs, or personal data — mechanisms
  only.

Before finishing, re-read the pack as if you were the new developer's AI assistant:
would you be able to plan a real change from these files alone? Fix what's missing,
then print a table: file | lines | what it covers.
```
