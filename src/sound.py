import pygame

theme = "assets/audio/Adventure-Time_Manlorette-Party.wav"

def play_music(path=theme, volume=1.0):
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)