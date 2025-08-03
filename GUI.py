import random
import pygame_gui
from typing import Optional, Any
from pygame_gui import UIManager, PackageResource
from pygame_gui.elements import *
from pygame_gui.windows import UIMessageWindow
from pygame_gui.core import ObjectID
import pygame
from pygame.sprite import Sprite, Group
from pygame.locals import *
import src.sound as sound

class Resolution:
    def __init__(self):
        self.resolution = (1280, 720)
        self.fullscreen = False
        
# old run_game.py code:

# pygame.mixer.pre_init()
# pygame.mixer.init()
# sound.play_music()
# pygame.init()

# pygame.display.set_caption('Quick Start')
# monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
# screen = pygame.display.set_mode((800, 600))

# manager = GUI.UIManager((800, 600), theme_path="data/themes/bullet_hell_theme.json")

# title = UIButton(relative_rect=pygame.Rect((screen.get_width() / 2, screen.get_height() * 0.3), (100, 50)),
#                               text="BULLET HELL",
#                               manager=manager)
        
# one_player_button = UIButton(relative_rect=pygame.Rect((screen.get_width() / 2, screen.get_height() * 0.4), (100, 50)),
#                                     text="ONE PLAYER MODE",
#                                     manager=manager)

# two_player_button = UIButton(relative_rect=pygame.Rect((screen.get_width() / 2, screen.get_height() * 0.5), (100, 50)), 
#                                     text="TWO PLAYER MODE",
#                                     manager=manager)

# settings_button = UIButton(relative_rect=pygame.Rect((screen.get_width() / 2, screen.get_height() * 0.6), (100, 50)),
#                                 text="SETTINGS",
#                                 manager=manager)

# quit_button = UIButton(relative_rect=pygame.Rect((screen.get_width() / 2, screen.get_height() * 0.7), (100, 50)),
#                             text="QUIT",
#                             manager=manager)

# clock = pygame.time.Clock()
# running = True
# while running:
#     dt = clock.tick(60)/1000.0
    
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         manager.process_events(event)
        
#         if event.type == GUI.UI_BUTTON_PRESSED:
#             if event.ui_element == one_player_button:
#                 print("one_player")
#             elif event.ui_element == two_player_button:
#                 print("two_player")
#             elif event.ui_element == settings_button:
#                 print("settings")
#             elif event.ui_element == quit_button:
#                 print("quit")
                
#     screen.fill("black")
        
#     manager.update(dt)
#     manager.draw_ui(screen)

#     pygame.display.update()    