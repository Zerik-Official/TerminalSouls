"""
This module contains common utility functions that are used throughout the game. 
These functions include determining the appropriate backend for the game engine based on the operating system and creating a generic loading animation in the terminal.
"""

# Library imports
import os
import time

def get_engine_backend() -> tuple[bool, str]:
    """
    Method to determinate the appropriate backend for the game engine based on the operating system. 
    If the platform is Windows, it returns "edge", if it's Linux, it returns "qt", if it's macOS, it returns "cocoa".
    If the platform is not supported, it returns "unsupported".

    Args:
        None
    Returns:
        tuple[bool, str]: A tuple containing a boolean indicating whether the backend is supported and a string indicating the backend to use.
    """
    
    platform: str = os.sys.platform

    if platform.startswith("win"):
        return True, "edge"
    elif platform.startswith("linux"):
        return True, "qt"
    elif platform.startswith("darwin"):
        return True, "cocoa"
    else:
        return False, "unsupported"


def generic_animation_load(message:str, points:int, wait_duration: int | float | None = 0.7) -> None:
    """
    Function to create a generic loading animation in the terminal. It takes a message, the number of points to display, and the duration to wait between each point.
    Args:
        message (str): The message to display before the loading animation.
        points (int): The number of points to display in the loading animation.
        wait_duration (int | float | None): The duration to wait between each point in seconds. Default is 0.7 seconds.
    Returns:
        None
    """

    print(f"{message}", end="", flush=True)
    for _ in range(points):
        print(".", end="", flush=True)
        time.sleep(wait_duration)
    
    print()