# 06 — Shooting (third-person aim)

Classic over-the-shoulder shooter: hold **Aim**, the camera tightens over the right shoulder, a crosshair appears, and **Fire** shoots where the crosshair points. Hold Fire to charge an **Arc Shot** that spends battery.

## AC_HM_Shooter — variables
| Variable | Type | Default |
|---|---|---|
| bAiming | Boolean | false |
| ClipSize / AmmoInClip | Integer | 6 / 6 (it's a revolver) |
| FireRange | Float | 6000 |
| BaseDamage | Float | 18 |
| FireCooldown | Float | 0.28 |
| bCanFire | Boolean | true |
| ArcShotChargeTime | Float | 0.9 |
| ArcShotBatteryCost | Float | 25 |
| HeldTime | Float | 0 |
| bReloading | Boolean | false |

## Aim
```
IA_Aim Started:
  bAiming = true ; LockOn.Unlock (if locked) ; Owner.DrawPistol
  Orient Rotation to Movement ✘ ; Use Controller Rotation Yaw ✔   (GASP: set its aim/strafe flag)
  Max Walk Speed → 250
  Timeline "AimZoom" (0→1 over 0.15 s):
     Spring Arm Target Arm Length = Lerp(320, 140, Alpha)
     Spring Arm Socket Offset     = Lerp((0,45,70), (0,70,60), Alpha)
     Camera Field of View         = Lerp(90, 70, Alpha)
  HUD → Show Crosshair

IA_Aim Completed:
  bAiming = false ; Owner.HolsterPistol ; reverse the timeline ; restore movement flags/speed ; hide crosshair
```
For an aim pose, play a looping upper-body "pistol aim" montage (Lyra/Paragon pistol anims) using a **Layered blend per bone** from `spine_01` in the Anim Blueprint, driven by a `bAiming` bool.

## Fire
```
IA_Fire Started      → Branch bAiming → HeldTime = 0
IA_Fire Triggered    → Branch bAiming → HeldTime += Get World Delta Seconds
                         → HUD.SetChargeFill(HeldTime / ArcShotChargeTime)
IA_Fire Completed    → Branch bAiming →
                         bArc = HeldTime >= ArcShotChargeTime AND Stats.Battery >= ArcShotBatteryCost
                         Shoot(bArc) ; HUD.SetChargeFill(0)
```

### Function `Shoot (bArc)`
```
Branch bCanFire AND not bReloading → else return
AmmoInClip <= 0 → play dry "click", Reload → return
AmmoInClip −= 1 ; bCanFire = false ; Set Timer (FireCooldown) → bCanFire = true
if bArc → Stats.Battery −= ArcShotBatteryCost

1) Where is the crosshair pointing?
   CamLoc/CamRot = Player Camera Manager → Get Camera Location / Rotation
   Line Trace (Visibility)  CamLoc → CamLoc + Forward(CamRot) × FireRange
   AimPoint = hit ? Impact Point : Trace End

2) Can the gun actually see it? (stops shooting through cover the camera sees past)
   Muzzle = PistolMesh Get Socket Location "Muzzle"
   bArc ? Multi Line Trace (Combat)  : Line Trace (Visibility)
        Muzzle → Muzzle + Normalize(AimPoint − Muzzle) × FireRange
   For each hit actor with AC_HM_Stats:
        Damage = BaseDamage × Stats(owner).DamageMultiplier × (bArc ? 3 : 1)
        Headshot? (Hit Bone Name == "head") → × 2
        TargetStats.ReceiveHit(Owner, Damage, bIsMelee = false, bKnockback = bArc, bLaunch = false)
   (Arc Shot pierces: keep going through every hit; normal shots stop at the first.)

3) Feedback
   Spawn muzzle flash at Muzzle, tracer beam to hit point (teal for Arc Shot)
   Play fire sound, small camera shake (Start Camera Shake) and recoil:
        Add Controller Pitch Input (−0.6) , Add Controller Yaw Input (Random −0.3..0.3)
   HUD hit-marker if something with Stats was hit
```

## Reload
```
IA_Reload Started → Reload
Reload: Branch not bReloading AND AmmoInClip < ClipSize AND Inventory.Ammo > 0
  bReloading = true → play reload montage → Delay 1.4
  Need = ClipSize − AmmoInClip ; Take = Min(Need, Inventory.Ammo)
  AmmoInClip += Take ; Inventory.Ammo −= Take ; bReloading = false
```

## Hip shot (used by the *Quick Draw* combo)
`HipShot(Target)`: same as Shoot but aims straight at `Target` (chest) from the muzzle, no aim needed, ×1.2 damage, costs 1 ammo.

## Grenades
```
IA_ThrowGrenade Started → Branch Inventory.Grenades > 0 AND not bAttacking
  Inventory.Grenades −= 1 → play throw montage
  Spawn Actor BP_HM_Grenade at hand_r socket
  Grenade's Projectile Movement: Velocity = (Camera Forward × 1400) + (0,0,350), Should Bounce ✔
```
`BP_HM_Grenade`: Sphere collision + Static Mesh (a tin can) + **Projectile Movement** (Bounciness 0.3, Friction 0.6).
```
Event BeginPlay → Delay FuseTime (2.2) →
  Sphere Overlap Actors (BlastRadius 450) → for each with AC_HM_Stats:
     falloff = 1 − (Distance / BlastRadius) → ReceiveHit(Instigator, BlastDamage(80) × falloff, false, true, false)
  Spawn explosion FX + sound, Start Camera Shake (World) → Destroy Actor
```

## HUD (WBP_HM_HUD)
Crosshair (hidden unless aiming), charge ring, ammo "4 / 6 · 36", health/stamina/battery bars, interact prompt, quest tracker line, XP bar. Bind each to the player's components with **events** (OnHealthChanged etc.), not Tick bindings.
