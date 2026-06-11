# UI Performance (Without Sacrificing Quality)

Use this when UI may affect frame rate, responsiveness, load time, or battery in a game, app, or website. The priority is the highest-quality design; performance is a constraint you meet **by the implementation**, never by lowering visual or interaction quality.

## Core Rule

- Design the best UI first. Then hit a performance budget by choosing equivalent-looking, cheaper techniques - not by removing effects, dropping fidelity, or simplifying the design.
- Performance is advisory guidance, like a profiler hint: it tells you to optimize the implementation, not to strip polish. Quality stays primary.
- If a budget genuinely cannot be met without a visible quality cut, surface it as an explicit tradeoff for a human to decide. Never degrade the design silently.
- Quality and performance usually agree: "glow on everything", frame stacking, and gradient soup are both AI-look tells and performance costs. Fixing them improves both.

## Quality-Preserving Techniques (same look, lower cost)

- Animate `transform` and `opacity` (GPU-composited) instead of layout properties (width/height/top/left/margin). Identical motion, no reflow/jank. See `motion-and-feedback.md`.
- Bake expensive static effects (glow, soft shadows, gradients, noise, ornaments) into images/sprites/atlases instead of recomputing them live every frame.
- Use sprite/texture atlases and batch draw calls so a rich HUD or many icons render cheaply.
- Reuse and recycle: virtualize long lists/grids (render only what is visible), pool particles and UI nodes, cache decoded images.
- Throttle non-critical updates: ambient motion, clocks, and background counters do not need every frame; keep critical state (health, cooldown, input feedback) at full rate.
- Reserve dimensions and avoid per-frame layout: fixed-size meters/counters, stable sizes, and (on web) `content-visibility`/`contain` prevent reflow without changing the look.
- Prefer one signature effect done well over the same effect on every element - cheaper and better-looking.

## Game UI

- Watch overdraw and fill-rate: stacked translucent panels, full-screen blur, and glow on every element are expensive on mobile/low-end GPUs. Keep the look with baked textures, fewer transparent layers, or solid/edge treatments that read identically.
- Give particles and effects a budget (max count, lifetime, spawn rate) and pool them; scale density per device tier instead of removing the effect.
- Batch HUD/widget draw calls (atlas, shared material); avoid a separate draw call per icon or slot.
- Keep per-frame UI work tiny: precompute layouts, update only changed widgets, throttle ambient motion. A HUD that drops frames hurts game feel more than a slightly cheaper effect - protect a stable frame rate, battery, and thermals.
- Test on a low-end target device, not just a high-end one; budget by device tier and scale effect density, never core readability.

## App (Native And Cross-Platform)

- Recycle/virtualize lists and grids; do not inflate a view per row.
- Keep the main/UI thread free: do image decode, parsing, and heavy work off it; show skeletons that match the final layout while loading.
- Cache and right-size images (decode at display size); never load a full-resolution asset into a small thumbnail.
- Minimize overdraw and view depth; flatten unnecessary nested containers (this also reduces frame stacking).
- 60fps scroll and responsive input are part of quality: jank and input lag read as low quality even with beautiful visuals.

## Web

- Core Web Vitals (LCP, CLS, INP), font loading, responsive images, and lazy-loading are covered in `app-ui-patterns.md` (Web Performance). Same principle: protect speed and stability through implementation choices, not by cutting design quality.

## Measure (advisory)

- Profile on a representative low-end device and throttled network; never judge performance on a fast dev machine alone.
- Set a budget per platform tier (frame time, draw calls, page weight, list-item cost) and track it; treat an overrun as a prompt to optimize the implementation first.
- Use the project's profiler (engine profiler, browser performance panel, platform tooling). `scripts/check_ui_tokens.py` flags a few static perf risks (layout-animated properties, heavy live effects) as INFO suggestions - hints to use a cheaper equivalent, never instructions to remove an effect.
- After optimization, if a budget still forces a visible quality cut, raise it as an explicit decision rather than degrading silently.

## Sources

- web.dev / Core Web Vitals; Apple and Google platform performance guidance; game engine profiling docs. See `references/source-bibliography.md` for the broader standards behind these rules.
