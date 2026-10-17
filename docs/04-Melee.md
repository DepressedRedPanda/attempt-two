# 04 — Melee combos, block & parry

Everything lives in **`AC_HM_Melee`** (attacking) and **`AC_HM_Stats`** (taking hits). Enemies use the same components, so bandits fight with the same rules as you.

## Combo strings
Each attack adds a letter: **L** = light, **H** = heavy. The current string is looked up in `DT_HM_Combos`. Found → play that row's montage. Not found → start over with just the new letter.

| Input | Move | Effect |
|---|---|---|
| L | Slash | — |
| L L | Backslash | — |
| L L L | **Tumbleweed** | spin, knockback, hits everyone around |
| L L H | **High Noon** | launcher uppercut |
| L H | **Spur Thrust** | guard break |
| H | Overhead | slow, strong |
| H H | **Anvil Drop** | ground slam AoE, costs battery |
| H L | **Quick Draw** | slash into a point-blank pistol shot |
| (after parry) L | **Riposte** | big counter hit |

Add new combos just by adding rows (and a montage) — no Blueprint changes.

## Montages
For every row make an **Anim Montage** from a sword animation and set it in the table's *Montage* column. Inside each montage add:
- **Montage Notify Window** named `Hit` — the frames where the blade can hurt.
- **Montage Notify Window** named `Combo` — near the end; pressing an attack here continues the string.

## AC_HM_Melee — variables
| Variable | Type | Default |
|---|---|---|
| CurrentComboString | String | "" |
| bAttacking, bComboWindowOpen, bInputBuffered, bHitWindowOpen | Boolean | false |
| BufferedInput | String | "" |
| ComboResetTime | Float | 0.8 |
| ParryWindowSeconds | Float | 0.2 |
| bRiposteReady | Boolean | false |
| HitActors | Array of Actor | — |
| OwnerChar | Character (ref) | set on BeginPlay = Get Owner → Cast to Character |
| WeaponMesh | Static Mesh Component (ref) | set by the owner on BeginPlay (SwordMesh) |

## Function `TryAttack (Input: String "L" or "H")`
```
Branch Stats.bIsDead OR owner bIsClimbing OR Shooter.bAiming → return

if bAttacking:
    if bComboWindowOpen → NextString = CurrentComboString + Input → go to PLAY
    else               → bInputBuffered = true, BufferedInput = Input → return
else:
    NextString = bRiposteReady AND Input=="L" ? "P" : Input

PLAY:
  Row name = (NextString == "P") ? "PARRY" : NextString
  Get Data Table Row (DT_HM_Combos, Row) 
     Not found → NextString = Input, Row = Input, Get Data Table Row again
  Branch Stats.Stamina >= Row.StaminaCost AND Stats.Battery >= Row.BatteryCost → else return
  Stats.SpendStamina(Row.StaminaCost); Stats.Battery −= Row.BatteryCost
  CurrentComboString = NextString ; CurrentRow = Row ; bRiposteReady = false
  bAttacking = true ; bComboWindowOpen = false ; bInputBuffered = false
  Owner → DrawSword (player only)
  If LockOn.bLockedOn → owner Set Actor Rotation toward target (yaw only)  ← makes combos track the target
  Play Montage (OwnerChar Mesh, Row.Montage)
     On Notify Begin (Name):
        "Combo" → bComboWindowOpen = true
                   if bInputBuffered → TryAttack(BufferedInput)
        "Hit"   → bHitWindowOpen = true ; Clear HitActors
     On Notify End (Name):
        "Combo" → bComboWindowOpen = false
        "Hit"   → bHitWindowOpen = false
     On Completed / On Interrupted:
        bAttacking = false
        Set Timer by Event (ComboResetTime) → if not bAttacking → CurrentComboString = ""
```

## Hit detection (Component Tick, or a 0.016 s looping timer)
```
Branch bHitWindowOpen
  Sphere Trace by Channel MULTI (Channel = Combat... or Visibility), radius 25
     Start = WeaponMesh Get Socket Location "Blade_Base"
     End   = WeaponMesh Get Socket Location "Blade_Tip"
     Ignore Self (owner)
  For each hit:
     Actor = Hit Actor ; skip if HitActors contains it or it's the owner
     Add to HitActors
     Get Component by Class (Actor, AC_HM_Stats) → valid?
       Damage = SwordBaseDamage (20) × CurrentRow.DamageMultiplier × Stats(owner).DamageMultiplier
       TargetStats.ReceiveHit(Attacker = Owner, Damage, bIsMelee = true,
                              bKnockback = Row.bKnockback, bLaunch = Row.bLaunch)
     Spawn hit spark Niagara at Impact Point, play sound
     Hit-stop: Set Global Time Dilation 0.05 → Delay 0.04 (real time) → 1.0   (feels great; keep it tiny)
```
For **bAreaOfEffect** rows (Tumbleweed, Anvil Drop) also do one **Sphere Overlap Actors** (radius 300) around the owner on the first Hit notify.
For **Quick Draw** call `Shooter.HipShot(LockOn.Target)` on the Hit notify.

Set the Combat trace channel to *Block* on enemy capsules/meshes (Collision presets → Custom → Combat: Block).

## Block & parry (on the player)
```
IA_Block Started:
   Stats.bIsBlocking = true
   Stats.bInParryWindow = true
   Set Timer by Event (Melee.ParryWindowSeconds = 0.2) → Stats.bInParryWindow = false
   Play "block idle" pose (Anim BP bool or looping montage)
IA_Block Completed:
   Stats.bIsBlocking = false
```
Tap = parry, hold = block. Light/Heavy are ignored while blocking.

## AC_HM_Stats — function `ReceiveHit(Attacker, Damage, bIsMelee, bKnockback, bLaunch)`
```
Branch bIsDead OR owner.bIsDodging → return         (dodge i-frames)

FacingAttacker = Dot(Owner Forward, Normalize(Attacker Loc − Owner Loc)) > 0.3

if bIsMelee AND FacingAttacker AND bInParryWindow:          ── PARRY ──
     Attacker → Get Component (AC_HM_Melee) → Stagger(1.2 s)
     Owner Melee.bRiposteReady = true → Set Timer 1.0 s → bRiposteReady = false
     Play parry montage + metal "clang" + sparks
     Set Global Time Dilation 0.3 → Delay 0.15 → 1.0
     return

if bIsMelee AND FacingAttacker AND bIsBlocking:             ── BLOCK ──
     SpendStamina(Damage × 1.5)
     if Stamina <= 0 → Guard break: bIsBlocking = false, Owner Melee.Stagger(1.0), Health −= Damage × 0.5
     else           → Health −= Damage × 0.1  (chip), small pushback (Launch Character −Forward × 200)
     return

── HIT ── (bullets always land here; you can't block bullets → use cover)
Health = Clamp(Health − Damage, 0, MaxHealth)
OnHealthChanged.Broadcast(Health, MaxHealth)
if bKnockback → Launch Character(owner, Normalize(Owner−Attacker) × 600 + (0,0,200))
if bLaunch    → Launch Character(owner, (0, 0, 700))
else play a hit-react montage (interrupts the target's attack = "flinch")
if Health <= 0 → Die
```
Event Dispatchers on AC_HM_Stats: `OnHealthChanged (Health, Max)`, `OnDied (Killer)`.

## Function `Stagger(Seconds)` on AC_HM_Melee
Stop Anim Montage → play stagger montage → bAttacking = true (blocks new attacks) → Delay Seconds → bAttacking = false.

## Input wiring (BP_HM_Player)
```
IA_LightAttack Started → Branch Shooter.bAiming → (false) Melee.TryAttack("L")
IA_HeavyAttack Started → Branch Shooter.bAiming → (false) Melee.TryAttack("H")
```
(On gamepad RT is both Heavy and Fire — the aim check decides which one happens.)
