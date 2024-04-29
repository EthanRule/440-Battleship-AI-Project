from colorama import Fore
import pygame

def initMusic():
    """
    Initialize and play background music.

    This function initializes the pygame mixer and loads the background music file.
    The music is played indefinitely and the volume is set to 0.01.

    """
    pygame.mixer.init()
    pygame.mixer.music.load("Strategy Background Music  No Copyright Music  Free Music.mp3")
    # Source: https://www.youtube.com/watch?v=BMGWF6U6d7c 
    pygame.mixer.music.play(-1)  # loop indefinitely
    pygame.mixer.music.set_volume(0.01)
