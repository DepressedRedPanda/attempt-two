# Step 1 — Walk around Dustfall in Unreal Engine 5.5.4

**Goal of this step:** you press Play and walk your character around the Heavy Mettle village graybox ("Dustfall"). Nothing else. No guns, enemies or quests yet. Each later feature gets its own small step like this one.

**Why 5.5.4?** It's the version you already have installed. The older guide (`START_HERE_WINDOWS_58.md`) needs 5.8 and its "Combat" template, which doesn't exist in 5.5. See `docs/DECISIONS.md`.

**Time:** about 30–45 minutes, most of it waiting for Unreal to compile shaders the first time.

**Words you'll see:**
- *Project*: the folder Unreal makes for your game. It holds everything.
- *Template*: a starter project from Epic with a working character already in it.
- *Blueprint*: Unreal's visual scripting (boxes connected by wires). No C++ needed.
- *Level / Map*: one playable place. Ours is called `L_Dustfall`.
- *PIE (Play In Editor)*: pressing the green Play button to test inside the editor.
- *Output Log*: Unreal's message window. Errors show up there in red.

---

## Part A — Make a fresh project from Epic's template

1. Open the **Epic Games Launcher** → **Unreal Engine** (left side) → **Library** tab.
2. Under *Engine Versions*, click **Launch** on **5.5.4**.
3. In the window that opens (the *Project Browser*), click **Games** on the left, then click **Third Person**.
4. On the right side set:
   - **Blueprint** (not C++). *This means no Visual Studio, ever, for now.*
   - Target Platform: **Desktop**
   - Starter Content: **unchecked** (keeps the project small)
5. At the bottom, set **Project Name** to `HeavyMettle` (no spaces). Leave the location as `Documents\Unreal Projects` unless you have a reason to change it.
6. Click **Create**. Wait. The first open can take 10+ minutes while "Compiling Shaders" counts down in the bottom-right corner. That's normal.
7. When the editor is open, click the green **Play ▶** button at the top.
   - ✅ **You should see:** a grey mannequin you can move with **W A S D**, look with the **mouse**, jump with **Space**.
   - Press **Esc** to stop playing.
8. **File → Save All.**

> 🛑 If step 7 doesn't work, stop here and tell me what you see. Everything after depends on it.

**Do NOT** open the `HeavyMettle.uproject` file from GitHub. It's a text placeholder, not a real project, and it asks for engine 5.8.

---

## Part B — Turn on Python (used only by the editor, not by the game)

1. Menu **Edit → Plugins**.
2. In the search box type `Python`. Tick **Python Editor Script Plugin**.
3. Search `Editor Scripting Utilities`. If it appears, tick it. (If it doesn't appear in 5.5, that's fine.)
4. Click **Restart Now** at the bottom. The editor closes and reopens.

*Why:* our level is built by a script so it's exactly the same on every computer and can be rebuilt anytime. The finished game doesn't use Python at all.

---

## Part C — Copy our scripts into your project

1. On GitHub, open https://github.com/DepressedRedPanda/attempt-two → green **Code** button → **Download ZIP**.
2. In File Explorer go to **Downloads**, right-click the ZIP → **Extract All** → **Extract**.
3. Open the extracted folder. Find the folder named **Scripts**.
4. Open a second File Explorer window and go to `Documents\Unreal Projects\HeavyMettle`. You should see **Content**, **Config** and **HeavyMettle.uproject**.
5. Copy **only the `Scripts` folder** into that HeavyMettle folder. You should now have `...\HeavyMettle\Scripts\build_dustfall.py`.

---

## Part D — Build the Dustfall level

1. Open the Output Log so you can see messages: menu **Window → Output Log**.
2. Menu **Tools → Execute Python Script…**
3. Browse to `HeavyMettle\Scripts\build_dustfall.py` and click **Open**.
4. Wait about a minute. Watch the Output Log.
   - ✅ **You should see** a line like `HEAVY METTLE: created/updated /Game/HeavyMettle/Maps/L_Dustfall with 238 actors`.
   - Some yellow `WARN` lines are OK. A red error or a "Traceback" is not. Copy the red lines and send them to me.
5. **File → Save All.**

---

## Part E — Make Dustfall the map that loads

1. Menu **Edit → Project Settings…**
2. On the left, click **Maps & Modes**.
3. Under **Default Maps**, set both **Editor Startup Map** and **Game Default Map** to `L_Dustfall`.
4. Under **Default Modes**, check **Default GameMode** says `BP_ThirdPersonGameMode`. (It should already. Don't change it.)
5. Close the settings window. **File → Save All.**

---

## Part F — Play and check

1. Open the level: **Content Drawer** (bottom-left) → **Content → HeavyMettle → Maps** → double-click **L_Dustfall**.
2. Press the green **Play ▶** button.
3. Test this list and note what happens:
   - [ ] You start at one end of a long dark road, near a wooden board labelled **MERCENARY JOBS**.
   - [ ] W A S D moves, mouse looks, Space jumps.
   - [ ] You can walk into at least one building through its doorway.
   - [ ] You can jump up the stone steps onto a raised wooden platform.
   - [ ] You can follow the road all the way through town and out to the red barricades and tall antenna at the **Old Relay**.
   - [ ] You never fall through the ground or get stuck.
4. Press **Esc** to stop.
5. Optional double-check: **Tools → Execute Python Script…** → `Scripts\verify_project.py`. The Output Log should end with `HEAVY METTLE: prerequisites present`. This only checks files exist; your own play test above is the real check.

---

## Part G — Tell me the results

Send me:
- Which checklist boxes worked, and which didn't.
- Any red text from the Output Log (copy/paste, or a phone photo is fine).
- A screenshot from inside the game, if you can.

I'll record the result in the README's **Works in PIE** checklist and then we pick the next small step. **Don't upload the project's Content folder to GitHub yet**; we'll set up Git LFS properly as its own step.

## Known small issues
- Two random cover blocks slightly overlap other props (one touches a leg of the East Patrol Post). Harmless for walking; if one traps you, tell me where.
