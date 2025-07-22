import pygame
import math
import sprites as sprt

#TODO: Make this into a bullet hell type game

def main():
    pygame.init()

    FPS = 60
    BULLET_SPAWN_RATE = 1 # bullets spawning per second




    resolution = (1280, 720)
    screen = pygame.display.set_mode(size=resolution)
    pygame.display.set_caption("Bullet Hell")
    clock = pygame.time.Clock()
    running = True

    player_group = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()

    player = sprt.Player()

    player_group.add(player)

    bullet_spawn_timer = 0

    hits = 0

    BULLET_SPAWN_RATE = math.floor(FPS / BULLET_SPAWN_RATE)

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # spawn bullets based on chosen spawn rate
        bullet_spawn_timer += 1
        if bullet_spawn_timer == BULLET_SPAWN_RATE:
            basic_bullet = sprt.Bullet()
            bullets_group.add(basic_bullet)
            bullet_spawn_timer = 0

        player_group.update()
        bullets_group.update()

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