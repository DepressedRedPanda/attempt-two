# 08 — Experience, levels & upgrades

Kill bandits, finish jobs, discover places → XP. Each level gives **upgrade points** to spend on one of five stats.

| Stat | Per point | Base |
|---|---|---|
| **Health** | +15 max health | 100 |
| **Stamina** | +10 max stamina, +1/s regen | 100 (regen 18/s) |
| **Battery** | +10 max battery | 100 |
| **Speed** | +3% move speed | 1.0× |
| **Damage** | +5% all damage | 1.0× |

XP needed per level comes from `DT_HM_Levels` (row name = the level you're at). Levels 1–9 give 1 point, 10+ give 2.

## XP sources (suggested)
| Source | XP |
|---|---|
| Cutthroat / Gunhand | 25 / 30 |
| Rustjaw Kade | 250 |
| Quest | from `DT_HM_Quests` (100–800) |
| Discovering a named place (trigger box) | 40 |
| Successful parry | 5 (rewards good play) |

## AC_HM_Progression
Variables: `Level (1)`, `XP (0)`, `XPToNextLevel (100)`, `UnspentPoints (0)`, `PointsHealth/Stamina/Battery/Speed/Damage (0)`.
Dispatchers: `OnXPChanged (XP, XPToNext, Level)`, `OnLevelUp (NewLevel)`.

```
AddXP (Amount)
   XP += Amount
   Loop While XP >= XPToNextLevel:
       XP −= XPToNextLevel ; Level += 1
       Row = Get Data Table Row (DT_HM_Levels, Name = ToString(Level − 1))
       UnspentPoints += Row.PointsAwarded
       NextRow = Get Data Table Row (DT_HM_Levels, ToString(Level)) → XPToNextLevel = NextRow.XPRequired
                  (row not found → max level, XPToNextLevel = 999999)
       OnLevelUp.Broadcast(Level)
   OnXPChanged.Broadcast(...)

SpendPoint (Stat: Name)   — "Health" | "Stamina" | "Battery" | "Speed" | "Damage"
   Branch UnspentPoints > 0 → UnspentPoints −= 1
   Switch on Name → Points<Stat> += 1
   ApplyStats

ApplyStats
   Stats.MaxHealth          = 100 + 15 × PointsHealth      (also add the difference to Health)
   Stats.MaxStamina         = 100 + 10 × PointsStamina
   Stats.StaminaRegenPerSec = 18 + PointsStamina
   Stats.MaxBattery         = 100 + 10 × PointsBattery
   Stats.MoveSpeedMultiplier = 1 + 0.03 × PointsSpeed
   Stats.DamageMultiplier   = 1 + 0.05 × PointsDamage
   Speed: Character Movement Max Walk Speed = BaseWalkSpeed × MoveSpeedMultiplier
          (GASP: multiply its walk/run/sprint speed variables in the sandbox character's
           Movement section instead, or it will overwrite Max Walk Speed every frame)
```

## AC_HM_Stats — stamina & battery upkeep (Component Tick)
```
Sprinting AND moving   → Stamina −= 20 × Delta ; at 0 → force stop sprint
TimeSinceStaminaUse > 1.0 s → Stamina += StaminaRegenPerSec × Delta
Battery += 1.5 × Delta   (slow trickle — the android's core)
Clamp all; broadcast OnStatsChanged at most ~10× per second
```
Functions: `SpendStamina(Amount)` (sets TimeSinceStaminaUse = 0), `Heal(Amount)`, `Die`.

## Level-up screen (WBP_HM_LevelUp)
- Opens on `OnLevelUp` (and from the quest log with a "Upgrade" button whenever `UnspentPoints > 0`).
- Five rows: stat name, current value → next value, a **+** button (`SpendPoint`).
- "Points: 2" at the top, Close button. Pause the game while open (`Set Game Paused`, set the widget to *Tick when paused*).

## Saving
`BP_HM_SaveGame` variables: Level, XP, UnspentPoints, the five Points*, the inventory integers, ActiveQuest, ActiveStep, CompletedQuests (Array of Name), PlayerLocation.
Save on quest complete and at the crafting bench: `Create Save Game Object → set vars → Save Game to Slot ("HM_Slot0", 0)`. Load in the player's BeginPlay if `Does Save Game Exist`.
