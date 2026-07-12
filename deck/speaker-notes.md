# Speaker notes & run-sheet — "Context Packs" presentation

Slot: 20–30 minutes (aim to finish slides at ~22–24 min, leave ~5 min for Q&A).
Audience: manager + team. Balanced pitch — business case for the manager, workflow for the developers.

---

## Timing map

| Section | Slides | Time | Cumulative |
|---|---|---|---|
| Opening (problem) | 1–3 | 4 min | 4 min |
| The proposal | 4–8 | 7 min | 11 min |
| Making it work + evidence | 9–13 | 8 min | 19 min |
| Business case & rollout | 14–17 | 5 min | 24 min |
| Summary + Q&A | 18 | 5–6 min | ~30 min |

If running long, compress slides 12–13 (freshness + security) to one minute each — their content works as "read the slide" material. Do NOT cut slide 11 (early findings) — it is the strongest evidence in the deck.

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
- The left panel is REAL generated output — the R3 recipe from the task-cookbook pack, produced by Claude Code from the sample transfer-service. Point at the PITFALL line: this is tribal knowledge the generator derived from the code on its own.
- Remaining assets to capture: screenshot of the pack attached in Duo (IntelliJ/VS Code) and the same in Copilot chat.

### 9 · Prompt experimentation (90 sec)
- Message for the manager: this is *engineering*, not vibes — and it is already underway. Five strategies written, five packs generated against a sample Spring Boot payments service, objective checks all passed.
- Call out the token sizes on the cards: every pack fits a chat context with headroom (1.7k–6.4k tokens).

### 10 · Validation testing (90 sec)
- Walk the four stages top to bottom; Stage 1 is DONE, Stages 2–3 are the Duo sessions we're asking time for.
- Key line: **"We don't ask the team to trust it — we ask them to test it, and the test kit is already built."**
- Mention scoring is weighted toward the agentic-workflow behaviour (40%) because that's the capability gap we're closing.

### 11 · Early findings (2 min) — the money slide
- Tell the trap story: the sample service constructs its Transfer entity in two code paths; miss one and data is silently lost. Only the task-cookbook pack warned about it unprompted, and the self-critique prompt *found it by testing its own output*.
- Key line: **"The experiment is already telling us something non-obvious: packs must encode how to CHANGE the code, not just describe it."**
- The right card is the credibility card: zero hallucinated classes, honest UNKNOWNs, clean hygiene scans.

### 12 · Keeping packs fresh (60 sec)
- Pre-empt the #1 objection (stale docs): packs are *generated*, so refresh = re-run a command.
- Cadence: once per PI as routine enabler work + ad hoc after big merges. Each pack stamped with date + commit hash.

### 13 · Security posture (60–90 sec)
- Slow down here if security stakeholders are in the room.
- Three pillars: no new data exposure (same code the tools already see), no new tools/licences, human applies every change.
- Honest caveat: generation prompts explicitly exclude secrets/hostnames, and packs get a human review before first commit.

### 14 · Benefits (90 sec)
- Lead with **whole-team uplift from licences we already pay for** — that's the manager's headline.
- Onboarding + living documentation are the secondary wins that keep paying even if AI tooling changes.

### 15 · Risks (60–90 sec)
- Present risks yourself before anyone raises them — it builds credibility.
- Don't read the table; say "the two I take most seriously are staleness and over-reliance" and give the one-line mitigation for each.

### 16 · SAFe rollout (2 min)
- The spike is marked IN PROGRESS — that's deliberate: prompts and packs already exist, so the remaining spike cost is just the Duo validation sessions.
- Emphasise the *decide* gate: go / adjust / stop. This is time-boxed, not open-ended.
- Metrics are on the slide; the survey (with vs without packs) is the one that convinces people.

### 17 · The ask (90 sec)
- The ask has shrunk since the work started: finish the spike (Duo runs), a few licensed-dev hours to re-run the winning prompt fresh, one pilot service, team feedback.
- Closing line: **"If it doesn't prove itself in one PI, we stop — and we keep the documentation either way."**

### 18 · Summary + Q&A
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

Demo assets to capture (replace the dashed placeholder boxes) — capture these DURING the
Duo validation runs, they're the same sessions:
- [ ] Slide 7: side-by-side screenshots of the *same task* in GitLab Duo — fresh session without context vs with the pack attached.
- [ ] Slide 8 (top right): screenshot of the pack attached in a Duo chat session (IntelliJ or VS Code).
- [ ] Slide 8 (bottom right): screenshot of the same pack attached in a Copilot chat session.
- [x] Slide 8 (left): real generated pack excerpt — DONE (R3 recipe from context-pack-v4).
- Optional upgrade after the Duo runs: add the winning variant + its scores to slide 11.

Logistics:
- [ ] Fill in presenter name + date on slide 1.
- [ ] Apply the corporate PowerPoint template/theme if required.
- [ ] Export a backup PDF in case the meeting room only has a browser.
- [ ] Test screen-share / room display with the actual deck (tables on slides 3, 10, 14 are the small-text risk).
- [ ] Have the pilot-service shortlist ready in case the manager asks "which service?" on the spot.
- [ ] Know your spike estimate (hours of licensed-dev time) — you will be asked.
