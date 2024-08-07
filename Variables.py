import pygame

pygame.init()

# Pantalla
ANCHOPANTALLA = 832
ALTOPANTALLA = 512

# Colores
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
white = (255, 255, 255)

# Personaje
VELOCIDAD = 3
VELOCIDAD_BALA = 9

# Escalas
ESCALA_PERSONAJE = 2
ESCALA_ARMA = 0.4
ESCALA_DISPARO = 0.3
ESCALA_ENEMIGO = 2
ESCALA_BOSS = 4

# Sniper
COOLDOWN_BALAS_SNIPER = 1000
DANO_SNIPER = 10

# Escopeta
COOLDOWN_BALAS_SHOTGUN = 600
DISTANCIA_MAXIMA_BALA = 150
DANO_SHOTGUN = 4

# Gun
COOLDOWN_BALAS_GUN = 400
DANO_GUN = 8

# Nivel
ARMA_SEGUN_LEVEL = 2

# Asignando colores a los textos
text_color = (0, 0, 0)
txt_color_play = (255, 255, 255)
txt_color_colission = (245, 176, 65)

# Creando fuentes de textos de opciones y título
text_titles = pygame.font.Font('fonts/PixelifySans-Regular.ttf', 60)
text_options = pygame.font.Font('fonts/PixelifySans-Regular.ttf', 35)
text_in_game = pygame.font.Font('fonts/PixelifySans-Regular.ttf', 25)
txt_ops_y = ALTOPANTALLA // 2 # Distancia del texto de las opciones desde TOP

score = pygame.font.Font('fonts/PixelifySans-Regular.ttf', 30)
