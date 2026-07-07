from __future__ import annotations
from typing import TYPE_CHECKING
from worlds.generic.Rules import set_rule, add_rule, CollectionState

if TYPE_CHECKING:
    from .__init__ import WinTheGameWorld

def set_all_rules(world: WinTheGameWorld) -> None:
    #TODO make region for stick the landing, as mushroom stairs and not all those who wander connect to it trivially.
    def needs_item(state: CollectionState, item: str):
        return state.has(item, world.player)
    def needs_glove(state: CollectionState, dir: str):
        return state.has_any(("Spider Gloves", f"{dir} Spider Glove"), world.player)
    def needs_either_glove(state: CollectionState):
        return state.has_any(("Spider Gloves", "Left Spider Glove", "Right Spider Glove"), world.player)
    def needs_both_gloves(state: CollectionState):
        return state.has("Spider Gloves", world.player) or state.has_all(("Left Spider Glove", "Right Spider Glove"), world.player)
    def right_or_jump_and_left(state: CollectionState):
        return needs_glove(state, "Right") or state.has_all(("Springheel Boots", "Left Spider Glove"), world.player)
    # REGION / ROOM RULES
    set_rule(world.get_entrance("Main Hallway Left to Hydra's Corner"), lambda state: needs_glove(state, "Right"))
    set_rule(world.get_entrance("Main Hallway Left to Upstream"), lambda state: needs_either_glove(state))
    set_rule(world.get_entrance("Quarry to Map Room"), lambda state: needs_item(state, "Springheel Boots") and needs_glove(state, "Right"))
    set_rule(world.get_entrance("Quarry to Never Could See Any Other Way"), lambda state: needs_item(state, "Cerulean Aura"))
    set_rule(world.get_entrance("Main Hallway Right to Shelter"), lambda state: state.has_any(("Crimson Aura", "Springheel Boots"), world.player))
    set_rule(world.get_entrance("Shelter to Footholds"), lambda state: needs_item(state, "Cerulean Aura"))
    set_rule(world.get_entrance("Footholds to Mushroom Stairs"), lambda state: needs_item(state, "Springheel Boots"))
    set_rule(world.get_entrance("Castle Area Outer to Brazen Machines"), lambda state: needs_glove(state, "Right"))
    set_rule(world.get_entrance("Brazen Machines to The Floor Is Lava"), lambda state: needs_glove(state, "Left"))
    set_rule(world.get_entrance("Castle Area Outer to Not Worth It!"), lambda state: needs_item(state, "Cerulean Aura"))
    set_rule(world.get_entrance("Main Hallway Right to Tower of Sorrows"), lambda state: state.has_any(("Cerulean Aura", "Springheel Boots", "Spider Gloves", "Left Spider Glove"), world.player))   
    set_rule(world.get_entrance("Tower of Sorrows to You Definitely Shouldn't Go Left"), lambda state: state.has_any(("Cerulean Aura", "Springheel Boots", "Spider Gloves", "Left Spider Glove"), world.player))
    set_rule(world.get_entrance("Tower of Sorrows to Main Hallway Right"), lambda state: state.has_any(("Cerulean Aura", "Springheel Boots", "Spider Gloves", "Right Spider Glove"), world.player))
    set_rule(world.get_entrance("Tower of Sorrows to Tower of Regrets"), lambda state: state.has_any(("Crimson Aura", "Springheel Boots", "Spider Gloves", "Left Spider Glove", "Right Spider Glove"), world.player))
    set_rule(world.get_entrance("Tower of Regrets to Falling Into a Greener Life"), lambda state: state.has_any(("Crimson Aura", "Springheel Boots", "Spider Gloves", "Right Spider Glove"), world.player))
    set_rule(world.get_entrance("Tower of Regrets to Rawr!"), lambda state: state.has_any(("Crimson Aura", "Springheel Boots", "Spider Gloves", "Left Spider Glove"), world.player))
    set_rule(world.get_entrance("Underground to Twisting Path"), lambda state: needs_item(state, "Springheel Boots"))
    set_rule(world.get_entrance("Underground to Magic Word Reveal"), lambda state: right_or_jump_and_left(state))
    set_rule(world.get_entrance("Starting Hallway to From Another World"), lambda state: state.has_any(("Crimson Aura", "Spider Gloves", "Left Spider Glove"), world.player) or state.has_all(("Springheel Boots", "Right Spider Glove"), world.player))
    set_rule(world.get_entrance("From Another World to Playing with Fire"), lambda state: state.has_any(("Springheel Boots", "Spider Gloves", "Left Spider Glove"), world.player))
    set_rule(world.get_entrance("Playing with Fire to Exit Strategy"), lambda state: needs_item(state, "Springheel Boots") and needs_glove(state, "Left"))
    set_rule(world.get_entrance("Exit Strategy to End Game Area"), lambda state: needs_item(state, "Springheel Boots") and needs_both_gloves(state))
    set_rule(world.get_entrance("Password Puzzle to Solved Puzzle"), lambda state: state.has_all(("Letter E", "Letter P", "Letter R", "Letter S", "Letter U"), world.player))
    set_rule(world.get_entrance("Mushroom Stairs to On the Count of Three"), lambda state: needs_glove(state, "Right"))
    set_rule(world.get_entrance("Main Hallway Left to Not All Those Who Wander Are Lost"), lambda state: needs_item(state, "Springheel Boots") and needs_glove(state, "Right"))
    set_rule(world.get_entrance("Not All Those Who Wander Are Lost to Leap of Faith"), lambda state: needs_glove(state, "Left"))
    set_rule(world.get_entrance("Cat Level Entrance to Secret Cat Level"), lambda state: needs_both_gloves(state))
    set_rule(world.get_entrance("Graveyard to Sea Cave"), lambda state: needs_item(state, "Crimson Aura"))
    set_rule(world.get_entrance("Sea Cave to Euclid Shrugged"), lambda state: needs_item(state, "Cerulean Aura"))
    set_rule(world.get_entrance("Graveyard to Alcove Entry"), lambda state: needs_glove(state, "Left"))
    set_rule(world.get_entrance("Alcove Entry to Abandoned Alcove"), lambda state: needs_item(state, "Springheel Boots") and needs_glove(state, "Right"))
    set_rule(world.get_entrance("Underground to Back to the Surface"), lambda state: needs_item(state, "Springheel Boots") or needs_glove(state, "Right"))
    set_rule(world.get_entrance("Starting Hallway to Taking the Long Way (Left)"), lambda state: needs_glove(state, "Right") or (needs_item(state, "Springheel Boots") and state.has_any(("Crimson Aura", "Left Spider Glove"), world.player)))
    set_rule(world.get_entrance("Not All Those Who Wander Are Lost to Taking the Long Way (Right)"), lambda state: needs_glove(state, "Left"))

    if world.options.logic_difficulty > 0: # Harder than normal
        add_rule(world.get_entrance("Underground to Twisting Path"), lambda state: needs_glove(state, "Right"), "or")
        add_rule(world.get_entrance("Underground to Back to the Surface"), lambda state: state.has("Left Spider Glove", world.player), "or")
        add_rule(world.get_entrance("Main Hallway Left to Not All Those Who Wander Are Lost"), lambda state: state.has_all(("Cerulean Aura", "Crimson Aura"), world.player) and needs_glove(state, "Right"), "or")
        if world.options.logic_difficulty > 1: # Harder than hard
            add_rule(world.get_entrance("Graveyard to Alcove Entry"), lambda state: state.has_all(("Springheel Boots", "Right Spider Glove"), world.player), "or")

    if world.options.require_unlock_teleporters:
        set_rule(world.get_entrance("Rawr! to Underground"), lambda state: state.has("Unlock Teleporters", world.player))
        set_rule(world.get_entrance("End Game Area to Password Puzzle"), lambda state: state.has("Unlock Teleporters", world.player))
        set_rule(world.get_entrance("Leap of Faith to Cat Level Entrance"), lambda state: state.has("Unlock Teleporters", world.player))

    if world.options.include_extra_roadblocks:
        set_rule(world.get_entrance("Main Hallway Left to Quarry"), lambda state: state.has("Unlock Quarry", world.player))
        set_rule(world.get_entrance("Mushroom Stairs to Castle Area Outer"), lambda state: state.has("Unlock Castle", world.player))
        set_rule(world.get_entrance("Main Hallway Right to Graveyard"), lambda state: state.has("Unlock Graveyard", world.player))
        set_rule(world.get_entrance("Underground to Mineshaft"), lambda state: state.has("Unlock Mineshaft", world.player))

    # if world.options.password_randomization: # Technically not required but will be required logically.
    #     add_rule(world.get_entrance("Password Puzzle to Solved Puzzle"), lambda state: state.has_all(("Magic Word", "Magic Symbol"), world.player), "or")

    # TREASURE RULES
    set_rule(world.get_location("Arcane Vocabulary - Top Treasure"), lambda state: needs_item(state, "Springheel Boots"))
    set_rule(world.get_location("Artisan Stone Walls - Treasure"), lambda state: needs_item(state, "Cerulean Aura"))
    set_rule(world.get_location("Avalon Calling - Treasure"), lambda state: right_or_jump_and_left(state))
    set_rule(world.get_location("Bat Cave - Treasure"), lambda state: needs_item(state, "Springheel Boots") or needs_glove(state, "Left"))
    set_rule(world.get_location("Contrived Lock/Key Mechanisms - Treasure"), lambda state: state.has_any(("Cerulean Aura", "Springheel Boots", "Spider Gloves", "Left Spider Glove"), world.player))
    set_rule(world.get_location("Don't Be Hasty - Top Treasure"), lambda state: needs_glove(state, "Right"))
    set_rule(world.get_location("Forgotten Tunnels - Left Treasure"), lambda state: needs_item(state, "Springheel Boots") or needs_glove(state, "Left"))
    set_rule(world.get_location("Hidden Crevasse - Treasure"), lambda state: needs_glove(state, "Left") or state.has_all(("Springheel Boots", "Right Spider Glove"), world.player))
    if world.options.logic_difficulty < 2: # Normal or Hard
        set_rule(world.get_location("Hops and Skips - Treasure"), lambda state: needs_item(state, "Springheel Boots"))
    set_rule(world.get_location("Hydra Is Myth - Treasure"), lambda state: needs_item(state, "Springheel Boots"))
    set_rule(world.get_location("KISS Principle - Treasure"), lambda state: needs_either_glove(state))
    set_rule(world.get_location("Mind the Gap - Treasure"), lambda state: needs_item(state, "Crimson Aura"))
    set_rule(world.get_location("Pit Stop - Treasure"), lambda state: needs_item(state, "Springheel Boots"))
    set_rule(world.get_location("Playing with Fire - Treasure"), lambda state: needs_item(state, "Springheel Boots") and needs_either_glove(state))
    set_rule(world.get_location("Prawn Shot First - Treasure"), lambda state: needs_item(state, "Springheel Boots") or needs_glove(state, "Right"))
    if world.options.logic_difficulty > 0: #Harder than normal
        add_rule(world.get_location("Prawn Shot First - Treasure"), lambda state: state.has("Left Spider Glove", world.player), "or")
    if world.options.logic_difficulty == 0: #Only normal.
        set_rule(world.get_location("Remnants of a Past Unknown - Treasure"), lambda state: state.has_any(("Crimson Aura", "Springheel Boots"), world.player))
    set_rule(world.get_location("Secret Passage - Treasure"), lambda state: needs_item(state, "Springheel Boots") or needs_glove(state, "Right"))
    set_rule(world.get_location("Shelter from the Storm - Treasure"), lambda state: state.has_any(("Cerulean Aura", "Springheel Boots"), world.player))
    set_rule(world.get_location("Snake, It's a Snake - Treasure"), lambda state: right_or_jump_and_left(state))
    set_rule(world.get_location("Swimming Upstream - Treasure"), lambda state: right_or_jump_and_left(state))
    set_rule(world.get_location("Taking the Long Way - Left Treasure"), lambda state: needs_glove(state, "Right") or (needs_item(state, "Springheel Boots") and (needs_glove(state, "Left") or needs_item(state, "Crimson Aura"))))
    set_rule(world.get_location("The Arbitrarium - Treasure"), lambda state: right_or_jump_and_left(state))
    set_rule(world.get_location("Tower of Sorrows - Treasure"), lambda state: state.has_any(("Cerulean Aura", "Springheel Boots", "Spider Gloves", "Right Spider Glove"), world.player))
    set_rule(world.get_location("Tower of Regrets - Treasure"), lambda state: needs_either_glove(state) or state.can_reach_region("Euclid Shrugged", world.player))
    set_rule(world.get_location("Uncertain Semiotics - Treasure"), lambda state: needs_item(state, "Springheel Boots"))
    set_rule(world.get_location("You Have to Start the Game - Treasure"), lambda state: needs_item(state, "Springheel Boots") and needs_glove(state, "Left"))

    # BELL RULES
    if world.options.bell_sanity:
        set_rule(world.get_location("Forgotten Tunnels - Bottom Bell"), lambda state: state.can_reach_location("Forgotten Tunnels - Left Treasure", world.player))
        set_rule(world.get_location("Hops and Skips - Bottom Bell"), lambda state: state.can_reach_location("Hops and Skips - Treasure", world.player))
        set_rule(world.get_location("Tower of Sorrows - Left Bell"), lambda state: state.can_reach_region("You Definitely Shouldn't Go Left", world.player))
        set_rule(world.get_location("Tower of Sorrows - Right Bell"), lambda state: state.can_reach_location("Contrived Lock/Key Mechanisms - Treasure", world.player))
        set_rule(world.get_location("You Definitely Shouldn't Go Left - Top Bell"), lambda state: state.can_reach_region("Never Could See Any Other Way", world.player))

    # UT doesn't understand go mode. And according to the discord I don't think it ever will because I use an item for goaling.
    # Also please for the love of god do not capitalize the "the" I fucked that up TWICE now.
    world.multiworld.completion_condition[world.player] = lambda state: needs_item(state, "Win the Game")
