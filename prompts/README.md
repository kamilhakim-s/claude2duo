# Context-pack generation prompts — experiment candidates

Five deliberately different strategies for generating a context pack with Claude Code.
Each prompt must produce (a) service context files and (b) instructions that make a chat AI
(GitLab Duo / Copilot) follow a **plan → refine → approve → execute-step-by-step** workflow.

| # | File | Strategy | Hypothesis being tested |
|---|---|---|---|
| 1 | `prompt-1-structured-spec.md` | Fixed 11-file specification, every file's contents prescribed | Prescriptive structure gives complete, predictable packs |
| 2 | `prompt-2-tech-lead-persona.md` | Persona-driven: "tech lead writing onboarding docs", quality bar instead of file spec | Freedom + a quality bar beats rigid structure |
| 3 | `prompt-3-compact-budget.md` | Aggressive compression: 3 files, hard token budget, table-first | Smaller packs leave more context headroom → better chat sessions |
| 4 | `prompt-4-task-cookbook.md` | Task-recipe style: "how do I…" cookbook + Q&A instead of reference docs | Chat AIs use procedural recipes better than reference material |
| 5 | `prompt-5-self-critique.md` | Two-phase: generate, then adversarially self-test and patch gaps | A self-review loop catches omissions the single pass misses |

Run each prompt with Claude Code **from a fresh session** at the sample app's repo root,
directing output to `docs/context-pack-v{N}/` so the five variants can be compared side by side.
Scoring method and Duo test protocol: see `../validation/validation-plan.md`.
