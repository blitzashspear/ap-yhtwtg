from __future__ import annotations
from typing import TYPE_CHECKING
from BaseClasses import Item
if TYPE_CHECKING:
    from .world import WinTheGameWorld
from .item_ids import ITEM_IDS
from .item_classifications import ITEM_CLASSIFICATIONS

class WinTheGameItem(Item):
    game = "You Have to Win the Game"

def create_item_with_correct_classification(world: WinTheGameWorld, item_name: str) -> WinTheGameItem:
    return WinTheGameItem(item_name, ITEM_CLASSIFICATIONS[item_name], ITEM_IDS[item_name], world.player)

def create_all_items(world: WinTheGameWorld) -> None:
    world.get_location("Eponymous").place_locked_item(create_item_with_correct_classification(world, "Win The Game"))
    itempool = []

    itempool.append(world.create_item("Cerulean Aura"))
    itempool.append(world.create_item("Crimson Aura"))
    itempool.append(world.create_item("Springheel Boots"))
    if world.options.split_spider_gloves:
        itempool.append(world.create_item("Left Spider Glove"))
        itempool.append(world.create_item("Right Spider Glove"))
    else:
        itempool.append(world.create_item("Spider Gloves"))
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        itempool.append(world.create_item(f"Letter {letter}"))

    if world.options.shuffle_lose_the_game:
        itempool.append(world.create_item("Lose The Game"))

    if world.options.shuffle_secret_rooms_trap:
        itempool.append(world.create_item("Secret Room Trap"))  

    if world.options.shuffle_stop_jumping_trap:
        itempool.append(world.create_item("Stop Jumping Trap"))

    #TODO make Nothing items respect world.options.local_nothing_percentage
    number_of_items = len(itempool)
    needed_number_of_filler_items = len(world.multiworld.get_unfilled_locations(world.player)) - number_of_items
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool