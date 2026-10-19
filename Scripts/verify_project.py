"""Inspect a local Unreal Editor session for first-playable Heavy Mettle assets.

Works with the provisional UE 5.5.4 baseline (plain Third Person Blueprint template)
and with the older 5.6+ Combat-variant plan. Read the UE Output Log after running.
This reports the local machine's real state; it does not certify gameplay, and it is
NOT a substitute for pressing Play yourself.
"""
import unreal

ASSETS = unreal.EditorAssetLibrary
LEVEL = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
ACTORS = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
MAP = "/Game/HeavyMettle/Maps/L_Dustfall"
ROOT = "/Game/HeavyMettle/Blueprints"
# Any one of these is a playable third-person character for the first walkaround.
PLAYER_BLUEPRINTS = ("BP_HM_Android", "BP_ThirdPersonCharacter", "BP_CombatCharacter")
critical = []
warnings = []

try:
    unreal.log("Heavy Mettle verify: engine " + unreal.SystemLibrary.get_engine_version())
except Exception:
    pass

if ASSETS.does_asset_exist(MAP):
    unreal.log("[PASS] Heavy Mettle Dustfall level asset exists")
    if not LEVEL.load_level(MAP):
        critical.append("Level exists but could not be opened")
    else:
        labels = [a.get_actor_label() for a in ACTORS.get_all_level_actors()]
        if any(lab == "HM_PlayerStart" for lab in labels):
            unreal.log("[PASS] PlayerStart is in the Dustfall level")
        else:
            critical.append("No Heavy Mettle PlayerStart")
        if any(lab.startswith("HM_BountyBoard_") for lab in labels):
            unreal.log("[PASS] Bounty board graybox found")
        else:
            warnings.append("Quest board proxy absent")
        bandits = sum(1 for lab in labels if lab.startswith("HM_RelayBandit_"))
        if bandits:
            unreal.log("[INFO] Enemy actors placed at the Old Relay: " + str(bandits))
        else:
            unreal.log("[INFO] No enemies placed yet (expected on UE 5.5; enemies are a later step)")
else:
    critical.append("Missing L_Dustfall. Run Scripts/build_dustfall.py.")

asset_names = {
    str(p).rsplit("/", 1)[-1].split(".")[0]
    for p in ASSETS.list_assets("/Game", recursive=True, include_folder=False)
}
players = [name for name in PLAYER_BLUEPRINTS if name in asset_names]
if players:
    unreal.log("[PASS] Playable character Blueprint found: " + ", ".join(players))
else:
    critical.append("No third-person character Blueprint found. Create the project from "
                    "Games > Third Person > Blueprint (see docs/START_HERE_UE55.md).")

if "BP_CombatEnemy" in asset_names:
    unreal.log("[INFO] Epic Combat-variant enemy available (UE 5.6+ template)")

for bp_name in ("BP_HM_Stats", "BP_HM_Inventory", "BP_HM_Combat",
                "BP_HM_QuestTracker", "BP_HM_QuestGiver", "BP_HM_CraftingBench",
                "BP_HM_LootPickup", "BP_HM_Bandit"):
    if ASSETS.does_asset_exist(ROOT + "/" + bp_name):
        unreal.log("[INFO] Editable Blueprint scaffold present: " + bp_name)

for value in warnings:
    unreal.log_warning("[WARNING] " + value)
if critical:
    for value in critical:
        unreal.log_error("[FAILED] " + value)
    raise RuntimeError("Heavy Mettle first-playable prerequisites missing")
unreal.log("HEAVY METTLE: prerequisites present. Now press Play and walk around - "
           "that manual test is the real check.")
