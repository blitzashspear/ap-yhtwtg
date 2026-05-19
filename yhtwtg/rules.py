from __future__ import annotations
from typing import TYPE_CHECKING
from worlds.generic.Rules import set_rule, add_rule

if TYPE_CHECKING:
    from .world import WinTheGameWorld

def set_all_rules(world: WinTheGameWorld) -> None:
    set_rule(world.get_entrance("Starting Area to Castle Area Outer"), lambda state: state.has_all(("Cerulean Aura", "Springheel Boots"), world.player))

    set_rule(world.get_location("Aqueous Humor - Treasure"), lambda state: state.has("Springheel Boots", world.player))
    set_rule(world.get_location("Artisan Stone Walls - Treasure"), lambda state: state.has("Cerulean Aura", world.player))
    set_rule(world.get_location("Bat Cave - Treasure"), lambda state: state.has("Springheel Boots", world.player))
    set_rule(world.get_location("Circular Logic - Treasure"), lambda state: state.has("Crimson Aura", world.player))
    set_rule(world.get_location("Cognitive Resonance - Treasure"), lambda state: state.has_all(("Cerulean Aura", "Crimson Aura"), world.player))
    set_rule(world.get_location("Contrived Lock/Key Mechanisms - Treasure"), lambda state: state.has_any(("Cerulean Aura", "Springheel Boots"), world.player))
    set_rule(world.get_location("Eponymous - Win the Game"), lambda state: state.has_all(("Letter E", "Letter P", "Letter R", "Letter S", "Letter U"), world.player))
    set_rule(world.get_location("Euclid Shrugged - Treasure"), lambda state: state.has_all(("Cerulean Aura", "Crimson Aura"), world.player))
    set_rule(world.get_location("Forgotten Tunnels - Left Treasure"), lambda state: state.has("Springheel Boots", world.player))
    set_rule(world.get_location("Hops and Skips - Treasure"), lambda state: state.has("Springheel Boots", world.player))
    set_rule(world.get_location("Mind the Gap - Treasure"), lambda state: state.has("Crimson Aura", world.player))
    set_rule(world.get_location("Pit Stop - Treasure"), lambda state: state.has("Springheel Boots", world.player))
    set_rule(world.get_location("Precarious Footholds - Treasure"), lambda state: state.has_all(("Cerulean Aura", "Crimson Aura"), world.player))
    if not world.options.harder_logic_difficulty:
        set_rule(world.get_location("Remnants of a Past Unknown - Treasure"), lambda state: state.has_any(("Crimson Aura", "Springheel Boots"), world.player))
    set_rule(world.get_location("Shelter from the Storm - Treasure"), lambda state: state.has_any(("Cerulean Aura", "Springheel Boots"), world.player))
    set_rule(world.get_location("Tower of Sorrows - Treasure"), lambda state: state.has_any(("Cerulean Aura", "Springheel Boots"), world.player))
    set_rule(world.get_location("Uncertain Semiotics - Treasure"), lambda state: state.has("Springheel Boots", world.player))

    if world.options.split_spider_gloves:
        set_rule(world.get_entrance("Starting Area to Teleporter Area"), lambda state: state.has_any(("Crimson Aura", "Springheel Boots", "Left Spider Glove"), world.player))
        set_rule(world.get_entrance("Castle Area Outer to Castle Area Inner"), lambda state: state.has_all(("Left Spider Glove", "Right Spider Glove"), world.player))
        set_rule(world.get_entrance("Starting Area to End Game Area"), lambda state: state.has_all(("Springheel Boots", "Left Spider Glove", "Right Spider Glove"), world.player))

        set_rule(world.get_location("Abandoned Alcove - Treasure"), lambda state: state.has_all(("Springheel Boots", "Left Spider Glove", "Right Spider Glove"), world.player))
        set_rule(world.get_location("Arcane Vocabulary - Top Treasure"), lambda state: state.has_all(("Springheel Boots", "Right Spider Glove"), world.player))
        set_rule(world.get_location("Avalon Calling - Treasure"), lambda state: state.has_any(("Left Spider Glove", "Right Spider Glove"), world.player))
        set_rule(world.get_location("Danger - Treasure"), lambda state: state.has_any(("Springheel Boots", "Left Spider Glove", "Right Spider Glove"), world.player))
        set_rule(world.get_location("Don't Be Hasty - Top Treasure"), lambda state: state.has_all(("Cerulean Aura", "Right Spider Glove"), world.player))
        set_rule(world.get_location("Hidden Crevasse - Treasure"), lambda state: state.has("Springheel Boots", world.player) and state.has_any(("Left Spider Glove", "Right Spider Glove"), world.player))
        set_rule(world.get_location("Hydra Is Myth - Treasure"), lambda state: state.has_all(("Springheel Boots", "Right Spider Glove"), world.player))
        set_rule(world.get_location("KISS Principle - Treasure"), lambda state: state.has_any(("Left Spider Glove", "Right Spider Glove"), world.player))
        set_rule(world.get_location("Leap of Faith - Treasure"), lambda state: state.has("Right Spider Glove", world.player))
        set_rule(world.get_location("Maps and Legends - Treasure"), lambda state: state.has_all(("Springheel Boots", "Right Spider Glove"), world.player))
        set_rule(world.get_location("Never Could See Any Other Way - Treasure"), lambda state: state.has("Cerulean Aura", world.player) or state.has_all(("Springheel Boots", "Left Spider Glove"), world.player) or state.has_all(("Springheel Boots", "Right Spider Glove"), world.player))
        set_rule(world.get_location("Playing with Fire - Treasure"), lambda state: state.has_all(("Springheel Boots", "Left Spider Glove"), world.player) or state.has_all(("Springheel Boots", "Right Spider Glove"), world.player))
        set_rule(world.get_location("Prawn Shot First - Treasure"), lambda state: state.has("Crimson Aura", world.player) and state.has_any(("Springheel Boots", "Left Spider Glove", "Right Spider Glove"), world.player))
        set_rule(world.get_location("Snake, It's a Snake - Treasure"), lambda state: state.has("Right Spider Glove", world.player) or state.has_all(("Springheel Boots", "Left Spider Glove"), world.player))
        set_rule(world.get_location("Swimming Upstream - Treasure"), lambda state: state.has("Right Spider Glove", world.player) or state.has_all(("Springheel Boots", "Left Spider Glove"), world.player))
        set_rule(world.get_location("Taking the Long Way - Left Treasure"), lambda state: state.has_all(("Left Spider Glove", "Right Spider Glove"), world.player) or state.has_all(("Springheel Boots", "Left Spider Glove"), world.player) or state.has_all(("Springheel Boots", "Right Spider Glove"), world.player))
        set_rule(world.get_location("Taking the Long Way - Right Treasure"), lambda state: state.has_all(("Cerulean Aura", "Crimson Aura", "Springheel Boots", "Left Spider Glove", "Right Spider Glove"), world.player))
        set_rule(world.get_location("The Arbitrarium - Treasure"), lambda state: (state.has_all(("Springheel Boots", "Left Spider Glove"), world.player) or state.has("Right Spider Glove", world.player)))
        set_rule(world.get_location("Tower of Regrets - Treasure"), lambda state: (state.has("Right Spider Glove", world.player) or state.has_all(("Springheel Boots", "Left Spider Glove"), world.player)) and state.has_any(("Cerulean Aura", "Springheel Boots"), world.player))
        set_rule(world.get_location("You Have to Start the Game - Treasure"), lambda state: state.has("Springheel Boots", world.player) and state.has_any(("Left Spider Glove", "Right Spider Glove"), world.player))

    else:
        set_rule(world.get_entrance("Starting Area to Teleporter Area"), lambda state: state.has_any(("Crimson Aura", "Springheel Boots", "Spider Gloves"), world.player))
        set_rule(world.get_entrance("Castle Area Outer to Castle Area Inner"), lambda state: state.has("Spider Gloves", world.player))
        set_rule(world.get_entrance("Starting Area to End Game Area"), lambda state: state.has_all(("Springheel Boots", "Spider Gloves"), world.player))

        set_rule(world.get_location("Abandoned Alcove - Treasure"), lambda state: state.has_all(("Springheel Boots", "Spider Gloves"), world.player))
        set_rule(world.get_location("Arcane Vocabulary - Top Treasure"), lambda state: state.has_all(("Springheel Boots", "Spider Gloves"), world.player))
        set_rule(world.get_location("Avalon Calling - Treasure"), lambda state: state.has("Spider Gloves", world.player))
        set_rule(world.get_location("Danger - Treasure"), lambda state: state.has_any(("Springheel Boots", "Spider Gloves"), world.player))
        set_rule(world.get_location("Don't Be Hasty - Top Treasure"), lambda state: state.has_all(("Cerulean Aura", "Spider Gloves"), world.player))
        set_rule(world.get_location("Hidden Crevasse - Treasure"), lambda state: state.has_all(("Springheel Boots", "Spider Gloves"), world.player))
        set_rule(world.get_location("Hydra Is Myth - Treasure"), lambda state: state.has_all(("Springheel Boots", "Spider Gloves"), world.player))
        set_rule(world.get_location("KISS Principle - Treasure"), lambda state: state.has("Spider Gloves", world.player))
        set_rule(world.get_location("Leap of Faith - Treasure"), lambda state: state.has("Spider Gloves", world.player))
        set_rule(world.get_location("Maps and Legends - Treasure"), lambda state: state.has_all(("Springheel Boots", "Spider Gloves"), world.player))
        set_rule(world.get_location("Never Could See Any Other Way - Treasure"), lambda state: state.has("Cerulean Aura", world.player) or state.has_all(("Springheel Boots", "Spider Gloves"), world.player))
        set_rule(world.get_location("Playing with Fire - Treasure"), lambda state: state.has_all(("Springheel Boots", "Spider Gloves"), world.player))
        set_rule(world.get_location("Prawn Shot First - Treasure"), lambda state: state.has("Crimson Aura", world.player) and state.has_any(("Springheel Boots", "Spider Gloves"), world.player))
        set_rule(world.get_location("Snake, It's a Snake - Treasure"), lambda state: state.has("Spider Gloves", world.player))
        set_rule(world.get_location("Swimming Upstream - Treasure"), lambda state: state.has("Spider Gloves", world.player))
        set_rule(world.get_location("Taking the Long Way - Left Treasure"), lambda state: state.has("Spider Gloves", world.player))
        set_rule(world.get_location("Taking the Long Way - Right Treasure"), lambda state: state.has_all(("Cerulean Aura", "Crimson Aura", "Springheel Boots", "Spider Gloves"), world.player))
        set_rule(world.get_location("The Arbitrarium - Treasure"), lambda state: state.has_all(("Springheel Boots", "Spider Gloves"), world.player))
        set_rule(world.get_location("Tower of Regrets - Treasure"), lambda state: state.has("Spider Gloves", world.player) and state.has_any(("Cerulean Aura", "Springheel Boots"), world.player))
        set_rule(world.get_location("You Have to Start the Game - Treasure"), lambda state: state.has_all(("Springheel Boots", "Spider Gloves"), world.player))

    if world.options.require_unlock_teleporters:
        add_rule(world.get_entrance("Starting Area to Teleporter Area"), lambda state: state.has("Unlock Teleporters", world.player))

        add_rule(world.get_location("Consolation Prize - Treasure"), lambda state: state.has("Unlock Teleporters", world.player))
        add_rule(world.get_location("Eponymous - Win the Game"), lambda state: state.has("Unlock Teleporters", world.player))
        add_rule(world.get_location("Secret Cat Level - Left Treasure"), lambda state: state.has("Unlock Teleporters", world.player))
        add_rule(world.get_location("Secret Cat Level - Right Treasure"), lambda state: state.has("Unlock Teleporters", world.player))

    world.multiworld.completion_condition[world.player] = lambda state: state.has("Win the Game", world.player)