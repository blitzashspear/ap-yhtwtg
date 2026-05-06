from __future__ import annotations
from typing import TYPE_CHECKING
from BaseClasses import Location
if TYPE_CHECKING:
    from .world import WinTheGameWorld
from .location_ids import LOCATION_IDS

class WinTheGameLocation(Location):
    game = "You Have to Win the Game"

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_IDS[location_name] for location_name in location_names}

def create_locations(world: WinTheGameWorld) -> None:
    starting_area = world.get_region("Starting Area")
    teleporter_area = world.get_region("Teleporter Area")
    castle_area_outer = world.get_region("Castle Area Outer")
    castle_area_inner = world.get_region("Castle Area Inner")
    end_game_area = world.get_region("End Game Area")

    starting_area_locations = [
        "Abandoned Alcove",
        "Arcane Vocabulary (Bottom)",
        "Arcane Vocabulary (Top)",
        "Artisan Stone Walls",
        "Bat Cave",
        "Cave In",
        "Cerulean Aura",
        "Circular Logic",
        "Cognitive Resonance",
        "Contrived Lock/Key Mechanisms",
        "Covert Operators (Left)",
        "Covert Operators (Right)",
        "Crimson Aura",
        "Danger",
        "Don't Be Hasty (Bottom)",
        "Don't Be Hasty (Top)",
        "Euclid Shrugged",
        "Great Hall",
        "Hops and Skips",
        "Hydra Is Myth",
        "KISS Principle",
        "Maps and Legends",
        "Mind the Gap",
        "Nice of You to Drop In",
        "Never Could See Any Other Way",
        "Obvious Movie Quote",
        "Precarious Footholds",
        "Pit Stop",
        "Prawn Shot First",
        "Remnants of a Past Unknown",
        "Shelter from the Storm",
        "Snake, It's a Snake",
        "Subterranea",
        "Swimming Upstream",
        "Taking the Long Way (Left)",
        "Taking the Long Way (Right)",
        "The Proper Motivation",
        "Tower of Regrets",
        "Tower of Sorrows",
        "Treasure Hunt",
        "Uncertain Semiotics",
        "You Have to Start the Game",
        "Yggdrasil"
    ]
    starting_area.add_locations(get_location_names_with_ids(starting_area_locations), WinTheGameLocation)

    teleporter_area_locations = [
        "Aqueous Humor",
        "Avalon Calling",
        "Descent",
        "Forgotten Tunnels (Left)",
        "Forgotten Tunnels (Right)",
        "Hidden Crevasse",
        "Like Ivy, Twisting",
        "Secret Passage",
        "Springheel Boots",
        "The Arbitrarium",
        "The Crab Cake Is a Lie"
    ]
    teleporter_area.add_locations(get_location_names_with_ids(teleporter_area_locations), WinTheGameLocation)

    castle_area_outer_locations = [
        "Attic Storeroom (Bottom)",
        "Don't Be Hasty (Bottom)",
        "Great Hall",
        "Spider Gloves",
        "Vestibule"
    ]
    castle_area_outer.add_locations(get_location_names_with_ids(castle_area_outer_locations), WinTheGameLocation)

    castle_area_inner_locations = [
        "An Even 0x80",
        "Attic Storeroom (Top)",
        "Leap of Faith",
        "Not Worth It!",
        "The Floor Is Lava"
    ]
    castle_area_inner.add_locations(get_location_names_with_ids(castle_area_inner_locations), WinTheGameLocation)

    end_game_area_locations = [
        "Consolation Prize",
        "Eponymous",
        "Hardcore Prawn",
        "Playing with Fire",
        "Secret Cat Level (Left)",
        "Secret Cat Level (Right)",
        "The Coin and the Courage",
        "You Have to Start the Game"
    ]
    end_game_area.add_locations(get_location_names_with_ids(end_game_area_locations), WinTheGameLocation)
