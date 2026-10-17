# Rules for AI assistants working on Heavy Mettle

This file is for **any** AI helping on this repo — ChatGPT / Codex, Gemini, GitHub Copilot, Claude. `CLAUDE.md`, `GEMINI.md` and `.github/copilot-instructions.md` all point here so everyone follows the same rules.

## The project
- Unreal Engine 5, **Blueprint-only. Never add C++** (no `Source/` folder, no `.Build.cs`, no `Modules` in the `.uproject`). The owner wants to open, run and edit everything without compiling.
- Read `docs/GDD.md` first for story and tone, then the numbered guides in `docs/`.

## What an AI can and can't change
- `.uasset` / `.umap` files are **binary**. A text-based AI can't read or edit them, and git can't merge them. Don't try to generate or patch them.
- Contribute through text files instead:
  - **Editor Python scripts** in `Content/Python/` that create or modify assets when the owner runs them inside the editor. Must be **idempotent** (skip what exists, never overwrite Blueprint work) and must log `[HeavyMettle] TODO:` instead of crashing when an API isn't available.
  - **Data** in `Data/*.csv` (imported as Data Tables). Keep the header names identical to the structures in `docs/01-Setup.md`.
  - **Guides** in `docs/` written as node-by-node Blueprint steps a beginner can follow.
  - Config in `Config/*.ini`.

## Naming
| Prefix | Asset |
|---|---|
| `BP_HM_` | Blueprint class |
| `AC_HM_` | Blueprint Actor Component |
| `WBP_HM_` | Widget Blueprint |
| `IA_` / `IMC_HM_` | Input Action / Mapping Context |
| `DT_HM_` / `S_HM_` | Data Table / Structure |
| `M_` `MI_` `T_` `SM_` `SK_` `AM_` | Material, instance, texture, static mesh, skeletal mesh, montage |
All game content lives under `/Game/HeavyMettle/`.

## Design rules to keep
- Lock-on only inside **~4.5 m**; beyond that the player aims and shoots.
- Cover heights are exactly **110 / 190 / 300 cm** and climbable (`Climbable` tag).
- Combos are **data-driven** (`DT_HM_Combos`); add moves as rows, not graph branches.
- Systems live in **components** (`AC_HM_*`) so enemies and the player share rules.
- Resource names: Health, Stamina, **Battery** (the "magic" bar), Speed, Damage.

## Honesty about what works
- Never bring back the old Hollowreach / VeilOfAsh C++ modules.
- Keep a **WORKS IN PIE** checklist in the README. Only tick a feature after it has actually been played in the editor (Play In Editor). Untested = planned, not done.

## Working together
- One AI/person per branch: `ai/<name>/<feature>` (e.g. `ai/gemini/crafting-ui`). Open a pull request into `main`; don't push straight to `main`.
- Before editing a Blueprint, lock it (`git lfs lock <file>`) so nobody else edits it at the same time.
- Keep pull requests small and say in the description which guide or system they touch.
- Never commit `Binaries/`, `Intermediate/`, `Saved/`, `DerivedDataCache/`.
