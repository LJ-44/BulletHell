import pygame
from math import floor
import sprites as sprt

#TODO
# right now:
# ( ) homing bullet
    # ( ) easy version - fire towards player's center position when spawned
    # ( ) hard version - fire towards player continually tracking player's position
# ( ) exploding bullet
    # ( ) get bullet to explode into shrapnel, shrapnel-player collision
    # ( ) fire towards player, explode when near player
# ( ) lives counter
# ( ) death system
# later:
# ( ) title screen
    # ( ) singleplayer mode 
    # ( ) 2 player mode
        # players choose their own color
        # whoever dies (or runs out of lives) first loses
    # ( ) difficulties
        # easy - left/right walls only, low spawn rate
        # medium - left/right/top walls, medium spawn rate
        # hard - all edges, high spawn rate
        # insane - all edges, very high spawn rate
        # hell - all edges, extremely high spawn rate
# ( ) high score
    # save score into file by read/write (text file?)
    # score = seconds survived * 10 
# ( ) death system
    # game over screen
    # 
# ( ) sound effects - 8 bit
# ( ) music - 8 bit (MANLORETTE PARTY - ADVENTURE TIME)
#TODO

def main():
    # constants
    FPS = 60
    BULLET_SPAWN_RATE = 1 # per second
    BULLET_SPAWN_RATE = floor(FPS / BULLET_SPAWN_RATE)
    
    # display
    pygame.init()
    resolution = (1280, 720)
    screen = pygame.display.set_mode(size=resolution)
    pygame.display.set_caption("Bullet Hell")
    clock = pygame.time.Clock()
    running = True

    # sprites
    player_group = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()
    player = sprt.Player()
    player_group.add(player)

    # variables
    bullet_spawn_timer = 0
    hits = 0

    running = True
    while running:

        # Exit pygame if user clicks X on game window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # spawn bullets based on chosen spawn rate
        bullet_spawn_timer += 1
        if bullet_spawn_timer == BULLET_SPAWN_RATE:
            normal_bullet = sprt.Bullet(left=True, right=True, top=True, bottom=True)
            homing_bullet = sprt.HomingBullet(target=player)
            bullets_group.add(normal_bullet, homing_bullet)
            bullet_spawn_timer = 0

        # update sprite positions
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