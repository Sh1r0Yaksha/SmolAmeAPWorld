from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle

class GameMode(Choice):
    """
    Which Game Mode the Player will be completing
    """

    display_name = "Game Mode"

    option_all_stages = 0
    option_bubba = 1
    option_cc = 2

    # Choice options must define an explicit default value.
    default = option_all_stages

@dataclass
class SmolAmeOptions(PerGameCommonOptions):
    game_mode: GameMode
