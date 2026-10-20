from __future__ import annotations
import json
from pathlib import Path

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from . import options as smolame_options  # rename due to a name conflict with World.options

if TYPE_CHECKING:
    from .world import SmolAmeWorld

area_items_path = Path(__file__).parent / "area_items.json"
with area_items_path.open("r", encoding="utf-8") as file:
    items = json.load(file)

ITEM_NAME_TO_ID = {}
item_id = 0
for region_name, item_data in items.items():
    for item_name, item_location in item_data.items():
        ITEM_NAME_TO_ID[f"{region_name}-{item_name}"] = item_id
        item_id += 1

class SmolAmeItem(Item):
    game = "Smol Ame"

def create_item_with_correct_classification(world: SmolAmeWorld, name: str) -> SmolAmeItem:
    classification_type = ItemClassification.filler

    if "entry button" in name.lower():
        classification_type = ItemClassification.progression

    if "bubba coin" in name.lower() and (
        world.options.game_mode in (
            smolame_options.GameMode.option_bubba,
            smolame_options.GameMode.option_cc,
        )
    ):
        classification_type = ItemClassification.progression

    if (
        "stache quota" in name.lower()
        and world.options.game_mode == smolame_options.GameMode.option_cc
    ):
        classification_type = ItemClassification.progression

    return SmolAmeItem(name, classification_type, ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: SmolAmeWorld) -> None:
    itempool: list[Item] = []

    for name, id in ITEM_NAME_TO_ID.items():
        itempool.append(world.create_item(name))
    
    number_of_items = len(itempool)

    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))

    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool