# Heavy Mettle — Decision log

Newest first. Each entry: what we decided, why, and what would change it.
"Verified" means a human ran it in Unreal and reported back. Everything else is planned or desk-checked only.

---

## 2026-10-18 — Provisional engine baseline: UE 5.5.4 (Claude)

**Decision.** Build the first playable game on **Unreal Engine 5.5.4**, using Epic's plain **Games > Third Person > Blueprint** template. This replaces the 5.8.3 + "Combat variant" baseline *for now*.

**Why.**
- 5.5.4 is already installed on the owner's PC. 5.8.3 is not.
- The Combat variant (player combos, health, enemy AI) only exists in UE 5.6 and newer, so it isn't available on 5.5.
- Free Fab assets will be preferred, but each pack's "Supported Engine Versions" must include 5.5 before import. (UAF H2H Combat was already noted as built for 5.6, so it stays out.)

**Consequences.**
- Enemies, melee, health and lock-on must be built in Blueprints (or from free 5.5-compatible Fab assets) instead of inherited from the Combat template.
- `place_combat_enemies.py` and `create_blueprint_scaffolds.py` are not part of the 5.5 path yet.
- `verify_project.py` no longer fails when the 5.6+ `BP_CombatEnemy` is missing. It now requires a third-person character Blueprint instead.
- Older 5.8 docs (`START_HERE_WINDOWS_58.md`, `BLUEPRINT_BUILD.md` section 0) are kept for reference, not deleted.

**Revisit if** a needed free asset or feature requires a newer engine, or the owner installs 5.6+. Any engine change gets its own entry here.

## 2026-10-18 — Scope: first playable only (owner)

Work only toward the first playable game (the 15-minute Missing Cells loop in `docs/CREATIVE_DIRECTION.md`). No sequel features. One small, testable change per pull request, each with beginner instructions and a manual test.

## 2026-10-18 — Which repository is Heavy Mettle (Claude)

`DepressedRedPanda/attempt-two` is the Heavy Mettle repo. `DepressedRedPanda/The-Game` is a separate C++ fantasy project (Veil of Ash: Hollowreach) and is not used, per the existing rule in `CLAUDE.md`.

## 2026-10-18 — Level generator kept as-is (Claude)

`Scripts/build_dustfall.py` only uses engine shapes and standard editor Python, so it should not depend on 5.8. It was dry-run outside Unreal with a stand-in module: 238 actors created, player spawn clear, 2 cosmetic cover overlaps. **Not yet run inside Unreal.** Step 1 (`docs/START_HERE_UE55.md`) is the real test.
