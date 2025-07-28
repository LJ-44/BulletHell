import pygame

def play_music(path="assets/audio/Adventure-Time_Manlorette-Party.mp3", volume=0.5):
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1) # loop music

def stop_music():
    pygame.mixer.music.stop()

def play_sound_effect(path="assets/audio/", volume = 1.0):
    sound = pygame.mixer.Sound(path)
    sound.set_volume(volume)
    sound.play()