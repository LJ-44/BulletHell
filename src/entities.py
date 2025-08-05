import pygame
import random
import os
from pygame.sprite import Sprite, Group
from pygame import Surface
import pygame_gui
from typing import Optional, Any, Tuple
class Entity:
    def __init__(self,
                 game,
                 type: str,
                 pos: Tuple[int, int], 
                 size: Tuple[int, int]):
        
        self.screen = pygame.display.get_surface()
        self.game = game
        self.type = type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collision = False
        
        self.action = ''
        self.animation_offset = (-3, -3)
        self.flip = False
        #self.set_action("idle")
        
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()
    
    def update(self, movement: Tuple[int, int] = (0, 0)):
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        
        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]
        
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True
        
        self.animation.update()
        
    def render(self, surface):
        surface.blit(
            pygame.transform.flip(surface=self.animation.img(), flip_x=self.flip, flip_y=False), 
            (self.pos[0] + self.animation_offset[0], self.pos[1] + self.animation_offset[1])
        )
        
class Player(Entity):
    def __init__(self, game, pos, size):
        super().__init__(game, "player", pos, size)

        self.set_action("idle")
        
    def slash(self):
        self.set_action("slash")
        
    def update(self, movement=(0,0)):
        super().update(movement)
            
        
        
        
        
