from __future__ import annotations
import json
from pathlib import Path

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import SmolAmeWorld

area_items_path = Path(__file__).parent / "area_items.json"
with area_items_path.open("r", encoding="utf-8") as file:
    area_items = json.load(file)


def create_and_connect_regions(world: SmolAmeWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: SmolAmeWorld) -> None:

    multiworld_regions = []

    for region_name in area_items:
        region = Region(region_name, world.player, world.multiworld)
        multiworld_regions.append(region)

    world.multiworld.regions += multiworld_regions    


def connect_regions(world: SmolAmeWorld) -> None:
    hub_region = world.get_region("Hub")
    for region_name in area_items:
        if region_name != "Hub":
            region = world.get_region(region_name)
            region.connect(hub_region, f" {region} to {hub_region}")
            hub_region.connect(region, f" {hub_region} to {region}")
