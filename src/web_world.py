from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld


# For our game to display correctly on the website, we need to define a WebWorld subclass.
class SmolAmeWebWorld(WebWorld):
    game = "Smol Ame"

    # You can choose between dirt, grass, grassFlowers, ice, jungle, ocean, partyTime, and stone.
    theme = "grassFlowers"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Smol Ame for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Shir0Yaksha"],
    )
    
    tutorials = [setup_en]