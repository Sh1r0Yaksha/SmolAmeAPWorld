from __future__ import annotations
import json
from pathlib import Path

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import SmolAmeWorld

ids_path = Path(__file__).parent / "IDs.json"
with ids_path.open("r", encoding="utf-8") as file:
    ids = json.load(file)


def get_included_regions(world: SmolAmeWorld) -> list[str]:
    """
    Regions that take part in generation (Hub included).
    Everything listed after "NOTHING" in area_items.json is Continued Adventures
    content, and is left out unless include_ca is enabled.
    """
    region_names = list(ids)

    if not world.options.include_ca.value:
        last_base_game_index = region_names.index("NOTHING")
        region_names = region_names[: last_base_game_index + 1]

    return region_names


def create_and_connect_regions(world: SmolAmeWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: SmolAmeWorld) -> None:

    multiworld_regions = []

    for region_name in get_included_regions(world):
        region = Region(region_name, world.player, world.multiworld)
        multiworld_regions.append(region)

    world.multiworld.regions += multiworld_regions    


def connect_regions(world: SmolAmeWorld) -> None:
    hub_region = world.get_region("Hub")
    region_names = get_included_regions(world)

    for region_name in region_names:
        if region_name != "Hub":
            region = world.get_region(region_name)
            region.connect(hub_region, f"{region_name} to Hub")
            hub_region.connect(region, f"Hub to {region_name}")