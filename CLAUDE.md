# CLAUDE.md — Vision AI teaching-slide production rules

These are mandatory instructions for every agent that creates, edits, registers, reviews, or approves visual teaching slides in this workspace.

## Authority and scope

1. Read [`IMAGE_STYLE_GUIDE.md`](IMAGE_STYLE_GUIDE.md) before making any slide image or image renderer.
2. For the model-selection course, also read the relevant Markdown source and [`teaching-images/vision-ai-model-selection/course-delivery/STYLE_AUDIT.md`](teaching-images/vision-ai-model-selection/course-delivery/STYLE_AUDIT.md).
3. When instructions conflict, the visual rules in `IMAGE_STYLE_GUIDE.md` outrank an existing renderer, an old PNG, a test that only checks pixels, a manifest state, or a previous QA row.
4. Existing `*_cardgrid.py` renderers and the phrase “technical blue grid” are not style references. Do not use them to create new delivery visuals.

## Required page decision before drawing

For every logical page, record a short preflight in the page QA document before rendering:

- the one-sentence lesson objective;
- whether it is **C — Engineer + AI Story** or **D — Before & After**, with a reason;
- one primary reading path from problem/input to method to evidence/limit to action;
- exactly three or four major visual nodes (a side rail and the bottom step summary do not count);
- one named, guide-conformant reference page to emulate;
- one sentence for the pale-yellow takeaway.

If this preflight cannot be completed, stop and design the page; do not start with an existing generic renderer.

## Non-negotiable visual contract

Every approved delivery image must have all of the following:

- white or very light blue-gray 16:9 canvas;
- bold black Traditional-Chinese headline without page number, slide number, title badge, logo, or watermark;
- C or D composition, one readable causal story, and three or four major visual nodes;
- rounded white/light-blue cards with pale-blue borders, blue pill headers, and thick blue causal arrows;
- concrete and technically plausible semiconductor, AOI, camera, sample, model, result, or engineering-action visuals;
- green = verified/pass, orange = uncertainty/review, red = risk/reject;
- a **single pale-yellow `#FFF4CC` takeaway banner**, orange-yellow border, and lightbulb icon at the bottom;
- text large enough to read in a classroom projection.

Never approve these substitutions:

- dense card-grid / dashboard layouts, including many equal-width tiny cards;
- deep dark, cyberpunk, glowing-control-room, or dark-dashboard canvases;
- a blue or white conclusion strip in place of the yellow takeaway;
- slide/page-number badges anywhere on the image;
- decorative engineers, robots, AI faces, unrelated PCB art, empty panels, tiny text, or multiple competing reading paths.

## Production and review gates

1. A new renderer or a new model family produces one prototype first.
2. Render it at final resolution and inspect the actual PNG, not only source code or a thumbnail.
3. Confirm the C/D layout, causal path, visual-node count, guide reference match, title legibility, colors, no page badge, and yellow takeaway.
4. Only then may the remaining pages in that family be generated. Inspect every final page individually before approval.
5. Any failed page blocks further production from the same renderer. Fix the renderer, create a versioned output, and re-run the prototype review.
6. Do not overwrite an approved file. Retain the old version for audit and register only the visual-reviewed new version as active.

## Validation requirements

Automated tests are necessary but insufficient.

- Tests must verify canvas size, bright background, and presence of the yellow takeaway region.
- Tests must not encode the old card-grid or blue-takeaway signature as a success condition.
- The renderer test, asset creation, manifest build, and manifest validation may succeed while the visual remains unapproved.
- `visual_status: approved` may be written only after the preflight and the final PNG visual review both pass.

## Five-file intent gate

The user's visual intent is carried by these five Markdown files and must be
visible in every new visual workitem: `CLAUDE.md`, `IMAGE_STYLE_GUIDE.md`,
`TEACHING_REVIEW_LOG.md`, `TEACHING_SCORING_RUBRIC.md`, and
`TEACHING_WEBPAGE_GUIDE.md`. A topic must first record a page preflight with
the objective, C/D decision, one reading path, exactly 3–4 major nodes, a
named reference page, and the single `#FFF4CC` takeaway. Run
`tools/validate_teaching_preflight.py` before rendering; it fails when the
brief, reference, node count, source packet, or user-review state is missing.
The validator is a consistency gate only: actual desktop/mobile PNG review
and explicit user acceptance remain separate evidence and status fields.

## Current remediation state

The audit originally found 181 active visual assets: 18 guide-conformant, 39 needing only page-badge removal, 18 needing takeaway/style correction, 102 dense-card-grid redesigns, and 4 dark-dashboard redesigns. `FDNIN-01` v03 is the first accepted C-story remediation prototype; `CLIP-01` v01 is the first new-family C-story prototype accepted under this gate, and `CLIP-02` v01 separately passed its architecture-page gate. `CLIP-03` v02 records the required response to a final-resolution readability failure: retain v01, shorten the too-close labels, then re-run all gates. `CLIP-04` v01 is the accepted D-story reference for a selection page: contrast an invalid shortcut with a same-contract local-evidence comparison. `SIGLIP-01` v01 separately passes the new-family C-story prototype gate and makes a pretraining-objective distinction visibly separate from a deployment claim. `SIGLIP-02` v02 records the glyph-compatibility rule: inspect every non-ASCII technical marker in the rendered PNG, retain a failed version, then substitute readable notation before approval. `SIGLIP-03` v01 confirms that the C-story contract layout remains acceptable only when each dependency is legible at final resolution. `SIGLIP-04` v01 applies the D-story baseline rule: objective name can never replace a fixed CLIP baseline with local truth, variance and P95 evidence. `DINOV2-01` v01 is the accepted visual-feature-backbone prototype: render the named downstream score/map/head owner and never present backbone features as a detector claim. `DINOV2-02` v01 separately confirms that the architectural patchify/ViT path must still end at a named downstream owner, rather than an implied output. `DINOV2-03` v02 documents the readability rule for operating contracts: omit redundant fine print rather than shrinking it; retain the rejected render and re-review the versioned replacement. `DINOV2-04` v01 applies the D-story boundary: select only an explicit few-shot or transfer route under fixed feature and local-evidence contracts. The current delivery totals are 193 active assets: 31 guide-conformant, 39 needing only page-badge removal, 18 needing takeaway/style correction, 101 dense-card-grid redesigns, and 4 dark-dashboard redesigns. Use any accepted prototype only as a structural reference, and repeat the same preflight and final-resolution review for each new family and logical page.

<!-- codex-external-advisors:begin v1 -->
## Codex-led external advisor workflow

Codex is the implementation owner. If Claude participates directly, provide planning or review advice only; do not edit, commit, deploy, or access credentials. Grok is treated the same way. Review `.codex/external-advisors.json` for shared provider defaults and keep generated reports out of Git.
<!-- codex-external-advisors:end -->

<!-- AI-PRODUCT-WORKFLOW:START -->
## Durable AI Product Workflow

This project has a persistent local AI workflow in `.ai-product-workflow/`. Its SQLite data, not conversation memory, is authoritative for product work and agent handoffs.

- Follow the controlled graph: Inbox → requirement review → plan → implementation → test → review → done.
- Never mark work done without stored implementation, test, and review evidence.
- Start the UI with `.ai-product-workflow/start-ai-workflow.ps1` and use it to resume work after interruptions.
- Codex is the sole execution runner and is disabled by default. Enable `AI_WORKFLOW_ENABLE_RUNNER=1` only with approval; enable `AI_WORKFLOW_ENABLE_CODE_WRITES=1` only for explicitly authorized implementation.
- Claude and Grok are optional external advisors, never execution agents and never state-transition authority. Keep them disabled unless `advisors.enabled` and an absolute adapter script are configured in `.ai-workflow/config.json`, or `AI_WORKFLOW_ENABLE_ADVISORS=1` is explicitly set for a session. An absolute `AI_WORKFLOW_ADVISOR_SCRIPT` can temporarily override the configured adapter path; never put CLI credentials or tokens in this repository or config file.
- Use the installed `.claude/skills/ai-product-workflow` skill for governed workflow work.
<!-- AI-PRODUCT-WORKFLOW:END -->
