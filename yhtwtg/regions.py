from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region

if TYPE_CHECKING:
    from .world import WinTheGameWorld

def create_regions(world: WinTheGameWorld) -> None:
    starting_area = Region("Starting Area", world.player, world.multiworld)
    teleporter_area = Region("Teleporter Area", world.player, world.multiworld)
    castle_area_outer = Region("Castle Area Outer", world.player, world.multiworld)
    castle_area_inner = Region("Castle Area Inner", world.player, world.multiworld)
    end_game_area = Region("End Game Area", world.player, world.multiworld)

    regions = [starting_area, teleporter_area, castle_area_outer, castle_area_inner, end_game_area]
    world.multiworld.regions += regions

    starting_area.connect(teleporter_area, "Starting Area to Teleporter Area", lambda state: state.has_any(("Crimson Aura", "Springheel Boots", "Spider Gloves"), world.player))
    starting_area.connect(castle_area_outer, "Starting Area to Castle Area Outer", lambda state: state.has_all(("Crimson Aura", "Springheel Boots", "Spider Gloves"), world.player))
    castle_area_outer.connect(castle_area_inner, "Castle Area Outer to Castle Area Inner", lambda state: state.has("Spider Gloves", world.player))
    starting_area.connect(end_game_area, "Starting Area to End Game Area", lambda state: state.has_all(("Springheel Boots", "Spider Gloves"), world.player))
