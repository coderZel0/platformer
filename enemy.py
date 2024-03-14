from tile import AnimatedTiles
from settings import tile_size
import random
import pygame

class Enemy(AnimatedTiles):
    def __init__(self,x,y,path):
        super().__init__(x,y,path)
        self.rect.y = y+tile_size-self.image.get_size()[1]
        self.speed = random.randint(3,5)

    def movement(self):
        self.rect.x += self.speed
    def flip_image(self):
        if self.speed>0:
            self.image=pygame.transform.flip(self.image,True,False)
    def reverse(self):
        self.speed *= -1    

    def update(self,shift):
        self.animate()
        self.flip_image()
        self.rect.x +=shift
        self.movement()            