# Heavy Mettle

*A spaghetti western in space.* An android falls from the sky onto a frontier planet, loses his memory, and takes mercenary work for the half-alien villagers who find him — chasing bandits, crossing a mining company, and getting into a little trouble along the way.

Third-person shooter + sword combos, built in **Unreal Engine 5 using Blueprints only (no C++)**, so it opens straight away and you can change anything yourself.

---

## What's in this repo

| Path | What it is |
|---|---|
| `HeavyMettle.uproject` | The Unreal project. Double-click it to open. Blueprint-only, no compiling needed. |
| `Config/` | Project settings: Enhanced Input, default map/game mode, the `Combat` and `Climb` trace channels. |
| `Content/Python/heavy_mettle_setup.py` | **Run once inside the editor.** Creates every Blueprint, input action, key binding, widget and a randomized test level. |
| `Data/*.csv` | Combos, crafting recipes, items, level-up curve, and the first 5 quests — import as Data Tables. |
| `docs/` | Step-by-step, node-by-node guides for building each system in Blueprints. |
| `AGENTS.md` | Shared rules for any AI helping on this repo (ChatGPT/Codex, Gemini, Copilot, Claude). |

## Quick start

1. Install Unreal Engine 5 from the Epic Games Launcher (use the newest version the **Game Animation Sample Project** supports — see [docs/01-Setup.md](docs/01-Setup.md)).
2. Install [Git LFS](https://git-lfs.com) and run `git lfs install` once (Unreal files are big binaries).
3. Clone this repo and double-click `HeavyMettle.uproject`.
4. In the editor: **Tools → Execute Python Script…** → pick `Content/Python/heavy_mettle_setup.py`.
5. Follow the guides in order:

| # | Guide | You get |
|---|---|---|
| 01 | [Setup & free assets](docs/01-Setup.md) | Engine, free packs, data tables, input check |
| 02 | [The character](docs/02-Character.md) | Human-looking android, sword on back, pistol on hip, flowing coat with cloth physics |
| 03 | [Traversal & climbing](docs/03-Traversal.md) | Vault chest-height, mantle head-height, climb ledges |
| 04 | [Melee combos, block & parry](docs/04-Melee.md) | Light/heavy strings, parry + riposte |
| 05 | [Lock-on](docs/05-LockOn.md) | Close-range (≈4–5 m) target lock |
| 06 | [Shooting](docs/06-Shooting.md) | Over-the-shoulder aim, hitscan pistol, charged Arc Shot |
| 07 | [Crafting & inventory](docs/07-Crafting.md) | Ammo, healing, grenades |
| 08 | [Experience & upgrades](docs/08-Progression.md) | Health, stamina, battery, speed, damage |
| 09 | [Enemies, villagers & quests](docs/09-Quests-AI.md) | Bandit AI, dialogue, quest triggers |
| 10 | [Level layout](docs/10-Level-Layout.md) | Random multi-elevation cover arenas |

The story, world and characters are in the [Game Design Doc](docs/GDD.md).

## Controls

| Action | Keyboard & mouse | Gamepad |
|---|---|---|
| Move / Look | WASD / Mouse | Left stick / Right stick |
| Jump · vault · mantle · climb | Space | A |
| Sprint | Left Shift | L3 |
| Dodge | Left Alt | B |
| Light attack | Left mouse | RB |
| Heavy attack | Q | RT |
| Block (tap = parry) | F | LB |
| Lock on / switch target | Middle mouse or Tab / Mouse wheel | R3 / D-pad ← → |
| Aim / Fire (hold = Arc Shot) | Right mouse / Left mouse | LT / RT |
| Reload · Interact | R · E | Y · X |
| Grenade · Heal | G · H | D-pad ↓ · D-pad ↑ |
| Crafting · Quest log | C · J | View · Menu |

Change any of these in `Content/HeavyMettle/Input/IMC_HM_Default`.

## WORKS IN PIE checklist
Tick a box only after it has actually been played in the editor.

- [ ] Setup script runs cleanly
- [ ] Movement + vault/mantle/ledge climb
- [ ] Sword & pistol on the body, coat cloth
- [ ] Melee combos, block, parry
- [ ] Lock-on (close range)
- [ ] Aim & shoot, reload, grenade
- [ ] Crafting, pickups, healing
- [ ] XP, level-up, upgrades
- [ ] Bandit AI, villagers, first quest

Also see the earlier planning docs: [Creative direction](docs/CREATIVE_DIRECTION.md), [Assets policy](docs/ASSETS.md), [Quest outlines](docs/QUESTS.md), `data/balance.json`.

> The setup script was written without access to a running Unreal Editor, so it hasn't been run yet. It's built to skip anything it can't do and print a **TODO** line in the Output Log telling you what to do by hand. If you see a red error, paste it into an issue or a chat and it can be fixed.
