from __future__ import annotations
import json
from pathlib import Path

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from . import options as smolame_options  # rename due to a name conflict with World.options

if TYPE_CHECKING:
    from .world import SmolAmeWorld

items_path = Path(__file__).parent / "items.json"
with items_path.open("r", encoding="utf-8") as file:
    items = json.load(file)

ITEM_NAME_TO_ID = {}

for item_name, data in items.items():
    ITEM_NAME_TO_ID[item_name] = data["ID"]

class SmolAmeItem(Item):
    game = "Smol Ame"

def create_item_with_correct_classification(world: SmolAmeWorld, name: str) -> SmolAmeItem:
    match world.options.game_mode:
        case smolame_options.GameMode.option_any:
            classification = items[name]["Classification"]["any"]
        case smolame_options.GameMode.option_all_stages:
            classification = items[name]["Classification"]["all_stages"]
        case smolame_options.GameMode.option_bubba:
            classification = items[name]["Classification"]["bubba"]
        case smolame_options.GameMode.option_cc:
            classification = items[name]["Classification"]["cc"]

    classification_type = {
        "filler": ItemClassification.filler,
        "progression": ItemClassification.progression,
    }[classification]


    return SmolAmeItem(name, classification_type, items[name]["ID"], world.player)


def create_all_items(world: SmolAmeWorld) -> None:
    itempool: list[Item] = []
    
    for name, data in items.items():
        for region, quantity in data["quantity"].items():
            for _ in range(quantity):
                itempool.append(world.create_item(name))

    number_of_items = len(itempool)

    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))

    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool
