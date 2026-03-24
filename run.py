"""
This is the main entry point for the Terminal Souls game. 
It initializes the game engine, detects the appropriate backend for the GUI based on the operating system, 
and starts the GUI. The script also includes a logo and some loading animations to enhance the user experience when launching the game.
"""
# Libraries
import time
from colorama import init, Style, Fore

# Internal modules
from gui import init_gui
from utils import (
    get_engine_backend, generic_animation_load
)

init()

logo: str = r"""
████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗         ███████╗ ██████╗ ██╗   ██╗██╗     ███████╗
╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║         ██╔════╝██╔═══██╗██║   ██║██║     ██╔════╝
   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║         ███████╗██║   ██║██║   ██║██║     ███████╗
   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║         ╚════██║██║   ██║██║   ██║██║     ╚════██║
   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗    ███████║╚██████╔╝╚██████╔╝███████╗███████║
   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝    ╚══════╝ ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
"""

if __name__ == "__main__":
    print(logo)
    generic_animation_load(f"[{Fore.GREEN}INFO{Style.RESET_ALL}] Detecting operating system and appropriate backend for the game engine", 3)
    supported, backend = get_engine_backend()
    if not supported:
        print(f"[{Fore.RED}ERROR{Style.RESET_ALL}] The operating system is not compatible with the game engine.")
        exit(1)
    
    generic_animation_load(f"[{Fore.GREEN}INFO{Style.RESET_ALL}] Initializing the GUI with the {backend} backend", 3)

    init_gui(backend, False)