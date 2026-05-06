from dataclasses import dataclass
from Options import PerGameCommonOptions, Range, Toggle, DeathLink

#TODO ALL OPTIONS
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
    Shuffle a "Lose The Game" item that teleports you to the starting room. Currently does nothing.
    """
    display_name = "Shuffle Lose The Game"
    default = True

class StopJumpingTrapPercentage(Range):
    """
    Adds traps that remove your ability to jump for a short time. Amount is based on percentage of remaining filler items. Currently does nothing.
    """
    display_name = "Stop Jumping Trap Percentage"
    default = 5
    range_start = 0
    range_end = 100

class TeleportToSecretRoomsTrap(Toggle):
    """
    Adds a trap that teleports you to the secret rooms included in the game. Currently does nothing.
    """
    display_name = "Teleport To Secret Rooms Trap"
    default = False

class LocalNothingPercentage(Range):
    """
    Percentage of "Nothing" items that are placed locally. Currently does nothing.
    """
    display_name = "Local Nothing Percentage"
    default = 50
    range_start = 0
    range_end = 100

@dataclass
class WinTheGameOptions(PerGameCommonOptions):
    #room_sanity: RoomSanity
    death_link: WinTheGameDeathLink
    death_link_amnesty: DeathLinkAmnesty
    #shuffle_lose_the_game: ShuffleLoseTheGame
    #stop_jumping_trap_percentage: StopJumpingTrapPercentage
    #teleport_to_secret_rooms_trap: TeleportToSecretRoomsTrap
    #local_nothing_percentage: LocalNothingPercentage