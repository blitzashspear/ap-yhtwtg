from __future__ import annotations
from typing import TYPE_CHECKING
from BaseClasses import Region, Location

if TYPE_CHECKING:
    from .__init__ import WinTheGameWorld
from .data.location_ids import LOCATION_IDS

class WinTheGameLocation(Location):
    game = "You Have to Win the Game"

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_IDS[location_name] for location_name in location_names}

def create_regions_and_locations(world: WinTheGameWorld) -> None:
    #TODO add taking the long way left, right, and room.
    regions = []

    starting_hallway = Region("Starting Hallway", world.player, world.multiworld)
    starting_hallway.add_locations(get_location_names_with_ids([
        "You Have to Start the Game - Treasure",
        "KISS Principle - Treasure",
        "Treasure Hunt - Treasure",
        "Danger - Treasure"
    ]), WinTheGameLocation)
    regions.append(starting_hallway)

    main_hallway_left = Region("Main Hallway Left", world.player, world.multiworld)
    main_hallway_left.add_locations(get_location_names_with_ids([
        "Subterranea - Treasure",
        "Hops and Skips - Treasure",
        "Arcane Vocabulary - Bottom Treasure",
        "Covert Operators - Right Treasure",
        "Yggdrasil - Treasure",
        "Artisan Stone Walls - Treasure"
    ]), WinTheGameLocation)
    regions.append(main_hallway_left)

    hydras_corner = Region("Hydra's Corner", world.player, world.multiworld)
    hydras_corner.add_locations(get_location_names_with_ids([
        "Hydra Is Myth - Treasure",
        "Arcane Vocabulary - Top Treasure"
    ]), WinTheGameLocation)
    regions.append(hydras_corner)

    upstream = Region("Upstream", world.player, world.multiworld)
    upstream.add_locations(get_location_names_with_ids([
        "Swimming Upstream - Treasure",
        "Snake, It's a Snake - Treasure"
    ]), WinTheGameLocation)
    regions.append(upstream)

    quarry = Region("Quarry", world.player, world.multiworld)
    quarry.add_locations(get_location_names_with_ids([
        "Mind the Gap - Treasure",
        "Nice of You to Drop In - Treasure",
        "Cerulean Aura - Treasure",
        "Covert Operators - Left Treasure",
        "Pit Stop - Treasure",
        "Obvious Movie Quote - Treasure",
        "Cave In - Treasure",
        "Don't Be Hasty - Top Treasure"
    ]), WinTheGameLocation)
    regions.append(quarry)

    map_room = Region("Map Room", world.player, world.multiworld)
    map_room.add_locations(get_location_names_with_ids([
        "Maps and Legends - Treasure"
    ]), WinTheGameLocation)
    regions.append(map_room)

    ncsaow = Region("Never Could See Any Other Way", world.player, world.multiworld)
    ncsaow.add_locations(get_location_names_with_ids([
        "Never Could See Any Other Way - Treasure"
    ]), WinTheGameLocation)
    regions.append(ncsaow)

    ydsgl = Region("You Definitely Shouldn't Go Left", world.player, world.multiworld)
    regions.append(ydsgl)

    main_hallway_right = Region("Main Hallway Right", world.player, world.multiworld)
    main_hallway_right.add_locations(get_location_names_with_ids([
        "Bat Cave - Treasure",
        "The Proper Motivation - Treasure",
        "Remnants of a Past Unknown - Treasure",
        "Contrived Lock/Key Mechanisms - Treasure"
    ]), WinTheGameLocation)
    regions.append(main_hallway_right)

    shelter = Region("Shelter", world.player, world.multiworld)
    shelter.add_locations(get_location_names_with_ids([
        "Shelter from the Storm - Treasure"
    ]), WinTheGameLocation)
    regions.append(shelter)

    footholds = Region("Footholds", world.player, world.multiworld)
    footholds.add_locations(get_location_names_with_ids([
        "Precarious Footholds - Treasure",
        "Cognitive Resonance - Treasure"
    ]), WinTheGameLocation)
    regions.append(footholds)

    mushroom_stairs = Region("Mushroom Stairs", world.player, world.multiworld)
    regions.append(mushroom_stairs)

    castle_area_outer = Region("Castle Area Outer", world.player, world.multiworld)
    castle_area_outer.add_locations(get_location_names_with_ids([
        "Vestibule - Treasure",
        "Attic Storeroom - Bottom Treasure",
        "Great Hall - Treasure",
        "Spider Gloves - Treasure"
    ]), WinTheGameLocation)
    regions.append(castle_area_outer)

    brazen_machines = Region("Brazen Machines", world.player, world.multiworld)
    regions.append(brazen_machines)

    not_worth_it = Region("Not Worth It!", world.player, world.multiworld)
    not_worth_it.add_locations(get_location_names_with_ids([
        "Not Worth It! - Treasure"
    ]), WinTheGameLocation)
    regions.append(not_worth_it)

    castle_area_inner = Region("Castle Area Inner", world.player, world.multiworld)
    castle_area_inner.add_locations(get_location_names_with_ids([
        "Attic Storeroom - Top Treasure",
        "The Floor Is Lava - Treasure",
        "An Even 0x80 - Treasure"
    ]), WinTheGameLocation)
    regions.append(castle_area_inner)

    tower_of_sorrows = Region("Tower of Sorrows", world.player, world.multiworld)
    tower_of_sorrows.add_locations(get_location_names_with_ids([
        "Tower of Sorrows - Treasure"
    ]), WinTheGameLocation)
    regions.append(tower_of_sorrows)

    tower_of_regrets = Region("Tower of Regrets", world.player, world.multiworld)
    regions.append(tower_of_regrets)

    fiagl = Region("Falling Into a Greener Life", world.player, world.multiworld)
    fiagl.add_locations(get_location_names_with_ids([
        "Tower of Regrets - Treasure"
    ]), WinTheGameLocation)
    regions.append(fiagl)

    rawr = Region("Rawr!", world.player, world.multiworld)
    regions.append(rawr)

    underground = Region("Underground", world.player, world.multiworld)
    underground.add_locations(get_location_names_with_ids([
        "Don't Be Hasty - Bottom Treasure",
        "Secret Passage - Treasure",
        "The Crab Cake Is a Lie - Treasure",
        "Springheel Boots - Treasure"
    ]), WinTheGameLocation)
    regions.append(underground)

    twisting_path = Region("Twisting Path", world.player, world.multiworld)
    twisting_path.add_locations(get_location_names_with_ids([
        "Aqueous Humor - Treasure",
        "Like Ivy, Twisting - Treasure"
    ]), WinTheGameLocation)
    regions.append(twisting_path)

    magic_word_reveal = Region("Magic Word Reveal", world.player, world.multiworld)
    magic_word_reveal.add_locations(get_location_names_with_ids([
        "Avalon Calling - Treasure"
    ]), WinTheGameLocation)
    regions.append(magic_word_reveal)

    from_another_world = Region("From Another World", world.player, world.multiworld)
    regions.append(from_another_world)

    playing_with_fire = Region("Playing with Fire", world.player, world.multiworld)
    playing_with_fire.add_locations(get_location_names_with_ids([
        "Playing with Fire - Treasure"
    ]), WinTheGameLocation)
    regions.append(playing_with_fire)

    exit_strategy = Region("Exit Strategy", world.player, world.multiworld)
    regions.append(exit_strategy)

    end_game_area = Region("End Game Area", world.player, world.multiworld)
    end_game_area.add_locations(get_location_names_with_ids([
        "The Coin and the Courage - Treasure",
        "Hardcore Prawn - Treasure"
    ]), WinTheGameLocation)
    regions.append(end_game_area)

    password_puzzle = Region("Password Puzzle", world.player, world.multiworld)
    password_puzzle.add_locations(get_location_names_with_ids([
        "Consolation Prize - Treasure",
    ]), WinTheGameLocation)
    regions.append(password_puzzle)

    solved_puzzle = Region("Solved Puzzle", world.player, world.multiworld)
    solved_puzzle.add_locations(get_location_names_with_ids([
        "Eponymous - Win the Game"
    ]), WinTheGameLocation)
    regions.append(solved_puzzle)

    otco3 = Region("Above Mushrooms", world.player, world.multiworld)
    regions.append(otco3)

    leap_of_faith = Region("Leap of Faith", world.player, world.multiworld)
    leap_of_faith.add_locations(get_location_names_with_ids([
        "Leap of Faith - Treasure"
    ]), WinTheGameLocation)
    regions.append(leap_of_faith)

    natwwal = Region("Not All Those Who Wander Are Lost", world.player, world.multiworld)
    regions.append(natwwal)

    cat_level_entrance = Region("Cat Level Entrance", world.player, world.multiworld)
    regions.append(cat_level_entrance)

    secret_cat_level = Region("Secret Cat Level", world.player, world.multiworld)
    secret_cat_level.add_locations(get_location_names_with_ids([
        "Secret Cat Level - Left Treasure",
        "Secret Cat Level - Right Treasure"
    ]), WinTheGameLocation)
    regions.append(secret_cat_level)

    graveyard = Region("Graveyard", world.player, world.multiworld)
    graveyard.add_locations(get_location_names_with_ids([
        "Uncertain Semiotics - Treasure",
        "Crimson Aura - Treasure"
    ]), WinTheGameLocation)
    regions.append(graveyard)

    sea_cave = Region("Sea Cave", world.player, world.multiworld)
    sea_cave.add_locations(get_location_names_with_ids([
        "Prawn Shot First - Treasure",
        "Circular Logic - Treasure"
    ]), WinTheGameLocation)
    regions.append(sea_cave)

    euclid_shrugged = Region("Euclid Shrugged", world.player, world.multiworld)
    euclid_shrugged.add_locations(get_location_names_with_ids([
        "Euclid Shrugged - Treasure"
    ]), WinTheGameLocation)
    regions.append(euclid_shrugged)

    alcove_entry = Region("Alcove Entry", world.player, world.multiworld)
    regions.append(alcove_entry)

    abandoned_alcove = Region("Abandoned Alcove", world.player, world.multiworld)
    abandoned_alcove.add_locations(get_location_names_with_ids([
        "Abandoned Alcove - Treasure"
    ]), WinTheGameLocation)
    regions.append(abandoned_alcove)

    back_to_the_surface = Region("Back to the Surface", world.player, world.multiworld)
    regions.append(back_to_the_surface)

    mineshaft = Region("Mineshaft", world.player, world.multiworld)
    mineshaft.add_locations(get_location_names_with_ids([
        "Forgotten Tunnels - Left Treasure",
        "Forgotten Tunnels - Right Treasure",
        "Descent - Treasure",
        "The Arbitrarium - Treasure",
        "Hidden Crevasse - Treasure"
    ]), WinTheGameLocation)
    regions.append(mineshaft)

    ttlw_left = Region("Taking the Long Way (Left)", world.player, world.multiworld)
    ttlw_left.add_locations(get_location_names_with_ids([
        "Taking the Long Way - Left Treasure"
    ]), WinTheGameLocation)
    regions.append(ttlw_left)

    ttlw_right = Region("Taking the Long Way (Right)", world.player, world.multiworld)
    ttlw_right.add_locations(get_location_names_with_ids([
        "Taking the Long Way - Right Treasure"
    ]), WinTheGameLocation)
    regions.append(ttlw_right)

    if world.options.room_sanity:
        starting_hallway.add_locations(get_location_names_with_ids([
            "You Have to Start the Game - Room Entry", 
            "KISS Principle - Room Entry", 
            "Snake, It's a Snake - Room Entry", 
            "Treasure Hunt - Room Entry",
            "Danger - Room Entry",
            "Harbinger - Room Entry"
        ]), WinTheGameLocation)

        main_hallway_left.add_locations(get_location_names_with_ids([
            "Abstract Bridge - Room Entry",
            "Which Path Will I Take? - Room Entry",
            "Subterranea - Room Entry",
            "Pit of Spikes - Room Entry",
            "Leaps and Bounds - Room Entry",
            "Hops and Skips - Room Entry",
            "Venn's Banality - Room Entry",
            "Arcane Vocabulary - Room Entry",
            "Cave In - Room Entry",
            "Crawlspace - Room Entry",
            "The Quarry Hub - Room Entry",
            "Covert Operators - Room Entry",
            "The Grand Vault - Room Entry",
            "Yggdrasil - Room Entry",
            "Artisan Stone Walls - Room Entry"
        ]), WinTheGameLocation)

        hydras_corner.add_locations(get_location_names_with_ids([
            "Hydra Is Myth - Room Entry"
        ]), WinTheGameLocation)

        upstream.add_locations(get_location_names_with_ids([
            "Swimming Upstream - Room Entry"
        ]), WinTheGameLocation)

        quarry.add_locations(get_location_names_with_ids([
            "I Wonder Where This Goes - Room Entry",
            "Mind the Gap - Room Entry",
            "Foot of the Throne - Room Entry",
            "Hollow King - Room Entry",
            "Slippery Slope - Room Entry",
            "Nice of You to Drop In - Room Entry",
            "Cerulean Aura - Room Entry",
            "Pit Stop - Room Entry",
            "Obvious Movie Quote - Room Entry",
            "Don't Be Hasty - Room Entry"
        ]), WinTheGameLocation)

        map_room.add_locations(get_location_names_with_ids([
            "Maps and Legends - Room Entry"
        ]), WinTheGameLocation)

        ncsaow.add_locations(get_location_names_with_ids([
            "Never Could See Any Other Way - Room Entry",
        ]), WinTheGameLocation)

        ydsgl.add_locations(get_location_names_with_ids([
            "You Definitely Shouldn't Go Left - Room Entry",
        ]), WinTheGameLocation)
                    
        main_hallway_right.add_locations(get_location_names_with_ids([
            "Cognitive Resonance - Room Entry",
            "Functional Spelæology - Room Entry",
            "Bat Cave - Room Entry",
            "Fungal Forest - Room Entry",
            "The Proper Motivation - Room Entry",
            "Remnants of a Past Unknown - Room Entry",
            "Ghosts - Room Entry",
            "The Loneliest Corner - Room Entry",
            "Contrived Lock/Key Mechanisms - Room Entry"
        ]), WinTheGameLocation)

        shelter.add_locations(get_location_names_with_ids([
            "Cave Painting - Room Entry",
            "Shelter from the Storm - Room Entry",
            "Under Construction - Room Entry",
            "Transplants - Room Entry"
        ]), WinTheGameLocation)
                    
        footholds.add_locations(get_location_names_with_ids([
            "Precarious Footholds - Room Entry",
        ]), WinTheGameLocation)

        mushroom_stairs.add_locations(get_location_names_with_ids([
            "Mushroom Staircase - Room Entry",
            "Stick the Landing - Room Entry",
            "Eden Maw - Room Entry",
            "Does Whatever A Spider Does - Room Entry"
        ]), WinTheGameLocation)

        castle_area_outer.add_locations(get_location_names_with_ids([
            "Vestibule - Room Entry",
            "Attic Storeroom - Room Entry",
            "Great Hall - Room Entry",
            "Hollow King Transformed - Room Entry",
            "Spider Gloves - Room Entry",
            "Worth It? - Room Entry"
        ]), WinTheGameLocation)   

        brazen_machines.add_locations(get_location_names_with_ids([
            "Brazen Machines - Room Entry"
        ]), WinTheGameLocation)    

        not_worth_it.add_locations(get_location_names_with_ids([
            "Not Worth It! - Room Entry"
        ]), WinTheGameLocation)

        castle_area_inner.add_locations(get_location_names_with_ids([
            "The Floor Is Lava - Room Entry",
            "An Even 0x80 - Room Entry",
            "Clarity Comes in Waves - Room Entry"
        ]), WinTheGameLocation)

        tower_of_sorrows.add_locations(get_location_names_with_ids([
            "Tower of Sorrows - Room Entry"
        ]), WinTheGameLocation)
        
        tower_of_regrets.add_locations(get_location_names_with_ids([
            "Tower of Regrets - Room Entry"
        ]), WinTheGameLocation)

        fiagl.add_locations(get_location_names_with_ids([
            "Falling Into a Greener Life - Room Entry"
        ]), WinTheGameLocation)

        rawr.add_locations(get_location_names_with_ids([
            "Rawr! - Room Entry"
        ]), WinTheGameLocation)

        underground.add_locations(get_location_names_with_ids([
            "A Memory of a Dream - Room Entry",
            "A Dream of a Memory - Room Entry",
            "Like Ivy, Twisting - Room Entry",
            "Welcome to the Underground - Room Entry",
            "Rock Transept - Room Entry",
            "Aqueous Humor - Room Entry",
            "Long Way Down - Room Entry",
            "Secret Passage - Room Entry",
            "The Crab Cake Is a Lie - Room Entry",
            "Be Seeing You - Room Entry",
            "Hidden Crevasse - Room Entry",
            "It's More Scared of You - Room Entry",
            "Mine Shaft - Room Entry",
            "Green Man - Room Entry",
            "Springheel Boots - Room Entry"
        ]), WinTheGameLocation)

        magic_word_reveal.add_locations(get_location_names_with_ids([
            "Avalon Calling - Room Entry",
            "Et in Aether ego - Room Entry"
        ]), WinTheGameLocation)

        from_another_world.add_locations(get_location_names_with_ids([
            "From Another World - Room Entry"
        ]), WinTheGameLocation)

        playing_with_fire.add_locations(get_location_names_with_ids([
            "Playing with Fire - Room Entry"
        ]), WinTheGameLocation)

        exit_strategy.add_locations(get_location_names_with_ids([
            "Exit Strategy - Room Entry"
        ]), WinTheGameLocation)

        end_game_area.add_locations(get_location_names_with_ids([
            "Hardcore Prawn - Room Entry",
            "A Brief Respite - Room Entry",
            "Before the Crash - Room Entry",
            "Hold On Tight and Don't Look Down - Room Entry",
            "The Coin and the Courage - Room Entry",
            "A Sickly Silver Moon - Room Entry",
            "This Is Where We Used to Live - Room Entry",
            "Catharsis in Catastrophe - Room Entry",
            "Linchpin - Room Entry",
            "Point of No Return - Room Entry"
        ]), WinTheGameLocation)

        password_puzzle.add_locations(get_location_names_with_ids([
            "Speak Now... - Room Entry",
            "Consolation Prize - Room Entry",
            "Warp Left - Room Entry",
            "Warp Middle - Room Entry",
            "Warp Right - Room Entry"
        ]), WinTheGameLocation)

        solved_puzzle.add_locations(get_location_names_with_ids([
            "Open Sesame - Room Entry",
            "Eponymous - Room Entry"
        ]), WinTheGameLocation)

        otco3.add_locations(get_location_names_with_ids([
            "On the Count of Three - Room Entry",
        ]), WinTheGameLocation)

        leap_of_faith.add_locations(get_location_names_with_ids([
            "Leap of Faith - Room Entry",
        ]), WinTheGameLocation)

        natwwal.add_locations(get_location_names_with_ids([
            "Not All Those Who Wander Are Lost - Room Entry",
        ]), WinTheGameLocation)

        cat_level_entrance.add_locations(get_location_names_with_ids([
            "Rough Landing - Room Entry",
            "Feline Foreshadowing - Room Entry"
        ]), WinTheGameLocation)

        secret_cat_level.add_locations(get_location_names_with_ids([
            "Secret Cat Level - Room Entry",
        ]), WinTheGameLocation)

        graveyard.add_locations(get_location_names_with_ids([
            "Castle Rock - Room Entry",
            "Uncertain Semiotics - Room Entry",
            "Observation Deck - Room Entry",
            "Fish Out of Water - Room Entry",
            "Don't Get Snippy With Me - Room Entry",
            "Bring a Mallet - Room Entry",
            "Dire Crab - Room Entry",
            "Crimson Aura - Room Entry"
        ]), WinTheGameLocation)

        euclid_shrugged.add_locations(get_location_names_with_ids([
            "Euclid Shrugged - Room Entry",
        ]), WinTheGameLocation)

        sea_cave.add_locations(get_location_names_with_ids([
            "Prawn Shot First - Room Entry",
            "Circular Logic - Room Entry"
        ]), WinTheGameLocation)

        alcove_entry.add_locations(get_location_names_with_ids([
            "Wellspring - Room Entry",
            "yeah but why u jelly tho - Room Entry"
        ]), WinTheGameLocation)

        abandoned_alcove.add_locations(get_location_names_with_ids([
            "Abandoned Alcove - Room Entry"
        ]), WinTheGameLocation)

        back_to_the_surface.add_locations(get_location_names_with_ids([
            "Back to the Surface - Room Entry"
        ]), WinTheGameLocation)

        mineshaft.add_locations(get_location_names_with_ids([
            "Forgotten Tunnels - Room Entry",
            "Descent - Room Entry",
            "The Arbitrarium - Room Entry"
        ]), WinTheGameLocation)

        ttlw_left.add_locations(get_location_names_with_ids([
            "Taking the Long Way - Room Entry"
        ]), WinTheGameLocation)

    world.multiworld.regions += regions

    starting_hallway.connect(main_hallway_left, "Starting Hallway to Main Left Hallway")
    main_hallway_left.connect(hydras_corner, "Main Hallway Left to Hydra's Corner")
    main_hallway_left.connect(quarry, "Main Hallway Left to Quarry")
    main_hallway_left.connect(upstream, "Main Hallway Left to Upstream")
    quarry.connect(map_room, "Quarry to Map Room")
    quarry.connect(ncsaow, "Quarry to Never Could See Any Other Way")
    main_hallway_left.connect(main_hallway_right, "Main Hallway Left to Main Hallway Right")
    main_hallway_right.connect(shelter, "Main Hallway Right to Shelter")
    shelter.connect(footholds, "Shelter to Footholds")
    footholds.connect(mushroom_stairs, "Footholds to Mushroom Stairs")
    mushroom_stairs.connect(castle_area_outer, "Mushroom Stairs to Castle Area Outer")
    castle_area_outer.connect(brazen_machines, "Castle Area Outer to Brazen Machines")
    brazen_machines.connect(castle_area_inner, "Brazen Machines to Castle Area Inner")
    castle_area_outer.connect(not_worth_it, "Castle Area Outer to Not Worth It!")
    ncsaow.connect(tower_of_sorrows, "Quarry Exit to Tower of Sorrows")
    ncsaow.connect(ydsgl, "Never Could See Any Other Way to You Definitely Shouldn't Go Left")
    main_hallway_right.connect(tower_of_sorrows, "Main Hallway Right to Tower of Sorrows")
    tower_of_sorrows.connect(ncsaow, "Tower of Sorrows to Never Could See Any Other Way")
    tower_of_sorrows.connect(ydsgl, "Tower of Sorrows to You Definitely Shouldn't Go Left")
    tower_of_sorrows.connect(main_hallway_right, "Tower of Sorrows to Main Hallway Right")
    tower_of_sorrows.connect(tower_of_regrets, "Tower of Sorrows to Tower of Regrets")
    tower_of_regrets.connect(fiagl, "Tower of Regrets to Falling Into a Greener Life")
    tower_of_regrets.connect(rawr, "Tower of Regrets to Rawr!")
    rawr.connect(underground, "Rawr! to Underground")
    underground.connect(twisting_path, "Underground to Twisting Path")
    underground.connect(magic_word_reveal, "Underground to Magic Word Reveal")
    starting_hallway.connect(from_another_world, "Starting Hallway to From Another World")
    from_another_world.connect(playing_with_fire, "From Another World to Playing with Fire")
    playing_with_fire.connect(exit_strategy, "Playing with Fire to Exit Strategy")
    exit_strategy.connect(end_game_area, "Exit Strategy to End Game Area")
    end_game_area.connect(password_puzzle, "End Game Area to Password Puzzle")
    password_puzzle.connect(solved_puzzle, "Password Puzzle to Solved Puzzle")
    mushroom_stairs.connect(otco3, "Mushroom Stairs to On the Count of Three")
    otco3.connect(leap_of_faith, "On the Count of Three to Leap of Faith")
    main_hallway_left.connect(natwwal, "Main Hallway Left to Not All Those Who Wander Are Lost")
    natwwal.connect(leap_of_faith, "Not All Those Who Wander Are Lost to Leap of Faith")
    leap_of_faith.connect(cat_level_entrance, "Leap of Faith to Cat Level Entrance")
    cat_level_entrance.connect(secret_cat_level, "Cat Level Entrance to Secret Cat Level")
    main_hallway_right.connect(graveyard, "Main Hallway Right to Graveyard")
    graveyard.connect(sea_cave, "Graveyard to Sea Cave")
    sea_cave.connect(euclid_shrugged, "Sea Cave to Euclid Shrugged")
    graveyard.connect(alcove_entry, "Graveyard to Alcove Entry")
    alcove_entry.connect(abandoned_alcove, "Alcove Entry to Abandoned Alcove")
    underground.connect(back_to_the_surface, "Underground to Back to the Surface")
    underground.connect(mineshaft, "Underground to Mineshaft")
    starting_hallway.connect(ttlw_left, "Starting Hallway to Taking the Long Way (Left)")
    natwwal.connect(ttlw_right, "Not All Those Who Wander Are Lost to Taking the Long Way (Right)")

    # Connections only with harder difficulty
    if world.options.logic_difficulty > 0: # Harder than normal
        main_hallway_right.connect(footholds, "Main Hallway Right to Footholds", lambda state: state.has("Springheel Boots", world.player) and state.has_any(("Left Spider Glove", "Spider Gloves"), world.player))

        if world.options.logic_difficulty > 1: # Harder than hard
            # The Speedrun Strat
            starting_hallway.connect(exit_strategy, "You Have to Start the Game to Exit Strategy", lambda state: state.has("Springheel Boots", world.player) and state.has_any(("Right Spider Glove", "Spider Gloves"), world.player))

            #TODO add ool connection with springheel and left glove. its possible but it is some hot garbage. i refuse to put it in logic unless i add a difficulty past extreme (2).
            castle_area_outer.connect(castle_area_inner, "Castle Area Outer to Castle Area Inner", lambda state: state.has("Springheel Boots", world.player) and state.has_any(("Spider Gloves", "Right Spider Glove"), world.player))