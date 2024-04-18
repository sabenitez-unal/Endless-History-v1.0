import pygame

pygame.init()

#  VARIABLES GENERALES DE MENÚS

# Creación de screen surface
screen = pygame.display.set_mode((1000, 500))
# Creando superficie encima de la screen surface
screen_surf = pygame.Surface((1000, 500))
screen_surf.fill((127, 179, 213))
# Asignando colores a los textos
text_color = (0, 0, 0)
txt_color_play = (255, 255, 255)
txt_color_colission = (245, 176, 65)
# Creando fuentes de textos de opciones y título
text_titles = pygame.font.Font('fonts/PixelifySans-Regular.ttf', 60)
text_options = pygame.font.Font('fonts/PixelifySans-Regular.ttf', 35)

# VARIABLES MENU PRINCIPAL


# Distancia del texto de las opciones desde TOP
txt_ops_y = 225
# Creando el regular surface del portal
portal_surf = pygame.image.load("images/portal_mainmenu.png").convert_alpha()
portal_surf = pygame.transform.rotozoom(portal_surf, 0, 1.3)
portal_rect = portal_surf.get_rect(center=(500, 250))
