# AI-WORKFLOW — mandatory operating mode

Attached files = source of truth for transfer-service. Four phases, in order, every
code-change request. **No implementation code before the developer replies APPROVED.**

**PLAN** — reply to any change request with ONLY a plan doc:
Goal & scope (incl. out-of-scope) · Assumptions & open questions · Affected files
(table: path | create/modify/delete | why) · Execution flow (Controller→Service→
Repository, naming real classes from SERVICE-MAP) · Numbered steps (no code; app
compiles after each) · Test plan per step (`./gradlew test`, TransferServiceTest style)
· Config/deploy impact · Rollback & risks (check GOTCHAS 1–4).
End: "Reply with corrections, or APPROVED to start."

**REFINE** — on feedback re-issue the FULL plan, bump DRAFT v2/v3…, one-line changelog
on top. Loop until APPROVED.

**GATE** — only the literal reply APPROVED unlocks code. Asked earlier → say the plan
needs approval, ask what to refine.

**EXECUTE** — one step per "next step"/"implement step N":
restate step + files → complete paste-ready code with placement markers ("replace
method `validate`", "new file `src/…`") — no fragments → follow SERVICE-MAP
CONVENTIONS (rules in service, records + static from(), ProblemDetail handler pattern,
SCREAMING_SNAKE_CASE reasons) → end with verify command + done/pending checklist +
"Reply 'next step', or paste any error and I fix this step."
Pasted error ⇒ fix current step only, re-output fully.
After the final step: list which pack files this change made stale (for regeneration).

**Rules** — never invent files/classes/endpoints not in the pack or shown code (ask);
real code beats the pack (say so on conflict); one step per reply unless told
"implement remaining steps"; changes touching balances must state their concurrency
assumption (GOTCHA 1).
