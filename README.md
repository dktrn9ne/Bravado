# Bravado

**You built it, you shipped it, now show your Bravado.**

Bravado is a workflow and starter renderer for short product films with strong typography, purposeful diagrams, choreographed transitions, and synchronized original sound. Give the agent a project website or GitHub repository. It studies the actual product, writes a seven-scene brief, creates a storyboard, and produces a reviewed MP4.

The installable agent skill is in [`skill/`](skill/SKILL.md). The copy in this repository includes a bootstrap starter and fetches verified fonts during setup. The personal Bravado skill is also installed in the user's skill directory.

The included Cadence example reproduces the production approach behind a 31-second product intro. The template is a starting grammar, not a claim that arbitrary project links can be transformed into a finished film without editorial decisions. For a different product, the agent changes the metaphor, scene graphics, copy, and numerical logic to fit the source.

## Quick start

```bash
python -m pip install -r requirements.txt
python setup_fonts.py
python inspect_source.py https://example.com --out output/source-notes.json
# Review facts and adapt projects/cadence.json to your project.
python render.py --brief projects/cadence.json --out output --stills
# Inspect output/review/storyboard.jpg, then render:
python render.py --brief projects/cadence.json --out output
```

Requires Python 3.10+, FFmpeg, and network access for initial font setup and source inspection. The renderer runs offline after dependencies and fonts are installed. Output: 1920×1080, 30 fps, 31 seconds, H.264 MP4 with AAC stereo audio. It also creates a separate original audio stem and storyboard frames. Output files are ignored by Git.

## Start from a project link

The [workflow](docs/WORKFLOW.md) explains how to move from a URL to a truthful film. `inspect_source.py` collects public metadata and README content; it does not assume a repository README or landing page proves a feature is live. The agent checks visuals and product behavior, drafts the story, and adapts the renderer. Use `projects/cadence.json` as an annotated example of the required fields.

Prompt the Bravado skill with:

> Make a 31-second Bravado film for https://myproject.example. Focus on how the product changes the user's day. Use the site's brand, build motion diagrams that explain the flow, and deliver the MP4, soundtrack, and editable project.

Or:

> Use Bravado on https://github.com/owner/repo. Inspect its README and app if available. Establish what's working now, then write and render a launch video.

## Quality standard

- One proposition per scene; no tiny paragraphs posing as motion design.
- Text entrances, numeric changes, diagram actions, transitions, and SFX share one frame-accurate timeline.
- Use a contrasting type scale, disciplined grids, deliberate negative space, and legible claims.
- Sound accents punctuate visual events; the bed leaves room for a future voiceover.
- Do not imply a demo animation or illustrative number is a live transaction.
- Inspect every storyboard frame and the exported MP4 with audio before delivery.

The workflow contains the review checklist and branching guidance for repo-only projects, animation motifs, and factual uncertainty.

## Configuration and extension

`render.py` reads JSON and produces seven scenes at fixed pacing. Change a project JSON for copy, palette, example metrics, and labels. For non-financial products, adapt `scene1`–`scene5` in a project branch: swap the fourteen-day timeline, money counter, wallet cards, and receipts for product-specific diagrams while retaining the reveal, transitions, color, and sound timing primitives. Do not shoehorn unrelated products into a payroll narrative.

`--stills` is fast and generates the storyboard before a full render. The GitHub Actions workflow can render the example or a specified brief and retain the MP4 and storyboard as build artifacts. No automatic public release is configured.

## Credit and fonts

This template is an original implementation inspired by the supplied Batter Up video. It does not include the reference footage or its audio. `setup_fonts.py` downloads pinned Inter, IBM Plex Mono, and Playfair Display binaries from Google Fonts; their embedded notices are listed in `fonts/NOTICES.txt`. Replace the typefaces where the brand warrants it and honor the applicable font licenses.
