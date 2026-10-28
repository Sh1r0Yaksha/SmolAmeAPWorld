from __future__ import annotations
import json
from pathlib import Path

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule

from . import options as smolame_options  # rename due to a name conflict with World.options
from .regions import get_included_regions

if TYPE_CHECKING:
    from .world import SmolAmeWorld

area_items_path = Path(__file__).parent / "area_items.json"
with area_items_path.open("r", encoding="utf-8") as file:
    area_items = json.load(file)



def set_all_rules(world: SmolAmeWorld) -> None:
    set_completion_condition(world)



def set_completion_condition(world: SmolAmeWorld) -> None:

    # Regions left out by include_ca don't exist in this world, so they can't be required.
    included_regions = [
        region_name
        for region_name in get_included_regions(world)
        if region_name != "Hub"
    ]

    Level_Clears = [
        f"{region_name}-Cleared"
        for region_name in included_regions
    ]

    # Item names are "<region>-<item>", so the region is everything before the last "-"
    Bubba_Coins = [
        item_name
        for item_name in world.item_name_to_id
        if "Bubba Coin" in item_name
        and item_name.rpartition("-")[0] in included_regions
    ]

    Stache_Quotas = [
        f"{region_name}-Stache Quota"
        for region_name in included_regions
    ]

    match world.options.game_mode:
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