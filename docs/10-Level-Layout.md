# 10 — Level layout: random cover at different heights

Rules every combat space follows:
1. Only three heights: **chest 110 cm**, **head 190 cm**, **ledge 300 cm** (or 380 = ledge stacked on head).
2. **Everything is climbable** (tag `Climbable`) unless it's on purpose not.
3. Every high platform has a **step chain**: chest block → head block → platform, so you can always get up.
4. Mix it up: no two fights should feel like the same room.

`L_Testbed` (made by the setup script) already follows these rules with a seeded random layout. Re-roll it with `heavy_mettle_setup.run(seed=123, rebuild_level=True)`.

## BP_HM_ArenaGenerator — random layouts inside the editor and at runtime
Drop it in any level, change **Seed**, and the layout regenerates immediately (it runs in the Construction Script, so you see it while editing). Ticking "Randomize On Play" gives a new layout every time.

Components: three **Instanced Static Mesh** components — `ChestISM`, `HeadISM`, `PlatformISM` — all using `/Engine/BasicShapes/Cube` (or your own crate/wall meshes sized to the heights), Collision = BlockAll, Component Tags = `Climbable`. Actor Tags: `Climbable`.

Variables (all *Instance Editable*): `Seed (7)`, `AreaSize (5000)`, `CoverCount (24)`, `HeadCount (12)`, `PlatformCount (5)`, `ChestHeight (110)`, `HeadHeight (190)`, `LedgeHeight (300)`, `SpawnClearRadius (400)`, `bRandomizeOnPlay (false)`.

**Construction Script**
```
Clear Instances (ChestISM, HeadISM, PlatformISM)
Stream = Make Random Stream (Seed)

Loop CoverCount:
   Spot = RandomSpot(Stream)
   Length = Random Integer in Range from Stream (2, 4)
   Yaw    = Random Integer in Range from Stream (0, 3) × 45
   ChestISM → Add Instance (Transform: Loc (Spot.X, Spot.Y, ChestHeight/2),
                              Rot (0, 0, Yaw), Scale (Length, 0.6, ChestHeight/100))

Loop HeadCount:  same idea, HeadISM, Scale (Random 2–3, 1, HeadHeight/100), Yaw 0 or 90

Loop PlatformCount:
   Spot = RandomSpot(Stream) ;  Top = Random Bool from Stream ? LedgeHeight : LedgeHeight + HeadHeight − ChestHeight
   PlatformISM → Add Instance (Loc (Spot, Top/2), Scale (6, 6, Top/100))
   HeadISM     → Add Instance (Loc (Spot + (400,0,0), HeadHeight/2),  Scale (2, 2, HeadHeight/100))   ← steps
   ChestISM    → Add Instance (Loc (Spot + (600,0,0), ChestHeight/2), Scale (2, 2, ChestHeight/100))
```
**Function RandomSpot(Stream) → Vector** (pure): pick X,Y with *Random Float in Range from Stream* (±AreaSize/2); if both |X| and |Y| < SpawnClearRadius, nudge X out to SpawnClearRadius. Return (X, Y, 0) **relative to the actor** (Add Instance uses local space by default).

**Event BeginPlay**: `bRandomizeOnPlay` → Seed = Random Integer (99999) → call a custom event that runs the same generation graph (put the generation in a function called from both places).

Navigation: put a **Nav Mesh Bounds Volume** over the arena and set *Project Settings → Navigation Mesh → Runtime Generation = Dynamic* so bandits path around runtime-generated cover.

## Designing real places (towns, canyons, mesas)
- Block out with the grey cubes first (or Modeling Mode → Create → Box with exact heights), play-test, then swap in art.
- **Dustwell (town):** low walls (chest) along streets, building corners (head), rooftops (ledge) reachable by crates → the classic western rooftop shootout.
- **Pump house (Dry Wells):** interior with chest-height machinery; a catwalk at ledge height for gunhands.
- **Canyon camp:** stacked rock shelves at all three heights; ore carts as moving chest-height cover.
- **Mesa (boss):** climb up a step chain under fire from lookouts; arena on top is flat with a ring of chest-height rocks so Kade can't be kited forever.
- Put materials (scrap/herbs/wire) on high ground to reward climbing.
