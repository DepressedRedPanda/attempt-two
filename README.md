# HEAVY METTLE
*A sci-fi spaghetti western built with Unreal Engine 5.8 Blueprints.*

**Status: first playable graybox foundation, not a finished game.** This repository includes design, project settings, and an Unreal Editor Python script for generating a village. GitHub cannot create/compile the actual Unreal .uasset combat Blueprints without a running Unreal Editor. The script must be run on a machine with Unreal 5.8 installed.

## The pitch
An apparently human android falls onto a dusty alien frontier world, loses his memory, and survives by taking odd mercenary jobs. Most locals are human/alien hybrids. Buildings, guilds, and social structures feel medieval, but there are firearms, power cells, scavenged machines, and crude electronics. No magic. The mystery of the crash takes a back seat to the village and its people.

## Fastest playable route (no C++ compiler)
1. Install **Unreal Engine 5.8.3** in Epic Games Launcher.
2. In Unreal's Project Browser select **Games > Third Person > Combat** variant, **Blueprint** (if asked), Desktop, and name the project **HeavyMettle**. This template already has movement, health, melee and targeting. You must use its actual binary Content assets; they are *not* in this GitHub repository.
3. Download this repository using GitHub's **Code > Download ZIP** (or clone it).
4. Copy the repository's **Scripts/** folder into the root of your generated HeavyMettle project. Do NOT overwrite the template project's Content, Config, or .uproject: those contain its prebuilt Combat mode, input mappings, and GameMode.
5. In the UE editor enable **Python Editor Script Plugin** and **Editor Scripting Utilities** if present. Restart the editor.
6. Use **Tools > Execute Python Script** and select **Scripts/build_dustfall.py**. It generates **/Game/HeavyMettle/Maps/L_Dustfall** from built-in engine meshes.
7. Use **File > Open Level**, open **L_Dustfall**, and click **Play**. You can traverse a frontier graybox using the Combat template player. The map contains cover, jumping elevations, rooftops, stair access, and signposted quest locations. Collision and navigation depend on your locally generated template.
8. Optionally run **Scripts/create_blueprint_scaffolds.py** to create future editable Blueprint actor/data *scaffolds*. These do not have behavior graphs or combat logic until those are implemented and tested locally.
9. Once you have played the map, set Project Settings > Maps & Modes > Editor Startup Map / Game Default Map to **L_Dustfall**, save, and commit the generated **Content/HeavyMettle** binary assets (Git LFS recommended).

### What works vs. what still needs construction
- **Available after steps 1-7:** Combat-template movement/targeting/melee and playable authored graybox village (assuming template works). Note: template mechanics are Epic's baseline, not yet customized for Heavy Mettle.
- **Design/scaffolds only:** pistol shooting, ammunition, crafting, quests, XP, battery, shield/parry fine-tuning, short-range-only lock-on, climb/mantle, bandit AI, dialogue, wearable sword/pistol, android visuals, and physical cloth coat. See docs/BLUEPRINT_BUILD.md.
- **Not shipped yet:** a packaged Windows game, custom Unreal binary Blueprint assets, free Fab asset imports, finished art.

## Why the repository itself is not a ready-to-open game
Unreal Blueprint logic, levels and animation assets are compiled binary .uasset files. Writing a .uproject file or Blueprint pseudocode to GitHub doesn't create those binaries. To avoid another 'could not be compiled' failure we use Epic's prebuilt Blueprint Combat template and construct the game in the editor; this repository supplies repeatable construction scripts, specs, and collaboration guidance.

## Suggested first mission
**The Missing Cells:** a merchant's battery freight was taken by raiders outside Cinder's Rest. Track them to a ruin, recover the goods by stealth or fighting, then decide whether to return the shipment, expose the merchant, or sell the cells yourself.

## Collaboration
- **CLAUDE.md**, **GEMINI.md**, and **.github/copilot-instructions.md** contain consistent instructions for other assistants whenever they are connected by you. Writing these files does **not** mean Claude, Gemini or Copilot has already worked on the repo.
- Never migrate C++ source from Hollowreach into this code-free foundation.
- No imported premium/free marketplace assets are redistributed by this repository without checking their individual licenses.
