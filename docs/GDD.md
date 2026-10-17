# Heavy Mettle — Game Design Doc

## Pitch
A spaghetti western in space. You play an android who fell from the sky, woke up in a crater with no memory, and now takes odd jobs for the frontier folk of a dusty alien planet. Third-person shooting at range, sword combos up close, climbing everywhere.

**Tone:** Sergio Leone meets dark-age village life. Dusty towns, wind, long shadows, standoffs. Technology instead of magic — but old, patched, hand-me-down technology. Mostly *old world* with flashes of *cyberpunk*: oil lamps next to flickering holo-signs, horses replaced by six-legged pack beasts, blacksmiths who also repair servos.

**How he got there is not important yet.** The game focuses on small jobs for villagers.

## The player — "Mettle"
- Designation stamped on his chest plate: **MTL-07**. The townsfolk can't pronounce it, so they call him **Mettle**.
- Built to look like a real human. Only small tells give him away: seams at the jaw and wrists, eyes that glow faintly in the dark, no breath in the cold.
- Personality: a lost kid. Polite, curious, takes everything literally, too eager to help, and occasionally helps the wrong people.
- Look: long flowing duster coat (cloth physics), sword on his back, revolver-style pistol on his right hip.
- **Battery** is his special resource (the "magic" bar). It powers the charged **Arc Shot** and heavy finishers, and recharges slowly or with Battery Cells.

## The world — the planet Vasq
- Hot, red-ochre desert, mesas, canyons, dead relay towers from some forgotten colony era.
- **The Vasqari** — the people. Human-alien hybrids: human faces and bodies with things like ridged brows, extra-jointed fingers, mottled skin, small horn nubs or ear fins. Most of them have never seen a "pure" human, so Mettle is a curiosity.
- **Dustwell** — the first town. A well-town built around air-condensers that pull water out of the sky. Water is wealth.
- **Factions**
  - **Marrow Extraction Co.** — off-world mining company. Polite, well-armed, owns the rail line, quietly squeezing the towns.
  - **The Rustjaw Gang** — bandits led by *Rustjaw Kade* (a lieutenant; the big boss stays off-screen for now). Stealing condenser cores and company ore.
  - **Townsfolk** — people who just want water and to be left alone.

## Core loop
1. Take a job from a villager or the town board.
2. Travel, climb and explore to the job site; gather crafting materials on the way.
3. Fight: lock on and use sword combos close-in, aim and shoot at range, use cover at different heights.
4. Get paid in Credits and XP → level up → put points into Health, Stamina, Battery, Speed or Damage.
5. Craft ammo, healing kits and grenades → take the next job.

## Starter cast
| Character | Role |
|---|---|
| **Marshal Oyeku** | Tired lawwoman of Dustwell. Gives bounties. |
| **Hollis Varn** | Smith with four arms. Teaches crafting. |
| **Elder Maudra** | Keeper of the condensers. Gives the water-theft job. |
| **Agent Pell** | Marrow Extraction Co. representative. Pays well, asks no questions, answers fewer. |
| **Rustjaw Kade** | Bandit lieutenant with a jaw of rusted plate. First boss. |

## First five jobs (also in `Data/DT_HM_Quests.csv`)
1. **Fallen Star** — tutorial. Climb out of the crater (vault/mantle/climb), follow the smoke to Dustwell, meet the Marshal.
2. **Mettle and Powder** — crafting tutorial with Hollis: gather scrap and powder, craft pistol rounds.
3. **Dry Wells** — bandits are stealing condenser cores. Clear the old pump house (first real fight: melee + shooting).
4. **Company Business** — Marrow Extraction wants a stolen ore cart back. At the canyon camp you learn the "bandits" are miners the company never paid. **Choice:** return the ore (more Credits, company favor) or let them keep it (less Credits, town favor). This is the "little bit of trouble".
5. **Bounty: Rustjaw Kade** — climb to a high mesa camp, clear lookouts on different elevations, fight Kade (heavy hitter, blocks often → parry him).

## Combat summary
- **Close range (inside ~4–5 m):** lock-on available. Light/heavy combo strings, block, parry → riposte.
- **Beyond lock-on range:** aim over the shoulder and shoot. Bullets aren't blockable — use cover.
- **Cover is at two heights:** chest-height (crouch behind, vault over) and head-height (full cover, mantle onto). Platforms above give high ground.
- **Stamina** for sprint, dodge, attacks, blocking. **Battery** for Arc Shot and finishers.

## Enemies (first pass)
| Enemy | Behavior |
|---|---|
| Rustjaw Cutthroat | Melee rusher, light attacks, staggers easily. |
| Rustjaw Gunhand | Keeps distance, shoots from cover and high ground. |
| Rustjaw Kade (boss) | Heavy attacks, blocks often, ground slam. Parry window is the way in. |

## Art direction
- Palette: ochre, rust, bone white, faded teal accents on tech, warm low sun.
- Strong silhouettes: coat tails, wide hats on villagers, ragged banners.
- Placeholder art first (grey boxes and free packs) — gameplay before polish.
