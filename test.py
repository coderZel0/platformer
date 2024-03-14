import pygame,sys

pygame.init()

screen = pygame.display.set_mode((500,500))

surface = pygame.image.load("assets/graphics/terrain/palm_large/large_1.png")
surface_rect = surface.get_rect(center = (250,250))

surface.fill("black",None,pygame.BLEND_RGBA_MULT)

surface_copy = surface.copy()
surface_copy.fill("black",None,pygame.BLEND_RGBA_MULT)
#surface.blit(surface_copy,(0,0))


while True:
    screen.fill("grey")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(surface,surface_rect)
    pygame.display.update()        