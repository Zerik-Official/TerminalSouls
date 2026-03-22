
# Library imports
import webview

# Internal modules
from gameEngine import GameEngine

# Initialize the game engine
engine: GameEngine = GameEngine()

def init_gui(gui_platform: str, dev_mode: bool = False) -> None:
    """
    Function to initialize the GUI of the game using the specified backend. It creates a webview window and starts the GUI loop.

    Args:
        gui_platform (str): The backend to use for the GUI. It can be "edge", "qt", or "cocoa".
        dev_mode (bool): A boolean indicating whether to start the GUI in development mode with debug enabled. Default is False.
    Returns:
        None
    """
    
    window: webview.Window = webview.create_window('TerminalSouls', url='templates/index/index.html', js_api=engine)
    webview.start(gui=gui_platform, debug=dev_mode)