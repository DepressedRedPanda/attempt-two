"""
Heavy Mettle - one-click project setup (runs INSIDE the Unreal Editor).

What it does
------------
Creates the empty-but-correctly-wired starting assets for the game so you
only have to fill in Blueprint graphs (the docs/ folder walks you through each
one, node by node):

  * Folder layout under /Game/HeavyMettle
  * Enhanced Input actions (IA_*) and the mapping context IMC_HM_Default
    with keyboard/mouse AND gamepad bindings
  * Blueprint classes: game mode, controller, player, enemies, villagers,
    weapons, grenade, pickups, crafting bench, arena generator
  * Blueprint Actor Components for every system (stats, melee, lock-on, ...)
  * Widget Blueprints for the HUD and menus
  * Starter variables on each Blueprint (when your engine version allows it)
  * A test level, L_Testbed, with lighting and a seeded random layout of
    chest-height and head-height cover plus raised platforms

How to run
----------
  Tools > Execute Python Script... > pick this file
or in the Output Log, switch the input box from "Cmd" to "Python" and type:
  import heavy_mettle_setup; heavy_mettle_setup.run()

It is safe to run more than once: anything that already exists is skipped,
so it will never overwrite work you've done in a Blueprint.

Optional: run(rebuild_level=True) regenerates the test level, and
run(seed=1234) picks a different random cover layout.
"""

import random
import unreal

ROOT = "/Game/HeavyMettle"
FOLDERS = [
    "Core", "Characters/Player", "Characters/Enemies", "Characters/NPCs",
    "Components", "Weapons", "Items", "Input", "UI", "Data", "Maps",
    "World/Blockout", "Animations/Montages", "Audio", "Materials", "AI",
]

asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
EAL = unreal.EditorAssetLibrary

created, skipped, warnings = [], [], []


def log(msg):
    unreal.log("[HeavyMettle] " + msg)


def warn(msg):
    warnings.append(msg)
    unreal.log_warning("[HeavyMettle] " + msg)


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def full(path, name):
    return "{}/{}/{}".format(ROOT, path, name)


def load_or_none(path, name):
    p = full(path, name)
    if EAL.does_asset_exist(p):
        return EAL.load_asset(p)
    return None


def make_blueprint(name, path, parent_class):
    existing = load_or_none(path, name)
    if existing:
        skipped.append(name)
        return existing
    factory = unreal.BlueprintFactory()
    factory.set_editor_property("parent_class", parent_class)
    bp = asset_tools.create_asset(name, "{}/{}".format(ROOT, path), unreal.Blueprint, factory)
    if bp:
        created.append(name)
    else:
        warn("Could not create Blueprint " + name)
    return bp


def make_widget(name, path="UI"):
    existing = load_or_none(path, name)
    if existing:
        skipped.append(name)
        return existing
    factory = unreal.WidgetBlueprintFactory()
    factory.set_editor_property("parent_class", unreal.UserWidget)
    wbp = asset_tools.create_asset(name, "{}/{}".format(ROOT, path), unreal.WidgetBlueprint, factory)
    if wbp:
        created.append(name)
    return wbp


def generated_class(bp):
    try:
        return bp.generated_class()
    except Exception:
        return unreal.load_object(None, bp.get_path_name() + "_C")


# ----------------------------------------------------------------------------
# Variables (best effort - the Python API for this differs between versions)
# ----------------------------------------------------------------------------
BEL = getattr(unreal, "BlueprintEditorLibrary", None)
_TYPE_CACHE = {}


def pin_type(type_name):
    if type_name in _TYPE_CACHE:
        return _TYPE_CACHE[type_name]
    t = None
    if BEL and hasattr(BEL, "get_basic_type_by_name"):
        candidates = {"float": ["real", "float", "double"]}.get(type_name, [type_name])
        for c in candidates:
            try:
                t = BEL.get_basic_type_by_name(c)
                if t is not None:
                    break
            except Exception:
                t = None
    _TYPE_CACHE[type_name] = t
    return t


_var_api_reported = False


def add_vars(bp, variables):
    """variables: list of (name, type_name) where type is float/int/bool/name/string/vector."""
    global _var_api_reported
    if not bp:
        return
    if not (BEL and hasattr(BEL, "add_member_variable")):
        if not _var_api_reported:
            warn("This engine version can't add Blueprint variables from Python. "
                 "Add them by hand - every variable is listed in docs/.")
            _var_api_reported = True
        return
    for var_name, type_name in variables:
        t = pin_type(type_name)
        if t is None:
            warn("Unknown variable type '{}' for {}.{}".format(type_name, bp.get_name(), var_name))
            continue
        try:
            BEL.add_member_variable(bp, var_name, t)
        except Exception as e:  # already exists, etc.
            pass


# ----------------------------------------------------------------------------
# Components (adds Blueprint/engine components to a Blueprint's component list)
# ----------------------------------------------------------------------------
def add_component(bp, comp_class, comp_name):
    if not bp or not comp_class:
        return
    try:
        sds = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
        handles = sds.k2_gather_subobject_data_for_blueprint(bp)
        lib = unreal.SubobjectDataBlueprintFunctionLibrary
        for h in handles:
            data = lib.get_data(h)
            if str(lib.get_variable_name(data)) == comp_name:
                return  # already there
        params = unreal.AddNewSubobjectParams(
            parent_handle=handles[0], new_class=comp_class, blueprint_context=bp)
        new_handle, fail_reason = sds.add_new_subobject(params)
        if not fail_reason.is_empty():
            warn("Adding {} to {}: {}".format(comp_name, bp.get_name(), fail_reason))
            return
        sds.rename_subobject(new_handle, unreal.Text(comp_name))
    except Exception as e:
        warn("Couldn't add component {} to {} automatically ({}). Add it in the "
             "Components panel by hand.".format(comp_name, bp.get_name(), e))


def compile_bp(bp):
    if bp and BEL and hasattr(BEL, "compile_blueprint"):
        try:
            BEL.compile_blueprint(bp)
        except Exception:
            pass


# ----------------------------------------------------------------------------
# Enhanced Input
# ----------------------------------------------------------------------------
IVT = unreal.InputActionValueType
INPUT_ACTIONS = {
    # name: value type
    "IA_Move": IVT.AXIS2D,
    "IA_Look": IVT.AXIS2D,
    "IA_Jump": IVT.BOOLEAN,          # jump / climb / mantle
    "IA_Sprint": IVT.BOOLEAN,
    "IA_Dodge": IVT.BOOLEAN,
    "IA_LightAttack": IVT.BOOLEAN,
    "IA_HeavyAttack": IVT.BOOLEAN,
    "IA_Block": IVT.BOOLEAN,         # hold = block, tap at the right moment = parry
    "IA_LockOn": IVT.BOOLEAN,
    "IA_SwitchTarget": IVT.AXIS1D,
    "IA_Aim": IVT.BOOLEAN,
    "IA_Fire": IVT.BOOLEAN,          # hold while aiming = charged Arc Shot (uses battery)
    "IA_Reload": IVT.BOOLEAN,
    "IA_Interact": IVT.BOOLEAN,
    "IA_ThrowGrenade": IVT.BOOLEAN,
    "IA_UseHeal": IVT.BOOLEAN,
    "IA_Crafting": IVT.BOOLEAN,
    "IA_QuestLog": IVT.BOOLEAN,
}

# (action, key, modifiers) - modifiers: "neg", "swz" (swizzle YXZ)
BINDINGS = [
    ("IA_Move", "W", ["swz"]), ("IA_Move", "S", ["swz", "neg"]),
    ("IA_Move", "D", []), ("IA_Move", "A", ["neg"]),
    ("IA_Move", "Gamepad_Left2D", []),
    ("IA_Look", "Mouse2D", ["negY"]), ("IA_Look", "Gamepad_Right2D", ["negY"]),
    ("IA_Jump", "SpaceBar", []), ("IA_Jump", "Gamepad_FaceButton_Bottom", []),
    ("IA_Sprint", "LeftShift", []), ("IA_Sprint", "Gamepad_LeftThumbstick", []),
    ("IA_Dodge", "LeftAlt", []), ("IA_Dodge", "Gamepad_FaceButton_Right", []),
    ("IA_LightAttack", "LeftMouseButton", []), ("IA_LightAttack", "Gamepad_RightShoulder", []),
    ("IA_HeavyAttack", "Q", []), ("IA_HeavyAttack", "Gamepad_RightTrigger", []),
    ("IA_Block", "F", []), ("IA_Block", "Gamepad_LeftShoulder", []),
    ("IA_LockOn", "MiddleMouseButton", []), ("IA_LockOn", "Tab", []),
    ("IA_LockOn", "Gamepad_RightThumbstick", []),
    ("IA_SwitchTarget", "MouseWheelAxis", []),
    ("IA_SwitchTarget", "Gamepad_DPad_Right", []), ("IA_SwitchTarget", "Gamepad_DPad_Left", ["neg"]),
    ("IA_Aim", "RightMouseButton", []), ("IA_Aim", "Gamepad_LeftTrigger", []),
    ("IA_Fire", "LeftMouseButton", []), ("IA_Fire", "Gamepad_RightTrigger", []),
    ("IA_Reload", "R", []), ("IA_Reload", "Gamepad_FaceButton_Top", []),
    ("IA_Interact", "E", []), ("IA_Interact", "Gamepad_FaceButton_Left", []),
    ("IA_ThrowGrenade", "G", []), ("IA_ThrowGrenade", "Gamepad_DPad_Down", []),
    ("IA_UseHeal", "H", []), ("IA_UseHeal", "Gamepad_DPad_Up", []),
    ("IA_Crafting", "C", []), ("IA_Crafting", "Gamepad_Special_Left", []),
    ("IA_QuestLog", "J", []), ("IA_QuestLog", "Gamepad_Special_Right", []),
]


def _factory(*names):
    for n in names:
        cls = getattr(unreal, n, None)
        if cls:
            return cls()
    return None


def make_input_actions():
    actions = {}
    for name, vtype in INPUT_ACTIONS.items():
        ia = load_or_none("Input", name)
        if ia:
            skipped.append(name)
        else:
            ia = asset_tools.create_asset(name, ROOT + "/Input", unreal.InputAction,
                                          _factory("InputAction_Factory", "InputActionFactory"))
            if not ia:
                warn("Could not create " + name)
                continue
            ia.set_editor_property("value_type", vtype)
            created.append(name)
        actions[name] = ia
    return actions


def _make_key(key_name):
    k = unreal.Key()
    k.set_editor_property("key_name", key_name)
    return k


def _modifier_objects(imc, mods):
    objs = []
    for m in mods:
        if m == "neg":
            objs.append(unreal.new_object(unreal.InputModifierNegate, outer=imc))
        elif m == "negY":
            n = unreal.new_object(unreal.InputModifierNegate, outer=imc)
            n.set_editor_property("x", False)
            n.set_editor_property("z", False)
            objs.append(n)
        elif m == "swz":
            s = unreal.new_object(unreal.InputModifierSwizzleAxis, outer=imc)
            s.set_editor_property("order", unreal.InputAxisSwizzle.YXZ)
            objs.append(s)
    return objs


def make_mapping_context(actions):
    name = "IMC_HM_Default"
    imc = load_or_none("Input", name)
    if imc:
        skipped.append(name)
        return imc
    imc = asset_tools.create_asset(name, ROOT + "/Input", unreal.InputMappingContext,
                                   _factory("InputMappingContext_Factory", "InputMappingContextFactory"))
    if not imc:
        warn("Could not create " + name)
        return None
    created.append(name)

    needs_manual_modifiers = []
    for action_name, key_name, mods in BINDINGS:
        ia = actions.get(action_name)
        if not ia:
            continue
        imc.map_key(ia, _make_key(key_name))
        if mods:
            needs_manual_modifiers.append((action_name, key_name, mods))

    # Modifiers have to be written back onto the stored mappings array.
    if needs_manual_modifiers:
        ok = False
        for prop in ("mappings", "default_key_mappings"):
            try:
                holder = imc.get_editor_property(prop)
                mappings = holder if isinstance(holder, unreal.Array) else holder.get_editor_property("mappings")
                for i in range(len(mappings)):
                    m = mappings[i]
                    a = m.get_editor_property("action").get_name()
                    k = str(m.get_editor_property("key").get_editor_property("key_name"))
                    for action_name, key_name, mods in needs_manual_modifiers:
                        if a == action_name and k == key_name:
                            m.set_editor_property("modifiers", _modifier_objects(imc, mods))
                            mappings[i] = m
                if isinstance(holder, unreal.Array):
                    imc.set_editor_property(prop, mappings)
                else:
                    holder.set_editor_property("mappings", mappings)
                    imc.set_editor_property(prop, holder)
                ok = True
                break
            except Exception:
                continue
        if not ok:
            warn("Mapped all keys, but couldn't add the Negate/Swizzle modifiers automatically. "
                 "Open IMC_HM_Default and add them as listed in docs/01-Setup.md (step 6).")
    EAL.save_loaded_asset(imc)
    return imc


# ----------------------------------------------------------------------------
# Blueprints
# ----------------------------------------------------------------------------
COMPONENT_VARS = {
    "AC_HM_Stats": [
        ("MaxHealth", "float"), ("Health", "float"),
        ("MaxStamina", "float"), ("Stamina", "float"), ("StaminaRegenPerSec", "float"),
        ("MaxBattery", "float"), ("Battery", "float"),
        ("MoveSpeedMultiplier", "float"), ("DamageMultiplier", "float"),
        ("bIsDead", "bool"), ("bIsBlocking", "bool"), ("bInParryWindow", "bool"),
    ],
    "AC_HM_Progression": [
        ("Level", "int"), ("XP", "int"), ("XPToNextLevel", "int"), ("UnspentPoints", "int"),
        ("PointsHealth", "int"), ("PointsStamina", "int"), ("PointsBattery", "int"),
        ("PointsSpeed", "int"), ("PointsDamage", "int"),
    ],
    "AC_HM_Melee": [
        ("CurrentComboString", "string"), ("bAttacking", "bool"), ("bComboWindowOpen", "bool"),
        ("bInputBuffered", "bool"), ("BufferedInput", "string"),
        ("ComboResetTime", "float"), ("ParryWindowSeconds", "float"),
        ("LightStaminaCost", "float"), ("HeavyStaminaCost", "float"),
        ("bHitWindowOpen", "bool"), ("bRiposteReady", "bool"), ("SwordBaseDamage", "float"),
    ],
    "AC_HM_LockOn": [
        ("LockOnRange", "float"), ("BreakLockRange", "float"), ("bLockedOn", "bool"),
    ],
    "AC_HM_Shooter": [
        ("bAiming", "bool"), ("AmmoInClip", "int"), ("ClipSize", "int"),
        ("FireRange", "float"), ("BaseDamage", "float"), ("FireCooldown", "float"),
        ("bCanFire", "bool"), ("ArcShotChargeTime", "float"), ("ArcShotBatteryCost", "float"),
        ("HeldTime", "float"), ("bReloading", "bool"),
    ],
    "AC_HM_Inventory": [("Scrap", "int"), ("Powder", "int"), ("Herbs", "int"),
                        ("Wire", "int"), ("Ammo", "int"), ("Medkits", "int"),
                        ("Grenades", "int"), ("BatteryCells", "int"), ("Credits", "int")],
    "AC_HM_Crafting": [("bMenuOpen", "bool"), ("bNearBench", "bool")],
    "AC_HM_QuestLog": [("ActiveQuest", "name"), ("ActiveStep", "int"), ("Counter", "int")],
    "AC_HM_Interactable": [("Prompt", "string"), ("bEnabled", "bool")],
}


def make_components():
    out = {}
    for name, variables in COMPONENT_VARS.items():
        bp = make_blueprint(name, "Components", unreal.ActorComponent)
        add_vars(bp, variables)
        compile_bp(bp)
        out[name] = bp
    return out


def find_asset_by_name(asset_name):
    """Find an asset anywhere in /Game (used to detect GASP's sandbox character)."""
    try:
        for p in EAL.list_assets("/Game", recursive=True, include_folder=False):
            if p.split("/")[-1].split(".")[0] == asset_name:
                return EAL.load_asset(p)
    except Exception:
        pass
    return None


def make_classes(comps):
    core = {
        "BP_HM_GameMode": unreal.GameModeBase,
        "BP_HM_PlayerController": unreal.PlayerController,
        "BP_HM_GameInstance": unreal.GameInstance,
        "BP_HM_SaveGame": unreal.SaveGame,
    }
    bps = {n: make_blueprint(n, "Core", c) for n, c in core.items()}

    # If the Game Animation Sample Project is already in the project, build the
    # player on top of its sandbox character so traversal (vault/mantle/climb)
    # and motion-matching locomotion come for free.
    gasp_bp = find_asset_by_name("CBP_SandboxCharacter")
    player_parent = generated_class(gasp_bp) if gasp_bp else unreal.Character
    if gasp_bp:
        log("Found GASP CBP_SandboxCharacter - BP_HM_Player will inherit from it.")
    else:
        log("GASP not found - BP_HM_Player uses Character. Reparent it later (docs/02-Character.md).")

    base = make_blueprint("BP_HM_CharacterBase", "Characters", unreal.Character)
    for c in ("AC_HM_Stats", "AC_HM_Melee"):
        add_component(base, generated_class(comps[c]), c.replace("AC_HM_", ""))
    compile_bp(base)

    player = make_blueprint("BP_HM_Player", "Characters/Player", player_parent)
    add_vars(player, [("bIsClimbing", "bool"), ("bIsDodging", "bool"),
                      ("ClimbTraceDistance", "float"), ("DodgeStaminaCost", "float")])
    for c in ("AC_HM_Stats", "AC_HM_Progression", "AC_HM_Melee", "AC_HM_LockOn",
              "AC_HM_Shooter", "AC_HM_Inventory", "AC_HM_Crafting", "AC_HM_QuestLog"):
        add_component(player, generated_class(comps[c]), c.replace("AC_HM_", ""))
    add_component(player, unreal.StaticMeshComponent, "SwordMesh")
    add_component(player, unreal.StaticMeshComponent, "PistolMesh")
    compile_bp(player)

    bandit = make_blueprint("BP_HM_Enemy_Bandit", "Characters/Enemies", generated_class(base) or unreal.Character)
    add_vars(bandit, [("XPReward", "int"), ("AttackRange", "float"), ("ShootRange", "float"),
                      ("bIsRanged", "bool"), ("bStaggered", "bool")])
    compile_bp(bandit)
    make_blueprint("BP_HM_Enemy_RustjawBoss", "Characters/Enemies", generated_class(bandit) or unreal.Character)
    make_blueprint("BP_HM_AIController_Bandit", "AI", unreal.AIController)

    villager = make_blueprint("BP_HM_NPC_Villager", "Characters/NPCs", unreal.Character)
    add_vars(villager, [("NPCName", "string"), ("QuestToGive", "name")])
    add_component(villager, generated_class(comps["AC_HM_Interactable"]), "Interactable")
    compile_bp(villager)

    sword = make_blueprint("BP_HM_Weapon_Sword", "Weapons", unreal.Actor)
    add_vars(sword, [("LightDamage", "float"), ("HeavyDamage", "float")])
    pistol = make_blueprint("BP_HM_Weapon_Pistol", "Weapons", unreal.Actor)
    grenade = make_blueprint("BP_HM_Grenade", "Weapons", unreal.Actor)
    add_vars(grenade, [("FuseTime", "float"), ("BlastRadius", "float"), ("BlastDamage", "float")])
    for b in (sword, pistol, grenade):
        compile_bp(b)

    pickup = make_blueprint("BP_HM_Pickup", "Items", unreal.Actor)
    add_vars(pickup, [("ItemID", "name"), ("Amount", "int")])
    bench = make_blueprint("BP_HM_CraftingBench", "Items", unreal.Actor)
    add_component(bench, generated_class(comps["AC_HM_Interactable"]), "Interactable")
    arena = make_blueprint("BP_HM_ArenaGenerator", "World", unreal.Actor)
    add_vars(arena, [("Seed", "int"), ("AreaSize", "float"), ("CoverCount", "int"),
                     ("PlatformCount", "int"), ("ChestHeight", "float"), ("HeadHeight", "float"),
                       ("HeadCount", "int"), ("LedgeHeight", "float"), ("SpawnClearRadius", "float"),
                       ("bRandomizeOnPlay", "bool")])
    qt = make_blueprint("BP_HM_QuestTrigger", "World", unreal.Actor)
    add_vars(qt, [("QuestID", "name"), ("StepIndex", "int"), ("bAdvanceOnOverlap", "bool"),
                  ("RemainingTargets", "int"), ("bStartsQuest", "bool"),
                  ("RequiredEvent", "string"), ("RequiredCount", "int")])
    for b in (pickup, bench, arena, qt):
        compile_bp(b)
    return bps


def make_widgets():
    for w in ("WBP_HM_HUD", "WBP_HM_LockOnMarker", "WBP_HM_InteractPrompt",
              "WBP_HM_Crafting", "WBP_HM_LevelUp", "WBP_HM_QuestLog", "WBP_HM_Dialogue",
              "WBP_HM_DamageNumber"):
        make_widget(w)


# ----------------------------------------------------------------------------
# Test level with random multi-height cover
# ----------------------------------------------------------------------------
CHEST = 110.0   # cm - vault over / take cover behind
HEAD = 190.0    # cm - full cover, mantle up onto it
LEDGE = 300.0   # cm - platforms you climb up to


def spawn_mesh(actors, mesh, loc, scale, label):
    a = actors.spawn_actor_from_object(mesh, loc)
    if a:
        a.set_actor_scale3d(scale)
        a.set_actor_label(label)
        a.set_editor_property("tags", [unreal.Name("Climbable")])
        try:
            a.set_folder_path("Blockout")
        except Exception:
            pass
    return a


def build_level(seed=7, rebuild=False):
    level_path = ROOT + "/Maps/L_Testbed"
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    if EAL.does_asset_exist(level_path) and not rebuild:
        skipped.append("L_Testbed")
        return
    if EAL.does_asset_exist(level_path):
        EAL.delete_asset(level_path)
    les.new_level(level_path)
    actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    V = unreal.Vector

    # Lighting
    sun = actors.spawn_actor_from_class(unreal.DirectionalLight, V(0, 0, 1000), unreal.Rotator(0, -40, -30))
    try:
        sun.light_component.set_editor_property("atmosphere_sun_light", True)
        sun.light_component.set_intensity(8.0)
        sun.light_component.set_light_color(unreal.LinearColor(1.0, 0.82, 0.6, 1.0))  # dusty western sun
    except Exception:
        pass
    actors.spawn_actor_from_class(unreal.SkyAtmosphere, V(0, 0, 0))
    actors.spawn_actor_from_class(unreal.SkyLight, V(0, 0, 500))
    actors.spawn_actor_from_class(unreal.ExponentialHeightFog, V(0, 0, 0))
    actors.spawn_actor_from_class(unreal.PlayerStart, V(0, 0, 120))
    nav = actors.spawn_actor_from_class(unreal.NavMeshBoundsVolume, V(0, 0, 200))
    if nav:
        nav.set_actor_scale3d(V(32, 32, 6))  # brush is 200cm, so this covers the 60m test area

    cube = EAL.load_asset("/Engine/BasicShapes/Cube")  # 100 x 100 x 100 cm
    rng = random.Random(seed)
    size = 6000.0

    spawn_mesh(actors, cube, V(0, 0, -50), V(size / 100.0, size / 100.0, 1), "Ground")

    def free_spot(radius=250):
        while True:
            x = rng.uniform(-size / 2 + 400, size / 2 - 400)
            y = rng.uniform(-size / 2 + 400, size / 2 - 400)
            if abs(x) > radius or abs(y) > radius:  # keep the spawn clear
                return x, y

    # chest-height cover (vault / crouch-cover)
    for i in range(28):
        x, y = free_spot()
        length = rng.choice([2, 3, 4])
        a = spawn_mesh(actors, cube, V(x, y, CHEST / 2), V(length, 0.6, CHEST / 100), "Cover_Chest_%02d" % i)
        if a:
            a.set_actor_rotation(unreal.Rotator(0, 0, rng.choice([0, 45, 90, 135])), False)
    # head-height walls (mantle)
    for i in range(16):
        x, y = free_spot()
        a = spawn_mesh(actors, cube, V(x, y, HEAD / 2), V(rng.choice([2, 3]), 1.0, HEAD / 100), "Cover_Head_%02d" % i)
        if a:
            a.set_actor_rotation(unreal.Rotator(0, 0, rng.choice([0, 90])), False)
    # raised platforms reached by stacking chest -> head -> ledge
    for i in range(6):
        x, y = free_spot(900)
        top = rng.choice([LEDGE, LEDGE + HEAD - CHEST])
        spawn_mesh(actors, cube, V(x, y, top / 2), V(6, 6, top / 100), "Platform_%02d" % i)
        # step-up blocks so every platform is reachable
        spawn_mesh(actors, cube, V(x + 400, y, HEAD / 2), V(2, 2, HEAD / 100), "Platform_%02d_StepHead" % i)
        spawn_mesh(actors, cube, V(x + 600, y, CHEST / 2), V(2, 2, CHEST / 100), "Platform_%02d_StepChest" % i)

    les.save_current_level()
    created.append("L_Testbed (seed %d)" % seed)


# ----------------------------------------------------------------------------
def run(seed=7, rebuild_level=False):
    with unreal.ScopedSlowTask(6, "Setting up Heavy Mettle...") as task:
        task.make_dialog(True)
        task.enter_progress_frame(1, "Folders")
        for f in FOLDERS:
            EAL.make_directory("{}/{}".format(ROOT, f))
        task.enter_progress_frame(1, "Input")
        actions = make_input_actions()
        make_mapping_context(actions)
        task.enter_progress_frame(1, "Components")
        comps = make_components()
        task.enter_progress_frame(1, "Blueprints")
        make_classes(comps)
        make_widgets()
        task.enter_progress_frame(1, "Saving")
        EAL.save_directory(ROOT, only_if_is_dirty=True, recursive=True)
        task.enter_progress_frame(1, "Test level")
        build_level(seed, rebuild_level)

    log("Created {}: {}".format(len(created), ", ".join(created)))
    log("Already existed (left untouched): {}".format(len(skipped)))
    for w in warnings:
        unreal.log_warning("[HeavyMettle] TODO: " + w)
    log("Done. Next: docs/01-Setup.md step 7.")


if __name__ == "__main__":
    run()
