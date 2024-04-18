import pygame

pygame.init()

# Creación de screen surface
screen = pygame.display.set_mode((1000, 500))

# Creando fuentes de textos de opciones y título
text_main_title = pygame.font.Font('freesansbold.ttf', 50)
text_options = pygame.font.Font('freesansbold.ttf', 25)

# Asignando colores a los textos
text_color = (0, 0, 0)
txt_color_play = (255, 255, 255)
txt_color_colission = (115, 192, 182)

# Creando superficie encima de la screen surface
screen_surf = pygame.Surface((1000, 500))
screen_surf.fill((255, 255, 255))

# Creando el regular surface del portal
portal_surf = pygame.image.load("images/portal_mainmenu.png").convert_alpha()
portal_rect = portal_surf.get_rect(center=(500, 250))
