from utils import get_frames
import pygame
from tile import AnimatedTiles
from settings import Gravity

class Player(AnimatedTiles):
    def __init__(self,x,y,path):
        super().__init__(x,y,path)
        self.run_frames = get_frames("assets/graphics/character/run")
        self.jump_frames = get_frames("assets/graphics/character/jump")
        self.direction = -1
        self.frame_speed = 0.4
        self.move_y = 0
        self.movement = False
        self.jump = False
    def flip_player(self):
        if self.direction < 0:
            self.image = pygame.transform.flip(self.image,True,False)
    def get_frames(self):
        if self.movement:
            self.frames = self.run_frames
        elif self.jump:
            self.frames = self.jump_frames
        elif self.move_y <0 and self.movement:
            self.frames = self.jump_frames    
        else: 
            self.frames = get_frames("assets/graphics/character/idle")                
    def update(self,shift,collision):
        dy =0
        dx =0
        #Gravity
        self.move_y += Gravity
        if self.move_y >10:
            self.move_y = 10
        dy += self.move_y    
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.movement=True
            self.direction =1
            dx = 5
        if keys[pygame.K_a]:
            self.movement =True
            self.direction =-1
            dx = -5
        if keys[pygame.K_d] ==False and keys[pygame.K_a]==False:
            self.movement = False 
        if keys[pygame.K_SPACE]:
            dy=0
            self.jump =True
            self.move_y = -10
            self.rect.y += self.move_y
        if keys[pygame.K_SPACE]==False:
            self.jump =False    

        if collision:
            dy=0

        self.get_frames()   
        self.animate()
        self.flip_player() 
        
        self.rect.x += shift  
        self.rect.x += dx  
        self.rect.y += dy