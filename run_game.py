import pygame
from pygame.locals import *
import sys
import math
from src.menu import *
import src.sprites as sprt
import src.sound as sound
import states_testing as state

# # UI
# main_menu = MainMenu()
# settings_screen = SettingsScreen()
# pause_screen = PauseScreen()
# difficulty_screen = DifficultyScreen()
# game_over_screen = GameOverScreen()

# # sprites
# player_group = pygame.sprite.Group()
# bullets_group = pygame.sprite.Group()
# player_one = sprt.Player1()
# player_two = sprt.Player2()

# player_group.add(player_one, player_two)

# # variables / flags
# normal_bullet_spawn_rate = 4 # bullets per second
# homing_bullet_spawn_rate = 1
# exploding_bullet_spawn_rate = 1
# lives = 3
# frame_count = 0
# player_one_hits = 0
# player_two_hits = 0
# homing_target = -1
# exploding_target = -1
# new_game = False

# # initial states
# game_state = GameState.MAIN_MENU
# player_mode = None
# difficulty = None

# Main Menu screen background animation?
# dimmed, similar to pause screen background, very cool

def main():
    # constants
    FPS = 60
    
    # display
    pygame.mixer.pre_init()
    pygame.mixer.init()
    sound.play_music()
    pygame.init()
    monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
    screen = pygame.display.set_mode(size=(1280, 720), flags=RESIZABLE)
    pygame.display.set_caption("Bullet Hell")
    clock = pygame.time.Clock()
    
    
    manager = state.StateManager()
    mainmenu = state.MainMenu(manager)
    
    # fullscreen = True
    running = True
    while running:
        
        screen.fill("black")
        
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                # elif event.key == K_f:
                #     fullscreen = not fullscreen
                #     if fullscreen:
                #         screen = pygame.display.set_mode(monitor_size, FULLSCREEN)
                #     else:
                #         screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), RESIZABLE)
            elif event.type == VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), RESIZABLE)
                for states in manager.states.values():
                    if hasattr(states, 'handle_resize'):
                        states.handle_resize()
                
        running &= manager.handle_events(events)
        manager.update()
        manager.draw(screen)
            
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__': main()