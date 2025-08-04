import pygame
from src.entities import Entity
from src.utils import *

class BulletHell:
    def __init__(self):
        
        resolution = (1920, 1080)
        self.screen = pygame.display.set_mode(size=resolution)
        self.display = pygame.Surface((960, 540))
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.assets = {
            "background": Animation(images=load_images(path="background"), image_duration=5, loop=True),
            "player": load_image(path="entities/player/player.png"),
            "bullets": load_images(path="entities/bullets"),
            "bullet_left": load_image(path="entities/bullets/bullet_left.png"),
            "bullet_right": load_image(path="entities/bullets/bullet_right.png"),
            "bullet_top": load_image(path="entities/bullets/bullet_top.png"),
            "bullet_bottom": load_image(path="entities/bullets/bullet_bottom.png"),
            "player/slash": Animation(images=load_images(path="entities/player/slash"), image_duration=5, loop=False),
            "player/walk": Animation(images=load_images(path="entities/player/walk"), image_duration=5, loop=False),
        }
        
        self.player = Entity(self, type="player", pos=(self.screen.get_width() / 2, self.screen.get_height() / 2), size=(40, 40))
        ...
        
    def run(self):
        while self.running:
            
            self.display.fill((14, 219, 248))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
            dt = self.clock.tick(60) / 1000.0
            pygame.quit()
        ...
        
if __name__ == "__main__":
    game = BulletHell()
    game.run()