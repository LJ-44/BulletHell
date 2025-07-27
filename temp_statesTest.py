import pygame
import sys
import math
from menu import *
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
    
    # display
    pygame.init()
    resolution = (800, 600)
    screen = pygame.display.set_mode(size=resolution)
    pygame.display.set_caption("Bullet Hell")
    clock = pygame.time.Clock()
    running = True
    
    # screens
    main_menu = MainMenu()
    pause_screen = PauseScreen()
    difficulty_screen = DifficultyScreen()

    # sprites
    player_group = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()
    player_one = sprt.Player()
    player_two = sprt.Player()
    player_group.add(player_one)

    # variables
    bullet_spawn_rate = 2 # bullets per second
    bullet_spawn_rate = math.floor(FPS / bullet_spawn_rate)
    lives = 3
    frame_count = 0
    count = 0
    hits = 0
    
    # initial states
    game_state = GameState.MAIN_MENU
    player_mode = None
    difficulty = None

    running = True
    while running:
        
        frame_count += 1
        
        # --------------------
        # Handle events first
        # --------------------

        mouse_up = False
        mouse_pos = pygame.mouse.get_pos()
        
        # Exit if user clicks X on window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game_state == GameState.GAMEPLAY:
                        game_state = GameState.PAUSED
                    elif game_state == GameState.PAUSED:
                        game_state = GameState.GAMEPLAY
                
        screen.fill('black')
        
        # --------------------
        # Update based on game state
        # --------------------
        
        if game_state == GameState.MAIN_MENU:
            # main menu buttons
            for ui_element in main_menu.ui_elements:
                action = ui_element.update(mouse_pos, mouse_up)
                if action is not None:
                    if action == PlayerMode.ONE_PLAYER:
                        game_state = GameState.CHOOSE_DIFFICULTY
                        player_mode = PlayerMode.ONE_PLAYER
                    elif action == PlayerMode.TWO_PLAYER:
                        game_state = GameState.CHOOSE_DIFFICULTY
                        player_mode = PlayerMode.TWO_PLAYER
                    elif action == GameState.SETTINGS:
                        game_state = GameState.SETTINGS
                    elif action == GameState.QUIT:
                        game_state = GameState.QUIT
                        
        elif game_state == GameState.CHOOSE_DIFFICULTY:
            
            for ui_element in difficulty_screen.ui_elements:
                action = ui_element.update(mouse_pos, mouse_up)
                if action is not None:
                    if action == Difficulty.EASY:
                        game_state = GameState.GAMEPLAY
                        difficulty = Difficulty.EASY
                    elif action == Difficulty.MEDIUM:
                        game_state = GameState.GAMEPLAY
                        difficulty = Difficulty.MEDIUM
                    elif action == Difficulty.HARD:
                        difficulty = Difficulty.HARD
                        game_state = GameState.GAMEPLAY
                    elif action == Difficulty.INSANE:
                        difficulty = Difficulty.INSANE
                        game_state = GameState.GAMEPLAY
                    elif action == Difficulty.HELL:
                        game_state = GameState.GAMEPLAY
                        difficulty = Difficulty.HELL
            ...
                
               
        elif game_state == GameState.GAMEPLAY:
            
            if difficulty == Difficulty.EASY:
                bullet_spawn_rate = 2
                ...
            elif difficulty == Difficulty.MEDIUM:
                bullet_spawn_rate = 4
                ...
            elif difficulty == Difficulty.HARD:
                bullet_spawn_rate = 7
                ...
            elif difficulty == Difficulty.INSANE:
                bullet_spawn_rate = 10
                ...
            elif difficulty == Difficulty.HELL:
                bullet_spawn_rate = 15
                ...
                
            # escape key pauses game
            if player_mode == PlayerMode.ONE_PLAYER:
                
                if frame_count % bullet_spawn_rate == 0:
                    normal_bullet = sprt.Bullet(left=True, right=True, top=True, bottom=True)
                    bullets_group.add(normal_bullet)
                    
                player_group.update()
                bullets_group.update()
                
                for bullet in bullets_group:
                    if (pygame.sprite.collide_rect(player_one, bullet) and not getattr(bullet, 'hit', False)):
                        hits += 1
                        bullet.hit = True
                        print(f'Hits: {hits}')
                
                
                ...
            elif player_mode == PlayerMode.TWO_PLAYER:
                
                
                ...
        
        elif game_state == GameState.PAUSED:
            for ui_element in pause_screen.ui_elements:
                if action is not None:
                    if action == GameState.GAMEPLAY:
                        game_state = GameState.GAMEPLAY
                    elif action == GameState.MAIN_MENU:
                        game_state = GameState.MAIN_MENU
                    elif action == GameState.QUIT:
                        game_state = GameState.QUIT
            ...
        elif game_state == GameState.SETTINGS:
            ...
        elif game_state == GameState.QUIT:
            running = False
        else:
            pass
        
        # --------------------
        # Draw everything
        # --------------------
        
        if game_state == GameState.MAIN_MENU:
            for ui_element in main_menu.ui_elements:
                ui_element.draw(screen)
            ...
        
        elif game_state == GameState.CHOOSE_DIFFICULTY:
            for ui_element in difficulty_screen.ui_elements:
                ui_element.draw(screen)
        
        elif game_state == GameState.GAMEPLAY:
            player_group.draw(screen)
            bullets_group.draw(screen)
            ...

            ...
        elif game_state == GameState.PAUSED:
            
            player_group.draw(screen)
            bullets_group.draw(screen)
            
            # background dimming overlay effect when pausing
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180)) 
            screen.blit(overlay, (0, 0))
            
            for ui_element in pause_screen.ui_elements:
                ui_element.draw(screen)
        else:
            pass

        pygame.display.flip()
        clock.tick(FPS)
        
        if frame_count % 60 == 0:
            print(game_state)
            print(player_mode)
            print(difficulty)

    pygame.quit()
    sys.exit()

if __name__ == '__main__': main()