---
name: bravado
description: Create a polished, short product motion film from a project website or GitHub repository. Use when the user asks for a Bravado video, launch intro, explainer, motion typography, animated product story, or synchronized brand-film sound design. Inspect the linked project, write a sourced visual brief, storyboard, render, review, and deliver MP4 plus editable source.
---

# Bravado

**You built it, you shipped it, now show your Bravado.**

## Intake

1. Accept a public site or GitHub repository URL. Inspect it with web search and direct UI/source tools as appropriate. For a repo, follow the homepage or deployment when available. Record the exact URL and access date. Read the page's visual presentation, not just its text.
2. Establish current product behavior, audience, brand assets, fonts, palette, key message, CTA, and evidence for any metric. Distinguish a working feature from a roadmap item. If a source is private or blocked, use what is available and identify the gap.
3. If the user gives an existing reference video, inspect its visual timeline and audio. Derive the motion grammar; do not lift its footage or soundtrack.

## Produce

1. Follow [the workflow](references/workflow.md) to write a seven-scene arc and frame-level beat sheet. State one idea per scene. Fit copy to the actual product and choose a graphic metaphor that explains it.
2. Bootstrap the template with `python scripts/bootstrap.py /absolute/output/directory`, then run `python setup_fonts.py` inside the copied directory. This copies the renderer, sample brief, and dependencies from `assets/starter`. Alternatively use the Bravado repository if the user already has it checked out.
3. Create a new JSON brief from `projects/cadence.json`. Adapt the code in `render.py` when the product is not a payroll flow: replace day tiles, money counter, wallet cards, and receipts with appropriate data and diagram logic. Do not merely rename Cadence labels.
4. Render stills first: `python render.py --brief projects/your-project.json --out output --stills`. Inspect `output/review/storyboard.jpg` and frames at the scene boundaries. Iterate the typography, crop, spacing, pacing, illustration, and motion.
5. Render the full MP4, listen to it, and decode-check it. Align audio hits to real visual actions. Inspect the exported video. Keep illustrative numbers visibly labeled and calculate them from consistent units.
6. Deliver the MP4 and editable project. Summarize the visual choices and remaining uncertainties. Save durable user-facing artifacts using the applicable storage workflow.

## Quality gate

Use [the quality bar](references/quality-bar.md) before delivery. The goal is the quality of the Cadence example: intentional typography, moving diagrams, coordinated scene choreography, and original sound. The template is a starting point, never a substitute for product-specific art direction. Do not promise an exact match to a tool or font unless source evidence supports it.
