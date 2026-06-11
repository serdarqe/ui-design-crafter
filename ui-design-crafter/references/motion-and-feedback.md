# Motion And Feedback

Use this when adding transitions, animation, micro-interactions, or multi-sensory feedback (visual, haptic, audio). Motion is part of the design, not decoration. Get a starting motion preset from `scripts/search_design_tokens.py "<domain>" --kind motion`.

## Core Rule

Motion must do a job: show state change, preserve continuity, direct attention, or confirm an action. If an animation does not help the user understand what happened or what to do next, cut it. "Everything animates" is an AI-generated tell, the motion equivalent of glow-on-everything.

## Timing And Easing

- Keep a small, consistent set of durations, not a unique value per element. Common scale: 90-120ms (hover/press feedback), 150-250ms (state change, small enter/exit), 250-400ms (larger transitions, sheets, screens). Game feedback often runs faster; calm/premium apps slower.
- Use decelerate (ease-out) for elements entering, accelerate (ease-in) for leaving, and standard ease-in-out for moves. A standard curve like `cubic-bezier(0.2, 0, 0, 1)` works for most UI; reserve overshoot/bounce for playful or reward moments.
- Match speed to domain: tactical/finance/SaaS = fast and quiet; casual/arcade/kids = snappier and more expressive; horror/premium = slower and deliberate.
- Never animate live data (prices, timers, counters) in a way that makes the value hard to read; update in place with stable dimensions.

## Micro-Interactions

- Give frequent controls (buttons, toggles, tabs, slots) a brief, consistent press/hover/active response. Keep it subtle and uniform so it reads as one material system.
- Animate one property cluster (opacity + transform) rather than layout properties (width/height/top/left) to avoid reflow jank and layout shift.
- Loading: prefer skeletons or progress that preserve final layout over spinners that collapse it. Use optimistic UI only when failure is rare and recoverable.
- Reserve attention-grabbing motion (pulse, shake, confetti, glow) for genuine state: success, error, reward, low-health, your-turn. If it is always on, it stops meaning anything.

## Reduced Motion (required)

- Always provide a `prefers-reduced-motion: reduce` path. Drop transforms, parallax, auto-playing loops, large slides, shake, and bounce; keep essential opacity/instant state changes.
- Reduced motion is accessibility, not an afterthought: vestibular users can get motion-sick from parallax and big transitions.
- In games, expose a "reduced motion / reduced flashing" option in settings, and avoid full-screen flashes (seizure risk) regardless of the setting.

## Multi-Sensory Feedback

- Pair an important state change with more than one channel: visual + sound and/or haptic, so it survives a muted device, a busy screen, or low vision.
- Never rely on sound or haptic alone for critical state; never rely on color alone (see `color-theory-for-ui.md`).
- Keep audio and haptic short, purposeful, and interruptible; respect system mute, volume, and haptic settings. Offer per-channel toggles (music, SFX, UI sounds, vibration).
- Game feel: pair hit/pickup/reward with a tight visual + audio + haptic combo, but keep readability of health, cooldown, and danger above the juice.

## App vs Game Notes

- App: motion is mostly continuity and status (navigation, expand/collapse, validation, toasts, loading). Keep it short, quiet, and consistent; respect reduced motion; never block input behind an animation.
- Game: motion is also game feel and reward, and can be more expressive, but the HUD and critical feedback must stay readable during effects, and reduced-motion/flash options are essential.

## Validation

- Does each animation communicate state, continuity, attention, or confirmation? If not, remove it.
- Is there a reduced-motion path, and does the UI still make sense with motion off?
- Do durations come from a small shared scale, or is every element different?
- Do counters, timers, and meters keep stable dimensions while changing?
- Is any critical signal delivered by motion/sound/haptic alone with no visual, color-independent backup?

## Sources

- Material Design motion (duration, easing, choreography); Apple HIG motion and "Reduce Motion".
- W3C WCAG 2.2: 2.3.1 Three Flashes, 2.3.3 Animation from Interactions, prefers-reduced-motion.
- Game UX references on feedback and game feel (see `source-bibliography.md`).
