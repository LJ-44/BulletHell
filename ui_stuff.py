import pygame
import pygame_gui as GUI
from pygame_gui import PackageResource
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton, UILabel
import src.sound as sound

pygame.mixer.pre_init()
pygame.mixer.init()
sound.play_music()
pygame.init()

pygame.display.set_caption('Quick Start')
screen = pygame.display.set_mode((800, 600))

manager = GUI.UIManager((800, 600), theme_path=PackageResource(package="data.themes",
                                                               resource="bullet_hell_theme.json"))

title = UILabel(relative_rect=pygame.Rect((screen.get_width() / 2, screen.get_height() * 0.3), (100, 50)),
                              text="BULLET HELL",
                              manager=manager,
                              object_id=ObjectID(class_id="@titles",
                                                 object_id="#game_title"))
        
one_player_button = UIButton(relative_rect=pygame.Rect((screen.get_width() / 2, screen.get_height() * 0.4), (100, 50)),
                                    text="ONE PLAYER MODE",
                                    manager=manager,
                                    object_id=ObjectID(class_id="@buttons",
                                                 object_id="#one_player_button"))

two_player_button = UIButton(relative_rect=pygame.Rect((screen.get_width() / 2, screen.get_height() * 0.5), (100, 50)), 
                                    text="TWO PLAYER MODE",
                                    manager=manager,
                                    object_id=ObjectID(class_id="@buttons",
                                                 object_id="#two_player_button"))

settings_button = UIButton(relative_rect=pygame.Rect((screen.get_width() / 2, screen.get_height() * 0.6), (100, 50)),
                                text="SETTINGS",
                                manager=manager,
                                object_id=ObjectID(class_id="@buttons",
                                                 object_id="#settings_button"))

quit_button = UIButton(relative_rect=pygame.Rect((screen.get_width() / 2, screen.get_height() * 0.7), (100, 50)),
                            text="QUIT",
                            manager=manager,
                            object_id=ObjectID(class_id="@buttons",
                                                 object_id="#quit_button"))

clock = pygame.time.Clock()
running = True
while running:
    dt = clock.tick(60)/1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        manager.process_events(event)
        
        if event.type == GUI.UI_BUTTON_PRESSED:
            if event.ui_element == one_player_button:
                print("one_player")
            elif event.ui_element == two_player_button:
                print("two_player")
            elif event.ui_element == settings_button:
                print("settings")
            elif event.ui_element == quit_button:
                print("quit")
                
    screen.fill("black")
        
    manager.update(dt)
    manager.draw_ui(screen)

    pygame.display.update()    