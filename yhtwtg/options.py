from dataclasses import dataclass
from Options import PerGameCommonOptions, Range, Toggle, DeathLink, Choice, OptionGroup, OptionSet

class RoomSanity(Toggle):
    """
    Make each room a location.
    """
    display_name = "Roomsanity"
    default = False

class BellSanity(Toggle):
    """
    Make each checkpoint bell a location.
    """
    display_name = "Bellsanity"
    default = False

class DeathLinkAmnesty(Range):
    """
    Amount of deaths before sending a DeathLink.
    """
    display_name = "DeathLink Amnesty"
    default = 25
    range_start = 1
    range_end = 100

class DeathLinkBehavior(Choice):
    """
    What will happen when recieving a DeathLink.
    Die just kills you.
    Reset warps you to the starting room.
    """
    display_name = "DeathLink Behavior"
    default = 0
    option_die = 0
    option_reset = 1

class TrapPercentage(Range):
    """
    Determines the percentage of traps that replace "Nothing" items.
    """
    display_name = "Trap Percentage"
    default = 0
    range_start = 0
    range_end = 100

class LoseTheGameWeight(Range):
    """
    This trap will teleport you to the starting room.
    A higher number means that you are more likely to see the given trap. A value of 0 means the trap will not appear.
    """
    display_name = "Shuffle Lose The Game Traps"
    default = 50
    range_start = 0
    range_end = 100

class StopJumpingTrapWeight(Range):
    """
    This trap will remove your ability to jump for a short time.
    A higher number means that you are more likely to see the given trap. A value of 0 means the trap will not appear.
    """
    display_name = "Shuffle Stop Jumping Traps"
    default = 50
    range_start = 0
    range_end = 100

class StopJumpingTrapLength(Range):
    """
    Adjust how long each Stop Jumping Trap lasts in seconds.
    """
    display_name = "Stop Jumping Trap Length"
    default = 5
    range_start = 1
    range_end = 10

class SecretRoomsTrapWeight(Range):
    """
    This trap will teleport you to the secret rooms included in the game. Either escape the rooms or die trying.
    A higher number means that you are more likely to see the given trap. A value of 0 means the trap will not appear.
    """
    display_name = "Shuffle Secret Rooms Traps"
    default = 50
    range_start = 0
    range_end = 100

class FreezeTrapWeight(Range):
    """
    This trap will freeze the game for a short time.
    A higher number means that you are more likely to see the given trap. A value of 0 means the trap will not appear.
    """
    display_name = "Shuffle Freeze Traps"
    default = 50
    range_start = 0
    range_end = 100

class FreezeTrapLength(Range):
    """
    Adjust how long each Freeze Trap lasts in seconds.
    """
    display_name = "Freeze Trap Length"
    default = 2
    range_start = 1
    range_end = 10

class FastTrapWeight(Range):
    """
    This trap will quadruple the game speed for a short time.
    A higher number means that you are more likely to see the given trap. A value of 0 means the trap will not appear.
    """
    display_name = "Shuffle Fast Traps"
    default = 50
    range_start = 0
    range_end = 100

class FastTrapLength(Range):
    """
    Adjust how long each Fast Trap lasts in seconds.
    """
    display_name = "Fast Trap Length"
    default = 8
    range_start = 1
    range_end = 10

class SplitSpiderGloves(Toggle):
    """
    Split the Spider Gloves into left and right items.
    """
    display_name = "Split Spider Gloves"
    default = False

class RequireUnlockTeleporters(Toggle):
    """
    Some teleporters take you to new areas. Enable this option to require an "Unlock Teleporters" item to access them.
    """
    display_name = "Require Unlock Teleporters"
    default = False
    
class LogicDifficullty(Choice):
    """
    Will place locations with harder jumps in logic. These include non-obvious movement, pixel perfect jumps, coyote jumping or all at once.
    """
    display_name = "Logic Difficulty"
    option_normal = 0
    option_hard = 1
    option_extreme = 2
    default = 0

class IncludeExtraRoadblocks(OptionSet):
    """
    Include up to 4 more roadblocks that require items to access.
    Quarry (Cerulean Aura Area)
    Mineshaft (Area Left of Springheel Boots)
    Castle (Spider Glove Area)
    Graveyard (Crimson Aura Area)
    """
    display_name = "Include Extra Roadblocks"
    default = []
    valid_keys = {"Quarry", "Mineshaft", "Castle", "Graveyard"}

class PasswordRandomization(Choice):
    """
    Randomize the password at the end of the game. This shuffles 2 new items: "Reveal Magic Word" and "Reveal Magic Symbol".
    These items will be logically required to beat the game, but won't actually do anything to block you.

    Off keeps the default password.
    Words chooses a password from a preset list.
    Any chooses a random jumble of 5 unique letters.
    """
    display_name = "Password Randomization"
    default = 0
    option_off = 0
    option_words = 1
    option_any = 2

class LocalNothingPercentage(Range):
    """
    Percentage of "Nothing" items that are placed locally. 
    """
    display_name = "Local Nothing Percentage"
    default = 50
    range_start = 0
    range_end = 90

class ShuffleCatDLC(Toggle):
    """
    Shuffles an item in the pool that turns the player into a cat for 9 lives.
    These lives do not count towards DeathLink and you are protected from its effects.
    """
    display_name = "Shuffle Cat DLC"
    default = True

# Tested with fuzzer n=2, this option breaks generation due to there being too many progression items to place in the multiworld.
# class HideLetterClassification(Toggle):
#     """
#     If turned on, all letters shuffled into the pool will be labelled progression.
#     """
#     display_name = "Hide Letter Classification"
#     default = False

class ResetTimer(Range):
    """
    While connected to the client, crouching for a set amount of time will warp you to the start (barring certain conditions)
    The value you give will be divided by 10. For example 50 becomes 5 seconds.
    """
    display_name = "Warp to Start Time"
    default = 50
    range_start = 10
    range_end = 100

class DisplayPasswordLetters(Toggle):
    """
    Enables the password display in the client.
    """
    display_name = "Display Password Letters"
    default = True

option_groups = [
    OptionGroup("Extra Locations", [RoomSanity, BellSanity]),
    OptionGroup("DeathLink", [DeathLink, DeathLinkAmnesty, DeathLinkBehavior]),
    OptionGroup("Traps", [TrapPercentage, LoseTheGameWeight, StopJumpingTrapWeight, StopJumpingTrapLength, SecretRoomsTrapWeight, FreezeTrapWeight, FreezeTrapLength, FastTrapWeight,FastTrapLength]),
    OptionGroup("Randomizer Changes", [SplitSpiderGloves, RequireUnlockTeleporters, LogicDifficullty, IncludeExtraRoadblocks, PasswordRandomization]),
    OptionGroup("Filler Options", [LocalNothingPercentage, ShuffleCatDLC]),
    OptionGroup("QOL", [ResetTimer, DisplayPasswordLetters])
]

@dataclass
class WinTheGameOptions(PerGameCommonOptions):
    room_sanity: RoomSanity
    bell_sanity: BellSanity

    death_link: DeathLink
    death_link_amnesty: DeathLinkAmnesty
    death_link_behavior: DeathLinkBehavior

    trap_percentage: TrapPercentage
    lose_the_game_weight: LoseTheGameWeight
    stop_jumping_trap_weight: StopJumpingTrapWeight
    stop_jumping_trap_length: StopJumpingTrapLength
    secret_rooms_trap_weight: SecretRoomsTrapWeight
    freeze_trap_weight: FreezeTrapWeight
    freeze_trap_length: FreezeTrapLength
    fast_trap_weight: FastTrapWeight
    fast_trap_length: FastTrapLength

    split_spider_gloves: SplitSpiderGloves
    require_unlock_teleporters: RequireUnlockTeleporters
    logic_difficulty: LogicDifficullty
    include_extra_roadblocks: IncludeExtraRoadblocks
    # TODO uncomment out for password rando
    # password_randomization: PasswordRandomization

    local_nothing_percentage: LocalNothingPercentage
    shuffle_cat_dlc: ShuffleCatDLC

    reset_timer: ResetTimer
    # display_password_letters: DisplayPasswordLetters
