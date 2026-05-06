# remaining to do

# Client start:
# Make sure the campaign is set to "Archipelago". Using the default campaign will break locations. If the player goes to a different campaign, do not send any checks. i dont know where the campaign name is yet.
# If the amount of items sent is not the same as the Amount of Treasure Found, do nothing.
# Sending items:
#     Link the newest treasure found to the id given to the location in treasure_ids.py.
#     Add an exception for "Win The Game" that checks that the integer at Times Won is not 0. This triggers the goal.

# Receiving items:
#     Lose The Game:
#         Add 1 to the integer at Times Lost, kill, and teleport the player to "You Have to Start the Game" (x=-3, y=0). i dont know how to teleport the player to a different room.
#     Stop Jumping Trap:
#         Change the byte at Maximum Jumps to 0 for 5 seconds, then change it back to its previous value. 
#     Secret Room Trap:
#         Teleport the player to "Spiral Out" (x=3, y=-4) or to "The Books Will Not" (x=4, y=-5). They must either die or go to "Sadness" (x=8, y=-2) for 5 seconds xsto escape. i dont know how to do this.
# """

# what went wrong:
# password room became flooded with garbage data when entering letter teleporters during a run.

import asyncio
from CommonClient import CommonContext, gui_enabled
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
    player_data_address = None
    player_attributes_address = None
    room_addresses = None
    unlocked_letters = []

    def __init__(self, server_address=None, password=None):
        super().__init__(server_address, password)
        try:
            self.WinTheGame = Pymem("TheGame.exe")
            # 32 bit program, all pointers are 4 bytes.
            pointer = self.WinTheGame.base_address
            for offset in PLAYER_DATA_CHAIN:
                pointer = self.WinTheGame.read_int(pointer + offset)
            self.player_data_address = pointer
            self.player_attributes_address = self.WinTheGame.read_int(pointer + PLAYER_ATTRIBUTES)

            room_pointer = self.WinTheGame.read_int(self.WinTheGame.base_address + ROOM_DATA)
            self.room_addresses = (room_pointer + ROOM_X, room_pointer + ROOM_Y)
        except:
            self.WinTheGame = None
            self.player_data_address = None
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
        if cmd in {"Connected"}:
            if args["slot_data"]["death_link"]:
                self.deathlinked = True
                self.deathlink_amnesty = args["slot_data"]["death_link_amnesty"]
                if self.WinTheGame:
                    self.death_timer_address = self.get_data(self.player_data_address, DEATH_TIMER_OFFSET, "float")[0]
        

    def on_deathlink(self):
        if self.WinTheGame is None or self.death_timer_address is None:
            return
        self.WinTheGame.write_float(self.death_timer_address, 0.6)

    def get_data(self, start, offset, data_type: str = "int") -> tuple:
        if self.WinTheGame is None:
            return None, None
        address = start + offset
        data = None
        if data_type == "int":
            data = self.WinTheGame.read_int(address)
        elif data_type == "byte":
            data = self.WinTheGame.read_bytes(address, 1)
        elif data_type == "float":
            data = self.WinTheGame.read_float(address)
        elif data_type == "str":
            data = self.WinTheGame.read_string(address, 32)
        return address, data
    
    def get_current_room_xy(self) -> tuple[int, int]:
        if self.WinTheGame is None or self.room_addresses is None:
            return (0, 0)
        return (self.WinTheGame.read_int(self.room_addresses[0]), self.WinTheGame.read_int(self.room_addresses[1]))

    def get_current_room_name(self) -> str:
        return self.get_data(self.WinTheGame.base_address, ROOM_NAME, "str")[1]

    def give_item(self, item: str) -> None:
        if self.WinTheGame is None or self.player_data_address is None:
            return
        #TODO cache this on start up?
        if item == "Cerulean Aura":
            self.WinTheGame.write_uchar(self.get_data(self.player_data_address, CERULEAN_AURA_OFFSET, "byte")[0], 1)
        elif item == "Crimson Aura":
            self.WinTheGame.write_uchar(self.get_data(self.player_data_address, CRIMSON_AURA_OFFSET, "byte")[0], 1)
        elif item == "Springheel Boots":
            self.WinTheGame.write_uchar(self.get_data(self.player_data_address, SPRINGHEEL_BOOTS_OFFSET, "byte")[0], 1)
            self.WinTheGame.write_uchar(self.get_data(self.player_attributes_address, MAX_JUMPS_OFFSET, "byte")[0], 2)
        elif item == "Spider Gloves":
            self.WinTheGame.write_uchar(self.get_data(self.player_data_address, SPIDER_GLOVES_OFFSET, "byte")[0], 1)
            self.WinTheGame.write_uchar(self.get_data(self.player_attributes_address, CAN_WALL_JUMP_OFFSET, "byte")[0], 1)
        elif "Letter" in item:
            self.unlocked_letters += item[-1]
        #TODO add lose the game and traps
        elif item == "Win The Game":
            self.finished_game = True

    def teleport_player(self, x: int, y: int) -> None:
        if self.WinTheGame is None or self.player_data_address is None:
            return
        player_coords = self.get_data(self.player_data_address, PLAYER_COORDS, "int")[1]
        self.WinTheGame.write_float(self.get_data(player_coords, PLAYER_X, "float")[0], x)
        self.WinTheGame.write_float(self.get_data(player_coords, PLAYER_Y, "float")[0], y)

async def watch_game(ctx: WinTheGameContext):
    #TODO change this line later so that WinTheGame can be defined later.
    while not ctx.exit_event.is_set() and ctx.WinTheGame != None:

        if ctx.deathlinked:
            if "DeathLink" not in ctx.tags:
                await ctx.update_death_link(True)
            deaths = ctx.get_data(ctx.player_data_address, DEATHS_OFFSET, "int")[1]
            if deaths > 0 and deaths % ctx.deathlink_amnesty == 0 and deaths != ctx.last_death:
                await ctx.send_death(f"{ctx.player_names[ctx.slot]} died in The Game.")
                ctx.last_death = deaths

        treasure_count = ctx.get_data(ctx.player_data_address, TREASURE_COUNT_OFFSET, "int")[1]
        treasure_vector = ctx.get_data(ctx.player_data_address, TREASURE_VECTOR_OFFSET, "int")[1]
        treasures = []
        for i in range(treasure_count):
            treasures.append(ctx.get_data(treasure_vector, 4*i, "int")[1]+1)
        if ctx.get_data(ctx.player_data_address, TIMES_WON_OFFSET, "int")[1] != 0: #GOAL
            treasures.append(99)
        await ctx.check_locations(treasures)

        recieved_item_ids = [network_item.item for network_item in ctx.items_received]
        for item, item_id in ITEM_IDS.items():
            if item_id in recieved_item_ids:
                ctx.give_item(item)

        if ctx.get_current_room_xy() == (0, -4):
            letter_mismatch = False
            room_name = re.sub(r'[^A-Z]', "", ctx.get_current_room_name())
            for letter in room_name:
                if letter not in ctx.unlocked_letters:
                    letter_mismatch = True
            if letter_mismatch:
                ctx.teleport_player(272.0, 110.0) # placing the player directly on the portal coordinates actually doesn't work.

        if ctx.finished_game:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

        await asyncio.sleep(0.5)

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