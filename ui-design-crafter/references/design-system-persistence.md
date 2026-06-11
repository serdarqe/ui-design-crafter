# Design System Persistence

Use this file when creating, changing, extending, or reviewing UI inside a project that may receive more than one design pass. The goal is to keep screens coherent across separate agent runs.

## Core Rule

Before designing or implementing UI, look for an existing project design system record. Reuse it unless the user explicitly asks to change direction.

Preferred project paths:

- `design-system/MASTER.md`
- `design-system/pages/{screen-name}.md`

If the project already uses another documented location, follow the project convention and do not create a competing system.

## When To Create Or Update

Create `design-system/MASTER.md` when:

- The project has no persistent design system record.
- The task establishes a new theme, product tone, UI kit, game UI language, or multi-screen visual system.
- You are building two or more related screens such as main menu + shop, dashboard + detail panel, or HUD + inventory.

Create or update `design-system/pages/{screen-name}.md` when:

- A screen needs page-specific layout, background, component, state, content, or responsive decisions.
- The screen intentionally diverges from the master system.
- A later task changes one screen without changing the whole product.

Update existing files when:

- A design decision changes.
- A new component/state/token is introduced.
- A visual QA result reveals a rule that should persist.

Do not update when:

- The change is tiny and does not affect future UI decisions.
- The repo has a mature design system elsewhere and the new file would duplicate it.
- The user asks for an isolated throwaway prototype.

## Discovery Order

1. Check for `design-system/MASTER.md`.
2. Check for `design-system/pages/`.
3. Check common alternatives such as `docs/design-system.md`, `docs/ui.md`, `DESIGN_SYSTEM.md`, `.storybook/`, token files, theme files, Tailwind config, Figma links, and existing component docs.
4. Inspect existing CSS variables, theme tokens, shared components, layout primitives, and screenshot/output folders.
5. Only create new design-system files after confirming no project convention already owns the same role.

## Master File Contract

`MASTER.md` records decisions that should remain stable across screens:

- Product, audience, platform, and input model.
- Theme row and blended theme logic.
- Background/scene art direction.
- Color roles and semantic token meaning.
- Typography and type scale.
- Spacing, radius, elevation, border, and motion rules.
- Component material and state language.
- Icon/source policy.
- Accessibility and QA gates.
- Open questions and known exceptions.

It should be concise enough to read before future UI work. Do not turn it into a changelog or a dumping ground.

## Page Override Contract

Page override files record only what differs or needs extra specificity for one screen:

- Screen purpose and primary task.
- Layout zones and responsive behavior.
- Background focal point and safe zones.
- Components used on that screen.
- State requirements and edge cases.
- Content/data assumptions.
- QA evidence and outstanding risks.

If a page file repeats most of `MASTER.md`, shorten it and reference the master.

## Update Rules

- Preserve user-authored decisions. Add new notes below existing sections instead of replacing the whole file.
- Never erase previous design direction without a clear reason.
- When changing a master decision, note the reason and the screens affected.
- Prefer specific tokens and component names over vague wording.
- Keep decisions implementation-neutral when possible, but reference actual project files when a token/component exists.
- Page overrides may refine master rules, but should not silently contradict them.

## Suggested Workflow

When starting UI work:

1. Read existing master/page files if present.
2. If absent and the task is multi-screen or establishes a visual system, create them from:
   - `assets/templates/design-system-master.md`
   - `assets/templates/page-override.md`
3. Fill only decisions that are known from the user request, codebase, existing UI, or implemented result.
4. During implementation, keep UI changes aligned with the master.
5. After visual QA, update page files with evidence and any accepted risks.

## Naming Pages

Use lowercase kebab-case page names:

- `main-menu.md`
- `shop.md`
- `mission-select.md`
- `inventory.md`
- `hud.md`
- `dashboard.md`
- `detail-panel.md`
- `settings.md`
- `onboarding.md`

If a code route already has a name, match the route where practical.

## Conflict Handling

If the user request conflicts with the master:

- Follow the user request for the current task.
- Explain the conflict briefly.
- Update the master or page override only when the change should persist.
- If uncertain, put the change under `Open Questions` instead of rewriting the system.

## Completion Check

Before final delivery on a UI task, answer:

- Did I check for an existing design system record?
- If this creates a visual direction, did I create or update `MASTER.md`?
- If this changes a specific screen, did I create or update its page override?
- Do the implementation, screenshot evidence, and persisted decisions agree?
- Did I avoid duplicating a mature existing design system?
