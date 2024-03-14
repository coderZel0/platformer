import pygame,sys
from utils import get_frames

class Icon(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.Surface((15,15))
        self.image.fill("green")
        self.rect = self.image.get_rect(center = pos)

class Node(pygame.sprite.Sprite):
    def __init__(self,pos,status,icon_speed,index):
        super().__init__()
        self.index = 0
        self.slower = 0
        self.status = status
        self.frames = get_frames(f"assets/graphics/overworld/{index}")
        self.image = self.frames[self.index]
        if status == "open":
            self.animate()
        else:
            self.image.fill("black",None,pygame.BLEND_RGBA_MULT)    
        self.rect = self.image.get_rect(center = pos)
        self.detection_zone = pygame.Rect(self.rect.centerx-(20/2),self.rect.centery-(20/2),20,20)
    def check_mouse_click(self):
        if self.status == "open":
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
                return True 
    def animate(self):
        self.slower += 3
        if self.slower > 10:
            self.index += 1
            if self.index > len(self.frames)-1:
                self.index = 0
            self.slower = 0    
        self.image = self.frames[self.index]    
class Overworld:
    def __init__(self,node_data,display_surface,curr_level,max_level,create_level):
        self.current_level = curr_level
        self.create_level = create_level
        self.max_level = max_level
        self.surface = display_surface
        self.node_data = node_data
        self.icon = pygame.sprite.GroupSingle()
        self.move_direction = pygame.math.Vector2(0,0)
        #self.current_level = cur_level
        self.node_group = pygame.sprite.Group()
        self.speed = 0.05
        self.setNodes(self.node_data)
        self.setIcon()
        self.moving = False
        
    def setIcon(self):
        pos = (self.node_group.sprites()[self.current_level]).rect.center
        self.icon.add(Icon(pos))
    def setNodes(self,node_data):
        for index,item in enumerate(node_data):
            for pos in item.values():
                if index <= self.max_level:
                    self.node_group.add(Node(pos,"open",self.speed,index))
                else:
                    self.node_group.add(Node(pos,"locked",self.speed,index))    
    def draw_lines(self,nodes):
        lines = [item["position"] for item in nodes]
        pygame.draw.lines(self.surface,"red",False,lines,6) 
    
    def input(self):
        keys = pygame.key.get_pressed()
        if not self.moving:
            if keys[pygame.K_RIGHT] and self.current_level<self.max_level:
                self.move_direction = self.get_move_direction("Right")
                self.current_level +=1
                self.moving = True
            elif keys[pygame.K_LEFT] and self.current_level >0:
                self.move_direction = self.get_move_direction("Left")
                self.current_level -=1   
                self.moving = True 
            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)    
    def get_move_direction(self,direction):
        start = pygame.math.Vector2(self.node_group.sprites()[self.current_level].rect.center)
        if direction == "Right":
            end = pygame.math.Vector2(self.node_group.sprites()[self.current_level+1].rect.center)
        else:
            end = pygame.math.Vector2(self.node_group.sprites()[self.current_level-1].rect.center)
        return(end - start)
    def update_icon_position(self):
        if self.moving and self.move_direction:
            self.icon.sprite.rect.center += self.speed*self.move_direction
            target_node = self.node_group.sprites()[self.current_level] 
            if target_node.detection_zone.collidepoint(self.icon.sprite.rect.center):
                self.moving = False   
                self.move_direction = pygame.math.Vector2(0,0)      
    def run(self):
        self.input()
        self.draw_lines(self.node_data)
        self.node_group.draw(self.surface)
        self.update_icon_position()
        self.icon.draw(self.surface) 
        for item in self.node_group:
            pygame.draw.rect(self.surface,"red",item.detection_zone)
        for item in self.node_group.sprites():
            if item.status =="open":
                item.animate()
            if item.check_mouse_click():
                self.create_level(self.current_level)    
                 



    