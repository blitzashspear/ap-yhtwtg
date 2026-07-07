# remaining TODO

# APWorld changes - future
# Password Rando:
#   Display magic word and symbol when obtained in client. Maybe use something like melee's trophy count.
# Switch from pymem to PyMemoryEditor for linux support
# Make percentage counter in the bottom right more accurate.
# New goal condition - Percentage Hunt. percentage bundles have been scattered across the world. Find them all. Bundles can range from 2% all the way to 10%.
# Add support for multiple traps.
# Change roadblocks to be a OptionSet
# Play the power up noise when finding a progression item.

import asyncio
from typing import TYPE_CHECKING
tracker_loaded = False
from CommonClient import gui_enabled, logger
from sys import platform
if TYPE_CHECKING:
    from worlds.tracker.TrackerClient import TrackerGameContext as SuperContext
else:
    try:
        if platform != 'darwin':
            from worlds.tracker.TrackerClient import TrackerGameContext as SuperContext
            tracker_loaded = True
        else:
            raise ModuleNotFoundError
    except ModuleNotFoundError:
        from CommonClient import CommonContext as SuperContext

from pymem import Pymem
from NetUtils import ClientStatus
from .data.item_ids import ITEM_IDS, ID_TO_ITEM
from .data.location_ids import LOCATION_IDS
from .data.room_coordinates import COORDS_TO_ROOM_NAME
from .data.bell_coordinates import COORDS_TO_BELL_NAME
from .data.client_constants import *
import re
# from kvui import MDLabel

class WinTheGameContext(SuperContext):
    game = "You Have to Win the Game"
    tags = {"AP"}
    items_handling = 0b111
    deathlinked = False
    deathlink_amnesty = None
    last_death: int = None
    WinTheGame: Pymem = None
    unlocked_letters: list[str] = []
    before_secret_room_data = ((None,None),(None,None)) # ((room_x, room_y), (player_x, player_y))
    split_spider_gloves = False
    has_left_glove = False
    has_right_glove = False
    teleporters_locked = False
    given_cerulean_aura = False
    given_crimson_aura = False
    given_springheel_boots = False
    given_spider_gloves = False
    password_rando = False
    password = "SUPER"
    magic_word = "VXSHU"
    magic_symbol = 3
    include_extra_roadblocks = False
    unlocked_quarry = False
    unlocked_mineshaft = False
    unlocked_castle = False
    unlocked_graveyard = False
    room_sanity = False
    bell_sanity = False

    cached_treasure_found: int = None
    cached_last_room = (None, None)
    cached_last_bell: str = None

    def __init__(self, server_address=None, password=None):
        super().__init__(server_address, password)

    def initialize_game(self):
        try:
            self.WinTheGame = Pymem("TheGame.exe")
            # 32 bit program, all pointers are 4 bytes.
            pointer = self.WinTheGame.base_address
            for offset in PLAYER_DATA_CHAIN:
                pointer = self.WinTheGame.read_int(pointer + offset)
            self.cerulean_aura_address = pointer + CERULEAN_AURA_OFFSET
            self.crimson_aura_address = pointer + CRIMSON_AURA_OFFSET
            self.springheel_boots_address = pointer + SPRINGHEEL_BOOTS_OFFSET
            self.spider_gloves_address = pointer + SPIDER_GLOVES_OFFSET
            self.death_timer_address = pointer + DEATH_TIMER_OFFSET
            self.deaths_address = pointer + DEATHS_OFFSET
            self.times_lost_address = pointer + TIMES_LOST_OFFSET
            self.times_won_address = pointer + TIMES_WON_OFFSET
            self.respawn_room_x_address = pointer + RESPAWN_ROOM_X_OFFSET
            self.respawn_room_y_address = pointer + RESPAWN_ROOM_Y_OFFSET
            self.respawn_player_x_address = pointer + RESPAWN_PLAYER_X_OFFSET
            self.respawn_player_y_address = pointer + RESPAWN_PLAYER_Y_OFFSET
            self.treasures_found_address = pointer + TREASURES_FOUND_OFFSET
            self.treasure_vector_address = pointer + TREASURE_VECTOR_OFFSET
            self.rooms_found_address = pointer + ROOMS_FOUND_OFFSET
            self.player_face_left_address = pointer + PLAYER_FACE_LEFT_OFFSET
            self.player_crouching_address = pointer + PLAYER_CROUCHING_OFFSET

            player_attributes_address = self.WinTheGame.read_int(pointer + PLAYER_ATTRIBUTES)
            self.on_wall_address = player_attributes_address + ON_WALL_OFFSET
            self.max_jumps_address = player_attributes_address + MAX_JUMPS_OFFSET
            self.can_wall_jump_address = player_attributes_address + CAN_WALL_JUMP_OFFSET

            player_coordinates = self.WinTheGame.read_int(pointer + PLAYER_COORDS)
            self.player_x_address = player_coordinates + PLAYER_X_OFFSET
            self.player_y_address = player_coordinates + PLAYER_Y_OFFSET

            room_pointer = self.WinTheGame.read_int(self.WinTheGame.base_address + ROOM_DATA)
            self.room_speed_address = room_pointer + ROOM_SPEED_OFFSET
            self.room_x_address = room_pointer + ROOM_X_OFFSET
            self.room_y_address = room_pointer + ROOM_Y_OFFSET
            self.total_treasure_address = room_pointer + TOTAL_TREASURE_OFFSET
            self.total_rooms_address = room_pointer + TOTAL_ROOMS_OFFSET

            self.room_name_address = self.WinTheGame.base_address + ROOM_NAME_OFFSET
            self.shown_campaign_message = False
            logger.info("Connected to You Have to Win the Game")
        except:
            self.WinTheGame = None

    async def server_auth(self, password_requested=False):
        if password_requested and not self.password:
            await super(WinTheGameContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd, args):
        # if i add shit here in the future, go to world.py, fill_slot_data and update that too
        super().on_package(cmd, args) # for UT
        if cmd in {"Connected"}:
            if args["slot_data"]["death_link"]:
                self.deathlinked = True
                self.deathlink_amnesty = args["slot_data"]["death_link_amnesty"]
            if args["slot_data"]["split_spider_gloves"]:
                self.split_spider_gloves = True
            if args["slot_data"]["require_unlock_teleporters"]:
                self.teleporters_locked = True
            # if args["slot_data"]["password_randomization"]:
            #     self.password_rando = True
            #     self.password = args["slot_data"]["password"]
            #     self.magic_word = args["slot_data"]["magic_word"]
            #     self.magic_symbol = args["slot_data"]["magic_symbol"]
            if args["slot_data"]["include_extra_roadblocks"]:
                self.include_extra_roadblocks = True
                self.unlocked_quarry = False
                self.unlocked_mineshaft = False
                self.unlocked_castle = False
                self.unlocked_graveyard = False
            if args["slot_data"]["room_sanity"]:
                self.room_sanity = True
            if args["slot_data"]["bell_sanity"]:
                self.bell_sanity = True

            # self.password_widget = MDLabel(text=f"", size_hint_x=None, width=120, halign="center")
            # self.ui.connect_layout.add_widget(self.password_widget)

    def on_deathlink(self, data):
        # I need a better solution to show who deathlinked than to just paste it into the client
        logger.info(data)
        self.WinTheGame.write_float(self.death_timer_address, 0.6)
    
    def get_current_room_coords(self) -> tuple[int, int]:
        return (self.WinTheGame.read_int(self.room_x_address), self.WinTheGame.read_int(self.room_y_address))
    
    def get_player_coords(self) -> tuple[float, float]:
        return (round(self.WinTheGame.read_float(self.player_x_address), 1), round(self.WinTheGame.read_float(self.player_y_address), 1))

    def give_item(self, item: str) -> None:
        if item == "Cerulean Aura" and not self.given_cerulean_aura:
            self.WinTheGame.write_uchar(self.cerulean_aura_address, 1)
            self.given_cerulean_aura = True
        elif item == "Crimson Aura" and not self.given_crimson_aura:
            self.WinTheGame.write_uchar(self.crimson_aura_address, 1)
            self.given_crimson_aura = True
        elif item == "Springheel Boots" and not self.given_springheel_boots:
            self.WinTheGame.write_uchar(self.springheel_boots_address, 1)
            self.WinTheGame.write_int(self.max_jumps_address, 2)
            self.given_springheel_boots = True
        elif item == "Spider Gloves" and not self.given_spider_gloves:
            self.WinTheGame.write_uchar(self.spider_gloves_address, 1)
            self.WinTheGame.write_uchar(self.can_wall_jump_address, 1)
            self.given_spider_gloves = True
        elif item == "Left Spider Glove":
            self.has_left_glove = True
        elif item == "Right Spider Glove":
            self.has_right_glove = True

        # Ripping the letter from the item name like a barbarian.
        elif "Letter" in item and item[-1] not in self.unlocked_letters:
            self.unlocked_letters += item[-1]

        elif item == "Lose The Game" and not self.received_trap(1):
            self.teleport_player_to_room(-3, 0, 76.0, 140.0) # You Have to Start the Game
        elif item == "Stop Jumping Trap" and not self.received_trap(2):
            asyncio.create_task(self.apply_stop_jumping_trap())
        elif item == "Secret Room Trap" and not self.received_trap(3):
            self.before_secret_room_data = (self.get_current_room_coords(), self.get_player_coords())
            self.teleport_player_to_room(3, -4, 73.0, 76.0) # Spiral Out
        elif item == "Freeze Trap" and not self.received_trap(4):
            asyncio.create_task(self.apply_room_speed_trap(0.0, 2))
        elif item == "Fast Trap" and not self.received_trap(5):
            asyncio.create_task(self.apply_room_speed_trap(4.0, 8))

        elif item == "Unlock Teleporters":
            self.teleporters_locked = False
            
        elif item == "Unlock Quarry":
            self.unlocked_quarry = True
        elif item == "Unlock Mineshaft":
            self.unlocked_mineshaft = True
        elif item == "Unlock Castle":
            self.unlocked_castle = True
        elif item == "Unlock Graveyard":
            self.unlocked_graveyard = True

        #TODO
        elif item == "Reveal Magic Word":
            pass
        elif item == "Reveal Magic Symbol":
            pass

        elif item == "Win the Game":
            self.finished_game = True

    def received_trap(self, trap_type: int) -> bool:
        """
        Returns whether the specified trap has already been received.
        Each trap corresponds to a single bit:

            Lose The Game Trap (1): 00001
            Stop Jumping Trap (2): 00010
            Secret Room Trap (3): 00100
            Freeze Trap (4):      01000
            Fast Trap (5):        10000

        Duplicate trap receives are ignored (from uses like send_item).
        """
        #TODO: Add support for multiple instances of the same trap. in the meantime we using bitwise operations in this bitch.
        times_lost_value = self.WinTheGame.read_int(self.times_lost_address)
        mask = 1 << (trap_type - 1)
        received = (times_lost_value & mask) != 0
        if not received:
            self.WinTheGame.write_int(self.times_lost_address, times_lost_value | mask)

        return received

    async def apply_stop_jumping_trap(self):
        max_jumps_value = self.WinTheGame.read_int(self.max_jumps_address)
        self.WinTheGame.write_int(self.max_jumps_address, 0)
        await asyncio.sleep(5)
        self.WinTheGame.write_int(self.max_jumps_address, max_jumps_value)

    async def apply_room_speed_trap(self, speed: float, seconds: int):
        self.WinTheGame.write_float(self.room_speed_address, speed)
        await asyncio.sleep(seconds)
        self.WinTheGame.write_float(self.room_speed_address, 1.0)

    def teleport_player(self, player_x: float, player_y: float) -> None:
        self.WinTheGame.write_float(self.player_x_address, player_x)
        self.WinTheGame.write_float(self.player_y_address, player_y)

    def teleport_player_to_room(self, room_x: int, room_y: int, player_x: float, player_y: float) -> None:
        # instead of doing something logical like hijacking the room compile function, i am going to abuse the fact that the respawn location isnt necessarily bound to a bell and can be put anywhere.
        self.WinTheGame.write_float(self.death_timer_address, 0.01)
        self.WinTheGame.write_int(self.respawn_room_x_address, room_x)
        self.WinTheGame.write_int(self.respawn_room_y_address, room_y)
        self.WinTheGame.write_float(self.respawn_player_x_address, player_x)
        self.WinTheGame.write_float(self.respawn_player_y_address, player_y)

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = "You Have to Win the Game Client"
        return ui
    
    # async def draw_password(self):
    #     #TODO
    #     # if no password rando, draw password with missing letters
    #     # if password rando, add a separate label for the magic word and magic symbol,
    #     # if both found, then display the draw the password
    #     # Only call when letters change
    #     password_display = ""
    #     for char in self.password:
    #         if char in self.unlocked_letters:
    #             password_display += char
    #         else:
    #             password_display += "-"
    #     self.password_widget.text = f"Password: {password_display}"
            
async def watch_game(ctx: WinTheGameContext):
    while not ctx.exit_event.is_set():
        if ctx.WinTheGame == None:
            ctx.initialize_game()
            await asyncio.sleep(1)
            continue

        # Campaign check. The original campaign only has 64.
        # Also the guard to make sure the game doesn't send out all of my checks at the title screen.
        total_treasures = ctx.WinTheGame.read_int(ctx.total_treasure_address)
        if total_treasures != 68: 
            if not ctx.shown_campaign_message:
                logger.info("Please use the Archipelago campaign.")
                ctx.shown_campaign_message = True
            await asyncio.sleep(5)
            continue

        current_room = ctx.get_current_room_coords()
        in_secret_rooms = current_room in SECRET_ROOM_COORDS

        if ctx.deathlinked:
            if "DeathLink" not in ctx.tags:
                await ctx.update_death_link(True)
            deaths = ctx.WinTheGame.read_int(ctx.deaths_address)
            if deaths > 0 and deaths % ctx.deathlink_amnesty == 0 and deaths != ctx.last_death:
                nth = lambda deaths: f"{deaths}{'th' if 10 <= deaths % 100 <= 20 else {1:'st', 2:'nd', 3:'rd'}.get(deaths % 10, 'th')}"
                await ctx.send_death(f"{ctx.player_names[ctx.slot]} died for the {nth(deaths)} time while traversing {COORDS_TO_ROOM_NAME[current_room][:-13]}.")
                ctx.last_death = deaths

        locations = []
        treasures_found = ctx.WinTheGame.read_int(ctx.treasures_found_address)
        if ctx.cached_treasure_found != treasures_found:
            ctx.cached_treasure_found = treasures_found
            # The address of the vector is dynamic.
            treasure_vector = ctx.WinTheGame.read_int(ctx.treasure_vector_address)
            # Keeping this loop. I would like treasures to send out missing checks on disconnect/reconnect, since they disappear in the world after collection.
            for i in range(treasures_found):
                locations.append(ctx.WinTheGame.read_int(treasure_vector + 4 * i) + 1)
            if ctx.WinTheGame.read_int(ctx.times_won_address) != 0: #GOAL
                locations.append(99)
        if not in_secret_rooms:
            # These next check types are checked once unlike the treasures. 
            # This means that any rooms explored or bells rung before connecting to archipelago wont be saved.
            if ctx.room_sanity and ctx.cached_last_room != current_room: 
                locations.append(LOCATION_IDS[COORDS_TO_ROOM_NAME[current_room]])
                ctx.cached_last_room = current_room
            if ctx.bell_sanity:
                latest_checkpoint = (ctx.WinTheGame.read_float(ctx.respawn_player_x_address), ctx.WinTheGame.read_float(ctx.respawn_player_y_address), 
                                     (ctx.WinTheGame.read_int(ctx.respawn_room_x_address), ctx.WinTheGame.read_int(ctx.respawn_room_y_address)))
                try:
                    bell = COORDS_TO_BELL_NAME[latest_checkpoint] # Starting the game and the secret rooms will break this line.
                    if ctx.cached_last_bell != bell:
                        ctx.cached_last_bell = bell
                        locations.append(LOCATION_IDS[bell])
                except KeyError:
                    pass
        if len(locations) != 0: # Only call this when needed, because oh my god ive been calling it every 10 ms in v0.3.0.
            await ctx.check_locations(locations)

        for network_item in ctx.items_received:
            ctx.give_item(ID_TO_ITEM[network_item.item])

        if ctx.split_spider_gloves:
            if (ctx.has_left_glove and ctx.WinTheGame.read_uchar(ctx.player_face_left_address) == 1) or (ctx.has_right_glove and ctx.WinTheGame.read_uchar(ctx.player_face_left_address) == 0):
                ctx.WinTheGame.write_uchar(ctx.can_wall_jump_address, 1)
            else:
                ctx.WinTheGame.write_uchar(ctx.on_wall_address, 0)
                ctx.WinTheGame.write_uchar(ctx.can_wall_jump_address, 0)

        if ctx.teleporters_locked:
            if current_room == (-3, 4): # Rawr!
                if ctx.WinTheGame.read_float(ctx.player_x_address) < 185.0:
                    ctx.WinTheGame.write_float(ctx.player_x_address, 185.0)
            elif current_room == (-2, -2): # Point of No Return
                if ctx.WinTheGame.read_float(ctx.player_x_address) < 50.0 and ctx.WinTheGame.read_float(ctx.player_y_address) > 100.0:
                    ctx.WinTheGame.write_float(ctx.player_x_address, 50.0)
            elif current_room == (6, 4): # Rough Landing
                ctx.WinTheGame.write_float(ctx.death_timer_address, 0.01)

        if ctx.include_extra_roadblocks:
            if current_room == (-6, 2) and not ctx.unlocked_quarry: # The Quarry Hub
                if ctx.WinTheGame.read_float(ctx.player_y_address) > 42.0:
                    ctx.WinTheGame.write_float(ctx.player_y_address, 41.8)
            elif (current_room == (-5, 5) or current_room == (-4, 5)) and not ctx.unlocked_mineshaft: # Mine Shaft or Green Man
                if ctx.WinTheGame.read_float(ctx.player_y_address) > 178.0:
                    ctx.WinTheGame.write_float(ctx.player_y_address, 145.0)
            elif current_room == (4, 1) and not ctx.unlocked_castle: #Eden Maw
                if ctx.WinTheGame.read_float(ctx.player_x_address) > 300.0:
                    ctx.WinTheGame.write_float(ctx.player_x_address, 300.0)
            elif current_room == (4, 3) and not ctx.unlocked_graveyard: # Remnants of a Past Unknown
                if ctx.WinTheGame.read_float(ctx.player_y_address) > 178.0:
                    ctx.teleport_player(90.0, 168.0)

        if in_secret_rooms:
            ctx.WinTheGame.write_int(ctx.respawn_room_x_address, ctx.before_secret_room_data[0][0])
            ctx.WinTheGame.write_int(ctx.respawn_room_y_address, ctx.before_secret_room_data[0][1])
            ctx.WinTheGame.write_float(ctx.respawn_player_x_address, ctx.before_secret_room_data[1][0])
            ctx.WinTheGame.write_float(ctx.respawn_player_y_address, ctx.before_secret_room_data[1][1])
        elif current_room == (0, -4): # Warp Middle
            letter_mismatch = False
            room_name = re.sub(r'[^A-Z]', "", ctx.WinTheGame.read_string(ctx.room_name_address, 50))
            for letter in room_name:
                if letter not in ctx.unlocked_letters:
                    letter_mismatch = True
            if letter_mismatch:
                ctx.teleport_player(272.0, 110.0) # placing the player directly on the portal coordinates actually doesn't work. Need to place slightly higher
        # elif current_room == (0, -5) and ctx.password_rando: # Warp Right
        #     room_name = re.sub(r'[^A-Z]', "", ctx.WinTheGame.read_string(ctx.room_name_address, 50))
        #     if room_name == ctx.password:
        #         await asyncio.sleep(1)
        #         ctx.teleport_player_to_room(-1, -2, 160.0, 80.0) # Open Sesame

        # Player anti-softlock.
        if ctx.WinTheGame.read_uchar(ctx.player_crouching_address) and not in_secret_rooms:
            crouch_time += 1
        else:
            crouch_time = 0
        if crouch_time >= 50: # Five seconds, since every loop is 0.1 seconds
            ctx.teleport_player_to_room(-3, 0, 76.0, 140.0) # You Have to Start the Game

        # # Password display.
        # if ctx.ui:
        #     await ctx.draw_password()

        if ctx.finished_game:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
        await asyncio.sleep(0.1)

def launch():
    async def main():
        ctx = WinTheGameContext()
        if tracker_loaded:
            ctx.run_generator()
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        game_watcher = asyncio.create_task(watch_game(ctx))
        await ctx.exit_event.wait()
        await game_watcher

    asyncio.run(main())
