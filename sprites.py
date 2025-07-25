import pygame
from pygame.sprite import Sprite
import math
import random

class GameObject(Sprite):
    def __init__(self, color: str, width: float, height: float, speed: int | float):
        Sprite.__init__(self)

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
                (math.floor(self.rect.height / 2)), 
                (self.screen_height - math.floor(self.rect.height / 2))
            )
        elif self.spawn_edge == "right":
            self.dx, self.dy = -self.speed, 0
            self.rect.right = self.screen_width
            self.rect.centery = random.randint(
                (math.floor(self.rect.height / 2)), 
                (self.screen_height - math.floor(self.rect.height / 2))
            )
        elif self.spawn_edge == "top":
            self.dx, self.dy = 0, self.speed
            self.rect.top = 0
            self.rect.centerx = random.randint(
                (math.floor(self.rect.width / 2)), 
                (self.screen_width - math.floor(self.rect.width / 2))
            )
        elif self.spawn_edge == "bottom":
            self.dx, self.dy = 0, -self.speed
            self.rect.bottom = self.screen_height
            self.rect.centerx = random.randint(
                (math.floor(self.rect.width / 2)), 
                (self.screen_width - math.floor(self.rect.width / 2))
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
        super().__init__(color="blue", width=9.0, height=9.0, speed=4)

        # collision detection
        self.hit = False

        self.target = target

        edges = ["left", "right", "top", "bottom"]
        spawn_edge = random.choice(edges)

        # spawn homing bullet on random edge of screen
        if spawn_edge == "left":
            self.rect.left = 0
            self.rect.centery = random.randint(0, self.screen_height)
        elif spawn_edge == "right":
            self.rect.right = self.screen_width
            self.rect.centery = random.randint(0, self.screen_height)
        elif spawn_edge == "top":
            self.rect.top = 0
            self.rect.centerx = random.randint(0, self.screen_width)
        elif spawn_edge == "bottom":
            self.rect.bottom = self.screen_height
            self.rect.centerx = random.randint(0, self.screen_width)

        self.bullet_position = pygame.Vector2(self.rect.center)
        
        # angle towards target
        to_target = pygame.Vector2(self.target.rect.center) - self.bullet_position
        self.angle = math.degrees(math.atan2(to_target.y, to_target.x))
        
        # track if bullet missed the player
        self.delta_angle = 0.0
        self.passed_player = False
        
        # bullet steering
        self.turn_rate = 1.0 # degrees per frame
            
    # easy tracking
    def update(self):
        
        target_vector = pygame.Vector2(self.target.rect.center) - self.bullet_position
        target_angle = math.degrees(math.atan2(target_vector.y, target_vector.x))
        
        if not self.passed_player:
            
            # smallest signed angle difference
            difference = ((target_angle - self.angle + 180) % 360) - 180
            
            # limit to turn rate
            if difference > self.turn_rate:
                difference = self.turn_rate
            elif difference < -self.turn_rate:
                difference = -self.turn_rate
                
            # turn
            self.angle += difference
            self.delta_angle = difference # store latest change in angle 
            
            velocity_vector = pygame.Vector2(math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle)))
            
            if velocity_vector.dot(target_vector) < 0:
                # flew past player
                self.passed_player = True
                
        else: 
            # continue trajectory after passing player
            self.angle += self.delta_angle / 2.5
            
        velocity_vector = pygame.Vector2(math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle)))
        
        self.bullet_position += velocity_vector * self.speed
        self.rect.center = (int(self.bullet_position.x), int(self.bullet_position.y))

        # erase object if it goes out of bounds
        if (self.rect.left < 0 or 
            self.rect.right > self.screen_width or
            self.rect.top < 0 or
            self.rect.bottom > self.screen_height): self.kill()

# class ExplodingBullet(GameObject):
#     def __init__(self):
#         # base class constructor
#         super().__init__(color="orange", width=8.0, height=8.0, speed=3)

#     def update(self): pass
#     ...