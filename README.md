# claude2duo — Context Packs presentation

Pitch deck proposing to use Claude Code (held by a few licensed developers) to generate
per-microservice **context packs** and a **standardised plan template**, so the whole team's
GitLab Duo and Microsoft Copilot chat sessions become service-aware and systematically useful.

The code and prompts for the context-pack generation itself live in a separate repository —
this repo only holds the presentation.

## Contents

| File | What it is |
|---|---|
| `deck/claude2duo-context-packs.pptx` | The 17-slide deck (20–30 min slot). Generated — do not hand-edit if you plan to regenerate. |
| `deck/build_deck.py` | Script that generates the deck with [python-pptx](https://python-pptx.readthedocs.io/). All shapes/tables are native PPT objects, so the output stays fully editable. |
| `deck/speaker-notes.md` | Per-slide talking points, timing map, anticipated objections with answers, and a pre-flight checklist (including the demo assets still to capture). |
| `prompts/` | Five candidate generation prompts (different strategies) for the prompt experiment — see `prompts/README.md`. |
| `validation/` | Validation plan, scoring sheet, and an experimental GitLab Duo API runner for comparing the five prompt variants. |
| `tickets/context-pack-generation-ticket.md` | Ready-to-paste Jira ticket for the Claude Code licence holder, containing the full generation prompt. The prompt produces the context pack plus `AI-WORKFLOW.md`, which makes Duo/Copilot follow a plan → refine → approve → execute-step-by-step workflow. |

## Regenerating the deck

```bash
pip install python-pptx
python3 deck/build_deck.py
```

Output is written to `deck/claude2duo-context-packs.pptx`.

## Before presenting

The deck contains four dashed **[DEMO ASSET — TO BE CAPTURED]** placeholders (slides 7–8)
for the before/after Duo comparison and the sample context pack screenshots. The full list,
plus room-logistics checks, is in the pre-flight checklist at the end of
`deck/speaker-notes.md`.
