# Heavy Mettle

A third-person, blueprint-driven Unreal Engine 5 game prototype.

Overview
- Title: Heavy Mettle
- Genre: Third-person shooter with melee combo system, climbing, crafting, XP/progression
- Setting: Spaghetti western in space — an android child lost on an alien planet, blending dark-age living with cyberpunk tech.
- Player: Android (modeled as human-like kid) w/ pistol on hip and sword on back, long flowing jacket with cloth physics.
- Implementation: Unreal Engine 5 (Blueprints-first, minimal/no C++). Use free assets from Epic/Quixel/Marketplace where possible. Use Git LFS for large binary assets.

Repository: https://github.com/DepressedRedPanda/attempt-two

Getting started
1. Install Unreal Engine 5.3+ (or latest free UE5 version with Marketplace/Quixel access).
2. Clone the repo:
   git clone https://github.com/DepressedRedPanda/attempt-two.git
3. Create a new Unreal Project (Third Person) named HeavyMettle in the repository root, or I can create a Blueprint project skeleton upon request.
4. Enable Git LFS and track large asset folders (Content/, .uproject binaries):
   git lfs install
   git lfs track "*.uasset"
   git lfs track "*.umap"
   git add .gitattributes

Notes
- This repo currently contains design docs and scaffolding only. I cannot upload UE binary assets or full .uproject files due to environment limitations, but I can produce Blueprint graphs, detailed step-by-step instructions, and sample assets to import.
- If you want, I can generate starter Blueprint graphs as text-based step lists, or prepare JSON metadata for tools that convert to assets.

What I added now
- Project design doc, roadmap, and standard Unreal .gitignore

Next suggestions (pick any):
- I can create a blueprint-only project skeleton (text instructions + folder layout) you can run locally.
- I can create detailed Blueprint graphs for: player movement, third-person camera, aiming, lock-on, melee combo system, block/parry window, crafting, XP system.
- I can create issue tasks and a project board in this repo.
- I can prepare an asset sourcing list (free Marketplace + Quixel) and a recommended starting asset pack.

Tell me which piece you'd like me to do next and I’ll add it to the repo and describe how to use it.

## Practical repository limitation

This checkout contains a text-only **HeavyMettle.uproject** shell, not Epic's proprietary binary Third Person Combat template assets. If you double-click the .uproject *before creating/copying the Third Person Combat template Content and game mode*, you will not have a usable combat character. The recommended starting point is to generate the Combat template locally, copy these scripts into that local project, and commit the resulting project files/assets once the Unreal Editor has successfully created and tested them. Local Python scripts only run in the Unreal Editor; they are not scripts that run inside the packaged game. No Unreal Engine installation is available in this chat environment to test PIE or package Windows binaries.
