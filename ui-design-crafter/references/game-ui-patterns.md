# Game UI Patterns

Use this reference for game HUDs, menus, inventories, shops, character screens, level select, pause screens, end screens, and touch/controller UI.

## HUD

- Keep gameplay visible. HUD should communicate state without fighting the action.
- Place urgent information near the player's focus area and persistent information near stable screen edges.
- Use strong silhouettes, readable type, and contrast that survives bright, dark, and busy gameplay backgrounds.
- Show health, ammo, cooldowns, resources, objectives, timers, and minimaps only when they affect current decisions.
- Add animation for state change, not constant distraction.
- Keep the center of fast action screens as clean as possible. Use corners and stable edge zones for persistent state.
- Use a 2-3 second glance test under gameplay pressure: critical status should be recognizable without reading long text.
- Use non-diegetic UI for detailed numeric/system information, spatial/geometric cues for direction and threat, diegetic UI for immersion, and meta UI for character state or perception.
- Use a chrome budget. Persistent HUD clusters should usually have either a framed container or framed child controls, not both.
- Avoid the "AI fantasy kit" look: repeated rounded rectangles with the same border, glow, inset highlight, and shadow on every button, slot, and panel.

## Menus

- Main menus need clear play/resume, settings, profile/progression, store where relevant, and exit/back behavior.
- Give the main menu one obvious dominant action (Play/Continue) that wins by size, position, and emphasis; everything else is secondary. Do not render every menu item as an identical glowing rounded rectangle - that is the clearest "AI fantasy kit" tell.
- Pause menus should prioritize resume, restart, settings, and quit. Keep the gameplay scene visible or dimmed when it helps orientation.
- Settings need audio, graphics, controls, accessibility, language, and reset defaults where relevant.
- Treat settings as an accessibility gateway, not a leftover options list.
- Include remapping, readable text size, subtitle controls, colorblind options, audio levels, graphics/performance, and reset defaults when relevant.
- Menus can be expressive, but their chrome should be intentional. Use hierarchy, typography, image composition, state fills, and spacing before adding another decorative frame.

## Inventory, Shop, And Progression

- Inventories need item rarity, type, quantity, equip state, comparison, sorting/filtering, and clear empty slots.
- Shops need price, affordability, owned/equipped state, preview, purchase confirmation, and error feedback.
- Skill trees and upgrades need prerequisites, cost, current rank, locked reasons, previewed effect, and confirmation.
- Character panels need stats, gear slots, cosmetic preview, and comparison states.
- Inventory slots need stable sizing, visible selected/equipped state, locked/unavailable reasons, and rarity cues that do not rely on hue alone.
- Shops must distinguish affordable, unaffordable, owned, equipped, previewed, and purchase-pending states.
- Reserve bright borders/glows for selected, equipped, rare, locked, warning, or purchase-pending states. Default shop cards and slots should be quieter so state changes matter.

## Bottom Action Bar

- The bottom bar (hotbar, ability bar, mobile action cluster) is the most touched surface in action and mobile games. Treat it as one tray with slots, not a row of independently framed cards.
- Keep slot count and slot size stable during play; do not reflow the bar when abilities go on cooldown or when an item is consumed.
- Place the highest-frequency or highest-stakes action where the dominant thumb/cursor naturally rests (Fitts's Law); keep destructive or rare actions out of that path.
- On touch, give each slot a real 44-64px target with spacing so adjacent slots are not mis-tapped during pressure; primary attack/jump should not sit one pixel from a menu button.
- Show keybind or button-prompt hints per slot on keyboard/controller; hide them on pure touch.

## Mobile Game Safe Areas And Ads

- Reserve safe areas first: notch/status bar, rounded corners, home indicator, browser chrome, and platform overlays. Use platform safe-area APIs or CSS `env(safe-area-inset-*)` where available.
- Test mobile game screens at 360x740, 390x844, and 430x932 before calling the layout complete. Bottom hotbars, sticky CTAs, nav, inventory trays, and shop actions must not sit under the home indicator.
- Treat ads as explicit layout regions: top/bottom banner, MREC/rectangle, rewarded-ad CTA, interstitial break, offerwall/store prompt, and consent surface. Reserve slots and define the collapsed/no-ad state.
- Ads must never cover the board, active playfield, timer, health, inventory, close/back controls, primary CTA, or required mission/shop decision. They should not create accidental tap paths near high-frequency actions.
- Rewarded-ad buttons must look like optional value exchange, not the main gameplay command. Use clear labels, reward amount, disabled/no-fill state, loading state, success state, and cancellation path.
- Interstitials belong between rounds, missions, deaths, or menu transitions. Do not interrupt active input, timed puzzles, combat, drag gestures, or purchase confirmation.
- Dev/test ad placeholders should be visually quiet and labeled as placeholders. Do not style them like primary content or let them become the screen's visual focus.

## Board, Playfield, And HUD Balance

- Start with the playable area. Define the minimum board/playfield size before fitting HUD, monetization, mission cards, or action bars around it.
- The board, camera, or action scene should remain the largest and clearest visual subject during play. Persistent HUD belongs on stable edges unless the mechanic requires center placement.
- HUD and action bars must not cover playable cells, target zones, drag paths, aim lines, critical timers, health/resource meters, or feedback bursts.
- Keep board-side panels compact and purposeful: goals, moves, score, threat, or next action. If a panel is not used during a decision, move it to pause, shop, inventory, or post-round.
- Use one bottom tray or distinct floating controls, not both with equal chrome. Inner slots can use fills, recesses, dividers, labels, cooldown overlays, or icon changes instead of full card frames.
- Check thumb zones for one-handed and two-handed play. Primary actions should be reachable; destructive, menu, shop, and ad actions should not sit in the fastest accidental-tap path.
- Timers, counters, move counts, currency, and cooldowns need tabular or fixed-width treatment so the playfield does not shift while values change.

## Cooldowns And Resource Bars

- Cooldown readout: radial sweep or fill over the slot plus a remaining-time number. Keep the icon visible (dimmed) underneath; do not blank the slot. Mark "ready" with a clear, brief state change, not a permanent glow.
- Distinguish "on cooldown" from "no resource" from "locked/unavailable" - three different reasons need three different reads, not one greyed-out look.
- Resource bars (health, mana, stamina, shield, energy) need full, partial, low/critical, empty, regenerating, and damage-flash states. Low/critical must be readable without color alone (segment, icon, number, pulse).
- Keep bars at a stable position and length; deplete the fill, do not shrink the whole widget. Add tick marks or a number when exact values affect decisions.
- Stacked bars (health over shield over armor) need clear layering order and contrast so players read remaining survivability at a glance.

## Item State Model

- Treat rarity, ownership, and equip status as separate dimensions that can combine: a card can be rare + owned + equipped, or common + unaffordable.
- Rarity: encode with frame treatment plus a label/tag, never hue alone. Keep the rarity scale consistent everywhere (shop, inventory, reward, tooltip).
- Locked: show the lock plus the reason (level, currency, prerequisite, event) instead of a silently disabled control.
- Owned vs equipped: "owned" changes the action (Buy -> Owned/Equip), "equipped" adds a persistent badge or border; both must differ from a plain affordable card.
- Affordable vs unaffordable: emphasize price and disable the action with a visible reason; do not hide the price or let players tap into a dead end.
- Default/at-rest items stay quiet so selected, equipped, rare, and locked states are the loud ones.

## Social And Multiplayer

- Lobby/party: show each slot's state clearly - empty, invited, joined, ready, host, you. Ready/host need a distinct mark, not color alone. Keep an obvious empty/invite state.
- Matchmaking has real states: searching, found, connecting, failed, cancel. Show progress and a cancel path; never freeze on a silent spinner.
- Friends/presence: online/away/offline/in-match must be readable without hover and not rely on a green/grey dot alone (add label or icon).
- Chat and emotes need moderation, mute/report, and a way to disable; keep chat from covering critical HUD or input zones; size text for expansion (see `internationalization.md`).
- Leaderboards: show the player's own rank and nearby ranks, not just the top; keep columns aligned with tabular numbers; handle ties, no-data, and very large ranks.
- Voice/quick-chat: show who is speaking and a mute control; never make voice the only channel for required coordination.

## Live-Ops And Meta Progression

- Battle pass / season track: show current tier, progress to next, free vs premium lanes, claimed/claimable/locked rewards, and time remaining. Claimable should be obvious; do not fake-lock owned items.
- Daily/streak/login rewards: show today, what is claimable, what is missed, and the streak state honestly. Avoid manipulative "you will lose your streak" pressure (see app dark-pattern notes in `app-ui-patterns.md`).
- Events/limited-time: show a real countdown and clear entry, rules, and rewards. Never use fake urgency or a countdown that resets.
- Currencies and offers: label each currency consistently, show real cost and balance, and keep store/offer prompts out of core play surfaces; reserve glow/badges for genuinely new or claimable items, not everything.
- Keep meta UI scannable: a returning player should see "what is new, what can I claim, what expires" in one glance.

## Input

- Touch UI needs large hit targets, thumb-friendly placement, and no tiny adjacent controls for high-pressure actions.
- Controller UI needs focus rings, predictable navigation order, button prompts, and clear selected states.
- Keyboard/mouse UI needs hover, focus, pressed, drag, and shortcut affordances where appropriate.
- Touch layouts need large targets and low error cost; avoid tiny adjacent controls during timed play.
- Controller layouts need focus memory: selected state, disabled state, and next/previous focus movement must be unmistakable.
- Mouse/keyboard layouts can support denser inventories, skill trees, hover previews, and shortcut overlays.

## Readability

- Test UI over representative gameplay backgrounds.
- Avoid thin strokes for critical HUD elements.
- Do not hide essential information behind decorative frames.
- Keep numbers, timers, cooldowns, and labels stable so they do not cause layout shifts during play.
- Do not use color alone for health, cooldown, threat, rarity, quest state, or warnings. Add shape, label, icon, pattern, audio, haptic, or motion.
- Use contrast and silhouette before glow. Glow can help state changes but should not be the only readability mechanism.
- Inspect the UI in grayscale or blurred screenshots. If every component is outlined with equal strength, reduce decorative borders and let only important state boundaries remain.

## Genre Hints

- Casual and puzzle games need low HUD noise, large targets, fast success feedback, and shallow menu depth.
- RPG and strategy games can support denser inventory, stats, comparison, and skill-tree screens, but need strong grouping and filters.
- Action and FPS games need minimal center UI, strong peripheral cues, clear damage/threat feedback, and fast settings access.
- Mobile games need touch-first HUD placement and monetization panels that do not obscure core play states.

## Sources

- See `references/source-bibliography.md` for the standards and research behind these rules.
