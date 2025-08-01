import pygame
from pygame.locals import *

pygame.init()
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
screen = pygame.display.set_mode((500, 500), RESIZABLE)
clock = pygame.time.Clock()
#pic = pygame.image.load("assets/images/megaman.png")  # You need an example picture in the same folder as this file!

fullscreen = False
running = True
while running:
    
    screen.fill('blue')
    
    pygame.draw.rect(surface=screen,
                     color='black',
                     rect=pygame.Rect((screen.get_width() / 2, screen.get_height() / 2), (10, 10)))
    
    pygame.event.pump()
    event = pygame.event.wait()
    if event.type == QUIT:
        running = False
    elif event.type == KEYDOWN:
        if event.key == K_ESCAPE:
            running = False
        elif event.key == K_f:
            fullscreen = not fullscreen
            if fullscreen:
                screen = pygame.display.set_mode(monitor_size, FULLSCREEN)
            else:
                screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), RESIZABLE)
    elif event.type == VIDEORESIZE:
        if not fullscreen:
            screen = pygame.display.set_mode((event.w, event.h), RESIZABLE)
        
    pygame.display.update()
    clock.tick(60)
        
pygame.quit()