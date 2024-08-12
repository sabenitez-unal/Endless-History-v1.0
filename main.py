import math
import random
import menus
import pygame
import sys

# Resolución.
width = 832
height = 512

vel_disparo = 4  # Velocidad de disparo
player_speed = 3  # Velocidad de movimiento del jugador
player_hp = 50 # Vida del jugador
player_run_mult = 2
enemy_speed = 2 #Velocidad del enemigo
daño_bala = 5  # Daño de la bala
tiempo_ultimo_disparo = 0  # Tiempo del último disparo
cadencia_disparo = 500  # Intervalo de tiempo entre disparos (en milisegundos)

# Tipos de enemigo
enemigo_melee = {"type": "melee", "hp": 10, "dmg": 10, "range": 20, "atck_speed": 1000,
                 "png": "Game-Project-PC-main/graphics/Personajes/Enemigos/Enemy.png"}
enemigo_range = {"type": "range", "hp": 10, "dmg": 10, "range": 200, "atck_speed": 1000,
                 "png": "Game-Project-PC-main/graphics/Personajes/Enemigos/Enemy.png"}
enemigo_boss = {"type": "range", "hp": 100, "dmg": 10, "range": 300, "atck_speed": 1500,
                 "png": "Game-Project-PC-main/graphics/Personajes/Enemigos/Enemy.png"}


# Coordenadas de donde se generan los enemigos.
nivel_1_coords = ((width // 2, 0), (width // 2, height), (0, height // 2),
                  (width, height // 2))
probabilidades_drop = [True] * 1 + [False] * 1


# Funcion Escalar imagen a una escala float como porcentaje
def escalar_img(image, scale):  # Funcion de escalar imagen
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, (w * scale, h * scale))
    return nueva_imagen


# Función que se encarga de la Generación de niveles
def generar_nivel(cant_enemigos_por_ronda, max_enemigos, coords_spawn, spawn_time):
    # cant_enemigos_por_ronda: Cantidad de enemigos por ronda (min, max)
    # max_enemigos: cantidad enemigos total
    # coords_spawn: Tupla de tuplas de coords, ej: ((izq), (arr), (der), (abajo))
    # spawn_time: cada cuanto spawnea cada ronda
    coords_spawn_temp = list(coords_spawn)
    lista_return = []
    ronda = 1
    while max_enemigos > 0:
        cant_enemigos_por_ronda_temp = random.randint(cant_enemigos_por_ronda[0], cant_enemigos_por_ronda[1])
        for i in range(cant_enemigos_por_ronda_temp):
            spawn_time_temp = spawn_time * ronda
            if not coords_spawn_temp:
                coords_spawn_temp = list(coords_spawn)
                spawn_time_temp += 500
            if coords_spawn_temp:
                coords_temp = coords_spawn_temp[random.randint(0, len(coords_spawn_temp) - 1)]
                ene_temp = Enemigo(enemigo_range)
                max_enemigos -= 1
                ene_temp.rect.center = coords_temp
                coords_spawn_temp.remove(coords_temp)
                ene_temp.tiempo_aparicion = spawn_time_temp
                lista_return.append(ene_temp)
        coords_spawn_temp = list(coords_spawn)
        ronda += 1
    for i in range(abs(max_enemigos)):
        lista_return.pop(-1)

    return lista_return


# Clase Jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hp = player_hp
        self.image_original = pygame.image.load("Game-Project-PC-main/graphics/Personajes/Jugador/Caballero.png").convert_alpha()
        self.image = escalar_img(self.image_original, 2) 
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)
        self.velocidad_x = 0
        self.velocidad_y = 0

    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        if self.rect.left < 64:
            self.rect.left = 64
        if self.rect.right > width - 64:
            self.rect.right = width - 64
        if self.rect.top < 40:
            self.rect.top = 40
        if self.rect.bottom > height - 70:
            self.rect.bottom = height - 70

        if self.hp <= 0:  # Verifica si el jugador está muerto
            self.hp = 0


# Clase enemigo
class Enemigo(Jugador):
    def __init__(self, tipo, tiempo_aparicion=0):
        self.tiempo_update = pygame.time.get_ticks()
        super().__init__()
        self.vivo = True
        self.hp = tipo["hp"]
        self.dmg = tipo["dmg"]
        self.range = tipo["range"]
        self.atck_speed = tipo["atck_speed"]
        self.tiempo_aparicion = tiempo_aparicion
        self.imagen = pygame.image.load(tipo["png"]).convert_alpha()
        self.image = escalar_img(self.image_original, 2)  # Cambia 0.5 al porcentaje que desees
        self.tipo = tipo["type"]

    # metodo follow con un objetivo que al ser singleplayer siempre sera el jugador
    def follow(self, objetivo):
        if self.hp <= 0:
            self.hp = 0
            self.vivo = False
        endx = 0
        endy = 0
        if self.rect.centerx > objetivo.rect.centerx:
            endx = -enemy_speed
        if self.rect.centerx < objetivo.rect.centerx:
            endx = enemy_speed
        if self.rect.centery > objetivo.rect.centery:
            endy = -enemy_speed
        if self.rect.centery < objetivo.rect.centery:
            endy = enemy_speed

        distancia = math.sqrt(
            ((self.rect.centerx - objetivo.rect.centerx) ** 2) + ((self.rect.centery - objetivo.rect.centery) ** 2))

        if self.tipo == "melee":
            if distancia < self.range and pygame.time.get_ticks() - self.tiempo_update >= self.atck_speed:
                objetivo.hp -= self.dmg
            else:
                self.move(endx, endy)

        if self.tipo == "range":
            if distancia < self.range + 50 and distancia > self.range - 50:
                if pygame.time.get_ticks() - self.tiempo_update >= self.atck_speed:
                    nuevo_disparo = Disparo(self, None, objetivo)
                    nuevo_disparo.rect.x = self.rect.x
                    nuevo_disparo.rect.y = self.rect.y
                    sprites.add(nuevo_disparo)
                    disparo_list_en.add(nuevo_disparo)
                    self.tiempo_update = pygame.time.get_ticks()
            elif distancia < self.range - 50:
                self.move(-endx, -endy)
            else:
                self.move(endx, endy)

        if self.rect.left < 64:
            self.rect.left = 64
        if self.rect.right > width - 64:
            self.rect.right = width - 64
        if self.rect.top < 40:
            self.rect.top = 40
        if self.rect.bottom > height - 70:
            self.rect.bottom = height - 70

    def spawn(self, lista_enemigos, objetivo):
        lista_enemigos.add(self)
        sprites.add(self)
        if self.vivo:
            self.follow(objetivo)
        else:
            if random.choice(probabilidades_drop):
                # INSERTAR AQUI UN OBJETO DE VIDA VIDA
                pass
            self.kill()

    def move(self, delta_x, delta_y):
        self.rect.x += delta_x
        self.rect.y += delta_y


# Clase disparo, el origen es para saber de donde sale
# direccion solo cuando hay jugador, y objetivo es none si es jugador tmb
class Disparo(pygame.sprite.Sprite):
    def __init__(self, origin=None, direccion=None, objetivo=None):
        super().__init__()
        self.image_original = pygame.image.load("Game-Project-PC-main/graphics/Armas/Balas/laser.png").convert_alpha()
        self.image = escalar_img(self.image_original, 0.5)  
        self.rect = self.image.get_rect()
        self.originx = origin.rect.x
        self.originy = origin.rect.y
        if objetivo:
            self.objetivox = objetivo.rect.x
            self.objetivoy = objetivo.rect.y
        else:
            if direccion:
                self.objetivox = direccion[0]
                self.objetivoy = direccion[1]
            else:
                if direccion == "up":
                    self.objetivox = self.originx
                    self.objetivoy = self.originy - 1
                if direccion == "down":
                    self.objetivox = self.originx
                    self.objetivoy = self.originy + 1
                if direccion == "left":
                    self.objetivox = self.originx - 1
                    self.objetivoy = self.originy
                if direccion == "right":
                    self.objetivox = self.originx + 1
                    self.objetivoy = self.originy


    def update(self, lista_enemigos):
        x1 = self.originx
        y1 = self.originy
        x2 = self.objetivox
        y2 = self.objetivoy
        deltx = x2 - x1
        delty = y2 - y1
        d = math.sqrt((deltx ** 2) + (delty ** 2))
        vx = deltx / (d / vel_disparo)
        vy = delty / (d / vel_disparo)
        self.rect.x += vx
        self.rect.y += vy
        if self.rect.x > width or self.rect.x < 0:
            self.kill()
        if self.rect.y > height or self.rect.x < 0:
            self.kill()
        # esta parte es para ver colisiones
        for enemigo in lista_enemigos:
            if enemigo.rect.colliderect(self.rect):
                enemigo.hp -= daño_bala
                print(enemigo.hp)
                self.kill()
                break


# Inicio del motor de pygame.
pygame.init()

# Estados del juego
game_paused, game_playing, game_menu, game_over = False, False, True, False

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Sprites de enemigos y disparos enemigos.
sprites = pygame.sprite.Group()
disparo_list_en = pygame.sprite.Group()
disparo_list_player = pygame.sprite.Group()
enemigos_list = pygame.sprite.Group()

mouse_pos = (0, 0)  # Posición del mouse
score = 0  # Puntaje inicial

# Clases de los menus
main_menu = menus.MainMenu(mouse_pos)
Pause_menu = menus.PauseMenu(mouse_pos)
Game_over_menu = menus.GameOverMenu(mouse_pos)
portal = pygame.sprite.GroupSingle()
portal.add(menus.Portal())

# Imagen del Jefe
boss_image = pygame.image.load("Game-Project-PC-main/graphics/Personajes/Enemigos/Enemy.png").convert_alpha()
boss_image = escalar_img(boss_image, 4)

# Estado del jefe
boss_state = False
boss = Enemigo(enemigo_boss, 15)

# Imágenes de Fondo
img_gameover = pygame.image.load("Game-Project-PC-main/graphics/Game Over/Sin menu/Gave Over - Sin Menu_0001.png").convert_alpha()
mainmenu_image = pygame.image.load(
    "Game-Project-PC-main/graphics/Cambio de Nivel/Fondo solo/Fondo 835 x 532/Fondo 835 x 532.gif").convert_alpha()
fondo1 = pygame.image.load("Game-Project-PC-main/graphics/Mapas/Prehistoria.png")

# Sprite del jugador.
jugador = Jugador()
player_list = pygame.sprite.Group()
player_list.add(jugador)
sprites.add(jugador)

# Generación de niveles.
nivel_1 = generar_nivel((3, 3), 6, nivel_1_coords, 10000)

disparando = False

while True:
    mouse_pos = pygame.mouse.get_pos()  # Posición del mouse

    if game_menu:  # En el menú principal
        menus.screen.blit(mainmenu_image, (0, 0))
        portal.draw(menus.screen)
        main_menu.update(mouse_pos)

        # Creando bucle de eventos
        for event in pygame.event.get():
            # Evento de cierre
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Evento de soltar botón del mouse
            if event.type == pygame.MOUSEBUTTONUP:
                # Evento de click sobre "Jugar"
                if main_menu.play_txt.collidepoint(mouse_pos):
                    # El juego corre
                    game_playing = True
                    game_menu = False
                    game_paused = False
                # Evento de click sobre "Salir"
                elif main_menu.quit_txt.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

    elif game_paused:  # Menú de pausa durante el juego
        menus.screen.fill((123, 245, 113))
        Pause_menu.update(mouse_pos)

        # Bucle de eventos
        for event in pygame.event.get():
            # Evento de cierre
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Evento de volver al juego
                if event.key == pygame.K_ESCAPE:
                    game_paused = False
                    game_playing = True
            # Evento de clicks dentro del menú
            if event.type == pygame.MOUSEBUTTONUP:
                # Evento de cierre
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # click sobre salir al menú
                if Pause_menu.quit_txt.collidepoint(mouse_pos):
                    game_playing = False
                    game_menu = True

    elif game_playing:  # El juego se ejecuta.
        # Dibujar fondo1
        screen.blit(fondo1, (0, 0))

        # Dibujar sprites
        sprites.draw(screen)

        # Actualizar posición del Jugador
        jugador.update()

        # Generación Boss
        if score == 50:
            enemigos_list.add(boss)
        elif score < 50:
            for ene in nivel_1:
                if pygame.time.get_ticks() >= ene.tiempo_aparicion:
                    ene.spawn(enemigos_list, jugador)

        # Actualizar posición del disparo
        disparo_list_en.update(player_list)
        disparo_list_player.update(enemigos_list)

        if jugador.hp == 0:
            game_over = True
            game_playing = False

        # Controles y eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Movimiento del jugador
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Evento de entrada a menú de pausa
                    game_paused = True
                elif event.key == pygame.K_a:
                    jugador.velocidad_x = -player_speed
                elif event.key == pygame.K_d:
                    jugador.velocidad_x = player_speed
                elif event.key == pygame.K_w:
                    jugador.velocidad_y = -player_speed
                elif event.key == pygame.K_s:
                    jugador.velocidad_y = player_speed

                elif event.key == pygame.K_SPACE:
                    jugador.velocidad_y *= player_run_mult
                    jugador.velocidad_x *= player_run_mult

            # Disparar con el mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo
                    disparando = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Botón izquierdo
                    disparando = False


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    jugador.velocidad_x = 0
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    jugador.velocidad_y = 0

        if disparando and pygame.time.get_ticks() - tiempo_ultimo_disparo >= cadencia_disparo:
            nuevo_disparo = Disparo(jugador, mouse_pos)
            nuevo_disparo.rect.center = jugador.rect.center
            sprites.add(nuevo_disparo)
            disparo_list_player.add(nuevo_disparo)
            tiempo_ultimo_disparo = pygame.time.get_ticks()

    elif game_over:
        menus.screen.blit(img_gameover, (0, 0))
        Game_over_menu.update(mouse_pos)

        for event in pygame.event.get():
            # Evento de cierre
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Evento de soltar botón del mouse
            if event.type == pygame.MOUSEBUTTONUP:
                # Evento de click sobre "Jugar"
                if Game_over_menu.txt_game_over.collidepoint(mouse_pos):
                    # El juego corre
                    game_playing = True
                    game_over = False

    # Actualizar pantalla
    pygame.display.update()
    clock.tick(60)  # Limitar la velocidad de fotogramas a 60 FPS

