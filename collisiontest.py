import pygame
import math
from menu import *
import sprites as sprt

FPS = 60
    
# display
pygame.init()
resolution = (1280, 720)
screen = pygame.display.set_mode(size=resolution)
pygame.display.set_caption("Collision Test")
clock = pygame.time.Clock()

# sprites
player_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()

# variables
normal_bullet_spawn_rate = 10 # bullets per second
frame_count = 0

player_one_hits = 0

one_player_mode = True
two_player_mode = False

running = True
while running:
    
    frame_count += 1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill('black')
    
    if one_player_mode:

        if frame_count % math.floor(FPS / normal_bullet_spawn_rate) == 0:
            normal_bullet = sprt.Bullet(left=True, right=True, top=True, bottom=True)
            bullets_group.add(normal_bullet)

        for bullet in bullets_group:
            if (pygame.sprite.collide_rect(player_one, bullet) and not getattr(bullet, 'hit_player_one', False)):
                player_one_hits += 1
                bullet.hit_player_one = True
                print(f'Player One Hit: {player_one_hits}')
    
    
        
    player_group.update()
    bullets_group.update()
    
    player_group.draw(screen)
    bullets_group.draw(screen)
    
    pygame.display.flip()
    clock.tick(FPS)
            
    