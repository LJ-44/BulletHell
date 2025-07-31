import pygame
from pygame.sprite import Sprite
import math
import random
from src.menu import *

class GameObject(Sprite):
    def __init__(self, color: str, width: float, height: float, speed: int | float):
        Sprite.__init__(self)

        self.screen = pygame.display.get_surface()

        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        self.image = pygame.Surface([width, height]).convert()
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self): pass

class Player1(GameObject):
    def __init__(self, 
                 color: str = 'green', 
                 width: float = 10.0, 
                 height: float = 10.0, 
                 speed: float = 3.0):
        # base class constructor
        super().__init__(color=color, width=width, height=height, speed=speed)

        # player spawn: center of screen
        self.rect.centerx = self.screen_width / 2
        self.rect.centery = self.screen_height / 2

    def update(self):
        # W,A,S,D to move player1
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]: self.rect.centery -= self.speed
        if keys[pygame.K_a]: self.rect.centerx -= self.speed
        if keys[pygame.K_s]: self.rect.centery += self.speed
        if keys[pygame.K_d]: self.rect.centerx += self.speed

        # restrict player to confines of display edges
        if (self.rect.top < 0): self.rect.top = 0
        if (self.rect.left < 0): self.rect.left = 0
        if (self.rect.right > self.screen_width): self.rect.right = self.screen_width
        if (self.rect.bottom > self.screen_height): self.rect.bottom = self.screen_height
        
class Player2(GameObject):
    def __init__(self,
                 color: str = "purple",
                 width: float = 10.0,
                 height: float = 10.0,
                 speed: float = 3.0):
    
        # base constructor
        super().__init__(color=color, width=width, height=height, speed=speed)

        # player spawn: center of screen
        self.rect.centerx = self.screen_width / 2
        self.rect.centery = self.screen_height / 2

    def update(self):
        # Arrow keys to move player2
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]: self.rect.centery -= self.speed
        if keys[pygame.K_LEFT]: self.rect.centerx -= self.speed
        if keys[pygame.K_DOWN]: self.rect.centery += self.speed
        if keys[pygame.K_RIGHT]: self.rect.centerx += self.speed

        # restrict player to confines of display edges
        if (self.rect.top < 0): self.rect.top = 0
        if (self.rect.left < 0): self.rect.left = 0
        if (self.rect.right > self.screen_width): self.rect.right = self.screen_width
        if (self.rect.bottom > self.screen_height): self.rect.bottom = self.screen_height


class Bullet(GameObject):
    def __init__(self, 
                 color: str = "red",
                 width: float = 5.0,
                 height: float = 5.0,
                 speed: float = 2.0,):
        # base class constructor
        super().__init__(color=color, width=width, height=height, speed=speed)

        # collision detection
        self.hit_player_one = False
        self.hit_player_two = False
        
        # store desired screen edges (chosen randomly for spawning)
        self.edges = ["left", "right", "top", "bottom"]
        
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
    def __init__(self, 
                 target: GameObject,
                 color: str = "blue",
                 width: float = 9.0,
                 height: float = 9.0,
                 speed: float = 4.0):
        # base class constructor
        super().__init__(color=color, width=width, height=height, speed=speed)

        # collision detection
        self.hit_player_one = False
        self.hit_player_two = False

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
        self.turn_rate = 0.4 # degrees per frame
            
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
            self.angle += self.delta_angle
            
        velocity_vector = pygame.Vector2(math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle)))
        
        self.bullet_position += velocity_vector * self.speed
        self.rect.center = (int(self.bullet_position.x), int(self.bullet_position.y))

        # erase object if it goes out of bounds
        if (self.rect.left < 0 or
            self.rect.right > self.screen_width or
            self.rect.top < 0 or
            self.rect.bottom > self.screen_height): self.kill()
class ExplodingBullet(GameObject):
    def __init__(self, 
                 target: GameObject,
                 sprite_group,
                 color: str = "orange",
                 width: float = 8.0,
                 height: float = 8.0,
                 speed: float = 3.0):
        # base class constructor
        super().__init__(color=color, width=width, height=height, speed=speed)
        
        self.sprite_group = sprite_group
        
        # collision detection
        self.hit_player_one = False
        self.hit_player_two = False

        self.target = target
        self.color = color

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
        

        self.explode_bullet = False
        
        # bullet steering
        self.turn_rate = 1.0 # degrees per frame
        
        # explosion effect stuff
        self.explosion_size = float(self.rect.width)
        self.max_explosion_size = 20 
        self.growth_rate = 0.25
        

    def update(self):
        
        target_vector = pygame.Vector2(self.target.rect.center) - self.bullet_position
        target_angle = math.degrees(math.atan2(target_vector.x, target_vector.y))
        
        target_vector = pygame.Vector2(self.target.rect.center) - self.bullet_position
        target_angle = math.degrees(math.atan2(target_vector.y, target_vector.x))
        
        if not self.explode_bullet:
            
            # smallest signed angle difference
            difference = ((target_angle - self.angle + 180) % 360) - 180
            
            # limit to turn rate
            if difference > self.turn_rate:
                difference = self.turn_rate
            elif difference < -self.turn_rate:
                difference = -self.turn_rate
                
            # turn
            self.angle += difference
            
            velocity_vector = pygame.Vector2(math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle)))
            
            if velocity_vector.distance_to(target_vector) < 125:
                self.explode_bullet = True
                
            self.bullet_position += velocity_vector * self.speed
            self.rect.center = (int(self.bullet_position.x), int(self.bullet_position.y))
                
        else: 
            # grow the explosion 
            self.explosion_size += self.growth_rate

            # update rect size
            bullet_size = int(self.explosion_size)
            self.rect.width = bullet_size
            self.rect.height = bullet_size
            self.rect.center = self.bullet_position

            # update image to match new size
            self.image = pygame.Surface((bullet_size, bullet_size), pygame.SRCALPHA)
            pygame.draw.rect(
                self.image,
                self.color,
                pygame.Rect(0, 0, bullet_size, bullet_size)
            )

            # explode into shrapnel
            if bullet_size >= self.max_explosion_size:
                for shrapnel in self.spawn_shrapnel():
                    self.sprite_group.add(shrapnel)
                self.kill()
        
        # erase object if it goes out of bounds
        if (self.rect.left < 0 or 
            self.rect.right > self.screen_width or
            self.rect.top < 0 or
            self.rect.bottom > self.screen_height): self.kill()
        
    def spawn_shrapnel(self):
        shrapnel_list = []
        shrapnel_count = random.randint(8, 12)
        for num_shrapnel in range(shrapnel_count):
            angle = random.randint(0, 360)
            shrapnel = ExplosionShrapnel(center_pos=self.rect.center, angle_deg=angle)
            shrapnel_list.append(shrapnel)
        return shrapnel_list
        
class ExplosionShrapnel(GameObject):
    def __init__(self, 
                 center_pos, 
                 angle_deg: int,
                 width: float = 6.0 , 
                 height: float = 6.0, 
                 speed: float = 4.0):
        
        color_list = ["red", "yellow", "orange"]
        color = random.choice(color_list)
        
        super().__init__(color=color, width=width, height=height, speed=speed)

        self.rect.center = center_pos
        self.shrapnel_position = pygame.Vector2(self.rect.center)
        self.angle = angle_deg
        
        self.direction = pygame.Vector2(math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle)))
        
        
    def update(self):
        
        self.shrapnel_position += self.direction * self.speed
        self.rect.center = (int(self.shrapnel_position.x), int(self.shrapnel_position.y))
        
        # erase object if it goes out of bounds
        if (self.rect.left < 0 or 
            self.rect.right > self.screen_width or
            self.rect.top < 0 or
            self.rect.bottom > self.screen_height): self.kill()
        ...
        
        