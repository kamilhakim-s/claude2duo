# Validation plan — choosing the best context-pack prompt

Goal: run all 5 prompts (`prompts/prompt-{1..5}-*.md`) against the sample Spring Boot app,
then score the resulting packs objectively and in real GitLab Duo sessions, and pick a winner.

## Stage 0 — Generation

For each prompt N (1–5):
1. Fresh Claude Code session at the sample app repo root (fresh session per prompt so no
   cross-contamination).
2. Paste the prompt verbatim; let it run to completion.
3. Output lands in `docs/context-pack-vN/`. Commit each variant so results are reproducible.

## Stage 1 — Automated/objective checks (no Duo needed, scriptable)

Run `validation/analyze_packs.py <sample-app-root>` (or check manually). Per variant:

| Check | Measure | Pass bar |
|---|---|---|
| Size | total lines, est. tokens, per-file max | every file < its prompt's cap; total pack < ~24k tokens |
| Hygiene | grep for secrets/tokens/hostname/IP patterns | zero hits |
| Fact accuracy | sample 15 named symbols (classes, endpoints, properties) per pack; verify each exists in the code | ≥ 14/15 |
| Coverage | checklist: all endpoints listed? all entities? profiles? test layers? utilities? | note gaps |
| Workflow file | AI-WORKFLOW contains all four phases + approval gate + step-wise execution + anti-hallucination rules | all present |

## Stage 2 — Duo Q&A test (same protocol per variant)

For each variant, open a **fresh** GitLab Duo Chat session (IDE), attach the pack per its
own INDEX/MANIFEST instructions, then ask the **fixed question set** (adapt the bracketed
parts to the sample app once, then keep identical across variants):

1. "What does this service do and what are its main flows?"
2. "List all REST endpoints with their purpose."
3. "Where is [chosen endpoint] implemented and what is its response shape?"
4. "How do I add a new field to [chosen entity], including the migration?"
5. "What is the error response format and which class produces it?"
6. "Which existing utility should I reuse to [something CONVENTIONS covers]?"
7. "How do I run only the integration tests?"
8. "What are the riskiest parts of this codebase I should be careful with?"

Score each answer 0–2: **0** wrong/generic (could describe any Spring Boot app),
**1** partially specific, **2** correct and names the real classes/files. Max 16 points.

Also record: did the attachment load without truncation? (yes/no), and rough context
headroom (does Duo still answer follow-ups sensibly after 10+ turns?).

## Stage 3 — Duo agentic-workflow test (the differentiator)

Same fresh-session setup. Give each variant the **same feature request** (pick one
realistic small feature for the sample app and reuse it verbatim across variants), then:

| Step | What to do | What to score (0–2 each) |
|---|---|---|
| W1 | State the feature request | Did it respond with a plan only — no code? |
| W2 | Inspect the plan | Affected-files table present and correct? |
| W3 | Inspect the plan | Execution flow section present and plausible? |
| W4 | Inspect the plan | Steps are small, ordered, individually compilable? |
| W5 | Give one correction (e.g. "also update the OpenAPI spec") | Full re-issued plan, version bumped, changelog line? |
| W6 | Say "give me the code" WITHOUT approving | Did it refuse and ask for APPROVED? |
| W7 | Reply APPROVED, then "implement step 1" | Complete paste-ready code with placement markers, verify command, checklist? |
| W8 | Paste a fake compile error for step 1 | Fixed only step 1, didn't jump ahead? |
| W9 | "next step" | Correct continuation with updated checklist? |

Max 18 points. Note qualitative observations (hallucinated files, drift, verbosity).

## Stage 4 — Decision

Record everything in `validation/scoresheet.csv`. Weighted total per variant:

- Stage 1 objective: 20% (fail on hygiene = disqualified regardless of score)
- Stage 2 Q&A: 30%
- Stage 3 workflow: 40%
- Practicality: 10% — generation time, pack size/headroom, how fiddly attachment was

Winner = highest weighted score. If two are close, prefer the smaller pack (headroom wins
in long sessions). Expect the final production prompt to be a hybrid — take the winning
skeleton and fold in whatever individual sections other variants did better.

## Automating the Duo runs (optional)

GitLab Duo Chat can be driven programmatically on GitLab 16.9+ via the GraphQL `aiAction`
mutation (and on newer versions an experimental REST `/api/v4/chat/completions` endpoint),
using a personal access token with the `api`/`ai_features` scope — see
`validation/duo_chat_runner.py`. Caveats:

- Must run **inside your corporate network** against your on-prem GitLab; this cannot be
  driven from outside.
- The API path can't attach IDE files; the script inlines pack content into the message,
  which tests content quality but NOT the IDE attach/truncation behaviour — keep Stage 2's
  "attachment loads" check manual either way.
- Availability depends on your GitLab version and Duo licence; if the mutation is not
  enabled for API callers on your instance, fall back to the manual protocol above (it is
  ~30–40 min per variant).
