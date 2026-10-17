# 03 — Traversal & climbing

The world is built from three heights, so the player is always choosing an elevation:

| Height | Size | Player action | Combat use |
|---|---|---|---|
| **Chest** | ~110 cm | Vault over / hop up | Crouch-cover, still shoot over it |
| **Head** | ~190 cm | Mantle up onto it | Full cover, blocks bullets |
| **Ledge** | ~300 cm+ | Jump, grab, climb up | High ground — snipers, escape routes |

Everything climbable has the actor tag **`Climbable`** (the setup script tags all blockout boxes). Press **Jump** facing any of them.

## Option A — GASP does it (recommended)
`CBP_SandboxCharacter` already has traversal: running at an obstacle and pressing Jump picks a **hurdle, vault or mantle** based on its height and depth, using motion warping. If `BP_HM_Player` inherits from it, chest- and head-height cover works out of the box.

You only add **ledge climbing** for the tall stuff (below), and call it from GASP's jump/traversal path when GASP's own traversal check fails. In `CBP_SandboxCharacter` find where the Jump input calls its traversal check (search the event graph for "Traversal"); in `BP_HM_Player` override that or hook the *fail* branch to `TryLedgeClimb`.

## Option B — our own simple climb (works with any character)
Add a **Motion Warping** component to `BP_HM_Player` (GASP already has one).

### Function `TryClimb` → returns Boolean
```
1. WALL CHECK
   Sphere Trace by Channel (Climb), radius 20
     Start = Actor Location
     End   = Actor Location + Forward × ClimbTraceDistance (70)
   No hit, or hit actor doesn't have tag "Climbable" → return false
   Save: WallPoint = Impact Point, WallNormal = Impact Normal

2. FIND THE TOP
   FeetZ = Actor Location Z − Capsule Half Height
   Line Trace by Channel (Climb)
     Start = WallPoint − WallNormal × 30 + (0, 0, FeetZ + 340 − WallPoint.Z)
     End   = same XY, Z = FeetZ + 40
   No hit → return false
   LedgeTop = Impact Point ;  Height = LedgeTop.Z − FeetZ

3. ROOM TO STAND?
   Capsule Trace (radius 34, half-height 88) at LedgeTop + (0, 0, 92)
   Hit → return false (no space)

4. PICK THE MOVE
   Height < 60          → return false (just walk/jump)
   60  – 130 (chest)    → Montage = M_Vault   (or M_MantleLow)
   130 – 220 (head)     → Montage = M_MantleHigh
   220 – 330 (ledge)    → Montage = M_ClimbLedge  (jump, hang, pull up)
   > 330                → return false

5. DO IT
   Motion Warping → Add or Update Warp Target from Location and Rotation
       Name = "LedgeTop", Location = LedgeTop, Rotation = Make Rot from X (−WallNormal)
   Character Movement → Set Movement Mode (Flying)
   Capsule → Set Collision Response to Channel (WorldStatic → Ignore)
   bIsClimbing = true
   Play Montage (Mesh, chosen montage)
     On Completed / Interrupted → Set Movement Mode (Walking)
                                 → Capsule collision back to Block → bIsClimbing = false
   return true
```

### Montage setup
In each climb montage add a **Motion Warping** notify state over the part where the body moves up/forward:
- Root Motion Modifier = **Skew Warp**, Warp Target Name = `LedgeTop`, Warp Translation ✔, Ignore Z ✘.
- The animation must have **root motion** (enable *Root Motion* on the anim sequence).

Animation sources: GASP's traversal montages (reuse them even without GASP's character), Mixamo *"Climbing"*, *"Braced Hang To Crouch"*, *"Jump Over"*.

### Wire it up
```
IA_Jump (Started) → Branch (bIsClimbing OR bAttacking) → stop
                  → TryClimb → false → Jump
```

## Tips
- Keep cover heights **exactly** 110 / 190 / 300 cm so every move lines up with the animations.
- Want chest-height cover that *can't* be vaulted (e.g. a fence with spikes)? Remove its `Climbable` tag.
- Debug: set each trace's Draw Debug Type to *For Duration* while tuning.
