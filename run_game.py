import pygame
from src.entities import Entity, Player
from src.utils import *

class BulletHell:
    def __init__(self):
        
        pygame.init()
        resolution = (1920, 1080)
        self.screen = pygame.display.set_mode(size=resolution)
        self.display = pygame.Surface(size=(994, 545))
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.assets = {
            "background": load_image(path="background/background_1_cropped.png"),
            #"background": Animation(images=load_images(path="background"), image_duration=5, loop=True),
            "player": load_image(path="entities/player/player.png"),
            "bullets": load_images(path="entities/bullets"),
            "bullet_left": load_image(path="entities/bullets/bullet_left.png"),
            "bullet_right": load_image(path="entities/bullets/bullet_right.png"),
            "bullet_top": load_image(path="entities/bullets/bullet_top.png"),
            "bullet_bottom": load_image(path="entities/bullets/bullet_bottom.png"),
            "player/idle": Animation(images=load_images(path="entities/player/idle"), image_duration=10, loop=False),
            "player/slash": Animation(images=load_images(path="entities/player/slash"), image_duration=5, loop=True),
            "player/walk": Animation(images=load_images(path="entities/player/walk"), image_duration=5, loop=True)
        }
        # movement bools: [left, right, up, down] 
        self.movement = [False, False, False, False]
        self.player = Player(self, pos=(self.display.get_width() / 2, self.display.get_height() / 2), size=(40, 40))
        
    def run(self):
        while self.running:
            
            self.display.blit(self.assets["background"], (0,0))
            
            x_move = self.movement[1] - self.movement[0]
            y_move = self.movement[3] - self.movement[2]
            
            self.player.update((x_move, y_move))
            self.player.render(self.display)
            
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                        
            if x_move != 0 or y_move != 0:
                length = (x_move ** 2 + y_move ** 2) ** 0.5
                x_move /= length
                y_move /= length
                self.player.set_action("walk")
            else:
                self.player.set_action("idle")
            
            self.screen.blit(pygame.transform.scale(surface=self.display, size=self.screen.get_size()))
            
            pygame.display.update()
                    
            dt = self.clock.tick(60) / 1000.0
            
        pygame.quit()
        
if __name__ == "__main__":
    game = BulletHell()
    game.run()