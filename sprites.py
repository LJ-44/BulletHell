import pygame
import math
import random

class GameObject(pygame.sprite.Sprite):
    def __init__(self, color: str, width: float, height: float, speed: int):
        pygame.sprite.Sprite.__init__(self)

        self.screen = pygame.display.get_surface()

        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self): pass

class Player(GameObject):
    def __init__(self):
        # base class constructor
        super().__init__(color="green", width=10.0, height=10.0, speed=3)

        # player spawn: center of screen
        self.rect.centerx = self.screen_width / 2
        self.rect.centery = self.screen_height / 2

    def update(self):
        # W,A,S,D or Arrow keys to move player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]: self.rect.centery -= self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: self.rect.centerx -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: self.rect.centery += self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: self.rect.centerx += self.speed

        # restrict player to confines of display edges
        if (self.rect.top < 0): self.rect.top = 0
        if (self.rect.left < 0): self.rect.left = 0
        if (self.rect.right > self.screen_width): self.rect.right = self.screen_width
        if (self.rect.bottom > self.screen_height): self.rect.bottom = self.screen_height

class Bullet(GameObject):
    def __init__(self):
        # base class constructor
        super().__init__(color="red", width=5.0, height=5.0, speed=2)

        # collision detection
        self.hit = False

        # bullet placed at random point outside the bounds on right-side edge of screen
        self.rect.left = self.screen_width
        self.rect.centery = random.randint((math.floor(self.rect.height / 2)), (self.screen_height - math.floor(self.rect.height / 2)))

    def update(self):
        
        #TODO: make bullet travel left from spawn point, if left edge of screen is hit, call self.kill() to remove from memory 

        self.rect.centerx -= self.speed

        if self.rect.left < 0:
            self.kill()
        ...

# class HomingBullet(GameObject):
#     def __init__(self):
#         # base class constructor
#         super().__init__(color="blue", width=7.0, height=7.0, speed=3)

#     def update(self): pass
#     ...

# class ExplodingBullet(GameObject):
#     def __init__(self):
#         # base class constructor
#         super().__init__(color="orange", width=8.0, height=8.0, speed=3)

#     def update(self): pass
#     ...