# remaining to do

# Client start:
# Make sure the campaign is set to "Archipelago". Using the default campaign will break locations. If the player goes to a different campaign, do not send any checks. i dont know where the campaign name is yet.
# If the amount of items sent is not the same as the Amount of Treasure Found (give or take a few), do nothing.

# Receiving items:
#     Add support for multiple traps.

# LATER RELEASE - REWRITE LOGIC
# Roomsanity
# Edit logic to add a "Unlock Portals" item that allows for the player to go through portals. This will be done by hardcoding rooms and just not allowing the player to access certain room coordinates by instantly killing them.
# i want to add password rando that would be dope

# add UT support

# what went wrong:
# password room became flooded with garbage data when entering letter teleporters during a run.

import asyncio
from CommonClient import CommonContext, gui_enabled, logger
from kvui import GameManager
from pymem import Pymem
from NetUtils import ClientStatus
from .item_ids import ITEM_IDS
from .client_constants import *
import re

class WinTheGameContext(CommonContext):
    game = "You Have to Win the Game"
    items_handling = 0b111
    deathlinked = False
    deathlink_amnesty = None
    death_timer_address = None
    last_death: int = None
    WinTheGame: Pymem = None
    player_attributes_address = None
    room_addresses = None
    unlocked_letters = []
    before_secret_room_data = ((None,None),(None,None)) # ((room_x, room_y), (player_x, player_y))
    split_spider_gloves = False
    has_left_glove = False
    has_right_glove = False

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
            self.treasure_count_address = pointer + TREASURE_COUNT_OFFSET
            self.treasure_vector_address = pointer + TREASURE_VECTOR_OFFSET
            self.player_face_left_address = pointer + PLAYER_FACE_LEFT_OFFSET

            player_attributes_address = self.WinTheGame.read_int(pointer + PLAYER_ATTRIBUTES)
            self.on_wall_address = player_attributes_address + ON_WALL_OFFSET
            self.max_jumps_address = player_attributes_address + MAX_JUMPS_OFFSET
            self.can_wall_jump_address = player_attributes_address + CAN_WALL_JUMP_OFFSET

            player_coordinates = self.WinTheGame.read_int(pointer + PLAYER_COORDS)
            self.player_x_address = player_coordinates + PLAYER_X_OFFSET
            self.player_y_address = player_coordinates + PLAYER_Y_OFFSET

            room_pointer = self.WinTheGame.read_int(self.WinTheGame.base_address + ROOM_DATA)
            self.room_x_address = room_pointer + ROOM_X_OFFSET
            self.room_y_address = room_pointer + ROOM_Y_OFFSET

            self.room_name_address = self.WinTheGame.base_address + ROOM_NAME_OFFSET

        except:
            self.WinTheGame = None
            self.player_attributes_address = None
            self.room_addresses = None

    async def server_auth(self, password_requested=False):
        if password_requested and not self.password:
            await super(WinTheGameContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def run_gui(self):
        class WinTheGameManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "You Have to Win the Game Client"

        self.ui = WinTheGameManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def on_package(self, cmd, args):
        # if i add shit here in the future, go to world.py, fill_slot_data and update that too
        if cmd in {"Connected"}:
            if args["slot_data"]["death_link"]:
                self.deathlinked = True
                self.deathlink_amnesty = args["slot_data"]["death_link_amnesty"]
            if args["slot_data"]["split_spider_gloves"]:
                self.split_spider_gloves = True
        
    def on_deathlink(self, data):
        self.WinTheGame.write_float(self.death_timer_address, 0.6)
    
    def get_current_room_coords(self) -> tuple[int, int]:
        return (self.WinTheGame.read_int(self.room_x_address), self.WinTheGame.read_int(self.room_y_address))
    
    def get_player_coords(self) -> tuple[float, float]:
        return (self.WinTheGame.read_float(self.player_x_address), self.WinTheGame.read_float(self.player_y_address))

    def give_item(self, item: str) -> None:
        if item == "Cerulean Aura":
            self.WinTheGame.write_uchar(self.cerulean_aura_address, 1)
        elif item == "Crimson Aura":
            self.WinTheGame.write_uchar(self.crimson_aura_address, 1)
        elif item == "Springheel Boots":
            self.WinTheGame.write_uchar(self.springheel_boots_address, 1)
            self.WinTheGame.write_int(self.max_jumps_address, 2)
        elif item == "Spider Gloves":
            self.WinTheGame.write_uchar(self.spider_gloves_address, 1)
            self.WinTheGame.write_uchar(self.can_wall_jump_address, 1)
        elif item == "Left Spider Glove":
            self.has_left_glove = True
        elif item == "Right Spider Glove":
            self.has_right_glove = True
        elif "Letter" in item:
            self.unlocked_letters += item[-1]
        #TODO traps can only be recieved once. At some point i want to add support for multiple traps but for now I just ignore duplicates.
        elif item == "Lose The Game":
            times_lost_value = self.WinTheGame.read_int(self.times_lost_address)
            if times_lost_value % 2 == 0:
                self.WinTheGame.write_int(self.times_lost_address, times_lost_value+1)
                self.teleport_player_to_room(-3, 0, 76.0, 153.985) # You Have to Start the Game
        elif item == "Stop Jumping Trap":
            asyncio.create_task(self.apply_stop_jumping_trap())
        elif item == "Secret Room Trap":
            # hundreds place will be used to make sure the trap is only applied once.
            times_lost_value = self.WinTheGame.read_int(self.times_lost_address)
            if times_lost_value//100 == 0:
                self.before_secret_room_data = (self.get_current_room_coords(), self.get_player_coords())
                self.WinTheGame.write_int(self.times_lost_address, times_lost_value+100)
                self.teleport_player_to_room(3, -4, 73.0, 76.0) # Spiral Out

        elif item == "Win The Game":
            self.finished_game = True

    async def apply_stop_jumping_trap(self):
        # tens place will be used to make sure the trap is only applied once.
        times_lost_value = self.WinTheGame.read_int(self.times_lost_address)
        if times_lost_value//10 == 0:
            max_jumps_value = self.WinTheGame.read_int(self.max_jumps_address)
            self.WinTheGame.write_int(self.times_lost_address, times_lost_value+10)
            self.WinTheGame.write_int(self.max_jumps_address, 0)
            await asyncio.sleep(5)
            self.WinTheGame.write_int(self.max_jumps_address, max_jumps_value)

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

async def watch_game(ctx: WinTheGameContext):
    #TODO i fear that joining with an already completed save will destroy the multiworld. i dont think i have a guard for this.
    while not ctx.exit_event.is_set():
        if ctx.WinTheGame == None:
            ctx.initialize_game()
            await asyncio.sleep(1)
            continue

        if ctx.deathlinked:
            if "DeathLink" not in ctx.tags:
                await ctx.update_death_link(True)
            deaths = ctx.WinTheGame.read_int(ctx.deaths_address)
            if deaths > 0 and deaths % ctx.deathlink_amnesty == 0 and deaths != ctx.last_death:
                await ctx.send_death(f"{ctx.player_names[ctx.slot]} died in The Game.")
                ctx.last_death = deaths

        treasure_count = ctx.WinTheGame.read_int(ctx.treasure_count_address)
        treasure_vector = ctx.WinTheGame.read_int(ctx.treasure_vector_address)
        treasures = []
        for i in range(treasure_count):
            treasures.append(ctx.WinTheGame.read_int(treasure_vector + 4 * i) + 1)
        if ctx.WinTheGame.read_int(ctx.times_won_address) != 0: #GOAL
            treasures.append(99)
        await ctx.check_locations(treasures)

        recieved_item_ids = [network_item.item for network_item in ctx.items_received]
        for item, item_id in ITEM_IDS.items():
            if item_id in recieved_item_ids:
                ctx.give_item(item)

        if ctx.split_spider_gloves:
                if ctx.has_left_glove and ctx.WinTheGame.read_uchar(ctx.player_face_left_address) == 1:
                    ctx.WinTheGame.write_uchar(ctx.can_wall_jump_address, 1)
                elif ctx.has_right_glove and ctx.WinTheGame.read_uchar(ctx.player_face_left_address) == 0:
                    ctx.WinTheGame.write_uchar(ctx.can_wall_jump_address, 1)
                else:
                    ctx.WinTheGame.write_uchar(ctx.on_wall_address, 0)
                    ctx.WinTheGame.write_uchar(ctx.can_wall_jump_address, 0)

        current_room = ctx.get_current_room_coords()
        if current_room in SECRET_ROOM_COORDS:
            ctx.WinTheGame.write_int(ctx.respawn_room_x_address, ctx.before_secret_room_data[0][0])
            ctx.WinTheGame.write_int(ctx.respawn_room_y_address, ctx.before_secret_room_data[0][1])
            ctx.WinTheGame.write_float(ctx.respawn_player_x_address, ctx.before_secret_room_data[1][0])
            ctx.WinTheGame.write_float(ctx.respawn_player_y_address, ctx.before_secret_room_data[1][1])
        elif current_room == (0, -4):
            letter_mismatch = False
            room_name = re.sub(r'[^A-Z]', "", ctx.WinTheGame.read_string(ctx.room_name_address, 32))
            for letter in room_name:
                if letter not in ctx.unlocked_letters:
                    letter_mismatch = True
            if letter_mismatch:
                ctx.teleport_player(272.0, 110.0) # placing the player directly on the portal coordinates actually doesn't work.

        if ctx.finished_game:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

        await asyncio.sleep(0.1)

def launch():
    async def main():
        ctx = WinTheGameContext()
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        game_watcher = asyncio.create_task(watch_game(ctx))
        await ctx.exit_event.wait()
        await game_watcher

    asyncio.run(main())