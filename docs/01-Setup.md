# 01 — Setup & free assets

## 1. Engine version
Install Unreal Engine 5 from the Epic Games Launcher. Pick the **newest version that the Game Animation Sample Project (GASP) lists on its Fab page** — GASP gives us motion-matched locomotion *and* vault/mantle traversal for free, so its version decides ours.

## 2. Free assets (all free, all usable in a commercial game under the Unreal/Fab license — still read each license)

| Need | Free source | Notes |
|---|---|---|
| Locomotion + vaulting/mantling over chest- and head-height obstacles | **Game Animation Sample Project** (Epic, on Fab) | Most important pack. Becomes the player's base class. |
| A real-human-looking character | **MetaHuman Creator** (Epic) | Make a young man; add android seams/glow in his material. GASP supports MetaHumans. |
| Sword, pistol, melee & shooting animations | **Paragon** characters (Epic, free on Fab) — e.g. Greystone, Kwang (sword), Twinblast, Revenant (pistols) | Retarget their animations with the IK Retargeter. |
| Pistol/rifle aim, fire, reload animations | **Lyra Starter Game** (Epic, free on Fab) | Also a great reference for shooter feel. |
| Extra sword/combat clips | **Mixamo** (Adobe, free) | Download as FBX "without skin", retarget to the UE mannequin. |
| Desert/rock/western props | Fab's free filter + the **monthly free** packs, Megascans on Fab | Grab anything "desert", "western", "medieval village", "sci-fi junk". |

How to add a Fab pack: Epic Games Launcher → **Fab** tab (or fab.com) → *Add to My Library* → **Add to Project** → choose `HeavyMettle`.
For GASP (it's a full project, not a pack): create it from the launcher as its own project, then in that project right-click the `Content` folder → **Migrate…** → pick `HeavyMettle/Content`.

## 3. Run the setup script
1. Open `HeavyMettle.uproject`. If it asks to enable plugins or restart, say yes.
2. **Tools → Execute Python Script…** → `Content/Python/heavy_mettle_setup.py`.
3. Read the **Output Log** (Window → Output Log). Lines starting with `[HeavyMettle] TODO:` are things to do by hand.

Re-running is safe — it never touches assets that already exist.
- Different random layout: Output Log → switch "Cmd" to "Python" →
  `import heavy_mettle_setup; heavy_mettle_setup.run(seed=42, rebuild_level=True)`

> **Tip:** migrate GASP **before** running the script. The script finds `CBP_SandboxCharacter` and makes `BP_HM_Player` its child, so climbing and locomotion work immediately.

## 4. Data tables
For each CSV in `Data/`, first make a matching **Structure** (Content Browser → right-click → Blueprint → Structure) in `HeavyMettle/Data`, with these exact field names:

| Structure | Fields (type) |
|---|---|
| `S_HM_Combo` | Sequence (String), DisplayName (Text), DamageMultiplier (Float), StaminaCost (Float), BatteryCost (Float), bKnockback (Boolean), bLaunch (Boolean), bAreaOfEffect (Boolean), Description (Text), **Montage (Anim Montage → Object Reference)** |
| `S_HM_Recipe` | DisplayName (Text), ResultAmount (Integer), ScrapCost, PowderCost, HerbsCost, WireCost (Integer), bNeedsBench (Boolean), Description (Text) |
| `S_HM_Item` | DisplayName (Text), MaxStack (Integer), Description (Text), Icon (Texture 2D → Object Reference) |
| `S_HM_Level` | XPRequired (Integer), PointsAwarded (Integer) |
| `S_HM_Quest` | Title (Text), Giver (Text), Step1, Step2, Step3, Step4 (Text), XPReward (Integer), CreditReward (Integer), Description (Text) |

Then drag each CSV into the `Data` folder → choose **DataTable** → pick the matching structure → name it like the file (`DT_HM_Combos`, …). Columns that aren't in the CSV (Montage, Icon) stay empty — fill them in later by opening the table.

## 5. Game mode & controller
1. Open `Core/BP_HM_GameMode` → Class Defaults → **Default Pawn Class** = `BP_HM_Player`, **Player Controller Class** = `BP_HM_PlayerController`, **HUD Class** = None.
2. Open `Core/BP_HM_PlayerController` → Event Graph:
   ```
   Event BeginPlay
    → Get Enhanced Input Local Player Subsystem (Self)
    → Add Mapping Context (Mapping Context = IMC_HM_Default, Priority = 1)
    → Create Widget (WBP_HM_HUD) → Add to Viewport
   ```
3. If `BP_HM_Player` inherits from GASP's `CBP_SandboxCharacter`, **don't** add events for IA_Move / IA_Look / IA_Jump / IA_Sprint in your player — GASP already handles movement, sprint and traversal with its own input. Our mapping context only adds the combat buttons on top.

## 6. Check the key bindings
Open `Input/IMC_HM_Default`. Every action should have keyboard and gamepad keys. The script tries to add these **modifiers**; if the Output Log says it couldn't, add them by hand:

| Action | Key | Modifiers |
|---|---|---|
| IA_Move | W | Swizzle Input Axis Values (YXZ) |
| IA_Move | S | Swizzle (YXZ) + Negate |
| IA_Move | A | Negate |
| IA_Look | Mouse XY 2D / Gamepad Right 2D | Negate (Y only) |
| IA_SwitchTarget | Gamepad D-pad Left | Negate |

## 7. Play
Open `Maps/L_Testbed`, press **Play**. You should spawn in the middle of a sunlit arena full of grey boxes at two heights. If bandits later won't walk around, press **P** in the viewport: green floor = navigation works. No green? Drag a **Nav Mesh Bounds Volume** in (Place Actors panel) and scale it to cover the arena.

## 8. Git LFS (saving your work to GitHub)
Unreal saves Blueprints as binary `.uasset` files. This repo already routes them through Git LFS (`.gitattributes`). Install it once with `git lfs install`. GitHub limits free LFS storage/bandwidth — check your account's current limits before committing big art packs; you can keep large free packs out of git and just note in the README which Fab packs to add.
