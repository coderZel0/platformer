from typing import overload
from level import Level
import pygame,sys
from settings import HEIGHT,WIDTH,tile_size
from levels import levels
from overworld import Overworld
from gameData import nodes

pygame.init()

class UI:
    def __init__(self,surface):
        self.surface = surface
        self.coin = pygame.image.load("assets/graphics/ui/coin.png")
        self.health_bar = pygame.image.load("assets/graphics/ui/health_bar.png")
        self.bar_rect = self.health_bar.get_rect(midleft=(20,20))
        self.bar_max = 152
        self.bar_height = 4
        self.bar_left = (53,17)
        
    def show_health_bar(self,current_health):
        self.surface.blit(self.health_bar,self.bar_rect)     
        current_width = (current_health/100)*self.bar_max
        pygame.draw.rect(self.surface,"yellow",pygame.Rect(self.bar_left,(current_width,self.bar_height)))

    def show_coin(self,coins):
        font = pygame.font.Font("assets/graphics/ui/ARCADEPI.TTF",20)
        font_surface = font.render(str(coins),None,"white")
        self.surface.blit(self.coin,(20,40)) 
        self.surface.blit(font_surface,(50,47))       
        
class Game:
    def __init__(self):
        self.current_level = 0
        self.current_health = 100
        self.coins = 0
        self.ui = UI(screen)
        self.max_level = 2
        self.level = Level(screen,levels[0],tile_size,self.create_overworld,self.current_level,self.update_coins)
        self.overworld = Overworld(nodes,screen,0,self.max_level,self.createLevel)
        self.status = "overworld"
    def createLevel(self,current_level):
        self.level = Level(screen,levels[current_level],tile_size,self.create_overworld,current_level,self.update_coins)
        self.status = "level"   
    def create_overworld(self,current_level,new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(nodes,screen,current_level,self.max_level,self.createLevel)
        self.status = "overworld"     
    def update_coins(self,amount):
        self.coins += amount
    def change_health(self,amount):
        self.current_health -=amount    
    def run(self):
        if self.status == "overworld":
            self.overworld.run()
        elif self.status == "level":
            self.level.run()   
            self.ui.show_health_bar(self.current_health)
            self.ui.show_coin(self.coins) 


screen = pygame.display.set_mode((WIDTH,HEIGHT))
#GAME INITIALISATION
game = Game()



run = True
while run:
    screen.fill('grey')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    game.run()
    pygame.time.Clock().tick(60)
    pygame.display.update()        