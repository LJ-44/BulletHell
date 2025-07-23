import pygame
from math import floor
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
    def __init__(self, left: bool = False, right: bool = True, top: bool = False, bottom: bool = False):
        # base class constructor
        super().__init__(color="red", width=5.0, height=5.0, speed=2)

        # collision detection
        self.hit = False
        
        # store desired screen edges (chosen randomly for spawning)
        self.edges = []
        if left: self.edges.append("left")
        if right: self.edges.append("right")
        if top: self.edges.append("top")
        if bottom: self.edges.append("bottom")
        
        self.spawn_edge = random.choice(self.edges)
        
        # spawn bullets on specified edges of screen
        if self.spawn_edge == "left":
            self.dx, self.dy = self.speed, 0
            self.rect.left = 0
            self.rect.centery = random.randint(
                (floor(self.rect.height / 2)), 
                (self.screen_height - floor(self.rect.height / 2))
            )
        elif self.spawn_edge == "right":
            self.dx, self.dy = -self.speed, 0
            self.rect.right = self.screen_width
            self.rect.centery = random.randint(
                (floor(self.rect.height / 2)), 
                (self.screen_height - floor(self.rect.height / 2))
            )
        elif self.spawn_edge == "top":
            self.dx, self.dy = 0, self.speed
            self.rect.top = 0
            self.rect.centerx = random.randint(
                (floor(self.rect.width / 2)), 
                (self.screen_width - floor(self.rect.width / 2))
            )
        elif self.spawn_edge == "bottom":
            self.dx, self.dy = 0, -self.speed
            self.rect.bottom = self.screen_height
            self.rect.centerx = random.randint(
                (floor(self.rect.width / 2)), 
                (self.screen_width - floor(self.rect.width / 2))
            )

    def update(self):
        
        # move bullet in desired x/y direction
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        
        # erase object if it goes out of bounds
        if (self.rect.left < 0 or 
            self.rect.right > self.screen_width or
            self.rect.top < 0 or
            self.rect.bottom > self.screen_height): self.kill()

class HomingBullet(GameObject):
    def __init__(self, target: GameObject):
        # base class constructor
        super().__init__(color="blue", width=7.0, height=7.0, speed=3)

        self.hit = False

        self.edges = ["left", "right", "top", "bottom"]
        self.spawn_edge = random.choice(self.edges)

        # spawn homing bullet on random edge of screen
        if self.spawn_edge == "left":
            self.rect.left = 0
            self.rect.centery = random.randint(
                (floor(self.rect.height / 2)), 
                (self.screen_height - floor(self.rect.height / 2))
            )
        elif self.spawn_edge == "right":
            self.rect.right = self.screen_width
            self.rect.centery = random.randint(
                (floor(self.rect.height / 2)), 
                (self.screen_height - floor(self.rect.height / 2))
            )
        elif self.spawn_edge == "top":
            self.rect.top = 0
            self.rect.centerx = random.randint(
                (floor(self.rect.width / 2)), 
                (self.screen_width - floor(self.rect.width / 2))
            )
        elif self.spawn_edge == "bottom":
            self.rect.bottom = self.screen_height
            self.rect.centerx = random.randint(
                (floor(self.rect.width / 2)), 
                (self.screen_width - floor(self.rect.width / 2))
            )
            
    # easy tracking
    def update(self):

        



        ...
    # constant tracking
    def update(self):

        ...

# class ExplodingBullet(GameObject):
#     def __init__(self):
#         # base class constructor
#         super().__init__(color="orange", width=8.0, height=8.0, speed=3)

#     def update(self): pass
#     ...