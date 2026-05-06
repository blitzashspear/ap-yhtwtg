from worlds.LauncherComponents import Component, Type, components, launch as launch_component, icon_paths

def launch_client() -> None:
    from .client import launch
    launch_component(launch, name="WinTheGameClient")

components.append(
    Component(
        display_name="You Have to Win the Game Client",
        script_name="WinTheGameClient",
        func=launch_client,
        game_name="You Have to Win the Game",
        component_type=Type.CLIENT,
        icon="wintheicon",
    )
)

icon_paths["wintheicon"] = f"ap:{__name__}/icons/wintheicon.png"
