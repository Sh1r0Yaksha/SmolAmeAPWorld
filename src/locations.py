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
    for region_name, quantity in data["quantity"].items():
        for i in range(quantity):
            LOCATION_NAME_TO_ID[f"{region_name}_{item_name}_{i}"] = location_id
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
        for region_name, quantity in data["quantity"].items():
            region = world.get_region(region_name)
            for i in range(quantity):
                location_name = f"{region_name}_{item_name}_{i}"
                region_location = get_location_name_with_id(location_name)
                region.add_locations(region_location, SmolAmeLocation)