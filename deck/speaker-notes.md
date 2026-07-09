# Speaker notes & run-sheet — "Context Packs" presentation

Slot: 20–30 minutes (aim to finish slides at ~22–24 min, leave ~5 min for Q&A).
Audience: manager + team. Balanced pitch — business case for the manager, workflow for the developers.

---

## Timing map

| Section | Slides | Time | Cumulative |
|---|---|---|---|
| Opening (problem) | 1–3 | 4 min | 4 min |
| The proposal | 4–8 | 8 min | 12 min |
| Making it work | 9–12 | 6 min | 18 min |
| Business case & rollout | 13–16 | 5 min | 23 min |
| Summary + Q&A | 17 | 5–7 min | ~30 min |

If running long, compress slides 11–12 (fresh-ness + security) to one minute each — their content works as "read the slide" material.

---

## Per-slide talking points

### 1 · Title (30 sec)
- One-sentence framing: "I want to show how the few Claude Code licences we have can make AI useful for the *whole* team — without new tools, licences or security exposure."
- Fill in your name and the date on the slide before presenting.

### 2 · The problem (90 sec)
- Key line: **"Our chat AIs aren't weak — they're starved of context."**
- Acknowledge the constraint is legitimate (licences + security), don't argue against it.
- Land the pain: every fresh Duo/Copilot session starts from zero; devs re-explain the service every time; answers are generic Spring Boot, not *our* service.

### 3 · Tooling landscape (90 sec)
- Walk the table quickly — the audience knows these tools.
- Key line: point at the bottom banner — **"Duo and Copilot both accept attached files. The blocker isn't the tool, it's what we feed it."**
- This slide sets up the whole idea; don't rush the observation.

### 4 · The idea in one picture (2 min)
- Walk the 5 steps left to right. Emphasise step 1 happens *once per service*, steps 3–5 happen *every day, by everyone*.
- Key line: **"Claude Code does the expensive systematic understanding once; everyone reuses it."**
- Stress step 5: humans apply all changes — nothing about our change-control process changes.

### 5 · What's in a context pack (2 min)
- Don't read all nine files; pick three: ARCHITECTURE (the map), CONVENTIONS (how we write code), GOTCHAS (what bites you).
- Mention every file is deliberately sized to fit Duo/Copilot attachment and context limits.
- Key line: **"Even if we never attached these to an AI, this is the service documentation we've always wanted — and it regenerates itself."**

### 6 · The plan template (90 sec)
- The template is what turns "chatting with an AI" into "systematic work".
- Key line: **"Predictable structure means predictable review — a plan with a test section and a rollback section, every time."**
- Repeat the safety point: dev copies the plan out and applies it manually; the AI never touches the repo.

### 7 · Before / after (2 min)
- Tell it as a story: "Maria needs to add an endpoint to the payments service…" — walk the *before* column, then the *after*.
- Demo asset placeholder here: replace with real side-by-side Duo screenshots before presenting (same prompt, with and without pack).

### 8 · Sample pack (90 sec)
- Pure show-and-tell slide once assets exist. Until then, describe what will be shown.
- Assets to capture: (1) 1–2 page excerpt of a real generated ARCHITECTURE.md / API-CONTRACTS.md; (2) screenshot of the pack attached in Duo (IntelliJ or VS Code); (3) same in Copilot chat.

### 9 · Prompt experimentation (90 sec)
- Message for the manager: this is *engineering*, not vibes — candidate prompts, fixed scoring criteria, iterate.
- The five criteria matter; call out **size** (must fit context caps) and **accuracy** (spot-checked by the service's own devs).

### 10 · Validation testing (90 sec)
- The test matrix is the acceptance gate: every cell green on the pilot service before scaling.
- Key line: **"We don't ask the team to trust it — we ask them to test it."**

### 11 · Keeping packs fresh (60 sec)
- Pre-empt the #1 objection (stale docs): packs are *generated*, so refresh = re-run a command.
- Cadence: once per PI as routine enabler work + ad hoc after big merges. Each pack stamped with date + commit hash.

### 12 · Security posture (60–90 sec)
- Slow down here if security stakeholders are in the room.
- Three pillars: no new data exposure (same code the tools already see), no new tools/licences, human applies every change.
- Honest caveat: generation prompts explicitly exclude secrets/hostnames, and packs get a human review before first commit.

### 13 · Benefits (90 sec)
- Lead with **whole-team uplift from licences we already pay for** — that's the manager's headline.
- Onboarding + living documentation are the secondary wins that keep paying even if AI tooling changes.

### 14 · Risks (60–90 sec)
- Present risks yourself before anyone raises them — it builds credibility.
- Don't read the table; say "the two I take most seriously are staleness and over-reliance" and give the one-line mitigation for each.

### 15 · SAFe rollout (2 min)
- Map to what the audience knows: spike next iteration → pilot for one PI → measure at PI boundary → scale as enabler stories.
- Emphasise the *decide* gate: go / adjust / stop. This is time-boxed, not open-ended.
- Metrics are on the slide; the survey (with vs without packs) is the one that convinces people.

### 16 · The ask (90 sec)
- Be concrete: one spike, a few hours of licensed-dev time, one pilot service, team feedback.
- Closing line: **"If it doesn't prove itself in one PI, we stop — and we keep the documentation either way."**

### 17 · Summary + Q&A
- Read the four bullets, then open the floor.

---

## Anticipated objections & answers

**"Why not just buy more Claude Code licences?"**
That may still happen, but it's a procurement + security decision outside our control and timeline. This works *now*, with what we already have, and even with more licences the packs remain valuable (onboarding, docs, review consistency).

**"AI-generated documentation is unreliable."**
Which is why accuracy is an explicit scoring criterion, packs are spot-checked by the service's own developers before first commit, and every pack carries the commit hash it was generated from. Compare it to the alternative: hand-written docs that are already stale.

**"Won't this leak sensitive information?"**
Packs only describe code Duo and Copilot can already access through their approved integrations. Generation prompts explicitly exclude secrets, credentials, hostnames and personal data, and there's a human review gate.

**"Who maintains this when you're busy?"**
Regeneration is one command per service; it's tracked as normal enabler work, once per PI. If the licensed devs change, the prompts and the process are in a repo — anyone with a licence can run them.

**"Devs will blindly apply AI plans."**
The template *forces* a test plan and rollback section, application is manual, and MRs go through the same review as today. The plan actually makes review easier because every change arrives in the same shape.

**"What if the packs don't fit in Duo's context window?"**
Size is a first-class evaluation criterion in the spike. Files get split or trimmed per tool until they fit with headroom; that's precisely what the validation matrix on slide 10 tests.

---

## Pre-flight checklist

Demo assets to capture (replace the dashed placeholder boxes):
- [ ] Slide 7: side-by-side screenshots of the *same task* in GitLab Duo — fresh session without context vs with the pack attached.
- [ ] Slide 8 (left): 1–2 page excerpt of a real generated pack (ARCHITECTURE.md + API-CONTRACTS.md) for the pilot service.
- [ ] Slide 8 (top right): screenshot of the pack attached in a Duo chat session (IntelliJ or VS Code).
- [ ] Slide 8 (bottom right): screenshot of the same pack attached in a Copilot chat session.

Logistics:
- [ ] Fill in presenter name + date on slide 1.
- [ ] Apply the corporate PowerPoint template/theme if required.
- [ ] Export a backup PDF in case the meeting room only has a browser.
- [ ] Test screen-share / room display with the actual deck (tables on slides 3, 10, 14 are the small-text risk).
- [ ] Have the pilot-service shortlist ready in case the manager asks "which service?" on the spot.
- [ ] Know your spike estimate (hours of licensed-dev time) — you will be asked.
