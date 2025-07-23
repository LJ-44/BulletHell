import pygame
import math
import sprites as sprt

#TODO: Make this into a bullet hell type game

def main():
    # constants
    FPS = 60
    BULLET_SPAWN_RATE = 25 # bullets spawning per second
    BULLET_SPAWN_RATE = math.floor(FPS / BULLET_SPAWN_RATE)
    
    # pygame initialization stuff
    pygame.init()
    resolution = (1280, 720)
    screen = pygame.display.set_mode(size=resolution)
    pygame.display.set_caption("Bullet Hell")
    clock = pygame.time.Clock()
    running = True

    # instantiating sprites / sprite groups
    player_group = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()
    player = sprt.Player()
    player_group.add(player)

    # counters / flags
    bullet_spawn_timer = 0
    hits = 0

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # spawn bullets based on chosen spawn rate
        bullet_spawn_timer += 1
        if bullet_spawn_timer == BULLET_SPAWN_RATE:
            normal_bullet = sprt.Bullet(left=True, right=True, top=True, bottom=True)
            bullets_group.add(normal_bullet)
            bullet_spawn_timer = 0

        player_group.update()
        bullets_group.update()

        # Counts number of times a unique bullet hits the player
        for bullet in bullets_group:
            if (pygame.sprite.collide_rect(player, bullet) and not getattr(bullet, 'hit', False)):
                hits += 1
                bullet.hit = True
                print(f'Hits: {hits}')

        screen.fill('black')
        
        player_group.draw(screen)
        bullets_group.draw(screen)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__': main()