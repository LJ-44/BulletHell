import pygame

theme = "assets/audio/Adventure-Time_Manlorette-Party.wav"

# TODO: add sound files below 

hit_sound = " "
death_sound = " "
normal_bullet_sound = " "
homing_bullet_sound = " "
exploding_bullet_sound = " "
button_hover_sound = " "
button_clicked_sound = " "


def play_music(path=theme, volume=0.5):
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1) # loop music

def stop_music():
    pygame.mixer.music.stop()

def play_sound_effect(path="assets/audio/", volume = 1.0):
    sound = pygame.mixer.Sound(path)
    sound.set_volume(volume)
    sound.play()