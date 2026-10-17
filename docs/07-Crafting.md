# 07 — Crafting & inventory

Deliberately simple: **four materials → four items**. No grids, no weight.

| Material | Where from |
|---|---|
| Scrap | Wrecks, broken machines, bandit drops |
| Black Powder | Bought in town, bandit drops |
| Dustbloom (herbs) | Glowing desert flowers |
| Copper Wire | Dead relay towers |

| Recipe (`DT_HM_Recipes`) | Cost | Makes | Bench? |
|---|---|---|---|
| Pistol Rounds | 1 scrap + 2 powder | 12 rounds | No — craft anywhere |
| Poultice Kit | 3 herbs + 1 wire | 1 medkit (heals 40%) | No |
| Can Grenade | 2 scrap + 3 powder + 1 wire | 1 grenade | **Yes** |
| Battery Cell | 1 scrap + 2 wire | restores 50% battery | **Yes** |

## AC_HM_Inventory
One Integer per item: `Scrap, Powder, Herbs, Wire, Ammo, Medkits, Grenades, BatteryCells, Credits`.

```
AddItem (ItemID: Name, Amount: Integer)
   Switch on Name → add to that variable, Clamp to the item's MaxStack (DT_HM_Items)
   OnInventoryChanged.Broadcast()
   HUD → show "+12 Pistol Rounds" toast

GetCount (ItemID) → Integer    (Switch on Name)
RemoveItem (ItemID, Amount) → Boolean   (false if not enough)
```

## AC_HM_Crafting
```
CanCraft (RecipeID) → Boolean
   Get Data Table Row (DT_HM_Recipes, RecipeID) → Row
   if Row.bNeedsBench AND not bNearBench → false
   return Inventory.Scrap  >= Row.ScrapCost  AND Inventory.Powder >= Row.PowderCost
      AND Inventory.Herbs  >= Row.HerbsCost  AND Inventory.Wire   >= Row.WireCost

Craft (RecipeID) → Boolean
   Branch CanCraft → false: play "nope" sound, return false
   RemoveItem each cost → AddItem(RecipeID, Row.ResultAmount)   (Recipe row names match item IDs)
   play crafting sound/sparks → QuestLog.ReportEvent("Crafted:" + RecipeID) → return true
```

## Crafting menu (WBP_HM_Crafting)
- Vertical Box filled on **Event Construct**: `Get Data Table Row Names (DT_HM_Recipes)` → for each → create a small button widget showing DisplayName, cost, and owned counts. Grey it out when `CanCraft` is false.
- Button clicked → `Crafting.Craft(RowName)` → refresh the list.
- Open/close:
```
IA_Crafting Started (player) → Crafting.bMenuOpen = !bMenuOpen
   open : Create Widget → Add to Viewport → Set Input Mode Game and UI → Show Mouse Cursor ✔
          Set Global Time Dilation 0.2   (world slows down, like a quick-draw moment)
   close: Remove from Parent → Set Input Mode Game Only → Show Mouse Cursor ✘ → Time Dilation 1.0
```

## Crafting bench (BP_HM_CraftingBench)
Mesh (an anvil/workbench) + Box collision (300×300×200) + `Interactable` component.
```
Box Begin Overlap (player) → Crafting.bNearBench = true
Box End Overlap  (player) → Crafting.bNearBench = false
Interactable.OnInteract   → open the crafting menu
```

## Using items
```
IA_UseHeal Started → Branch Inventory.Medkits > 0 AND Stats.Health < Stats.MaxHealth
   RemoveItem("Medkit", 1) → play quick "inject" montage (0.8 s, can be interrupted!)
   On montage complete → Stats.Heal(MaxHealth × 0.4)
```
Battery Cells: use from the crafting menu (button "Use") or bind a key later.

## Pickups (BP_HM_Pickup)
Static mesh + Sphere collision (radius 120) + a bobbing/rotating movement + a soft glow.
Variables `ItemID` (Name, *Instance Editable*) and `Amount` (Integer, *Instance Editable*).
```
Sphere Begin Overlap (player) → Inventory.AddItem(ItemID, Amount) → sound → Destroy Actor
```
Enemies drop one on death (see 09). Place pickups by hand around the map for materials.
