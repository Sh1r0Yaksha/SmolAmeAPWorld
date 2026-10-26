from __future__ import annotations
import json
from pathlib import Path

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from .items import SmolAmeItem
from .regions import get_included_regions

area_items_path = Path(__file__).parent / "area_items.json"
with area_items_path.open("r", encoding="utf-8") as file:
    area_items = json.load(file)


if TYPE_CHECKING:
    from .world import SmolAmeWorld


# Built from the full json on purpose, so IDs stay the same whether or not include_ca is on.
LOCATION_NAME_TO_ID = {}

location_id = 1

for region_name, item_data in area_items.items():
    for item_name, location_name in item_data.items():
        LOCATION_NAME_TO_ID[f"{region_name}-{location_name}"] = location_id
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
    for region_name in get_included_regions(world):
        region = world.get_region(region_name)
        for location_name in area_items[region_name].values():
            location_name_id = get_location_name_with_id(f"{region_name}-{location_name}")
            region.add_locations(location_name_id, SmolAmeLocation)   


def create_all_events(world: SmolAmeWorld):
    for region_name in get_included_regions(world):
        if region_name != "Hub":
            region = world.get_region(region_name)

            region.add_event(f"{region_name} MOM Cleared",
                            f"{region_name}-Cleared",
                            location_type=SmolAmeLocation,
                            item_type=SmolAmeItem)