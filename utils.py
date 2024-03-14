from csv import reader
import pygame
from os import walk
from settings import tile_size

def get_level_data(csv_file):
    with open(csv_file) as file:
        data = reader(file,delimiter=',')
        return[list(row) for row in data]


def get_cut_graphics(path):
    surface_list =[]
    surface = pygame.image.load(path).convert_alpha()
    s_width,s_height = surface.get_size()
    count_col = s_width//tile_size
    count_row = s_height//tile_size

    for y_index in range(count_row):
        for x_index in range(count_col):
            x = x_index*tile_size
            y = y_index*tile_size
            new_surface = pygame.Surface((tile_size,tile_size),flags=pygame.SRCALPHA)
            new_surface.blit(surface,(0,0),pygame.Rect(x,y,tile_size,tile_size))
            surface_list.append(new_surface)

    return surface_list    

def get_frames(path):
    surface_list=[]
    for _,_,images in walk(path):
        for image in images:
            full_path = path+"/"+image
            img = pygame.image.load(full_path)
            surface_list.append(img)       
    return surface_list
