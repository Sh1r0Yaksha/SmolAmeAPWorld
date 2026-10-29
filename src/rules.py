from __future__ import annotations
import json
from pathlib import Path
from worlds.generic.Rules import forbid_items_for_player
from .regions import get_included_regions, get_level_regions, ids
from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule

from . import options as smolame_options  # rename due to a name conflict with World.options

if TYPE_CHECKING:
    from .world import SmolAmeWorld

def set_all_rules(world: SmolAmeWorld) -> None:
    set_item_placement_rules(world)
    set_completion_condition(world)

def set_item_placement_rules(world: SmolAmeWorld) -> None:
    """
    A region's MOM Button Unlock items can never be placed on any
    MOM Button check of that same region.
    """
    for region_name in get_included_regions(world):
        region_data = ids[region_name]

        unlock_items = {
            f"{region_name}-{item_name}"
            for item_name in region_data.get("items", {})
            if item_name.startswith("MOM Button")
        }
        if not unlock_items:
            continue

        for check_name in region_data.get("checks", {}):
            if check_name.startswith("MOM Button"):
                location = world.get_location(f"{region_name}-{check_name}")
                forbid_items_for_player(location, unlock_items, world.player)

def set_completion_condition(world: SmolAmeWorld) -> None:

    # Regions left out by include_ca don't exist in this world, so they can't be required.
    included_regions = get_level_regions(world)

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
        f"{region_name}-Stache Quota Completed"
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