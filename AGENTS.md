# Notes for coding agents

Read `README.md` first: it has the file map and explains each behavior.

- Target: vanilla Minecraft Java 26.2 (data pack format 107.1, resource pack format 88.0). No mods, no plugins.
- Edit `datapack/`, `resourcepack/`, and `tools/`. Never edit `dist/`; it is build output.
- `datapack/data/clanka_spanka/recipe/clanka_spanka.json` and `datapack/data/clanka_spanka/function/give.mcfunction`
  are generated: change `COMPONENTS` / `RECIPE` in `tools/build.py` instead.
- After any change run `python tools/build.py`, load the datapack on a 26.2 server (or `/reload`), and check the
  server log for errors mentioning `clanka_spanka`. 26.2 rejects unknown JSON fields at load time.
- Clankers are members of the `clankers` team. The team name appears in `enchantment/clanker_spanking.json` and
  `function/whap.mcfunction`; keep them in sync.
- What a spank does lives in `function/spank.mcfunction`; the extra damage number lives in
  `enchantment/clanker_spanking.json`.
