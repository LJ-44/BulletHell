import pygame
import pygame_gui as GUI
from pygame_gui.elements import UIButton, UITextBox
from pygame.locals import *

pygame.init()

pygame.display.set_caption('Quick Start')
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
screen = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color("#000000"))

manager = GUI.UIManager((800, 600), theme_path="data/themes/bullet_hell_theme.json")
manager.add_font_paths(font_name="Bullet_Hell", regular_path="assets/font/BulletHell_font.ttf")

button = UIButton(relative_rect=pygame.Rect((350, 275), (100,50)),
                               text="Hello",
                               manager=manager,)
title = UITextBox(relative_rect=pygame.Rect((250, 175), (100,50)), 
                  html_text="BULLET HELL", 
                  manager=manager)

title.set_active_effect(GUI.TEXT_EFFECT_FADE_IN)

clock = pygame.time.Clock()
running = True
while running:
    dt = clock.tick(60)/1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        manager.process_events(event)
        
        if event.type == GUI.UI_BUTTON_PRESSED:
            if event.ui_element == button:
                print("Hello")
        
    manager.update(dt)

    screen.blit(background, (0, 0))
    manager.draw_ui(screen)

    pygame.display.update()