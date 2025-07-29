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


def play_music(path=theme, volume=0.4):
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1) # loop music

def stop_music():
    pygame.mixer.music.stop()

def play_hit_sound(path=hit_sound, volume=1.0):
    sound = pygame.mixer.Sound(path)
    sound.set_volume(volume)
    sound.play()

def play_death_sound(path=death_sound, volume=1.0):
    sound = pygame.mixer.Sound(path)
    sound.set_volume(volume)
    sound.play()

def play_normal_bullet_sound(path=normal_bullet_sound, volume=1.0):
    sound = pygame.mixer.Sound(path)
    sound.set_volume(volume)
    sound.play()

def play_homing_bullet_sound(path=homing_bullet_sound, volume=1.0):
    sound = pygame.mixer.Sound(path)
    sound.set_volume(volume)
    sound.play()

def play_exploding_bullet_sound(path=exploding_bullet_sound, volume=1.0):
    sound = pygame.mixer.Sound(path)
    sound.set_volume(volume)
    sound.play()

def play_button_hover_sound(path=button_hover_sound, volume=0.5):
    sound = pygame.mixer.Sound(path)
    sound.set_volume(volume)
    sound.play()

def play_button_clicked_sound(path=button_clicked_sound, volume=0.5):
    sound = pygame.mixer.Sound(path)
    sound.set_volume(volume)
    sound.play()