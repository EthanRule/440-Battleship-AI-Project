from colorama import Fore
import pygame
def initMusic():
    pygame.mixer.init()
    pygame.mixer.music.load("Strategy Background Music  No Copyright Music  Free Music.mp3") # https://www.youtube.com/watch?v=BMGWF6U6d7c 
    pygame.mixer.music.play(-1)  # loop indefinitely
    pygame.mixer.music.set_volume(0.01)