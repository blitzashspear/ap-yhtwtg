from __future__ import annotations
from typing import TYPE_CHECKING
from BaseClasses import Item, ItemClassification
from worlds.generic.Rules import CollectionState
if TYPE_CHECKING:
    from .__init__ import WinTheGameWorld
from .data.item_ids import ITEM_IDS
from .data.item_classifications import ITEM_CLASSIFICATIONS
from .data.valid_passwords import VALID_PASSWORDS

class WinTheGameItem(Item):
    game = "You Have to Win the Game"

def create_item_with_custom_classification(world: WinTheGameWorld, item_name: str, classification: ItemClassification) -> WinTheGameItem:
    return WinTheGameItem(item_name, classification, ITEM_IDS[item_name], world.player)

def create_item_with_correct_classification(world: WinTheGameWorld, item_name: str) -> WinTheGameItem:
    return WinTheGameItem(item_name, ITEM_CLASSIFICATIONS[item_name], ITEM_IDS[item_name], world.player)

def create_all_items(world: WinTheGameWorld) -> None:
    world.get_location("Eponymous - Win the Game").place_locked_item(create_item_with_correct_classification(world, "Win the Game"))
    itempool: list[Item] = []

    itempool.append(world.create_item("Cerulean Aura"))
    itempool.append(world.create_item("Crimson Aura"))
    itempool.append(world.create_item("Springheel Boots"))
    if world.options.split_spider_gloves:
        itempool.append(world.create_item("Left Spider Glove"))
        itempool.append(world.create_item("Right Spider Glove"))
    else:
        itempool.append(world.create_item("Spider Gloves"))

    password = "SUPER"
    # if world.options.password_randomization > 0:
    #     if world.options.password_randomization == 1: # Words
    #         password = world.multiworld.random.choice(VALID_PASSWORDS)
    #     elif world.options.password_randomization == 2: # Any
    #         password = world.multiworld.random.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 5)
    #     itempool.append(world.create_item("Magic Word"))
    #     itempool.append(world.create_item("Magic Symbol"))
    #     magic_symbol = world.multiworld.random.randrange(1, 10) # 1-9
    #     magic_word = ""
    #     for letter in password:
    #         ascii = ord(letter) - magic_symbol
    #         if ascii < ord("A"):
    #             ascii += 26
    #         magic_word += chr(ascii)
    #     world.password = password
    #     world.magic_word = magic_word
    #     world.magic_symbol = magic_symbol

    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if letter in password:
            itempool.append(create_item_with_custom_classification(world, f"Letter {letter}", ItemClassification.progression_skip_balancing))
        else:
            itempool.append(world.create_item(f"Letter {letter}"))

    if world.options.shuffle_lose_the_game:
        itempool.append(world.create_item("Lose The Game"))

    if world.options.shuffle_secret_rooms_trap:
        itempool.append(world.create_item("Secret Room Trap"))  

    if world.options.shuffle_stop_jumping_trap:
        itempool.append(world.create_item("Stop Jumping Trap"))
    
    if world.options.shuffle_freeze_trap:
        itempool.append(world.create_item("Freeze Trap"))

    if world.options.shuffle_fast_trap:
        itempool.append(world.create_item("Fast Trap"))

    if world.options.require_unlock_teleporters:
        itempool.append(world.create_item("Unlock Teleporters"))

    if world.options.include_extra_roadblocks:
        itempool.append(world.create_item("Unlock Quarry"))
        itempool.append(world.create_item("Unlock Mineshaft"))
        itempool.append(world.create_item("Unlock Castle"))
        itempool.append(world.create_item("Unlock Graveyard"))

    # what the fuck is this
    if world.multiworld.players > 1:
        unfilled_locations = world.multiworld.get_unfilled_locations(world.player)
        sphere_one = world.multiworld.get_reachable_locations(CollectionState(world.multiworld),world.player)
        reserved_sphere_one = world.random.sample(sphere_one, 2)
        for location in world.random.sample(unfilled_locations, len(unfilled_locations)*world.options.local_nothing_percentage//100):
            if location not in reserved_sphere_one:
                world.get_location(location.name).place_locked_item(world.create_filler())

    itempool_filler_items = len(world.multiworld.get_unfilled_locations(world.player)) - len(itempool)
    itempool += [world.create_filler() for _ in range(itempool_filler_items)]

    world.multiworld.itempool += itempool