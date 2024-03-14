from enemy import Enemy
from sys import platform
import pygame
from utils import get_cut_graphics, get_level_data
from tile import Palm, Tile,Crate,Coin
from player import Player

class Level:
    def __init__(self,surface,level_data,tile_size,create_overworld,current_level,update_coins):
        self.display_surface = surface
        self.current_level = current_level
        self.world_shift = 0
        self.update_coins = update_coins
        self.create_overworld = create_overworld
        self.new_max_level = level_data["unlock"]
        self.level_data = level_data
        self.content = level_data["content"]
        self.terrain = self.get_sprite_group(tile_size,"terrain")
        self.grass = self.get_sprite_group(tile_size,"grass")
        self.crates = self.get_sprite_group(tile_size,"crates")
        self.coins = self.get_sprite_group(tile_size,"coins")
        self.fg_palms = self.get_sprite_group(tile_size,"fg_palms")
        self.bg_palms = self.get_sprite_group(tile_size,"bg_palms")
        #Enemy
        self.enemy = self.get_sprite_group(tile_size,"enemies")
        #constraint
        self.constraints = self.get_sprite_group(tile_size,"constraints")
        #Player
        self.player_collided =False
        self.player_map_data = get_level_data(self.level_data["player"])
        self.player_sprite = pygame.sprite.GroupSingle()
        self.setup_player(tile_size)
        self.collision_sprites = self.fg_palms.sprites()+self.terrain.sprites()+self.crates.sprites()

    def get_sprite_group(self,size,type):
        if type == "terrain":
            tiles = get_cut_graphics("assets/graphics/terrain/terrain_tiles.png")
        if type == "grass":
            tiles = get_cut_graphics("assets/graphics/decoration/grass/grass.png") 
   
        layer_data = get_level_data(self.level_data[type])
        sprite_group = pygame.sprite.Group()
        for row_index,row in enumerate(layer_data):
            for col_index,col in enumerate(row):
                if col !='-1': 
                    x = col_index * size
                    y = row_index * size 
                    if type == "crates":
                        tile = Crate(x,y,pygame.image.load("assets/graphics/terrain/crate.png"))
                    elif type == "coins":
                        if col == "0":
                            tile = Coin(x,y,"assets/graphics/coins/gold",5)
                        else:
                            tile = Coin(x,y,"assets/graphics/coins/silver",1)
                    elif type == "fg_palms":
                        if col=="0":tile = Palm(x,y,"assets/graphics/terrain/palm_small",40) 
                        else:tile = Palm(x,y,"assets/graphics/terrain/palm_large",70)
                    elif type == "bg_palms":
                        tile = Palm(x,y,"assets/graphics/terrain/palm_bg",62) 
                    elif type == "enemies":
                        tile = Enemy(x,y,"assets/graphics/enemy/run")
                    elif type == "constraints":
                        tile = Tile(x,y)  
                    else:                        
                        tile = Tile(x,y,tiles[int(col)])
                    sprite_group.add(tile)
        return sprite_group       
    def setup_player(self,size):
        for row_index,row in enumerate(self.player_map_data):
            for col_index,col in enumerate(row):
                if col =="0":
                    x = col_index*size
                    y = row_index*size
                    sprite = Player(x,y,"assets/graphics/character/idle")
                    self.player_sprite.add(sprite)
    def player_collide(self,collision_sprites):
        for sprite in collision_sprites:
                if pygame.sprite.spritecollide(sprite,self.player_sprite,False):
                    return True   

    def coin_collision(self):
        hit_coins = pygame.sprite.spritecollide(self.player_sprite.sprite,self.coins,True)
        if hit_coins:
            for coin in hit_coins:
                self.update_coins(coin.value)
    def enemy_collision_reverse(self):
        for enemy in self.enemy.sprites():
            if pygame.sprite.spritecollide(enemy,self.constraints,False):
                enemy.reverse()
    def start(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.create_overworld(self.current_level,self.new_max_level)
    def run(self):
        self.start()
        #Bg_palms
        self.bg_palms.draw(self.display_surface)
        self.bg_palms.update(self.world_shift)
        #Terrain
        self.terrain.draw(self.display_surface)
        self.terrain.update(self.world_shift)
        #Player
        self.player_sprite.draw(self.display_surface)
        self.player_sprite.update(self.world_shift,self.player_collide(self.collision_sprites))
        #Enemies
        self.enemy.draw(self.display_surface)
        self.enemy.update(self.world_shift)
        #Constraints
        self.constraints.update(self.world_shift)
        self.enemy_collision_reverse()
        #Crates
        self.crates.draw(self.display_surface)
        self.crates.update(self.world_shift)
        #Grass
        self.grass.draw(self.display_surface)
        self.grass.update(self.world_shift)   
        #Coins
        self.coins.draw(self.display_surface)
        self.coins.update(self.world_shift)
        #Palms
        self.fg_palms.draw(self.display_surface)
        self.fg_palms.update(self.world_shift)
        #Collision
        self.coin_collision()
        