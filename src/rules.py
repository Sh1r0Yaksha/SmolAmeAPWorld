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


def set_all_rules(world: SmolAmeWorld) -> None:

    set_item_placement_rules(world)
    set_completion_condition(world)

def set_item_placement_rules(world: SmolAmeWorld) -> None:
    for region in world.multiworld.get_regions(world.player):
        if region.name != "hub":
            for location in region.locations:
                location.item_rule = (
                    lambda item: item.name != "level_entry_button"
                )


def set_completion_condition(world: SmolAmeWorld) -> None:
    mom_button_count = 0
    bubba_count = 0
    stache_quota_count = 0

    for item_name, data in items.items():
        for quantity in data["quantity"].values():
            if item_name == "mom_button":
                mom_button_count += quantity
            elif item_name == "bubba":
                bubba_count += quantity
            elif item_name == "stache_quota":
                stache_quota_count += quantity
                
    match world.options.game_mode:
        case smolame_options.GameMode.option_any:
            world.set_completion_rule(
                Has("mom_button", count=mom_button_count)
            )
        case smolame_options.GameMode.option_all_stages:
            world.set_completion_rule(
                Has("mom_button", count=mom_button_count)
            )
        case smolame_options.GameMode.option_bubba:
            world.set_completion_rule(
                Has("mom_button", count=mom_button_count)
                & Has("bubba", count=bubba_count)
            )
        case smolame_options.GameMode.option_cc:
            world.set_completion_rule(
                Has("mom_button", count=mom_button_count)
                & Has("bubba", count=bubba_count)
                & Has("stache_quota", count=stache_quota_count)
            )
