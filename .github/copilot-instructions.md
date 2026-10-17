# Copilot: Heavy Mettle
- Unreal Engine 5.8.3, Blueprint-only runtime project. Avoid introducing C++ modules/build rules.
- Base Epic Third Person **Combat** variant, not Lyra.
- Alien frontier village, ground-level mercenary quests; no magic.
- Melee proximity targeting max 350cm and line-of-sight; beyond that manual TPS aiming only.
- Light/heavy combo chains, block/parry, pistol and sword body sockets, Chaos Cloth jacket after gameplay.
- Built-in engine primitives for graybox; Fab content only with individual compatibility and license verification.
- Use data/balance.json as canonical tuning reference and update it when implementing gameplay.
- Commit generated .uasset/.umap under Git LFS; cannot edit or run them purely from GitHub text.
- State what was actually compiled/tested in Unreal Editor. Favor short testable PRs, not unverified bulk changes.
