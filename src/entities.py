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
        
        self.game = game
        self.type = type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {"top":False, "bottom":False, "left":False, "right":False}
        
        self.action = ''
        self.animation_offset = (-3, -3)
        self.flip = False
        
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def update(self, movement: Tuple[int, int] = (0, 0)):
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        
        entity_rect = self.rect()
        
        
        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]
        
    def render(self, surface):
        surface.blit(self.game.assets[self.type], self.pos)
        
        
