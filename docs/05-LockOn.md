# 05 — Lock-on (close range only)

Lock-on only works on enemies **within ~4.5 m** (`LockOnRange = 450` cm — tune between 300 and 500). Anyone farther away has to be aimed at and shot (see 06). This keeps lock-on a sword tool and makes the gun a skill.

## AC_HM_LockOn — variables
| Variable | Type | Default |
|---|---|---|
| LockOnRange | Float | 450 |
| BreakLockRange | Float | 700 (lock drops if they get farther than this) |
| bLockedOn | Boolean | false |
| Target | Actor (ref) | — |
| MarkerWidget | WBP_HM_LockOnMarker (ref) | — |
| OwnerChar | Character | Get Owner → Cast |

## Function `FindBestTarget (IgnoreActor) → Actor`
```
Sphere Overlap Actors (Owner location, Radius = LockOnRange,
                       Object types = Pawn, Class filter = BP_HM_CharacterBase, Ignore = [Owner])
For each Actor:
   skip if its AC_HM_Stats.bIsDead or Actor == IgnoreActor
   Line Trace (Visibility) from camera to Actor → skip if a wall is in the way
   Score = Dot(Camera Forward, Normalize(Actor − Camera))      ← closer to screen center wins
   keep highest Score
return best (or None)
```

## Toggle (BP_HM_Player)
```
IA_LockOn Started → LockOn.ToggleLock

ToggleLock:
  if bLockedOn → Unlock
  else Target = FindBestTarget(None) → valid? → Lock

Lock:
  bLockedOn = true
  Character Movement: Orient Rotation to Movement ✘, Use Controller Desired Rotation ✔
  MarkerWidget = Create Widget (WBP_HM_LockOnMarker) → Add to Viewport

Unlock:
  bLockedOn = false ; Target = None
  Orient Rotation to Movement ✔, Use Controller Desired Rotation ✘
  MarkerWidget → Remove from Parent
```
(If on GASP: GASP has its own rotation mode. Instead of the two movement flags, set GASP's *strafe / "Wants To Strafe"* style variable to true while locked on — search its variables for "Strafe".)

## Every tick while locked on (Component Tick)
```
Branch bLockedOn
  Target invalid OR Target dead OR Distance(Owner, Target) > BreakLockRange → Unlock → return
  Shooter.bAiming → Unlock → return             (aiming always takes over)

  LookAt = Find Look at Rotation (Camera Location, Target Location − (0,0,40))
  New    = RInterp To (Get Control Rotation, LookAt, Delta, Interp Speed 8)
  Controller → Set Control Rotation (Make Rotator: Roll 0, Pitch = Clamp(New.Pitch, −25, 10), Yaw = New.Yaw)

  Marker: Project World to Screen (Player Controller, Target Location + (0,0,60))
          → MarkerWidget Set Position in Viewport (Screen Pos, Remove DPI Scale ✔)
```
Ignore mouse/stick look input while locked (in the IA_Look handler: Branch LockOn.bLockedOn → do nothing).

## Switching targets
```
IA_SwitchTarget Triggered (Action Value = float; wheel up/down or D-pad ←/→)
  Branch bLockedOn AND (no switch in the last 0.25 s)
  Dir = Sign(value)
  Among Sphere Overlap results (same filters as above, excluding current Target):
     Side = Dot(Camera Right, Normalize(Actor − Target))
     keep actors where Side × Dir > 0, pick the one with the smallest Distance to Target
  found → Target = it
```

## Lock-on marker widget
`WBP_HM_LockOnMarker`: a Canvas with one small Image (a diamond or a crosshair ring, 32×32, alignment 0.5/0.5). Optional: a little rotate animation.

## Enemies
Bandits don't need this component — their AI controller faces the player with **Set Focus** (see 09).
