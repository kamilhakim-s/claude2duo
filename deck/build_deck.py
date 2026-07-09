#!/usr/bin/env python3
"""Generate the "Context Packs" presentation deck (claude2duo-context-packs.pptx).

Regenerate with:  python3 deck/build_deck.py
Output:           deck/claude2duo-context-packs.pptx

All slides are built from native PPT shapes/tables so the deck stays fully
editable in PowerPoint afterwards.
"""

import os

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

# ---------------------------------------------------------------- palette ---
INK = RGBColor(0x1F, 0x29, 0x33)        # near-black text
MUTED = RGBColor(0x5A, 0x6B, 0x7A)      # secondary text
ACCENT = RGBColor(0x0E, 0x63, 0xB0)     # corporate blue
ACCENT_DARK = RGBColor(0x0A, 0x46, 0x7E)
ACCENT_LIGHT = RGBColor(0xE3, 0xEE, 0xF8)
GOOD = RGBColor(0x1E, 0x7A, 0x45)       # green
WARN = RGBColor(0xB4, 0x5E, 0x12)       # amber/brown
BG = RGBColor(0xFF, 0xFF, 0xFF)
CARD_BG = RGBColor(0xF4, 0xF7, 0xFA)
PLACEHOLDER_BG = RGBColor(0xFD, 0xF3, 0xE3)
PLACEHOLDER_EDGE = RGBColor(0xD9, 0xA4, 0x40)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

prs = Presentation()
prs.slide_width = SLIDE_W
prs.slide_height = SLIDE_H
BLANK = prs.slide_layouts[6]

FONT = "Calibri"


# ---------------------------------------------------------------- helpers ---
def add_slide():
    return prs.slides.add_slide(BLANK)


def textbox(slide, left, top, width, height):
    box = slide.shapes.add_textbox(left, top, width, height)
    box.text_frame.word_wrap = True
    return box


def set_text(tf, runs_per_para, align=PP_ALIGN.LEFT):
    """runs_per_para: list of paragraphs, each a list of (text, size, bold, color) runs."""
    tf.word_wrap = True
    for i, runs in enumerate(runs_per_para):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        for text, size, bold, color in runs:
            r = p.add_run()
            r.text = text
            r.font.name = FONT
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.color.rgb = color


def title_bar(slide, title, kicker=None):
    """Standard content-slide header: accent rule + title."""
    rule = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(0.55), Inches(0.55), Inches(0.09))
    rule.fill.solid()
    rule.fill.fore_color.rgb = ACCENT
    rule.line.fill.background()

    box = textbox(slide, Inches(0.6), Inches(0.68), Inches(12.1), Inches(1.0))
    paras = []
    if kicker:
        paras.append([(kicker.upper(), 12, True, ACCENT)])
    paras.append([(title, 30, True, INK)])
    set_text(box.text_frame, paras)


def bullets(slide, left, top, width, height, items, size=16, gap=6):
    """items: list of (text, level) or (text, level, bold) or (text, level, bold, color)."""
    box = textbox(slide, left, top, width, height)
    tf = box.text_frame
    for i, item in enumerate(items):
        text, level = item[0], item[1]
        bold = item[2] if len(item) > 2 else False
        color = item[3] if len(item) > 3 else INK
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.level = level
        p.space_after = Pt(gap)
        prefix = "" if level == 0 and bold else ("• " if level == 0 else "– ")
        r = p.add_run()
        r.text = prefix + text
        r.font.name = FONT
        r.font.size = Pt(size if level == 0 else size - 2)
        r.font.bold = bold
        r.font.color.rgb = color
    return box


def card(slide, left, top, width, height, fill=CARD_BG, line=None):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shp.adjustments[0] = 0.06
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line:
        shp.line.color.rgb = line
        shp.line.width = Pt(1.25)
    else:
        shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def card_text(shp, paras, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    tf = shp.text_frame
    tf.vertical_anchor = anchor
    tf.margin_left = Inches(0.18)
    tf.margin_right = Inches(0.18)
    tf.margin_top = Inches(0.12)
    tf.margin_bottom = Inches(0.12)
    set_text(tf, paras, align=align)


def demo_placeholder(slide, left, top, width, height, label, detail):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shp.adjustments[0] = 0.05
    shp.fill.solid()
    shp.fill.fore_color.rgb = PLACEHOLDER_BG
    shp.line.color.rgb = PLACEHOLDER_EDGE
    shp.line.width = Pt(1.5)
    shp.line.dash_style = 2  # dashed
    shp.shadow.inherit = False
    card_text(
        shp,
        [
            [("[ DEMO ASSET — TO BE CAPTURED ]", 12, True, WARN)],
            [(label, 16, True, INK)],
            [(detail, 12, False, MUTED)],
        ],
        align=PP_ALIGN.CENTER,
        anchor=MSO_ANCHOR.MIDDLE,
    )
    return shp


def footer(slide, n):
    box = textbox(slide, Inches(11.9), Inches(7.05), Inches(1.1), Inches(0.35))
    set_text(box.text_frame, [[(str(n), 11, False, MUTED)]], align=PP_ALIGN.RIGHT)


def arrow(slide, left, top, width, height=Inches(0.28)):
    shp = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, left, top, width, height)
    shp.fill.solid()
    shp.fill.fore_color.rgb = ACCENT
    shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def style_table(table, header_fill=ACCENT, header_color=WHITE, body_size=12, header_size=13):
    for j, cell in enumerate(table.rows[0].cells):
        cell.fill.solid()
        cell.fill.fore_color.rgb = header_fill
        for p in cell.text_frame.paragraphs:
            for r in p.runs:
                r.font.name = FONT
                r.font.size = Pt(header_size)
                r.font.bold = True
                r.font.color.rgb = header_color
    for row in list(table.rows)[1:]:
        for cell in row.cells:
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE
            for p in cell.text_frame.paragraphs:
                for r in p.runs:
                    r.font.name = FONT
                    r.font.size = Pt(body_size)
                    r.font.color.rgb = INK


def fill_table(slide, rows, left, top, width, height, col_widths=None, bold_first_col=False):
    n_rows, n_cols = len(rows), len(rows[0])
    gfx = slide.shapes.add_table(n_rows, n_cols, left, top, width, height)
    table = gfx.table
    if col_widths:
        total = sum(col_widths)
        for j, w in enumerate(col_widths):
            table.columns[j].width = Emu(int(width * w / total))
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = table.cell(i, j)
            cell.text = val
            cell.margin_left = Inches(0.08)
            cell.margin_right = Inches(0.08)
            cell.margin_top = Inches(0.04)
            cell.margin_bottom = Inches(0.04)
            if bold_first_col and j == 0 and i > 0:
                for p in cell.text_frame.paragraphs:
                    for r in p.runs:
                        r.font.bold = True
    style_table(table)
    return table


# ============================================================ 1 · TITLE ====
s = add_slide()
band = slide_bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, SLIDE_H)
band.fill.solid()
band.fill.fore_color.rgb = ACCENT_DARK
band.line.fill.background()
band.shadow.inherit = False

stripe = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(5.9), SLIDE_W, Inches(0.12))
stripe.fill.solid()
stripe.fill.fore_color.rgb = RGBColor(0x6A, 0xB0, 0xE8)
stripe.line.fill.background()
stripe.shadow.inherit = False

box = textbox(s, Inches(0.9), Inches(2.0), Inches(11.5), Inches(2.6))
set_text(box.text_frame, [
    [("CONTEXT PACKS", 16, True, RGBColor(0x9E, 0xC9, 0xEE))],
    [("Scaling AI-assisted development\nbeyond our Claude Code licenses", 40, True, WHITE)],
])
box = textbox(s, Inches(0.9), Inches(4.7), Inches(11.5), Inches(1.0))
set_text(box.text_frame, [
    [("Using Claude Code to make GitLab Duo and Microsoft Copilot dramatically more effective for the whole team",
      18, False, RGBColor(0xD5, 0xE5, 0xF4))],
])
box = textbox(s, Inches(0.9), Inches(6.3), Inches(11.5), Inches(0.8))
set_text(box.text_frame, [
    [("Proposal to the team  ·  20–30 min  ·  <presenter name>  ·  <date>", 14, False, RGBColor(0xA9, 0xC4, 0xDC))],
])

# ====================================================== 2 · THE PROBLEM ====
s = add_slide()
title_bar(s, "A two-tier AI developer experience", kicker="The problem")

c1 = card(s, Inches(0.6), Inches(1.8), Inches(6.0), Inches(3.3))
card_text(c1, [
    [("Tier 1 — a few developers", 16, True, ACCENT)],
    [("Claude Code (agentic)", 20, True, INK)],
    [("• Reads the whole codebase systematically", 14, False, INK)],
    [("• Plans and executes multi-step changes", 14, False, INK)],
    [("• Limited seats: licence cap + security review means most of the team can't get it", 14, False, INK)],
])
c2 = card(s, Inches(6.85), Inches(1.8), Inches(6.0), Inches(3.3))
card_text(c2, [
    [("Tier 2 — everyone else", 16, True, WARN)],
    [("GitLab Duo & Microsoft Copilot (chat)", 20, True, INK)],
    [("• Chat-mode only, with a hard context cap", 14, False, INK)],
    [("• Sees fragments of code, not the service as a system", 14, False, INK)],
    [("• Every fresh session starts from zero — the developer re-explains the service each time", 14, False, INK)],
])

c3 = card(s, Inches(0.6), Inches(5.35), Inches(12.25), Inches(1.5), fill=ACCENT_LIGHT)
card_text(c3, [
    [("The gap: ", 16, True, ACCENT_DARK),
     ("our chat AIs are not weak models — they are strong models that are starved of context. "
      "They give generic answers to questions about very specific Spring Boot services, so most developers "
      "get a fraction of the value we are already paying for.", 16, False, INK)],
], anchor=MSO_ANCHOR.MIDDLE)
footer(s, 2)

# ============================================= 3 · TOOLING LANDSCAPE =======
s = add_slide()
title_bar(s, "What each tool can and cannot do today", kicker="Current tooling landscape")
rows = [
    ["", "Claude Code", "GitLab Duo Chat", "Microsoft Copilot Chat"],
    ["Availability", "Few licensed developers", "Whole team (IntelliJ / VS Code)", "Whole team"],
    ["Mode", "Agentic — plans, reads, edits", "Chat, IDE-integrated", "Chat"],
    ["Code access", "Entire repository, systematic", "Open files / snippets in IDE", "Attached files, incl. images & many formats"],
    ["Context", "Very large, managed automatically", "Capped per session", "Capped per session"],
    ["Systematic multi-step work", "Yes", "No — needs hand-fed context", "No — needs hand-fed context"],
    ["Today's blocker", "Licence cap & security scope", "Doesn't know the service", "Doesn't know the service"],
]
fill_table(s, rows, Inches(0.6), Inches(1.85), Inches(12.25), Inches(3.9),
           col_widths=[2.3, 3.1, 3.3, 3.5], bold_first_col=True)
c = card(s, Inches(0.6), Inches(6.05), Inches(12.25), Inches(0.95), fill=ACCENT_LIGHT)
card_text(c, [
    [("Observation: ", 15, True, ACCENT_DARK),
     ("Duo and Copilot both accept attached files. If the right context arrived pre-packaged, "
      "the “doesn't know the service” blocker disappears.", 15, False, INK)],
], anchor=MSO_ANCHOR.MIDDLE)
footer(s, 3)

# ================================================= 4 · IDEA IN ONE PIC ====
s = add_slide()
title_bar(s, "The idea in one picture", kicker="Proposal")

steps = [
    ("1 · Generate", "Licensed devs run Claude Code with a standard prompt over each microservice", ACCENT),
    ("2 · Commit", "Context pack (a small set of .md files) is committed to the service repo", ACCENT),
    ("3 · Attach", "Any developer attaches the pack to a fresh Duo or Copilot session", ACCENT),
    ("4 · Plan", "The chat AI fills in our standard plan template for the feature / change", ACCENT),
    ("5 · Apply", "Developer reviews and applies the changes manually, as normal", GOOD),
]
x = Inches(0.6)
w = Inches(2.21)
gap = Inches(0.32)
for i, (t, d, col) in enumerate(steps):
    cx = Emu(int(x) + i * int(w + gap))
    cc = card(s, cx, Inches(2.0), w, Inches(2.5), fill=CARD_BG, line=col)
    card_text(cc, [
        [(t, 15, True, col)],
        [(d, 12, False, INK)],
    ])
    if i < len(steps) - 1:
        arrow(s, Emu(int(cx) + int(w) - Inches(0.02)), Inches(3.1), Emu(int(gap) + Inches(0.04)))

c = card(s, Inches(0.6), Inches(4.9), Inches(12.25), Inches(1.9), fill=ACCENT_LIGHT)
card_text(c, [
    [("Why this works", 16, True, ACCENT_DARK)],
    [("Claude Code does the expensive, systematic part once per service — understanding the whole codebase. "
      "The result is distilled into files small enough for Duo / Copilot context windows. "
      "Every developer then starts each chat session with the AI already “knowing” the service, "
      "and code changes stay fully under developer control.", 14, False, INK)],
])
footer(s, 4)

# ================================================ 5 · CONTEXT PACK ========
s = add_slide()
title_bar(s, "What's in a context pack", kicker="Proposal")
box = textbox(s, Inches(0.6), Inches(1.6), Inches(12.2), Inches(0.5))
set_text(box.text_frame, [[("One folder of Markdown files per microservice — each file sized to fit chat attachment and context limits.",
                            15, False, MUTED)]])

files = [
    ("SERVICE-OVERVIEW.md", "Purpose, responsibilities, owners, key business flows"),
    ("ARCHITECTURE.md", "Module layout, dependency map, upstream / downstream services"),
    ("API-CONTRACTS.md", "REST endpoints, request/response shapes, error conventions"),
    ("DATA-MODEL.md", "Entities, relationships, key tables and migrations"),
    ("CONVENTIONS.md", "Code patterns, naming, error handling, how we write services"),
    ("CONFIG-PROFILES.md", "Spring Boot config, profiles, feature flags, secrets handling"),
    ("DEPLOYMENT.md", "OpenShift topology, routes, resources, pipelines"),
    ("TESTING.md", "Test layers, fixtures, how to add and run tests"),
    ("GOTCHAS.md", "Known pitfalls, tech debt, sharp edges"),
]
cols = 3
cw = Inches(3.95)
ch = Inches(1.25)
for i, (name, desc) in enumerate(files):
    r, cidx = divmod(i, cols)
    left = Emu(int(Inches(0.6)) + cidx * int(Inches(4.15)))
    top = Emu(int(Inches(2.25)) + r * int(Inches(1.45)))
    cc = card(s, left, top, cw, ch)
    card_text(cc, [
        [(name, 13, True, ACCENT_DARK)],
        [(desc, 11.5, False, INK)],
    ])
c = card(s, Inches(0.6), Inches(6.6), Inches(12.25), Inches(0.65), fill=ACCENT_LIGHT)
card_text(c, [
    [("Side effect: this is living, always-regenerable documentation — valuable even without any AI.", 14, True, ACCENT_DARK)],
], anchor=MSO_ANCHOR.MIDDLE)
footer(s, 5)

# ============================================== 6 · PLAN TEMPLATE =========
s = add_slide()
title_bar(s, "The standardised plan template", kicker="Proposal")
box = textbox(s, Inches(0.6), Inches(1.6), Inches(12.2), Inches(0.6))
set_text(box.text_frame, [[("A fixed structure the chat AI must fill in for any feature or change — so output is predictable, reviewable and easy to apply by hand.",
                            15, False, MUTED)]])

sections = [
    ("1 · Goal & scope", "What we're changing and explicitly what we're not"),
    ("2 · Affected files", "Exact files to touch, and why each one"),
    ("3 · Step-by-step changes", "Ordered steps with code snippets per step"),
    ("4 · Test plan", "Unit / integration tests to add or update, how to run them"),
    ("5 · Config & deployment", "Spring profiles, OpenShift manifests, flags"),
    ("6 · Rollback & risks", "How to revert, what could break"),
]
for i, (t, d) in enumerate(sections):
    r, cidx = divmod(i, 2)
    left = Emu(int(Inches(0.6)) + cidx * int(Inches(6.25)))
    top = Emu(int(Inches(2.35)) + r * int(Inches(1.25)))
    cc = card(s, left, top, Inches(6.0), Inches(1.05))
    card_text(cc, [
        [(t, 14, True, ACCENT_DARK)],
        [(d, 12, False, INK)],
    ])

c = card(s, Inches(0.6), Inches(6.25), Inches(12.25), Inches(1.0), fill=ACCENT_LIGHT)
card_text(c, [
    [("The developer copies the filled-in plan out of Duo / Copilot and applies it manually — "
      "human review is built into every step. No AI writes to our repos except through a developer.", 14, False, INK)],
], anchor=MSO_ANCHOR.MIDDLE)
footer(s, 6)

# ====================================== 7 · DEVELOPER WORKFLOW (B/A) ======
s = add_slide()
title_bar(s, "A developer's day, before and after", kicker="Developer workflow")

c1 = card(s, Inches(0.6), Inches(1.75), Inches(6.0), Inches(2.6), line=WARN)
card_text(c1, [
    [("Before — Duo with no context", 15, True, WARN)],
    [("• “Add an endpoint to service X” → generic Spring Boot boilerplate", 12.5, False, INK)],
    [("• Dev pastes snippets file-by-file to explain the service", 12.5, False, INK)],
    [("• Hits the context cap, answers drift, session restarted", 12.5, False, INK)],
    [("• Result often ignores our conventions and config patterns", 12.5, False, INK)],
])
c2 = card(s, Inches(6.85), Inches(1.75), Inches(6.0), Inches(2.6), line=GOOD)
card_text(c2, [
    [("After — Duo with a context pack", 15, True, GOOD)],
    [("• Dev attaches the pack + plan template to a fresh session", 12.5, False, INK)],
    [("• AI answers in terms of our actual endpoints, entities, conventions", 12.5, False, INK)],
    [("• Produces a filled-in plan with concrete files and snippets", 12.5, False, INK)],
    [("• Dev reviews, applies manually, raises MR as usual", 12.5, False, INK)],
])

demo_placeholder(s, Inches(0.6), Inches(4.55), Inches(12.25), Inches(2.35),
                 "Before / after session comparison",
                 "Side-by-side screenshots of the same task in GitLab Duo: one fresh session with no context, "
                 "one with the context pack attached — same prompt, visibly different quality of answer.")
footer(s, 7)

# ================================================ 8 · SAMPLE PACK =========
s = add_slide()
title_bar(s, "What a real pack looks like", kicker="Sample context pack")
demo_placeholder(s, Inches(0.6), Inches(1.75), Inches(7.4), Inches(5.1),
                 "Excerpt of a generated context pack",
                 "1–2 pages of the actual ARCHITECTURE.md and API-CONTRACTS.md generated by Claude Code "
                 "for the pilot service, showing the level of detail and accuracy.")
demo_placeholder(s, Inches(8.2), Inches(1.75), Inches(4.65), Inches(2.45),
                 "Pack loaded in GitLab Duo",
                 "Screenshot: files attached in a Duo chat session in IntelliJ / VS Code.")
demo_placeholder(s, Inches(8.2), Inches(4.4), Inches(4.65), Inches(2.45),
                 "Pack loaded in Copilot",
                 "Screenshot: same pack attached to a Microsoft Copilot chat session.")
footer(s, 8)

# ====================================== 9 · PROMPT EXPERIMENTATION ========
s = add_slide()
title_bar(s, "Finding the best generation prompt", kicker="Making it work")
box = textbox(s, Inches(0.6), Inches(1.6), Inches(12.2), Inches(0.55))
set_text(box.text_frame, [[("We don't assume the first prompt is right. We run a short, structured trial-and-error loop per file type.",
                            15, False, MUTED)]])

loop = [
    ("Draft", "2–3 candidate prompts per context file type"),
    ("Generate", "Run each prompt with Claude Code on the pilot service"),
    ("Score", "Grade outputs against fixed criteria"),
    ("Refine", "Keep the winner, fix its weaknesses, re-run"),
]
for i, (t, d) in enumerate(loop):
    left = Emu(int(Inches(0.6)) + i * int(Inches(3.2)))
    cc = card(s, left, Inches(2.35), Inches(2.85), Inches(1.5), line=ACCENT)
    card_text(cc, [
        [(t, 15, True, ACCENT)],
        [(d, 12, False, INK)],
    ])
    if i < len(loop) - 1:
        arrow(s, Emu(int(left) + int(Inches(2.85))), Inches(2.95), Inches(0.35))

c = card(s, Inches(0.6), Inches(4.2), Inches(12.25), Inches(2.7))
card_text(c, [
    [("Evaluation criteria (scored per candidate)", 15, True, ACCENT_DARK)],
    [("• Accuracy — does it match the real code? (spot-checked by the service's developers)", 13, False, INK)],
    [("• Completeness — endpoints, entities, conventions all covered", 13, False, INK)],
    [("• Size — fits Duo and Copilot attachment / context limits with room for a conversation", 13, False, INK)],
    [("• Usefulness — does a Duo/Copilot session with this file answer service-specific questions correctly?", 13, False, INK)],
    [("• Regenerability — same prompt on updated code produces a cleanly updated file", 13, False, INK)],
])
footer(s, 9)

# ============================================ 10 · VALIDATION TESTING =====
s = add_slide()
title_bar(s, "Proving the packs load and actually help", kicker="Validation testing")
rows = [
    ["Test", "GitLab Duo (IntelliJ / VS Code)", "Microsoft Copilot"],
    ["Pack loads in a fresh session", "Attach files, verify no truncation", "Attach files, verify no truncation"],
    ["Q&A: service-specific questions", "Answers cite real endpoints / entities", "Answers cite real endpoints / entities"],
    ["Plan template: small change", "Produces correct filled-in plan", "Produces correct filled-in plan"],
    ["Plan template: new feature", "Plan judged usable by service dev", "Plan judged usable by service dev"],
    ["Context headroom", "Meaningful conversation still possible after attach", "Meaningful conversation still possible after attach"],
]
fill_table(s, rows, Inches(0.6), Inches(1.85), Inches(12.25), Inches(3.4),
           col_widths=[3.4, 4.4, 4.4], bold_first_col=True)
c = card(s, Inches(0.6), Inches(5.55), Inches(12.25), Inches(1.35), fill=ACCENT_LIGHT)
card_text(c, [
    [("Acceptance bar: ", 14, True, ACCENT_DARK),
     ("every cell green on the pilot service before we scale out. Failures feed back into the prompt-refinement loop "
      "(e.g. split files that are too large, add missing sections).", 14, False, INK)],
], anchor=MSO_ANCHOR.MIDDLE)
footer(s, 10)

# ============================================== 11 · KEEPING FRESH ========
s = add_slide()
title_bar(s, "Keeping packs fresh (and cheap to keep fresh)", kicker="Making it work")
items = [
    ("Regeneration is one command", "Packs are generated, not hand-written. Refreshing a service is re-running the winning prompt — minutes, not days.", ACCENT),
    ("Cadence", "Regenerate once per PI as a routine enabler task, plus ad-hoc after significant merges to a service.", ACCENT),
    ("Ownership", "The licensed Claude Code developers own generation; each service team spot-checks its own pack.", ACCENT),
    ("Drift guardrails", "Every pack carries a generated-on date + commit hash. Optional CI reminder when a service changes heavily since last generation.", WARN),
]
top = Inches(1.85)
for i, (t, d, col) in enumerate(items):
    cc = card(s, Inches(0.6), Emu(int(top) + i * int(Inches(1.28))), Inches(12.25), Inches(1.1), line=col)
    card_text(cc, [
        [(t + " — ", 14, True, ACCENT_DARK), (d, 13.5, False, INK)],
    ], anchor=MSO_ANCHOR.MIDDLE)
footer(s, 11)

# ================================================= 12 · SECURITY ==========
s = add_slide()
title_bar(s, "Security & compliance posture", kicker="Making it work")
items = [
    ("No new data exposure", "Packs describe code that Duo and Copilot can already access through their approved integrations. We change the form of the context, not its scope.", GOOD),
    ("No new tools, no new licences", "Everything runs on tooling that is already procured and security-approved: Claude Code for the few, Duo / Copilot for the many.", GOOD),
    ("Human in the loop by design", "Chat AIs only produce plans and snippets; a developer applies every change manually and it goes through normal MR review.", GOOD),
    ("Content hygiene", "Generation prompts explicitly exclude secrets, credentials, internal hostnames and personal data; packs are reviewed before first commit.", WARN),
]
top = Inches(1.85)
for i, (t, d, col) in enumerate(items):
    cc = card(s, Inches(0.6), Emu(int(top) + i * int(Inches(1.28))), Inches(12.25), Inches(1.1), line=col)
    card_text(cc, [
        [(t + " — ", 14, True, ACCENT_DARK), (d, 13.5, False, INK)],
    ], anchor=MSO_ANCHOR.MIDDLE)
footer(s, 12)

# ================================================= 13 · BENEFITS ==========
s = add_slide()
title_bar(s, "What we get", kicker="Benefits")
benefits = [
    ("Whole-team uplift", "Every developer gets near-agentic AI help from the licences we already pay for — no new seats needed."),
    ("Faster onboarding", "New joiners read the pack (or chat with it) instead of spelunking for weeks."),
    ("Living documentation", "Regenerable, always-current service docs as a permanent side effect."),
    ("Better reviews", "Standardised plans make AI-assisted changes predictable and easy to review."),
    ("Compounding asset", "Prompts and templates improve every iteration and apply to every new service."),
    ("Low cost to try", "A time-boxed spike by the licensed devs; no procurement, no platform work."),
]
for i, (t, d) in enumerate(benefits):
    r, cidx = divmod(i, 3)
    left = Emu(int(Inches(0.6)) + cidx * int(Inches(4.15)))
    top = Emu(int(Inches(1.95)) + r * int(Inches(2.3)))
    cc = card(s, left, top, Inches(3.95), Inches(2.05))
    card_text(cc, [
        [(t, 15, True, ACCENT_DARK)],
        [(d, 13, False, INK)],
    ])
footer(s, 13)

# =============================================== 14 · RISKS ===============
s = add_slide()
title_bar(s, "Risks and how we handle them", kicker="Risks & mitigations")
rows = [
    ["Risk", "Mitigation"],
    ["Packs go stale and mislead the AI", "Per-PI regeneration cadence; generated-on date + commit hash in every pack; regeneration is one command"],
    ["Over-reliance on AI-produced plans", "Plan template forces explicit test & rollback sections; manual apply + normal MR review remain mandatory"],
    ["Packs too large for chat context caps", "Size is an explicit evaluation criterion; split or trim files per tool limits during the spike"],
    ["Maintenance burden on licensed devs", "Generation is automated; effort is minutes per service per PI, tracked as enabler work"],
    ["Quality varies across services", "Standard prompts + acceptance bar per pack; service team spot-check before first commit"],
]
fill_table(s, rows, Inches(0.6), Inches(1.85), Inches(12.25), Inches(4.6),
           col_widths=[4.2, 8.0], bold_first_col=True)
footer(s, 14)

# ============================================ 15 · SAFe ROLLOUT ===========
s = add_slide()
title_bar(s, "Rollout, the SAFe way", kicker="Rollout plan")
phases = [
    ("Spike — next iteration", "Prompt experiments on 1 pilot service; validate pack loads in Duo & Copilot; pick winning prompts", ACCENT),
    ("Pilot — one PI", "2–3 services; real feature work by non-licensed devs using packs + plan template; collect metrics", ACCENT),
    ("Measure & decide", "Review metrics + dev feedback at PI boundary; go / adjust / stop", WARN),
    ("Scale", "Roll out to all services as enabler stories; per-PI regeneration becomes routine", GOOD),
]
for i, (t, d, col) in enumerate(phases):
    left = Emu(int(Inches(0.6)) + i * int(Inches(3.2)))
    cc = card(s, left, Inches(1.95), Inches(2.85), Inches(2.6), line=col)
    card_text(cc, [
        [(t, 14, True, col)],
        [(d, 12, False, INK)],
    ])
    if i < len(phases) - 1:
        arrow(s, Emu(int(left) + int(Inches(2.85))), Inches(3.1), Inches(0.35))

c = card(s, Inches(0.6), Inches(4.95), Inches(12.25), Inches(1.9))
card_text(c, [
    [("Success metrics for the pilot", 15, True, ACCENT_DARK)],
    [("• Pack load success rate in Duo and Copilot sessions (target: 100% of pilot packs)", 13, False, INK)],
    [("• Developer survey: usefulness of answers with vs without packs", 13, False, INK)],
    [("• Share of changes where the filled-in plan was usable with minor edits", 13, False, INK)],
    [("• Time-to-first-usable-answer on service-specific questions, before vs after", 13, False, INK)],
])
footer(s, 15)

# ================================================== 16 · THE ASK ==========
s = add_slide()
title_bar(s, "What I'm asking for today", kicker="The ask")
asks = [
    ("Approve the spike", "One time-boxed spike in the next iteration for the prompt experiments and pilot pack"),
    ("Time-box for licensed devs", "A few hours of Claude Code time from the licensed developers during the spike"),
    ("Nominate a pilot service", "One representative Spring Boot service (and later 2–3 for the PI pilot)"),
    ("Team commitment", "Pilot developers agree to use the packs on real tasks and give honest feedback"),
]
for i, (t, d) in enumerate(asks):
    r, cidx = divmod(i, 2)
    left = Emu(int(Inches(0.6)) + cidx * int(Inches(6.25)))
    top = Emu(int(Inches(1.95)) + r * int(Inches(1.85)))
    cc = card(s, left, top, Inches(6.0), Inches(1.6), line=ACCENT)
    card_text(cc, [
        [(t, 16, True, ACCENT)],
        [(d, 13, False, INK)],
    ])
c = card(s, Inches(0.6), Inches(5.95), Inches(12.25), Inches(1.0), fill=ACCENT_LIGHT)
card_text(c, [
    [("If the pilot doesn't prove itself in one PI, we stop — the only sunk cost is the spike, "
      "and we keep the generated documentation either way.", 15, True, ACCENT_DARK)],
], anchor=MSO_ANCHOR.MIDDLE)
footer(s, 16)

# ================================================== 17 · SUMMARY ==========
s = add_slide()
band = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, SLIDE_H)
band.fill.solid()
band.fill.fore_color.rgb = ACCENT_DARK
band.line.fill.background()
band.shadow.inherit = False

box = textbox(s, Inches(0.9), Inches(1.3), Inches(11.5), Inches(1.2))
set_text(box.text_frame, [[("Summary", 34, True, WHITE)]])
box = textbox(s, Inches(0.9), Inches(2.5), Inches(11.5), Inches(3.4))
set_text(box.text_frame, [
    [("•  A few Claude Code licences can lift the whole team: generate context packs once, reuse them everywhere.", 18, False, WHITE)],
    [("", 8, False, WHITE)],
    [("•  Duo and Copilot become service-aware assistants instead of generic chatbots — with zero new tools or data exposure.", 18, False, WHITE)],
    [("", 8, False, WHITE)],
    [("•  Developers stay in control: standardised plans, manual apply, normal MR review.", 18, False, WHITE)],
    [("", 8, False, WHITE)],
    [("•  One spike + one PI pilot tells us if it works — measured, time-boxed, SAFe-friendly.", 18, False, WHITE)],
])
box = textbox(s, Inches(0.9), Inches(6.2), Inches(11.5), Inches(0.8))
set_text(box.text_frame, [[("Questions?", 24, True, RGBColor(0x9E, 0xC9, 0xEE))]])

# ------------------------------------------------------------------- save --
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "claude2duo-context-packs.pptx")
prs.save(out)
print(f"Wrote {out} ({len(prs.slides._sldIdLst)} slides)")
