import pygame
from src.entities import *
from src.utils import *

class BulletHell:
    def __init__(self):
        
        pygame.init()
        resolution = (1920, 1080)
        self.screen = pygame.display.set_mode(size=resolution)
        self.display = pygame.Surface(size=(994, 546))
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.assets = {
            "background": load_image(path="background/background_1.png"),
            #"background/background": Animation(images=load_images(path="background"), image_duration=7, loop=True),
            "player": load_image(path="entities/player/player.png"),
            "bullets": load_images(path="entities/bullets"),
            "bullet_left": load_image(path="entities/bullets/bullet_left.png"),
            "bullet_right": load_image(path="entities/bullets/bullet_right.png"),
            "bullet_top": load_image(path="entities/bullets/bullet_top.png"),
            "bullet_bottom": load_image(path="entities/bullets/bullet_bottom.png"),
            "player/idle": Animation(images=load_images(path="entities/player/idle"), image_duration=1, loop=False),
            "player/slash": Animation(images=load_images(path="entities/player/slash"), image_duration=2, loop=False),
            "player/slash_overlay": Animation(images=load_images(path="entities/player/slash_overlay"), image_duration=2, loop=False),
            "player/walk": Animation(images=load_images(path="entities/player/walk"), image_duration=5, loop=True)
        }
        # movement bools: [left, right, up, down] 
        self.slash = False
        self.player_movement = [False, False, False, False]
        self.player = Player(self, pos=(self.display.get_width() / 2, self.display.get_height() / 2), size=(26, 12))
        
    def run(self):
        while self.running:
            
            self.display.blit(self.assets["background"], (0,0))
            
            player_move_x = self.player_movement[1] - self.player_movement[0]
            player_move_y = self.player_movement[3] - self.player_movement[2]
            
            self.player.update((player_move_x, player_move_y))
            self.player.render(self.display)
            
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                # if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #     if self.player.action != "slash" or self.player.animation.done:
                #             self.player.set_action("slash")
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.player_movement[2] = True
                    if event.key == pygame.K_a:
                        self.player_movement[0] = True
                    if event.key == pygame.K_s:
                        self.player_movement[3] = True
                    if event.key == pygame.K_d:
                        self.player_movement[1] = True
                    if event.key == pygame.K_f:
                        if self.player.action == "walk":
                            self.player.set_overlay_action("slash_overlay")
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.player_movement[2] = False
                    if event.key == pygame.K_a:
                        self.player_movement[0] = False
                    if event.key == pygame.K_s:
                        self.player_movement[3] = False
                    if event.key == pygame.K_d:
                        self.player_movement[1] = False
                        
            if not hasattr(self.player, 'animation') or self.player.animation.done or self.player.animation.loop:
                if player_move_x != 0 or player_move_y != 0:
                    self.player.set_action("walk")
                else:
                    self.player.set_action("idle")
            
            self.screen.blit(pygame.transform.scale(surface=self.display, size=self.screen.get_size()))
            
            pygame.display.update()
                    
            self.clock.tick(60)
            
        pygame.quit()
        
if __name__ == "__main__":
    game = BulletHell()
    game.run()