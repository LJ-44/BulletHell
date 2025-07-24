import pygame
from math import floor
import random

class GameObject(pygame.sprite.Sprite):
    def __init__(self, color: str, width: float, height: float, speed: int | float):
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
        super().__init__(color="blue", width=9.0, height=9.0, speed=0.1)

        # collision detection
        self.hit = False

        self.target = target

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

        self.bullet_position = pygame.Vector2(self.rect.center)
        self.velocity = (pygame.Vector2(self.target.rect.center) - self.bullet_position).normalize()
        self.passed_player = False
            
    # easy tracking
    def update(self):

        # TODO FIX ALL OF THIS!!!!!!!!

        # update vector pointing from bullet -> target
        self.bullet_to_target_vector = pygame.Vector2(self.target.rect.center) - self.rect.center

        # update bullet velocity vector using linear interpolation of velocity & to_target vectors
        self.steer_strength = 0.0001
        self.velocity = self.velocity.lerp(self.bullet_to_target_vector, self.steer_strength)

        if self.passed_player == False:
            if self.bullet_to_target_vector.length() != 0:
                self.bullet_to_target_vector.normalize()

            if self.velocity.length() != 0:
                self.velocity.normalize() * self.speed

            # check if dot product is negative (angle between vectors > 90 degrees)
            if self.velocity.dot(self.bullet_to_target_vector) < 0:
                self.passed_player = True
                self.velocity_after_pass = self.velocity

            # update bullet trajectory using velocity vector
            self.bullet_position += self.velocity
            self.rect.center = (int(self.bullet_position.x), int(self.bullet_position.y))

        else:
            self.bullet_position += self.velocity_after_pass
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