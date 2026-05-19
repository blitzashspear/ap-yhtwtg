from dataclasses import dataclass
from Options import PerGameCommonOptions, Range, Toggle, DeathLink, Choice

#TODO roomsanity and localnothing percentage unimplemented
#TODO new ideas: freeze trap.
class RoomSanity(Toggle):
    """
    Make each room a location. Currently does nothing.
    """
    display_name = "Room Sanity"
    default = False

class WinTheGameDeathLink(DeathLink):
    __doc__ = DeathLink.__doc__
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
    Adds a trap that teleports you to the secret rooms included in the game. 
    """
    display_name = "Shuffle Secret Rooms Trap"
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

class LocalNothingPercentage(Range):
    """
    Percentage of "Nothing" items that are placed locally.
    """
    display_name = "Local Nothing Percentage"
    default = 50
    range_start = 0
    range_end = 90

class HarderLogicDifficullty(Toggle):
    """
    Will place items with very hard jumps into logic.
    """
    display_name = "Harder Logic Difficulty"
    default = False


@dataclass
class WinTheGameOptions(PerGameCommonOptions):
    # room_sanity: RoomSanity
    death_link: WinTheGameDeathLink
    death_link_amnesty: DeathLinkAmnesty
    shuffle_lose_the_game: ShuffleLoseTheGame
    shuffle_stop_jumping_trap: ShuffleStopJumpingTrap
    shuffle_secret_rooms_trap: ShuffleSecretRoomsTrap
    split_spider_gloves: SplitSpiderGloves
    require_unlock_teleporters: RequireUnlockTeleporters
    # local_nothing_percentage: LocalNothingPercentage
    harder_logic_difficulty: HarderLogicDifficullty