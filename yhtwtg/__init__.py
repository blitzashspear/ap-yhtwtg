from worlds.AutoWorld import World, WebWorld
from BaseClasses import Tutorial
from . import items, regions, rules
from .options import WinTheGameOptions, option_groups
from .data.location_ids import LOCATION_IDS
from .data.item_ids import ITEM_IDS
from worlds.LauncherComponents import Component, Type, components, launch as launch_component, icon_paths

def launch_client() -> None:
    from .client import launch
    launch_component(launch, name="WinTheGameClient")

components.append(
    Component(
        display_name="You Have to Win the Game Client",
        script_name="WinTheGameClient",
        func=launch_client,
        game_name="You Have to Win the Game",
        component_type=Type.CLIENT,
        icon="wintheicon"
    )
)
icon_paths["wintheicon"] = f"ap:{__name__}/icons/wintheicon.png"

class WinTheGameWebWorld(WebWorld):
    game = "You Have to Win the Game"
    theme = "dirt"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up You Have to Win the Game for Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["blitzashspear"]
    )
    option_groups = option_groups
    tutorials = [setup_en]

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
    origin_region_name = "Starting Hallway"
    ut_can_gen_without_yaml = True
    password = "SUPER"
    magic_word = "VXSHU"
    magic_symbol = 3
    
    def create_regions(self) -> None:
        regions.create_regions_and_locations(self)

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
            # Please for the love of christ stop forgetting to put .value on the yaml options.
            "room_sanity": self.options.room_sanity.value,
            "bell_sanity": self.options.bell_sanity.value,
            "death_link": self.options.death_link.value,
            "death_link_amnesty": self.options.death_link_amnesty.value,
            "death_link_behavior": self.options.death_link_behavior.value,
            "stop_jumping_trap_length": self.options.stop_jumping_trap_length.value,
            "freeze_trap_length": self.options.freeze_trap_length.value,
            "fast_trap_length": self.options.fast_trap_length.value,
            "split_spider_gloves": self.options.split_spider_gloves.value,
            "require_unlock_teleporters": self.options.require_unlock_teleporters.value,
            "logic_difficulty": self.options.logic_difficulty.value,
            "include_extra_roadblocks": self.options.include_extra_roadblocks.value,
            "reset_timer": self.options.reset_timer.value,
            #TODO uncomment out for password rando
            # "password_randomization": self.options.password_randomization.value,
            # "display_password_letters": self.options.display_password_letters.value,

            # "password": self.password,
            # "magic_word": self.magic_word,
            # "magic_symbol": self.magic_symbol
        }

    @staticmethod
    def interpret_slot_data(slot_data: dict):
        return slot_data
    
    def generate_early(self) -> None:
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            self.passthrough = re_gen_passthrough["You Have to Win the Game"]
            self.options.room_sanity.value = self.passthrough["room_sanity"]
            self.options.bell_sanity.value = self.passthrough["bell_sanity"]
            self.options.split_spider_gloves.value = self.passthrough["split_spider_gloves"]
            self.options.require_unlock_teleporters.value = self.passthrough["require_unlock_teleporters"]
            self.options.logic_difficulty.value = self.passthrough["logic_difficulty"]
            self.options.include_extra_roadblocks.value = self.passthrough["include_extra_roadblocks"]
            # TODO uncomment out for password rando
            # self.options.password_randomization.value = self.passthrough["password_randomization"]
