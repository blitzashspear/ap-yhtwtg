from dataclasses import dataclass
from Options import PerGameCommonOptions, Range, Toggle, DeathLink, Choice, OptionGroup

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
    Amount of deaths before sending a death link.
    """
    display_name = "Death Link Amnesty"
    default = 25
    range_start = 1
    range_end = 100

class ShuffleLoseTheGame(Toggle):
    """
    Adds a "Lose The Game" trap that teleports you to the starting room.
    """
    display_name = "Shuffle Lose The Game"
    default = True

class ShuffleStopJumpingTrap(Toggle):
    """
    Adds a trap that removes your ability to jump for a short time.
    """
    display_name = "Shuffle Stop Jumping Trap"
    default = False

class ShuffleSecretRoomsTrap(Toggle):
    """
    Adds a trap that teleports you to the secret rooms included in the game. Either escape the rooms or die trying.
    """
    display_name = "Shuffle Secret Rooms Trap"
    default = False

class ShuffleFreezeTrap(Toggle):
    """
    Adds a trap that freezes the game for a short time.
    """
    display_name = "Shuffle Freeze Trap"
    default = False

class ShuffleFastTrap(Toggle):
    """
    Adds a trap that quadruples the game speed for a short time.
    """
    display_name = "Shuffle Fast Trap"
    default = False

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
    Will place locations with harder jumps in logic. These include non-obvious movement, pixel perfect jumps, coyotoe jumping or all at once.
    """
    display_name = "Logic Difficulty"
    option_normal = 0
    option_hard = 1
    option_extreme = 2
    default = 0

class IncludeExtraRoadblocks(Toggle):
    """
    Includes 4 more roadblocks that require unlocks to access.
    The Quarry (Cerulean Aura Area)
    The Mineshaft (Area Left of Springheel Boots)
    The Castle (Spider Glove Area)
    The Graveyard (Crimson Aura Area)
    """
    display_name = "Include Extra Roadblocks"
    default = False

# class IncludeExtraRoadblocks(OptionSet):
#     """
#     Includes 4 more roadblocks that require unlocks to access.
#     The Quarry (Cerulean Aura Area)
#     The Mineshaft (Area Left of Springheel Boots)
#     The Castle (Spider Glove Area)
#     The Graveyard (Crimson Aura Area)
#     """
#     display_name = "Include Extra Roadblocks"
#     default = []

class PasswordRandomization(Choice):
    """
    Randomize the password at the end of the game. This shuffles 2 new items: "Reveal Magic Word" and "Reveal Magic Symbol".
    These items will be logically required to beat the game, but won't actually do anything to block you.

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

class HideLetterClassification(Toggle):
    """
    If turned on, all letters shuffled into the pool will be progression.
    """
    display_name = "Hide Letter Classification"
    default = False

option_groups = [
    OptionGroup("Extra Locations", [RoomSanity, BellSanity]),
    OptionGroup("DeathLink", [DeathLink, DeathLinkAmnesty]),
    OptionGroup("Traps", [ShuffleLoseTheGame, ShuffleStopJumpingTrap, ShuffleSecretRoomsTrap, ShuffleFreezeTrap, ShuffleFastTrap]),
    OptionGroup("Randomizer Changes", [SplitSpiderGloves, RequireUnlockTeleporters, LogicDifficullty, IncludeExtraRoadblocks, PasswordRandomization]),
    # OptionGroup("Randomizer Changes", [SplitSpiderGloves, RequireUnlockTeleporters, LogicDifficullty, IncludeExtraRoadblocks, PasswordRandomization]),
    OptionGroup("Filler Options", [LocalNothingPercentage])
    # OptionGroup("Filler Options", [LocalNothingPercentage, HideLetterClassification])
]

@dataclass
class WinTheGameOptions(PerGameCommonOptions):
    room_sanity: RoomSanity
    bell_sanity: BellSanity

    death_link: DeathLink
    death_link_amnesty: DeathLinkAmnesty

    shuffle_lose_the_game: ShuffleLoseTheGame
    shuffle_stop_jumping_trap: ShuffleStopJumpingTrap
    shuffle_secret_rooms_trap: ShuffleSecretRoomsTrap
    shuffle_freeze_trap: ShuffleFreezeTrap
    shuffle_fast_trap: ShuffleFastTrap

    split_spider_gloves: SplitSpiderGloves
    require_unlock_teleporters: RequireUnlockTeleporters
    logic_difficulty: LogicDifficullty
    include_extra_roadblocks: IncludeExtraRoadblocks
    # password_randomization: PasswordRandomization

    local_nothing_percentage: LocalNothingPercentage
    # hide_letter_classification: HideLetterClassification
