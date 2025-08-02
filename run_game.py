import pygame
import pygame_gui as GUI

pygame.init()

pygame.display.set_caption('Quick Start')
screen = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color("#000000"))

manager = GUI.UIManager((800, 600))

button = GUI.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100,50)),
                               text="Hello",
                               manager=manager)

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