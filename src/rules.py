from __future__ import annotations
import json
from pathlib import Path

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule

from . import options as smolame_options  # rename due to a name conflict with World.options

if TYPE_CHECKING:
    from .world import SmolAmeWorld

items_path = Path(__file__).parent / "items.json"
with items_path.open("r", encoding="utf-8") as file:
    items = json.load(file)

regions_path = Path(__file__).parent / "regions.json"
with regions_path.open("r", encoding="utf-8") as file:
    regions = json.load(file)


def set_all_rules(world: SmolAmeWorld) -> None:

    set_item_placement_rules(world)
    set_completion_condition(world)

def set_item_placement_rules(world: SmolAmeWorld) -> None:
    for region in world.multiworld.get_regions(world.player):
        if region.name != "hub":
            for location in region.locations:
                location.item_rule = (
                    lambda item: item.name != "Level Entry Button"
                )


def set_completion_condition(world: SmolAmeWorld) -> None:
    mom_button_count = 0
    bubba_count = 0
    stache_quota_count = 0

    for item_name, data in items.items():
        if item_name == "MOM Button":
            mom_button_count = sum(
                len(locations)
                for locations in data.get("Area", {}).values()
            )

        elif item_name == "Bubba":
            bubba_count = sum(
                len(locations)
                for locations in data.get("Area", {}).values()
            )

        elif item_name == "Stache Quota":
            # One Stache Quota check in each level
            stache_quota_count = sum(
                1 for region_name in regions
                if region_name != "Hub"
            )

    match world.options.game_mode:
        case smolame_options.GameMode.option_any:
            world.set_completion_rule(
                Has("MOM Button", count=mom_button_count)
            )

        case smolame_options.GameMode.option_all_stages:
            world.set_completion_rule(
                Has("MOM Button", count=mom_button_count)
            )

        case smolame_options.GameMode.option_bubba:
            world.set_completion_rule(
                Has("MOM Button", count=mom_button_count)
                & Has("Bubba", count=bubba_count)
            )

        case smolame_options.GameMode.option_cc:
            world.set_completion_rule(
                Has("MOM Button", count=mom_button_count)
                & Has("Bubba", count=bubba_count)
                & Has("Stache Quota", count=stache_quota_count)
            )