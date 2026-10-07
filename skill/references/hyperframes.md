# HyperFrames in Bravado

Bravado owns research, the truthful story, art direction and review. HyperFrames
owns seeking the HTML/GSAP timeline, previewing it in Studio and rendering MP4.
This is an optional backend; existing Python briefs and renders keep working.

## Setup and authoring

From `hyperframes/`, run `npm ci` (Node 22+), then `npm run build`.
HyperFrames 0.8.140 and GSAP 3.14.2 are pinned in the lockfile. FFmpeg is required.
The CLI manages its browser runtime on first use; initial setup needs network
access. GSAP and the soundtrack are copied locally, so composition playback does
not depend on a CDN.

Edit `brief.json` or run `npm run build -- /absolute/path/to/brief.json`.
This schema is separate from the Python payroll starter: source, accessed date,
status, brand, CTA, three hex colors and exactly seven headline/detail/label scenes.
Copy is HTML-escaped and length-limited; use shorter headlines if the layout audit
finds overflow. System fonts are used in this starter; ship licensed local fonts
and declare `@font-face` when adapting a brand.

Build creates `index.html`, `beat-sheet.json`, local GSAP and `sound-design.wav`.
The beats use the 0, 3, 7.5, 12, 17.5, 23, 27, 31 second windows. Headlines and
three diagram nodes share sound hits. Audio is deterministic synthesis, stereo
48 kHz PCM; there are no borrowed samples. Change the score for the project.

Adapt `build.mjs` for the project's visual model. You may edit generated HTML
directly in Studio, but rebuilding overwrites it: retain those edits in the
generator or preserve an independently authored composition before rebuilding.
Do not imply that relabeling three nodes proves a product feature or live demo.

## Review and export

1. Run `npm test` and `npm run check`. A successful audit supplements visual review.
2. Run `npm run preview` to open Studio. Review all seven scenes and sound.
3. Use `npx hyperframes snapshot --at 1.5` for stills; repeat at scene midpoints
   (5.25, 9.75, 14.75, 20.25, 25, 29). Inspect one frame before and at each cut,
   plus the entrance 0.25 and 0.65 seconds after it and the final frame at 30.9833.
4. After editorial approval, run `npm run render`. This requests delivery quality,
   1920×1080 at 60 fps, with output at `output/bravado-hyperframes.mp4`.
5. Run `npm run verify`: Bravado checks 31 seconds, 60 fps, H.264/AAC stereo,
   resolution and complete decoding of both streams. Watch and listen to the
   exported file; technical verification cannot establish perceptual quality.

Deliver the MP4 and editable project: brief, beat sheet, HTML, generator, package
files and local assets. Exclude `node_modules`; recipients restore with `npm ci`.
Record factual gaps and any playback/listening limits honestly. No command here
publishes the film or changes the source product.

## Compatibility

Upstream documentation: [HyperFrames](https://github.com/heygen-com/hyperframes).
Run the pinned dependency via npm scripts. Upgrading the pin is a deliberate
change: rebuild, audit, inspect boundaries and verify another export. Run the
Python regression suite too when changing shared Bravado code.
