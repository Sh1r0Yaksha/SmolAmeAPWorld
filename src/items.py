from __future__ import annotations
import json
from pathlib import Path
import random

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from . import options as smolame_options  # rename due to a name conflict with World.options
from .regions import get_included_regions

if TYPE_CHECKING:
    from .world import SmolAmeWorld

ids_path = Path(__file__).parent / "IDs.json"
with ids_path.open("r", encoding="utf-8") as file:
    ids = json.load(file)

# Built from the full json on purpose, so IDs stay the same whether or not include_ca is on.
ITEM_NAME_TO_ID = {}

for region_name, region_data in ids.items():
    for item_name, item_id in region_data.get("items", {}).items():
        ITEM_NAME_TO_ID[f"{region_name}-{item_name}"] = item_id

class SmolAmeItem(Item):
    game = "Smol Ame"

def create_item_with_correct_classification(world: SmolAmeWorld, name: str) -> SmolAmeItem:
    classification_type = ItemClassification.filler

    if "MOM Button" in name:
        classification_type = ItemClassification.progression

    if "Bubba Coin" in name:
        if (world.options.game_mode in (
                    smolame_options.GameMode.option_bubba,
                    smolame_options.GameMode.option_cc,
                )):
            classification_type = ItemClassification.progression
        else:
            classification_type = ItemClassification.useful

    
    return SmolAmeItem(name, classification_type, ITEM_NAME_TO_ID[name], world.player)

def get_random_filler_item_name(world: SmolAmeWorld) -> str:
    return random.choices(
        ["General-Moustache", "General-10 Moustache"],
        weights=[90, 10],
        k=1
    )[0]

def create_all_items(world: SmolAmeWorld) -> None:
    itempool: list[Item] = []

    for region_name in get_included_regions(world):
        for item_name in ids[region_name]['items']:
            itempool.append(world.create_item(f"{region_name}-{item_name}"))
    
    number_of_items = len(itempool)

    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))

    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool

