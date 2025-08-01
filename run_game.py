import pygame
import pygame_gui
from pygame.locals import *



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
    
    manager = pygame_gui.UIManager()

    running = True
    while running:
        
        screen.fill("black")
        
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                running = False
            
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__': main()