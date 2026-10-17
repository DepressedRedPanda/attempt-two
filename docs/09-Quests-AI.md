# 09 — Enemies, villagers & quests

## Bandit AI (BP_HM_Enemy_Bandit + BP_HM_AIController_Bandit)
No behavior trees — a simple "think" timer in Blueprint is enough for now and easy to edit.

**BP_HM_Enemy_Bandit** (child of `BP_HM_CharacterBase`, so it has `Stats` and `Melee`):
- Class Defaults → **AI Controller Class = BP_HM_AIController_Bandit**, Auto Possess AI = *Placed in World or Spawned*.
- Instance-editable vars: `bIsRanged`, `AttackRange (180)`, `ShootRange (2000)`, `XPReward (25)`.
- Mesh: UE mannequin or a Paragon character with a Vasqari tint (see GDD). Collision → Combat channel: Block.

**BP_HM_AIController_Bandit**
```
Event OnPossess → Me = Cast to BP_HM_Enemy_Bandit
                → Set Timer by Event (Think, 0.25 s, Looping)
                → Me.Stats.OnDied → Bind → Clear Timer, Unpossess

Think:
  Player = Get Player Character ; Dist = Distance(Me, Player)
  Dist > 3000 → Stop Movement → return                         (asleep)
  Set Focus (Player)                                            (always faces you)

  MELEE bandit:
    Dist <= AttackRange → Stop Movement
         → if not Me.Melee.bAttacking AND Random Bool with Weight 0.6
              → Me.Melee.TryAttack( Random Bool weighted 0.75 ? "L" : "H" )
    else → AI Move To (Player, Acceptance Radius = AttackRange − 40)

  RANGED bandit:
    Dist < 500 → back off: AI Move To (Me − Normalize(Player − Me) × 400)
    Dist <= ShootRange AND Line Trace (Me eyes → Player) clear AND ShootCooldown done
         → Stop Movement → EnemyShoot
    else → AI Move To (Player, Acceptance Radius = ShootRange × 0.7)

EnemyShoot:
  Hit chance = 0.55 (−0.25 if the player is sprinting/dodging, −0.3 if player is crouched behind chest cover)
  Random Float < chance → Player.Stats.ReceiveHit(Me, 8, false, false, false)
  muzzle flash + tracer toward the player (offset randomly on a miss) ; ShootCooldown 1.2–2 s
```
Give the AI breathing room: only **2 bandits melee at once** — keep a count on the GameMode (`AttackTokens`), take one before attacking, give it back after.

**Death** (bind `Stats.OnDied` in `BP_HM_CharacterBase`):
```
Disable Movement ; Capsule → No Collision
Mesh → Set Collision Profile "Ragdoll" → Set Simulate Physics ✔        (ragdoll)
Killer's Progression.AddXP(XPReward)
Spawn BP_HM_Pickup (ItemID random of Scrap/Powder/Ammo, Amount 1–3)
QuestLog.ReportEvent("Killed:" + Get Display Name of class)   (via Get Player Character)
Set Life Span 15
```

**Rustjaw Kade** (`BP_HM_Enemy_RustjawBoss`, child of Bandit): Health 600, uses "H" 50% of the time, holds block for 1 s every few seconds (so the player must parry or guard-break with **Spur Thrust**), and at 50% health uses **Anvil Drop**.

## Villagers (BP_HM_NPC_Villager)
- Interactable component (`Prompt = "Talk"`), `NPCName`, `QuestToGive` (Name), and **DialogueLines (Array of Text)** — add this array by hand.
- Idle: a looping idle animation; optionally wander with *AI Move To* random points (Get Random Reachable Point in Radius).
```
Interactable.OnInteract (Interactor)
  Show WBP_HM_Dialogue (Name, Lines) — click/press E to advance each line
  On dialogue finished:
     QuestToGive not None AND not completed AND not active → QuestLog.StartQuest(QuestToGive)
     If this NPC is the *turn-in* for the active quest's last step → QuestLog.AdvanceStep
```

## Interaction (player side)
Every 0.1 s (looping timer):
```
Sphere Trace (Visibility, radius 40) Camera → 250 cm forward (or Capsule Overlap 150 cm)
Hit actor has AC_HM_Interactable AND bEnabled → FocusedInteractable = it, HUD shows "[E] " + Prompt
else → clear prompt
IA_Interact Started → FocusedInteractable.OnInteract.Broadcast(Self)
```
`AC_HM_Interactable` only holds `Prompt`, `bEnabled`, and an Event Dispatcher `OnInteract (Interactor: Actor)`.

## Quests
### AC_HM_QuestLog
Vars: `ActiveQuest (Name)`, `ActiveStep (Integer)`, `CompletedQuests (Array of Name)`, `Counter (Integer)`.
Dispatcher: `OnQuestUpdated (QuestID, StepText)`.
```
StartQuest (ID):  ActiveQuest = ID ; ActiveStep = 1 ; Counter = 0 ; Broadcast (HUD shows title + Step1)
AdvanceStep:      ActiveStep += 1
                  Row = Get Data Table Row (DT_HM_Quests, ActiveQuest)
                  StepText = Select (ActiveStep: Step1..Step4)
                  StepText empty OR ActiveStep > 4 → CompleteQuest  else Broadcast
CompleteQuest:    Progression.AddXP(Row.XPReward) ; Inventory.AddItem("Credits", Row.CreditReward)
                  Add ActiveQuest to CompletedQuests ; ActiveQuest = None ; save game ; big HUD banner
ReportEvent (Event: String)    ← kills, pickups, crafting call this
                  Find any BP_HM_QuestTrigger listening for (ActiveQuest, ActiveStep, Event) → let it count
```

### BP_HM_QuestTrigger (placed in levels — this is how you build quests without code)
Instance-editable vars: `QuestID`, `StepIndex`, `bAdvanceOnOverlap`, `bStartsQuest`, `RequiredEvent (String, e.g. "Collected:Scrap")`, `RequiredCount (Integer)`, **`LinkedActors (Array of Actor)`**.
```
Box Begin Overlap (player):
    bStartsQuest → QuestLog.StartQuest(QuestID)
    bAdvanceOnOverlap AND QuestLog.ActiveQuest == QuestID AND ActiveStep == StepIndex → AdvanceStep

BeginPlay: for each LinkedActors → Bind Event to OnDestroyed → RemainingTargets −= 1
           → when 0 AND quest/step match → AdvanceStep        ("defeat these bandits")

OnEvent (from ReportEvent): Event == RequiredEvent AND quest/step match → Counter += 1
           → Counter >= RequiredCount → AdvanceStep            ("collect 4 scrap")
```
Example — **Dry Wells**: trigger box at the pump house (StepIndex 1, advance on overlap) → trigger linked to the 4 bandits inside (StepIndex 2) → a pickup of ItemID "CondenserCore" with a trigger requiring "Collected:CondenserCore" (StepIndex 3) → Elder Maudra is the turn-in (StepIndex 4).

**Company Business choice:** at step 3, the dialogue widget shows two buttons. "Return the ore" → Credits ×1.5, set a `CompanyFavor` bool on the GameInstance. "Let them keep it" → Credits ×0.5, `TownFavor` = true. Later quests can check these.

### Quest log screen (WBP_HM_QuestLog, key J)
Active quest title, description, current step (✔ for done steps), list of completed quests, and the "Upgrade" button if `UnspentPoints > 0`.
