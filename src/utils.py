import os
import pygame

BASE_IMG_PATH = "assets/images/"

def load_image(path):
    img = pygame.image.load(file=(BASE_IMG_PATH + path)).convert()
    img.set_colorkey((0,0,0))
    return img

def load_images(path):
    images = []
    for img_name in os.listdir(BASE_IMG_PATH + path):
        images.append(load_image(path + "/" + img_name))
    return images

class Animation:
    def __init__(self, images, image_duration, loop=True):
        
        self.images = images
        self.image_duration = image_duration
        self.loop = loop
        self.done = False
        self.game_frame = 0
        
    def update(self):
        if self.loop:
            self.game_frame = (self.game_frame + 1) % (self.image_duration * len(self.images))
        else:
            self.game_frame = min(self.game_frame + 1, self.image_duration * len(self.images) - 1)
            if self.game_frame >= self.image_duration * len(self.images) - 1:
                self.done = True