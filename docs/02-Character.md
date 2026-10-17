# 02 — The character: Mettle

Goal: a human-looking android with a **sword on his back**, a **pistol on his right hip**, and a **long duster coat that flows** with cloth physics.

## 1. Base class
- **With GASP (recommended):** `BP_HM_Player` → **Class Settings → Parent Class = `CBP_SandboxCharacter`**. (The setup script already does this if GASP was in the project.) You inherit motion-matched movement, sprint, and vault/mantle traversal.
- **Without GASP:** leave the parent as `Character`, set the mesh to the UE5 mannequin (`SKM_Manny`) and add the movement events in step 5.

## 2. Make him look human (MetaHuman)
1. Open **MetaHuman Creator**, make a young man (late teens look — he's "a kid"). Short messy hair, clean face.
2. Bring him into the project (MetaHuman plugin / Fab → Add to Project).
3. GASP ships with a way to drive MetaHumans: follow GASP's own *"Using MetaHumans"* note in its level/README. In short: the MetaHuman body follows the sandbox character's skeleton with **Leader Pose** or a **Retarget Pose From Mesh** node.
4. Android tells (material tweaks on the MetaHuman skin material instance):
   - Faint **seam lines** at jaw, neck and wrists (a seam texture in the detail normal slot).
   - **Eyes:** raise emissive on the iris a little — glow only shows in dark places.
   - Optional: a small open panel on the forearm using a decal.

## 3. Sockets for the sword and pistol
Open the character's **Skeleton** asset → right-click a bone → **Add Socket**:

| Socket | Bone | Purpose | Starting transform (tweak with Preview Asset) |
|---|---|---|---|
| `Sheath_Back` | `spine_05` | Sword resting on back | Loc (−10, −18, 0) · Rot (0, 0, 135) |
| `Holster_Hip_R` | `thigh_r` (or `pelvis`) | Pistol on right hip | Loc (−5, 12, −5) · Rot (0, 90, 0) |
| `Sword_Hand` | `hand_r` | Sword in hand | Loc (0, 0, 0) · Rot (0, 0, 90) |
| `Pistol_Hand` | `hand_r` | Pistol in hand when aiming | Loc (0, 0, 0) · Rot (0, 0, 0) |

Right-click each socket → **Add Preview Asset** → your sword/pistol mesh, and nudge it until it looks right.

## 4. Attach the weapons
The script added `SwordMesh` and `PistolMesh` (Static Mesh components) to `BP_HM_Player`. In the Components panel:
1. Drag each one onto **Mesh** (the character mesh).
2. `SwordMesh` → Details → **Parent Socket = `Sheath_Back`**, Static Mesh = your sword, **Collision = NoCollision**.
3. `PistolMesh` → **Parent Socket = `Holster_Hip_R`**, Static Mesh = your pistol, Collision = NoCollision.
4. Add a socket named `Muzzle` on the pistol *static mesh* (open the mesh → Socket Manager) at the barrel tip, and sockets `Blade_Base` / `Blade_Tip` on the sword mesh. The combat guides use them.

**Draw / sheathe (functions on BP_HM_Player):**
```
DrawSword:     Attach Component To Component (Target SwordMesh, Parent Mesh, Socket "Sword_Hand",
               Location/Rotation/Scale rule = Snap to Target)
SheatheSword:  same, Socket "Sheath_Back"
DrawPistol:    SheatheSword → Attach PistolMesh to "Pistol_Hand"
HolsterPistol: Attach PistolMesh to "Holster_Hip_R"
```
- Call `DrawSword` at the start of any melee attack.
- On **IA_Aim Started** call `DrawPistol`; on **IA_Aim Completed** call `HolsterPistol`.
- After 6 seconds with no attack (`Set Timer by Event`, reset every attack) call `SheatheSword`.
- Later, swap the instant attach for a short draw montage with an **Anim Notify** that calls the attach.

## 5. Movement (only if you're NOT on GASP)
```
IA_Move (Triggered)  → Break Vector2D → Add Movement Input (Get Actor Forward from Control Rotation yaw, Y)
                                      → Add Movement Input (Right vector, X)
IA_Look (Triggered)  → Add Controller Yaw Input (X) → Add Controller Pitch Input (Y)
IA_Jump (Started)    → TryClimb (see 03) → if false → Jump
IA_Sprint Started/Completed → Max Walk Speed 600 / 350   (drains Stamina in Tick, see 08)
```
Camera: Spring Arm (Target Arm Length 320, Socket Offset (0, 45, 70), Use Pawn Control Rotation ✔) → Camera.
Character Movement → **Orient Rotation to Movement ✔**, Use Controller Rotation Yaw ✘.

## 6. Dodge
```
IA_Dodge (Started) → Branch (Stats.Stamina >= DodgeStaminaCost AND not bIsDodging)
  → Stats.SpendStamina(DodgeStaminaCost) → bIsDodging = true
  → Launch Character (Last Movement Input Vector × 900, or −Forward × 700 if no input; XY override ✔)
  → (Optional) play a roll montage
  → Delay 0.45 → bIsDodging = false
```
While `bIsDodging` is true, `ReceiveHit` (see 04) ignores damage — that's the i-frames.

## 7. The long coat with cloth physics
1. **Get a coat.** Options: a free long coat from Fab, MetaHuman's long-coat outfit options, or model one. It must be a **Skeletal Mesh** skinned to the same skeleton.
2. Add it to `BP_HM_Player` as a **Skeletal Mesh Component** named `Coat`, child of `Mesh`. In Construction Script / BeginPlay: `Coat → Set Leader Pose Component (Mesh)`.
3. Open the coat skeletal mesh → **Clothing** (Window → Clothing):
   - Right-click the coat's material section in the viewport → **Create Clothing Data from Section** → then **Apply Clothing Data** to that section.
   - **Activate Cloth Paint**. Paint **Max Distance**:
     - Shoulders, collar, chest: **0** (pinned to the body).
     - Waist: ~5.
     - Coat tails / hem: **40–60** (free to swing).
     - Smooth the gradient — hard jumps look rubbery.
   - Paint **Backstop** at waist level so the coat can't pass inside the legs.
4. Cloth Config (Chaos):
   - Mass: Density ~0.35 (leather-heavy coat)
   - Gravity Scale 1.0 · Damping 0.02 · Friction 0.6
   - **Long Range Attachment / Tether Stiffness** 1.0 (stops stretching)
   - Collision Thickness 2.0 · Self Collision off (performance)
5. Collisions: open the character's **Physics Asset** → make sure thighs and calves have capsules; on the coat's clothing data pick that physics asset under **Physics Asset**. This stops the coat clipping through legs.
6. Wind: drop a **Wind Directional Source** in the level (Strength 0.3–0.6, a little Gust). Coat tails will flap in the desert wind — very western.
7. If the coat jitters on dodge/teleport: on the Coat component, enable **Teleport → Reset Cloth** when distance > 300.
