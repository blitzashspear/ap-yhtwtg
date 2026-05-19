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
        "Abandoned Alcove - Treasure",
        "Arcane Vocabulary - Bottom Treasure",
        "Arcane Vocabulary - Top Treasure",
        "Artisan Stone Walls - Treasure",
        "Bat Cave - Treasure",
        "Cave In - Treasure",
        "Cerulean Aura - Treasure",
        "Circular Logic - Treasure",
        "Cognitive Resonance - Treasure",
        "Contrived Lock/Key Mechanisms - Treasure",
        "Covert Operators - Left Treasure",
        "Covert Operators - Right Treasure",
        "Crimson Aura - Treasure",
        "Danger - Treasure",
        "Don't Be Hasty - Bottom Treasure",
        "Don't Be Hasty - Top Treasure",
        "Euclid Shrugged - Treasure",
        "Great Hall - Treasure",
        "Hops and Skips - Treasure",
        "Hydra Is Myth - Treasure",
        "KISS Principle - Treasure",
        "Maps and Legends - Treasure",
        "Mind the Gap - Treasure",
        "Nice of You to Drop In - Treasure",
        "Never Could See Any Other Way - Treasure",
        "Obvious Movie Quote - Treasure",
        "Precarious Footholds - Treasure",
        "Pit Stop - Treasure",
        "Playing with Fire - Treasure",
        "Prawn Shot First - Treasure",
        "Remnants of a Past Unknown - Treasure",
        "Shelter from the Storm - Treasure",
        "Snake, It's a Snake - Treasure",
        "Subterranea - Treasure",
        "Swimming Upstream - Treasure",
        "Taking the Long Way - Left Treasure",
        "Taking the Long Way - Right Treasure",
        "The Proper Motivation - Treasure",
        "Tower of Regrets - Treasure",
        "Tower of Sorrows - Treasure",
        "Treasure Hunt - Treasure",
        "Uncertain Semiotics - Treasure",
        "You Have to Start the Game - Treasure",
        "Yggdrasil - Treasure",
        "You Have to Start the Game - Treasure"
    ]
    starting_area.add_locations(get_location_names_with_ids(starting_area_locations), WinTheGameLocation)

    teleporter_area_locations = [
        "Aqueous Humor - Treasure",
        "Avalon Calling - Treasure",
        "Descent - Treasure",
        "Forgotten Tunnels - Left Treasure",
        "Forgotten Tunnels - Right Treasure",
        "Hidden Crevasse - Treasure",
        "Like Ivy, Twisting - Treasure",
        "Secret Passage - Treasure",
        "Springheel Boots - Treasure",
        "The Arbitrarium - Treasure",
        "The Crab Cake Is a Lie - Treasure",
    ]
    teleporter_area.add_locations(get_location_names_with_ids(teleporter_area_locations), WinTheGameLocation)

    castle_area_outer_locations = [
        "Attic Storeroom - Bottom Treasure",
        "Don't Be Hasty - Bottom Treasure",
        "Great Hall - Treasure",
        "Spider Gloves - Treasure",
        "Vestibule - Treasure"
    ]
    castle_area_outer.add_locations(get_location_names_with_ids(castle_area_outer_locations), WinTheGameLocation)

    castle_area_inner_locations = [
        "An Even 0x80 - Treasure",
        "Attic Storeroom - Top Treasure",
        "Leap of Faith - Treasure",
        "Not Worth It! - Treasure",
        "The Floor Is Lava - Treasure"
    ]
    castle_area_inner.add_locations(get_location_names_with_ids(castle_area_inner_locations), WinTheGameLocation)

    end_game_area_locations = [
        "Consolation Prize - Treasure",
        "Eponymous - Win the Game",
        "Hardcore Prawn - Treasure",
        "Secret Cat Level - Left Treasure",
        "Secret Cat Level - Right Treasure",
        "The Coin and the Courage - Treasure"
    ]
    end_game_area.add_locations(get_location_names_with_ids(end_game_area_locations), WinTheGameLocation)
