from __future__ import annotations
from typing import TYPE_CHECKING
from worlds.generic.Rules import set_rule

if TYPE_CHECKING:
    from .world import WinTheGameWorld

def set_all_rules(world: WinTheGameWorld) -> None:
    #ts lwk unreadable
    set_rule(world.get_entrance("Starting Area to Teleporter Area"), lambda state: state.has_any(("Crimson Aura","Springheel Boots","Spider Gloves"), world.player))
    set_rule(world.get_entrance("Starting Area to Castle Area Outer"), lambda state: state.has_all(("Cerulean Aura", "Crimson Aura", "Springheel Boots"), world.player))
    set_rule(world.get_entrance("Castle Area Outer to Castle Area Inner"), lambda state: state.has("Spider Gloves", world.player))
    set_rule(world.get_entrance("Starting Area to End Game Area"), lambda state: state.has_all(("Springheel Boots", "Spider Gloves"), world.player))

    set_rule(world.get_location("Abandoned Alcove"), lambda state: state.has_all(("Springheel Boots","Spider Gloves"), world.player))
    set_rule(world.get_location("Aqueous Humor"), lambda state: state.has("Springheel Boots", world.player))
    set_rule(world.get_location("Arcane Vocabulary (Top)"), lambda state: state.has_all(("Springheel Boots","Spider Gloves"), world.player))
    set_rule(world.get_location("Artisan Stone Walls"), lambda state: state.has("Cerulean Aura", world.player))
    set_rule(world.get_location("Avalon Calling"), lambda state: state.has("Spider Gloves", world.player))
    set_rule(world.get_location("Bat Cave"), lambda state: state.has("Springheel Boots", world.player))
    set_rule(world.get_location("Circular Logic"), lambda state: state.has("Crimson Aura", world.player))
    set_rule(world.get_location("Cognitive Resonance"), lambda state: state.has_all(("Cerulean Aura", "Crimson Aura"), world.player))
    set_rule(world.get_location("Contrived Lock/Key Mechanisms"), lambda state: state.has_any(("Cerulean Aura", "Springheel Boots"), world.player))
    set_rule(world.get_location("Danger"), lambda state: state.has_any(("Springheel Boots", "Spider Gloves"), world.player))
    set_rule(world.get_location("Don't Be Hasty (Top)"), lambda state: state.has_all(("Cerulean Aura", "Spider Gloves"), world.player))
    set_rule(world.get_location("Eponymous"), lambda state:state.has_all(("Letter E", "Letter P", "Letter R", "Letter S", "Letter U"), world.player))
    set_rule(world.get_location("Euclid Shrugged"), lambda state: state.has_all(("Cerulean Aura", "Crimson Aura"), world.player))
    set_rule(world.get_location("Forgotten Tunnels (Left)"), lambda state: state.has("Springheel Boots", world.player))
    set_rule(world.get_location("Hidden Crevasse"), lambda state: state.has_all(("Springheel Boots", "Spider Gloves"), world.player))
    set_rule(world.get_location("Hops and Skips"), lambda state: state.has("Springheel Boots", world.player))
    set_rule(world.get_location("Hydra Is Myth"), lambda state: state.has_all(("Springheel Boots", "Spider Gloves"), world.player))
    set_rule(world.get_location("KISS Principle"), lambda state: state.has("Spider Gloves", world.player))
    set_rule(world.get_location("Leap of Faith"), lambda state: state.has("Spider Gloves", world.player))
    set_rule(world.get_location("Maps and Legends"), lambda state: state.has_all(("Springheel Boots", "Spider Gloves"), world.player))
    set_rule(world.get_location("Mind the Gap"), lambda state: state.has("Crimson Aura", world.player))
    set_rule(world.get_location("Never Could See Any Other Way"), lambda state: state.has_any(("Cerulean Aura", "Springheel Boots", "Spider Gloves"), world.player))
    set_rule(world.get_location("Pit Stop"), lambda state: state.has("Springheel Boots", world.player))
    set_rule(world.get_location("Prawn Shot First"), lambda state: state.has("Crimson Aura", world.player) and state.has_any(("Springheel Boots", "Spider Gloves"), world.player))
    set_rule(world.get_location("Precarious Footholds"), lambda state: state.has_all(("Cerulean Aura", "Crimson Aura"), world.player))
    set_rule(world.get_location("Remnants of a Past Unknown"), lambda state: state.has_any(("Crimson Aura", "Springheel Boots"), world.player))
    set_rule(world.get_location("Shelter from the Storm"), lambda state: state.has_any(("Cerulean Aura", "Springheel Boots"), world.player))
    set_rule(world.get_location("Snake, It's a Snake"), lambda state: state.has("Spider Gloves", world.player))
    set_rule(world.get_location("Swimming Upstream"), lambda state: state.has("Spider Gloves", world.player))
    set_rule(world.get_location("Taking the Long Way (Left)"), lambda state: state.has("Spider Gloves", world.player) or state.has_all(("Crimson Aura", "Springheel Boots"), world.player))    
    set_rule(world.get_location("Taking the Long Way (Right)"), lambda state: state.has_all(("Cerulean Aura", "Crimson Aura", "Springheel Boots", "Spider Gloves"), world.player))   
    set_rule(world.get_location("The Arbitrarium"), lambda state: state.has_all(("Springheel Boots", "Spider Gloves"), world.player)) 
    set_rule(world.get_location("Tower of Regrets"), lambda state: state.has("Spider Gloves", world.player) and state.has_any(("Cerulean Aura", "Springheel Boots"), world.player))
    set_rule(world.get_location("Tower of Sorrows"), lambda state: state.has_any(("Cerulean Aura", "Springheel Boots"), world.player))
    set_rule(world.get_location("Uncertain Semiotics"), lambda state: state.has("Springheel Boots", world.player))

    world.multiworld.completion_condition[world.player] = lambda state: state.has("Win The Game", world.player)