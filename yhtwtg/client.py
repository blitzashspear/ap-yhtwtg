# APWorld ideas im not doing because im tired boss
# YOLO Trap, next death warps you to the starting room.
# Switch from pymem to PyMemoryEditor for linux support.
# Make percentage counter in the bottom right more accurate.
# New goal condition - Percentage Hunt. percentage bundles have been scattered across the world. Find them all. Bundles can range from 2% all the way to 10%.
# Play the power up noise when finding a progression item.
# Traplink based on items from other games.
# Whatever the fuck Group DeathLink is.
# Switch to Rule Builder.
# Extra Spicy map.
# YAML option for custom password.

import asyncio
from typing import TYPE_CHECKING

tracker_loaded = False
from CommonClient import gui_enabled, logger
if TYPE_CHECKING:
    from worlds.tracker.TrackerClient import TrackerGameContext as SuperContext
else:
    try:
        from worlds.tracker.TrackerClient import TrackerGameContext as SuperContext
        tracker_loaded = True        
    except ModuleNotFoundError:
        from CommonClient import CommonContext as SuperContext

from pymem import Pymem
from NetUtils import ClientStatus
from .data.item_ids import ID_TO_ITEM
from .data.location_ids import LOCATION_IDS
from .data.room_coordinates import COORDS_TO_ROOM_NAME
from .data.bell_coordinates import COORDS_TO_BELL_NAME
from .data.client_constants import *
import os
import re
from kvui import GameManager # import required even if unused
from kivy.uix.label import Label
from kivy.uix.layout import Layout
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image # why the fuck doesnt vscode recongize this import

class WinTheGameContext(SuperContext):
    game = "You Have to Win the Game"
    tags = {"AP"}
    items_handling = 0b111
    death_link_active = False
    death_link_amnesty = 25
    death_link_behavior = "checkpoint"
    last_death_link: int = None
    WinTheGame: Pymem = None
    unlocked_letters: list[str] = []
    before_secret_room_data = ((None,None),(None,None)) # ((room_x, room_y), (player_x, player_y))
    split_spider_gloves = False
    has_left_glove = False
    has_right_glove = False
    teleporters_locked = False
    password_rando = False
    solved_password = "SUPER"
    magic_word = "VXSHU"
    show_magic_word = False
    magic_symbol = 3
    show_magic_symbol = False
    auto_solve_password = False
    unlocked_quarry = True
    unlocked_mineshaft = True
    unlocked_castle = True
    unlocked_graveyard = True
    room_sanity = False
    bell_sanity = False
    is_cat = False
    cat_stored_deaths: int = None
    stop_jumping_trap_length = 5
    freeze_trap_length = 2
    fast_trap_length = 8

    cached_treasure_found: int = None
    cached_last_room = (None, None)
    cached_last_bell: str = None
    resynced = False
    items_given = 0

    reset_timer = 25
    display_password_letters = True
    connected = False

    finished_game = False
    informed_server = False

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
            self.player_is_cat_address = room_pointer + PLAYER_IS_CAT_OFFSET

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
            self.connected = True
            self.room_sanity = args["slot_data"]["room_sanity"]
            self.bell_sanity = args["slot_data"]["bell_sanity"]

            if args["slot_data"]["death_link"]:
                self.death_link_active = True
                self.death_link_amnesty = args["slot_data"]["death_link_amnesty"]
                self.death_link_behavior = args["slot_data"]["death_link_behavior"]

            self.stop_jumping_trap_length = args["slot_data"]["stop_jumping_trap_length"]
            self.freeze_trap_length = args["slot_data"]["freeze_trap_length"]
            self.fast_trap_length = args["slot_data"]["fast_trap_length"]

            self.split_spider_gloves = args["slot_data"]["split_spider_gloves"]
            self.teleporters_locked = args["slot_data"]["require_unlock_teleporters"]

            if "Quarry" in args["slot_data"]["include_extra_roadblocks"]:
                self.unlocked_quarry = False
            if "Mineshaft" in args["slot_data"]["include_extra_roadblocks"]:
                self.unlocked_mineshaft = False
            if "Castle" in args["slot_data"]["include_extra_roadblocks"]:
                self.unlocked_castle = False
            if "Graveyard" in args["slot_data"]["include_extra_roadblocks"]:
                self.unlocked_graveyard = False

            self.reset_timer = args["slot_data"]["reset_timer"]

            if args["slot_data"]["password_randomization"]:
                self.password_rando = True
                self.solved_password = args["slot_data"]["solved_password"]
                self.magic_word = args["slot_data"]["magic_word"]
                self.magic_symbol = args["slot_data"]["magic_symbol"]
                self.auto_solve_password = args["slot_data"]["auto_solve_password"]

            if not self.password_rando:
                self.show_magic_word = True
                self.show_magic_symbol = True

            self.update_password_tab()
                    
    # Receiving DeathLinks
    def on_deathlink(self, data):
        if not self.is_cat:
            if data["source"] != self.player_names[self.slot]:
                logger.info(data["cause"])
            self.WinTheGame.write_float(self.death_timer_address, 0.6)
            # Hacky and stupid but so is the rest of my code !! !
            if self.death_link_behavior == "reset":
                async def reset_after_60_ms():
                    await asyncio.sleep(0.6)
                    self.teleport_player_to_room(-3, 0, 76.0, 140.0) # You Have to Start the Game
                asyncio.create_task(reset_after_60_ms())
            
    def get_current_room_coords(self) -> tuple[int, int]:
        return (self.WinTheGame.read_int(self.room_x_address), self.WinTheGame.read_int(self.room_y_address))
    
    def get_player_coords(self) -> tuple[float, float]:
        return (round(self.WinTheGame.read_float(self.player_x_address), 1), round(self.WinTheGame.read_float(self.player_y_address), 1))

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

        elif "Letter" in item and item[-1] not in self.unlocked_letters:
            self.unlocked_letters += item[-1]
            self.update_password_tab()

        elif item == "Lose the Game" and self.resynced:
            self.teleport_player_to_room(-3, 0, 76.0, 140.0) # You Have to Start the Game
        elif item == "Stop Jumping Trap" and self.resynced:
            asyncio.create_task(self.apply_stop_jumping_trap())
        elif item == "Secret Room Trap" and self.resynced:
            if self.get_current_room_coords() not in SECRET_ROOM_COORDS:
                self.before_secret_room_data = (self.get_current_room_coords(), self.get_player_coords())
            self.teleport_player_to_room(3, -4, 73.0, 76.0) # Spiral Out
        elif item == "Freeze Trap" and self.resynced:
            asyncio.create_task(self.apply_room_speed_trap(0.0, self.freeze_trap_length))
        elif item == "Fast Trap" and self.resynced:
            asyncio.create_task(self.apply_room_speed_trap(4.0, self.fast_trap_length))

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

        elif item == "Reveal Magic Word":
            self.show_magic_word = True
            self.update_password_tab()
        elif item == "Reveal Magic Symbol":
            self.show_magic_symbol = True
            self.update_password_tab()

        elif item == "Playable Cat DLC*" and self.resynced:
            asyncio.create_task(self.become_cat())

        elif item == "Win the Game":
            self.finished_game = True

    async def become_cat(self):
        self.cat_stored_deaths = self.WinTheGame.read_int(self.deaths_address)
        self.WinTheGame.write_int(self.deaths_address, 0)
        await asyncio.sleep(1)
        self.WinTheGame.write_uchar(self.player_is_cat_address, 1)
        self.is_cat = True

    async def apply_stop_jumping_trap(self):
        max_jumps_value = self.WinTheGame.read_int(self.max_jumps_address)
        if max_jumps_value != 0:
            self.stored_max_jumps = max_jumps_value
            self.WinTheGame.write_int(self.max_jumps_address, 0)
            await asyncio.sleep(self.stop_jumping_trap_length)
            self.WinTheGame.write_int(self.max_jumps_address, self.stored_max_jumps)

    async def apply_room_speed_trap(self, speed: float, seconds: int):
        self.WinTheGame.write_float(self.room_speed_address, speed)
        await asyncio.sleep(seconds)
        self.WinTheGame.write_float(self.room_speed_address, 1.0)

    def teleport_player(self, player_x: float, player_y: float) -> None:
        self.WinTheGame.write_float(self.player_x_address, player_x)
        self.WinTheGame.write_float(self.player_y_address, player_y)

    def teleport_player_to_room(self, room_x: int, room_y: int, player_x: float, player_y: float) -> None:
        # the respawn location isnt necessarily bound to a bell and can be put anywhere.
        # i dont know how to hijack functions lmao
        self.WinTheGame.write_float(self.death_timer_address, 0.01)
        self.WinTheGame.write_int(self.respawn_room_x_address, room_x)
        self.WinTheGame.write_int(self.respawn_room_y_address, room_y)
        self.WinTheGame.write_float(self.respawn_player_x_address, player_x)
        self.WinTheGame.write_float(self.respawn_player_y_address, player_y)

    def get_latest_checkpoint(self) -> tuple[float, float, int, int]:
        return (self.WinTheGame.read_float(self.respawn_player_x_address), self.WinTheGame.read_float(self.respawn_player_y_address), 
                self.WinTheGame.read_int(self.respawn_room_x_address), self.WinTheGame.read_int(self.respawn_room_y_address))

    def update_password_tab(self) -> None:
        if getattr(self, "ui", None) is not None:
            self.ui.update_password_tab()

    # Yeah, I'll admit it. I vibecoded the shit out everything kivy related.
    # None of the assets are generative AI, those are from the game itself.
    def make_gui(self):
        class NotConnectedLayout(BoxLayout):
            ctx: WinTheGameContext

            def __init__(self, ctx: WinTheGameContext) -> None:
                super().__init__(orientation="horizontal", size_hint_y=0.12)
                self.ctx = ctx
                self.add_widget(Label(text="Not connected to Archipelago.", font_size="30dp"))

            def show(self):
                self.opacity = 1.0
                self.size_hint_y = 0.12
                self.disabled = False

            def hide(self):
                self.opacity = 0.0
                self.size_hint_y = None
                self.height = "0dp"
                self.disabled = True

        class ConnectedLayout(BoxLayout):
            ctx: WinTheGameContext

            def __init__(self, ctx: WinTheGameContext) -> None:
                self.ctx = ctx
                super().__init__(orientation="vertical", size_hint_y=0.12)
                self.letters_label = Label(
                    text="Unlocked Letters:",
                    font_size="30dp",
                    halign="center",
                    valign="middle",
                    text_size=(None, None),
                    markup=True
                )
                self.add_widget(self.letters_label)

                self.magic_row = BoxLayout(
                    orientation="horizontal",
                    size_hint=(None, None),
                    size=("340dp", "96dp"),
                    spacing="15dp",
                    pos_hint={"center_x": 0.5}
                )

                self.magic_word_box = AnchorLayout(
                    size_hint=(None, None),
                    size=("140dp", "96dp"),
                    anchor_x="center",
                    anchor_y="center"
                )
                self.magic_word_content = BoxLayout(
                    orientation="vertical",
                    size_hint=(None, None),
                    size=("140dp", "48dp"),
                    spacing="6dp"
                )
                self.magic_word_label = Label(
                    font_size="30dp",
                    color=(0.925, 0.384, 0.969, 1),
                    size_hint=(1, None),
                    height="25dp",
                    halign="center",
                    valign="middle"
                )
                self.magic_word_content.add_widget(self.magic_word_label)
                self.magic_word_image = Image(
                    source=os.path.join(os.path.dirname(__file__), "assets", "word_line.png"),
                    size_hint=(1, None),
                    height="25dp",
                    allow_stretch=True,
                    keep_ratio=True,
                    opacity=0
                )
                self.magic_word_content.add_widget(self.magic_word_image)
                self.magic_word_box.add_widget(self.magic_word_content)

                self.magic_symbol_box = AnchorLayout(
                    size_hint=(None, None),
                    size=("160dp", "96dp"),
                    anchor_x="center",
                    anchor_y="center"
                )
                self.magic_symbol_content = BoxLayout(
                    orientation="horizontal",
                    size_hint=(None, None),
                    size=("144dp", "48dp"),
                    spacing="0dp"
                )
                self.magic_symbol_left_image = Image(
                    source=os.path.join(os.path.dirname(__file__), "assets", "magic_symbol_left.png"),
                    size_hint=(None, None),
                    size=("48dp", "48dp"),
                    allow_stretch=True,
                    keep_ratio=True,
                    opacity=0
                )
                self.magic_symbol_label = Label(
                    font_size="36dp",
                    color=(0.925, 0.384, 0.969, 1),
                    size_hint=(None, None),
                    size=("36dp", "40dp"),
                    halign="center",
                    valign="middle",
                    text=""
                )
                self.magic_symbol_label.bind(size=self.magic_symbol_label.setter('text_size'))
                self.magic_symbol_right_image = Image(
                    source=os.path.join(os.path.dirname(__file__), "assets", "magic_symbol_right.png"),
                    size_hint=(None, None),
                    size=("48dp", "48dp"),
                    allow_stretch=True,
                    keep_ratio=True,
                    opacity=0
                )
                self.magic_symbol_content.add_widget(self.magic_symbol_left_image)
                self.magic_symbol_content.add_widget(self.magic_symbol_label)
                self.magic_symbol_content.add_widget(self.magic_symbol_right_image)
                self.magic_symbol_box.add_widget(self.magic_symbol_content)

                self.magic_row.add_widget(self.magic_word_box)
                self.magic_row.add_widget(self.magic_symbol_box)
                self.add_widget(self.magic_row)

                self.auto_password_label = Label(
                    font_size="30dp",
                    halign="center",
                    valign="middle",
                    text_size=(None, None)
                )
                self.add_widget(self.auto_password_label)

            def show(self):
                self.opacity = 1.0
                self.size_hint_y = 0.12
                self.disabled = False

            def hide(self):
                self.opacity = 0.0
                self.size_hint_y = None
                self.height = "0dp"
                self.disabled = True

            def update(self):
                unlocked_letters_text = "Unlocked Letters:\n"
                for letter in sorted(self.ctx.unlocked_letters):
                    color = "ffffff"
                    if letter in self.ctx.solved_password:
                        color = "ec62f7"
                    unlocked_letters_text += f"[color={color}]{letter} [/color]"
                self.letters_label.text = unlocked_letters_text
                if self.ctx.show_magic_word:
                    self.magic_word_label.text = self.ctx.magic_word
                    self.magic_word_image.opacity = 1
                if self.ctx.show_magic_symbol:
                    self.magic_symbol_left_image.opacity = 1
                    self.magic_symbol_right_image.opacity = 1
                    self.magic_symbol_label.text = str(abs(self.ctx.magic_symbol))
                    if self.ctx.magic_symbol < 0:
                        self.magic_symbol_left_image.source = os.path.join(os.path.dirname(__file__), "assets", "magic_symbol_left_alt.png")
                        self.magic_symbol_right_image.source = os.path.join(os.path.dirname(__file__), "assets", "magic_symbol_right_alt.png")

                password_check = True
                for letter in self.ctx.solved_password:
                    if letter not in self.ctx.unlocked_letters:
                        password_check = False
                        break
                if self.ctx.show_magic_word and self.ctx.show_magic_symbol and password_check and self.ctx.auto_solve_password:
                    self.auto_password_label.text = f"Password:\n{self.ctx.solved_password}"

        class PasswordTabLayout(BoxLayout):
            ctx: WinTheGameContext
            layout_not_connected: NotConnectedLayout

            def __init__(self, ctx: WinTheGameContext) -> None:
                super().__init__(orientation="vertical", padding="8dp")

                self.ctx = ctx
                self.layout_not_connected = NotConnectedLayout(self.ctx)
                self.add_widget(self.layout_not_connected)
                self.layout_connected = ConnectedLayout(self.ctx)
                self.add_widget(self.layout_connected)
                self.layout_connected.hide()

            def update(self) -> None:
                if self.ctx.connected:
                    self.layout_connected.show()
                    self.layout_not_connected.hide()
                    self.layout_connected.update()
                else:
                    self.layout_connected.hide()
                    self.layout_not_connected.show()

        ui = super().make_gui() # For UT
        class WinTheGameGameManager(ui):
            ctx: WinTheGameContext
            base_title = "You Have to Win the Game Client"
            password_layout: PasswordTabLayout
            password_tab: Widget

            def build(self) -> Layout:
                container = super().build()
                self.password_layout = PasswordTabLayout(self.ctx)
                self.password_tab = self.add_client_tab("Password", self.password_layout)
                return container
            
            def update_password_tab(self) -> None:
                self.password_layout.update()
            
        return WinTheGameGameManager
    # AI slop over. Back to your regularly scheduled human slop.

    async def disconnect(self):
        try:
            if self.split_spider_gloves:
                self.WinTheGame.write_uchar(self.on_wall_address, 0)
                self.WinTheGame.write_uchar(self.can_wall_jump_address, 0)
            if self.is_cat:
                self.remove_cat_status()
        except:
            pass
        await super().disconnect()

    def remove_cat_status(self):
        self.WinTheGame.write_uchar(self.player_is_cat_address, 0)
        self.WinTheGame.write_int(self.deaths_address, self.cat_stored_deaths)
        self.is_cat = False


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
            await asyncio.sleep(1)
            continue

        if not ctx.connected:
            await asyncio.sleep(1)
            continue

        current_room = ctx.get_current_room_coords()
        in_secret_rooms = current_room in SECRET_ROOM_COORDS

        deaths = ctx.WinTheGame.read_int(ctx.deaths_address)
        if ctx.is_cat and deaths == 9:
            ctx.remove_cat_status()
        elif ctx.death_link_active:
            if "DeathLink" not in ctx.tags:
                await ctx.update_death_link(True)
            if deaths > 0 and deaths % ctx.death_link_amnesty == 0 and deaths != ctx.last_death_link:
                nth = lambda n: f"{n}{'th' if 10 <= n % 100 <= 20 else {1:'st', 2:'nd', 3:'rd'}.get(n % 10, 'th')}"
                await ctx.send_death(f"{ctx.player_names[ctx.slot]} died for the {nth(deaths)} time while traversing {COORDS_TO_ROOM_NAME[current_room][:-13]}.")
                ctx.last_death_link = deaths

        locations = []
        treasures_found = ctx.WinTheGame.read_int(ctx.treasures_found_address)
        if ctx.cached_treasure_found != treasures_found:
            ctx.cached_treasure_found = treasures_found
            # The address of the vector is dynamic.
            treasure_vector = ctx.WinTheGame.read_int(ctx.treasure_vector_address)
            # I would like treasures to send out missing checks on disconnect/reconnect, since they disappear in the world after collection.
            for i in range(treasures_found):
                locations.append(ctx.WinTheGame.read_int(treasure_vector + 4 * i) + 1)
        if ctx.WinTheGame.read_int(ctx.times_won_address) != 0: #GOAL
            locations.append(99)
        # These next check types are checked once unlike the treasures. 
        # This means that any rooms explored or bells rung before connecting to Archipelago wont be saved.
        try:
            if ctx.room_sanity and ctx.cached_last_room != current_room: 
                locations.append(LOCATION_IDS[COORDS_TO_ROOM_NAME[current_room]])
                ctx.cached_last_room = current_room
            if ctx.bell_sanity:
                latest_checkpoint = ctx.get_latest_checkpoint()
                bell = COORDS_TO_BELL_NAME[latest_checkpoint]
                if ctx.cached_last_bell != bell:
                    ctx.cached_last_bell = bell
                    locations.append(LOCATION_IDS[bell])
        except KeyError: # Cases are secret rooms, starting the game.
            pass
        if len(locations) != 0:
            await ctx.check_locations(locations)

        times_lost: int = ctx.WinTheGame.read_int(ctx.times_lost_address)
        amount_of_received_items = len(ctx.items_received)
        if amount_of_received_items == 0:
            ctx.resynced = True
        else:
            if not ctx.resynced:
                amount_of_received_items = times_lost
                times_lost = 0
            if times_lost < amount_of_received_items:
                while times_lost < amount_of_received_items:
                    ctx.give_item(ID_TO_ITEM[ctx.items_received[times_lost].item])
                    times_lost += 1
                ctx.WinTheGame.write_int(ctx.times_lost_address, times_lost)
                if not ctx.resynced:
                    ctx.resynced = True

        if ctx.split_spider_gloves:
            left_check = ctx.has_left_glove and ctx.WinTheGame.read_uchar(ctx.player_face_left_address) == 1
            right_check = ctx.has_right_glove and ctx.WinTheGame.read_uchar(ctx.player_face_left_address) == 0
            if left_check and right_check:
                ctx.split_spider_gloves = False
                ctx.WinTheGame.write_uchar(ctx.spider_gloves_address, 1)
                ctx.WinTheGame.write_uchar(ctx.can_wall_jump_address, 1)
            elif left_check or right_check:
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

        if current_room == (-6, 2) and not ctx.unlocked_quarry: # The Quarry Hub
            if ctx.WinTheGame.read_float(ctx.player_y_address) > 42.0:
                ctx.WinTheGame.write_float(ctx.player_y_address, 41.8)
        elif (current_room == (-5, 5) or current_room == (-4, 5)) and not ctx.unlocked_mineshaft: # Mine Shaft or Green Man
            if ctx.WinTheGame.read_float(ctx.player_y_address) > 170.0 and ctx.WinTheGame.read_float(ctx.player_x_address) < 188.0:
                ctx.WinTheGame.write_float(ctx.player_x_address, 20.0)
                ctx.WinTheGame.write_float(ctx.player_y_address, 110.0)
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
                # Placing the player directly on the portal coordinates actually doesn't work. Need to place slightly higher.
                ctx.teleport_player(272.0, 110.0)
        elif current_room == (1, -4) and ctx.password_rando: # Warp Right
            room_name = re.sub(r'[^A-Z]', "", ctx.WinTheGame.read_string(ctx.room_name_address, 50))
            await asyncio.sleep(3)
            if room_name == ctx.solved_password:
                ctx.teleport_player_to_room(-1, -2, 160.0, 80.0) # Open Sesame
            else:
                ctx.teleport_player_to_room(-1, -3, 160.0, 80.0) # Speak Now...
            

        # Player anti-softlock.
        if ctx.WinTheGame.read_uchar(ctx.player_crouching_address) and not in_secret_rooms:
            crouch_time += 1
        else:
            crouch_time = 0
        if crouch_time >= ctx.reset_timer:
            ctx.teleport_player_to_room(-3, 0, 76.0, 140.0) # You Have to Start the Game

        if ctx.finished_game and not ctx.informed_server:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.informed_server = True

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
