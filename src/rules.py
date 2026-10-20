from __future__ import annotations
import json
from pathlib import Path

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule

from . import options as smolame_options  # rename due to a name conflict with World.options

if TYPE_CHECKING:
    from .world import SmolAmeWorld

area_items_path = Path(__file__).parent / "area_items.json"
with area_items_path.open("r", encoding="utf-8") as file:
    area_items = json.load(file)



def set_all_rules(world: SmolAmeWorld) -> None:

    set_item_placement_rules(world)
    set_completion_condition(world)

def set_item_placement_rules(world: SmolAmeWorld) -> None:
    # Entry button not placed in the level itself
    for region in world.multiworld.get_regions(world.player):
        for location in region.locations:
            location.item_rule = lambda item, region_name=region.name: (
                not (
                    "entry button" in item.name.lower()
                    and region_name.lower() in item.name.lower()
                )
            )


def set_completion_condition(world: SmolAmeWorld) -> None:

    Level_Clears = [
        f"{region_name} Cleared"
        for region_name in area_items
    ]

    Bubba_Coins = [
        item_name
        for item_name in world.item_name_to_id
        if "bubba coin" in item_name.lower()
    ]

    Stache_Quotas = [
        item_name
        for item_name in world.item_name_to_id
        if "stache quota" in item_name.lower()
    ]

    match world.options.game_mode:
        case smolame_options.GameMode.option_any:
            world.set_completion_rule(HasAll(*Level_Clears))

        case smolame_options.GameMode.option_all_stages:
            world.set_completion_rule(HasAll(*Level_Clears))

        case smolame_options.GameMode.option_bubba:
            world.set_completion_rule(
                HasAll(*Level_Clears)
                & HasAll(*Bubba_Coins)
            )

        case smolame_options.GameMode.option_cc:
            world.set_completion_rule(
                HasAll(*Level_Clears)
                & HasAll(*Bubba_Coins)
                & HasAll(*Stache_Quotas)
            )