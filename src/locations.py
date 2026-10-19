from __future__ import annotations
import json
from pathlib import Path

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

items_path = Path(__file__).parent / "items.json"
with items_path.open("r", encoding="utf-8") as file:
    items = json.load(file)

regions_path = Path(__file__).parent / "regions.json"
with regions_path.open("r", encoding="utf-8") as file:
    regions = json.load(file)

if TYPE_CHECKING:
    from .world import SmolAmeWorld

LOCATION_NAME_TO_ID = {}

location_id = 0

for item_name, data in items.items():
    if "Area" in data:
        for region_name, locations in data["Area"].items():
            for location_name in locations:
                LOCATION_NAME_TO_ID[f"{region_name}-{location_name}"] = location_id
                location_id += 1
    else:
        for region_name in regions:
            LOCATION_NAME_TO_ID[f"{region_name}-{item_name}"] = location_id
            location_id += 1

class SmolAmeLocation(Location):
    game = "Smol Ame"


def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

def get_location_name_with_id(location_name: str) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name]}

def create_all_locations(world: SmolAmeWorld) -> None:
    create_regular_locations(world)


def create_regular_locations(world: SmolAmeWorld) -> None:
    for item_name, data in items.items():
        if "Area" in data:
            for region_name, locations in data["Area"].items():
                region = world.get_region(region_name)
                for location_name in locations:
                    location_name_id = get_location_name_with_id(f"{region_name}-{location_name}")
                    region.add_locations(location_name_id, SmolAmeLocation)
        else:
            for region_name in regions:
                location_name_id = get_location_name_with_id(f"{region_name}-{item_name}")
                region = world.get_region(region_name)
                region.add_locations(location_name_id, SmolAmeLocation)
                