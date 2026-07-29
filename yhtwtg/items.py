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
    if world.options.password_randomization > 0:
        if world.options.password_randomization == 1: # Words
            password = world.random.choice(VALID_PASSWORDS)
        elif world.options.password_randomization == 2: # Any
            password = world.random.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 5)
        itempool.append(world.create_item("Reveal Magic Word"))
        itempool.append(world.create_item("Reveal Magic Symbol"))
        magic_symbol = world.random.choice([i for i in range(-9, 10) if i != 0]) # -9 to -1 and 1 to 9
        magic_word = ""
        for letter in password:
            ascii = ord(letter) + magic_symbol
            if ascii > ord("Z"):
                ascii -= 26
            elif ascii < ord("A"):
                ascii += 26
            magic_word += chr(ascii)
        world.password = password
        world.magic_word = magic_word
        world.magic_symbol = magic_symbol

    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if letter in password:
            itempool.append(create_item_with_custom_classification(world, f"Letter {letter}", ItemClassification.progression_deprioritized_skip_balancing))
        else:
            itempool.append(world.create_item(f"Letter {letter}"))

    if world.options.require_unlock_teleporters:
        itempool.append(world.create_item("Unlock Teleporters"))

    for roadblock in world.options.include_extra_roadblocks:
        itempool.append(world.create_item(f"Unlock {roadblock}"))

    if world.options.shuffle_cat_dlc:
        itempool.append(world.create_item("Playable Cat DLC*"))

    if world.options.trap_percentage > 0:
        nothing_amount = len(world.multiworld.get_unfilled_locations(world.player)) - len(itempool)
        traps = world.random.choices(
            population=[
                "Lose the Game",
                "Stop Jumping Trap",
                "Secret Room Trap",
                "Freeze Trap",
                "Fast Trap"
            ],
            weights=[
                world.options.lose_the_game_weight,
                world.options.stop_jumping_trap_weight,
                world.options.secret_rooms_trap_weight,
                world.options.freeze_trap_weight,
                world.options.fast_trap_weight
            ],
            k=nothing_amount * world.options.trap_percentage // 100
        )
        for trap in traps:
            itempool.append(world.create_item(trap))

    # Pre-places a percentage of "Nothing" items locally. 
    # Will set aside an arbitrary number of sphere one locations (2) at random.
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
