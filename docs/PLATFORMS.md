# Platforms: PC, PlayStation 5, Xbox, Switch 2

Goal: ship Heavy Mettle on **every major platform**, with PS5 as a headline target.
Unreal Engine 5 supports all of them, and **Blueprint-only projects can be shipped on consoles** — no C++ required for the game itself.

## The honest part: what it takes
| Platform | What you need | Can you start today? |
|---|---|---|
| **Windows (Steam / Epic Games Store)** | Unreal Engine from the launcher. Steam requires a one-time Steam Direct fee per game. | ✅ Yes — package from the editor |
| **Mac / Linux** | Mac build needs a Mac + Xcode. Linux builds can be made from Windows with Epic's cross-compile toolchain. | ✅ Yes |
| **PlayStation 5** | Become a registered developer through **PlayStation Partners** (Sony approves you — usually you need a company/business entity and a game pitch). After approval: PS5 dev kit (rented/bought from Sony), Sony's SDK, and Epic's PS5 platform code, which Epic only gives to verified console developers. | ⏳ Apply when there's a playable demo |
| **Xbox Series X\|S** | **ID@Xbox** program (free to apply, Microsoft approves). Then the GDK, dev kit (or a retail Xbox in Developer Mode for testing), and Epic's Xbox platform code. | ⏳ Apply with a demo |
| **Nintendo Switch 2** | Apply as a developer on the **Nintendo Developer Portal**. Then dev kit, SDK, Epic's Switch platform code. Needs the heaviest optimization. | ⏳ Later |

Key facts:
- **Console code is under NDA.** Nobody — not Claude, ChatGPT, Gemini or Copilot — can download Sony/Microsoft/Nintendo SDKs or put console build files on GitHub. Never commit console SDK files or console-specific config to this public repo; use a private repo or private branch once approved.
- Console builds use a **source-built engine** (from Epic's GitHub) plus the platform extension Epic grants after approval. The Blueprint content we make now carries straight over.
- Each console has a **certification** checklist (Sony TRC, Xbox XR, Nintendo lotcheck): saves, trophies/achievements, pause on controller disconnect, user switching, text/button naming rules, etc. Design for these from day one so it's not a rewrite later.

## The plan
1. **Now — build it "console-shaped" on PC.** Everything below in "Rules we follow now".
2. **First milestone — Windows demo** (the first 15–20 minute vertical slice). Put it on itch.io or a Steam page / Next Fest demo to show people.
3. **Form a business entity** (e.g. an LLC) — most console programs require it.
4. **Apply to ID@Xbox and PlayStation Partners** with the demo video and build. (Many indie teams also partner with a **porting studio or publisher** who already have dev kits — a realistic option for a solo developer.)
5. Once approved: get the platform code from Epic, build from source, run on a dev kit, then work through certification.

## Rules we follow now (so consoles are easy later)
**Controls**
- Every feature must be fully playable with a **gamepad only**. No mouse-only menus. (Bindings already exist for both.)
- Menus must be navigable with the D-pad/stick: use Unreal's **CommonUI** plugin for widgets (it handles focus, back button, and shows the right button icons per platform — PlayStation shapes, Xbox letters, Switch letters).
- Show button prompts by platform: ✕ ○ □ △ / L1 R1 L2 R2 on PlayStation, A B X Y / LB RB LT RT on Xbox.
- PS5 extras later (not now): DualSense adaptive triggers on the pistol trigger (resistance when aiming, a "snap" on Arc Shot) and haptics for sword clashes/parries. These come from Sony's SDK after approval.

**Performance budget**
| Target | Resolution | FPS | Notes |
|---|---|---|---|
| PS5 / Xbox Series X | 1440p upscaled to 4K (TSR) | 30 quality / **60 performance mode** | Lumen + Nanite OK |
| Xbox Series S | 1080p upscaled | 30–60 | Lower Lumen quality, smaller shadow maps |
| Switch 2 | 720–1080p | 30 | Plan for Lumen off (baked/simple lighting), lower-poly assets |
| PC | Scalable | Unlocked | Settings menu |

- Use **Engine Scalability** levels (Low/Medium/High/Epic) and test the game on *Medium* regularly — that's roughly where consoles land.
- Keep **cloth** to the coat only, with a limited number of cloth meshes on screen (NPC coats = no cloth, or very cheap cloth).
- Limit enemies to ~10 active at once, use **Instanced Static Meshes** for cover/blockout (the arena generator already does), use texture sizes 2K max for most props.
- Turn on **stat unit** / **stat gpu** (console commands) during play-tests and keep frame time under **16.6 ms** on a mid-range PC for 60 fps headroom.

**Saving**
- Save only through **Save Game to Slot** (already the plan) — on consoles Unreal maps this to the platform's save system. Don't write files anywhere else.
- Auto-save at checkpoints; consoles expect a "Saving…" icon and no quitting mid-save.

**Text & UI**
- All on-screen text in **String Tables** / localizable Text (not hard-coded strings), so it can be translated and so platform naming rules ("Wireless Controller" vs "Gamepad") can be swapped.
- Minimum text size ~28 px at 1080p (TV distance). Subtitles option, colorblind-friendly HUD colors.
- Handle **controller disconnected → pause** and **app suspend/resume** (Unreal events: *Application Will Enter Background* / *Has Entered Foreground*).

**Assets & licenses**
- Every Fab / Epic asset must allow **commercial use on all platforms** — Epic content under the Unreal license generally does; check each third-party listing.
- Avoid PC-only middleware.

## Engine version
Stay on one engine version per milestone. Before applying to a console program, check which engine versions Epic's console code supports at that time and upgrade to it if needed.
