from __future__ import annotations
import json
from pathlib import Path

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import SmolAmeWorld

regions_path = Path(__file__).parent / "regions.json"
with regions_path.open("r", encoding="utf-8") as file:
    regions = json.load(file)


def create_and_connect_regions(world: SmolAmeWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: SmolAmeWorld) -> None:

    multiworld_regions = []
    
    for name, connection in regions.items():
        region = Region(name, world.player, world.multiworld)
        multiworld_regions.append(region)

    world.multiworld.regions += multiworld_regions    


def connect_regions(world: SmolAmeWorld) -> None:
    for region_name, connections in regions.items():
        region = world.get_region(region_name)
        for connected_region in connections:
            connection = world.get_region(connected_region)
            region.connect(connection, f" {region} to {connected_region}")
