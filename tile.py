from os import path
import pygame
from settings import tile_size
from utils import get_frames

class Tile(pygame.sprite.Sprite):
    def __init__(self,x,y,surface=pygame.Surface((tile_size,tile_size))):
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect(topleft=(x,y))

    def update(self,shift):
        self.rect.x += shift

class Crate(Tile):
    def __init__(self,x,y,surface):
        super().__init__(x,y,surface)
        self.rect = self.image.get_rect(bottomleft=(x,y+tile_size))  

class AnimatedTiles(pygame.sprite.Sprite):
    def __init__(self,x,y,path):
        super().__init__()
        self.frames = get_frames(path) 
        self.frame_index = 0
        self.frame_speed = 0.14
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x,y))    

    def animate(self):
        self.frame_index += self.frame_speed
        if self.frame_index>len(self.frames):
            self.frame_index =0
        self.image = self.frames[int(self.frame_index)]

    def update(self,shift):
        self.animate()
        self.rect.x += shift    

class Coin(AnimatedTiles):
    def __init__(self,x,y,path,value):
        super().__init__(x,y,path)
        self.value = value
        self.rect = self.image.get_rect(center = (x+tile_size//2,y+tile_size//2)) 

class Palm(AnimatedTiles):
    def __init__(self,x,y,path,offset):
        super().__init__(x,y,path)
        self.rect = self.image.get_rect(topleft=(x,y-offset))
                                    