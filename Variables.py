import pygame

pygame.init()

# Colores
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
white = (255, 255, 255)

# Nivel
ARMA_SEGUN_LEVEL = 1

# Asignando colores a los textos
text_color = (0, 0, 0)
txt_color_play = (255, 255, 255)
txt_color_go = (255, 255, 255)
txt_color_colission = (245, 176, 65)

# Creando fuentes de textos de opciones y título
text_titles = pygame.font.Font('fonts/PixelifySans-Regular.ttf', 60)
text_options = pygame.font.Font('fonts/PixelifySans-Regular.ttf', 35)
text_in_game = pygame.font.Font('fonts/PixelifySans-Regular.ttf', 25)

score = pygame.font.Font('fonts/PixelifySans-Regular.ttf', 30)
