from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

class WinTheGameWebWorld(WebWorld):
    game = "You Have to Win the Game"
    theme = "dirt"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up You Have to Win the Game for Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["blitzashspear"],
    )

    tutorials = [setup_en]
