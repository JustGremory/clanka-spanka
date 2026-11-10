"""Writes the recipe and give function from one item definition, then zips both packs.

Run: python tools/build.py
Output: dist/ClankaSpanka-datapack.zip, dist/ClankaSpanka-resourcepack.zip,
and the resource pack SHA-1 (for resource-pack-sha1 in server.properties).
"""
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "datapack" / "data" / "clanka_spanka"

BASE_ITEM = "minecraft:iron_sword"  # supplies damage, attack speed, durability
COMPONENTS = {
    "minecraft:item_name": "Clanka Spanka",
    "minecraft:item_model": "clanka_spanka:clanka_spanka",
    "minecraft:enchantments": {"clanka_spanka:clanker_spanking": 1},
    "minecraft:enchantment_glint_override": False,
    "minecraft:lore": [{"text": "for the clankas", "color": "gray"}],
}

RECIPE = {
    "type": "minecraft:crafting_shapeless",
    "category": "equipment",
    "ingredients": ["minecraft:leather", "minecraft:leather", "minecraft:iron_nugget"],
    "result": {"id": BASE_ITEM, "components": COMPONENTS},
}


def give_command() -> str:
    # JSON values are valid SNBT, so components can be dumped as-is.
    parts = ",".join(f"{key}={json.dumps(value)}" for key, value in COMPONENTS.items())
    return f"give @s {BASE_ITEM}[{parts}]\n"


def write_generated() -> None:
    recipe = DATA / "recipe" / "clanka_spanka.json"
    recipe.parent.mkdir(parents=True, exist_ok=True)
    recipe.write_text(json.dumps(RECIPE, indent=2) + "\n", encoding="utf-8")
    function = DATA / "function" / "give.mcfunction"
    function.parent.mkdir(parents=True, exist_ok=True)
    function.write_text(give_command(), encoding="utf-8")


def zip_dir(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(src.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(src).as_posix())


def main() -> None:
    write_generated()
    datapack = ROOT / "dist" / "ClankaSpanka-datapack.zip"
    resourcepack = ROOT / "dist" / "ClankaSpanka-resourcepack.zip"
    zip_dir(ROOT / "datapack", datapack)
    zip_dir(ROOT / "resourcepack", resourcepack)
    print(f"wrote {datapack}")
    print(f"wrote {resourcepack}")
    print(f"resource pack sha1: {hashlib.sha1(resourcepack.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
