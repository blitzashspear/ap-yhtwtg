from worlds.AutoWorld import World
from . import items, locations, regions, rules

from .web_world import WinTheGameWebWorld
from .options import WinTheGameOptions

from .location_ids import LOCATION_IDS
from .item_ids import ITEM_IDS

class WinTheGameWorld(World):
    """
    You Have to Win the Game is a free exploration platformer with a retro 1980s PC aesthetic.
    Run, jump, and avoid deadly pitfalls as you explore the ruins of a lost world in search of hidden treasures and rare artifacts!
    """

    game = "You Have to Win the Game"
    web = WinTheGameWebWorld()
    options_dataclass = WinTheGameOptions
    options: WinTheGameOptions
    location_name_to_id = LOCATION_IDS
    item_name_to_id = ITEM_IDS
    origin_region_name = "Starting Area"
    def create_regions(self) -> None:
        regions.create_regions(self)
        locations.create_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.WinTheGameItem:
        return items.create_item_with_correct_classification(self, name)
    
    def get_filler_item_name(self) -> str:
        return "Nothing"
    
    def fill_slot_data(self):
        return {
            "death_link": self.options.death_link,
            "death_link_amnesty": self.options.death_link_amnesty,
            "split_spider_gloves": self.options.split_spider_gloves,
            "require_unlock_teleporters": self.options.require_unlock_teleporters,
            "logic_difficulty": self.options.logic_difficulty,
        }