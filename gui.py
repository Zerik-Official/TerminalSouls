"""
This module is responsible for initializing and running the graphical user interface (GUI) of the Terminal Souls game. 
It uses the webview library to create a window that loads the game's HTML interface. 
The module also integrates with the game engine to allow interaction between the GUI and the game's logic.
"""
# Library imports
import os
import webview

# Internal modules
from gameEngine import GameEngine

# Initialize the game engine
engine: GameEngine = GameEngine()

# Allow loading local files in the webview, which is necessary to load the game's HTML interface from the templates folder.
webview.settings['ALLOW_FILE_URLS'] = True

def init_gui(gui_platform: str, dev_mode: bool = False) -> None:
    """
    Function to initialize the GUI of the game using the specified backend. It creates a webview window and starts the GUI loop.

    Args:
        gui_platform (str): The backend to use for the GUI. It can be "edge", "qt", or "cocoa".
        dev_mode (bool): A boolean indicating whether to start the GUI in development mode with debug enabled. Default is False.
    Returns:
        None
    """

    game_interface_path: str = os.path.abspath("templates/index/index.html").replace("\\", "/")
    
    window: webview.Window = webview.create_window(
        'TerminalSouls', 
        url=f"file:///{game_interface_path}", 
        js_api=engine,
        width=1200,
        height=740,
        minimized=False,
        maximized=False
        )
    
    webview.start(
        gui=gui_platform, 
        debug=dev_mode
        )