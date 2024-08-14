import math
import os
import random
import sys

import pygame

import menus

# Resolución.
width = 832
height = 512

vel_disparo = 4  # Velocidad de disparo
player_speed = 3  # Velocidad de movimiento del jugador
player_hp = 50  # Vida del jugador
player_run_mult = 2
enemy_speed = 1.7  # Velocidad del enemigo
dano_bala = 5  # Daño de la bala
tiempo_ultimo_disparo = 0  # Tiempo del último disparo
cadencia_disparo = 500  # Intervalo de tiempo entre disparos (en milisegundos)

# Tipos de enemigo
enemigo_melee = {"type": "melee", "hp": 10, "dmg": 10, "range": 20, "atck_speed": 1000,
                 "png": "graphics/Personajes/Enemigos/Enemy.png", "scale": 2}
enemigo_range = {"type": "range", "hp": 10, "dmg": 10, "range": 180, "atck_speed": 1000,
                 "png": "graphics/Personajes/Enemigos/Enemy.png", "scale": 2}
enemigo_boss = {"type": "range", "hp": 100, "dmg": 20, "range": 220, "atck_speed": 1500,
                "png": "graphics/Personajes/Enemigos/Enemy.png", "scale": 8}

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


# Clase Curación
class Curacion(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.curado = False
        self.image = escalar_img(pygame.image.load("graphics/Objects/corazon.png").convert_alpha(), 1)
        self.rect = self.image.get_rect()
        self.rect.center = position
        sprites.add(self)
        curaciones_list.add(self)

    def update(self, jugador):
        if self.rect.colliderect(jugador.rect):
            if not self.curado:
                jugador.hp += 10
                self.curado = False
            self.kill()


# Clase Jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hp = player_hp
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.animaciones_cd = 100
        self.frame_index = 0
        self.animaciones = personaje_animaciones
        self.animaciones_lado = self.animaciones[0]
        self.image = self.animaciones_lado[self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)
        self.score = 0

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

        if self.velocidad_x > 0:
            self.animaciones_lado = self.animaciones[3]
        if self.velocidad_x < 0:
            self.animaciones_lado = self.animaciones[2]
        if self.velocidad_y > 0:
            self.animaciones_lado = self.animaciones[0]
        if self.velocidad_y < 0:
            self.animaciones_lado = self.animaciones[1]
        if self.velocidad_x == 0 and self.velocidad_y == 0:
            self.frame_index = 1

        if self.hp <= 0:  # Verifica si el jugador está muerto
            self.hp = 0

        if self.hp >= 50:
            self.hp = 50

        self.image = self.animaciones_lado[self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= self.animaciones_cd:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0


# Clase Enemigo
class Enemigo(Jugador):
    def __init__(self, tipo, tiempo_aparicion=0):
        self.tiempo_update = pygame.time.get_ticks()
        super().__init__()
        self.vivo = True
        self.puntaje_agregado = False
        self.hp = tipo["hp"]
        self.dmg = tipo["dmg"]
        self.range = tipo["range"]
        self.atck_speed = tipo["atck_speed"]
        self.tiempo_aparicion = tiempo_aparicion
        self.imagen = pygame.image.load(tipo["png"]).convert_alpha()
        self.image = escalar_img(self.imagen, tipo["scale"])
        self.tipo = tipo["type"]

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
            if self.range + 50 > distancia > self.range - 50:
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
            if not self.puntaje_agregado:
                objetivo.score += 1
                self.puntaje_agregado = True

                # Verificar si se genera un objeto de curación
                if random.choice(probabilidades_drop):
                    nueva_curacion = Curacion(self.rect.center)
                    sprites.add(nueva_curacion)

            self.kill()

    def move(self, delta_x, delta_y):
        self.rect.x += delta_x
        self.rect.y += delta_y


# Clase disparo, el origen es para saber de donde sale
# direccion solo cuando hay jugador, y objetivo es none si es jugador también.
class Disparo(pygame.sprite.Sprite):
    def __init__(self, origin, direccion=None, objetivo=None):
        super().__init__()
        self.image_original = pygame.image.load("graphics/Armas/Balas/laser.png").convert_alpha()
        self.image = escalar_img(self.image_original, 0.5)  # Redimensionar la imagen
        self.rect = self.image.get_rect()
        self.rect.center = origin.rect.center  # Inicializar el disparo en el centro del jugador

        # Calcular la dirección del disparo
        if objetivo:
            objetivo_vector = pygame.math.Vector2(objetivo.rect.center)
            origen_vector = pygame.math.Vector2(self.rect.center)
            self.direccion = (objetivo_vector - origen_vector).normalize()
        else:
            if direccion:
                direccion_vector = pygame.math.Vector2(direccion)
                origen_vector = pygame.math.Vector2(self.rect.center)
                self.direccion = (direccion_vector - origen_vector).normalize()
            else:
                raise ValueError("Debe proporcionar un objetivo o una dirección")

    def update(self, lista_enemigos):
        # Mover el disparo en la dirección calculada
        self.rect.centerx += self.direccion.x * vel_disparo
        self.rect.centery += self.direccion.y * vel_disparo

        # Verificar si el disparo está fuera de la pantalla
        if (self.rect.right < 0 or self.rect.left > width or
                self.rect.bottom < 0 or self.rect.top > height):
            self.kill()

        # Verificar colisiones con enemigos
        for enemigo in lista_enemigos:
            if enemigo.rect.colliderect(self.rect):
                enemigo.hp -= dano_bala
                self.kill()
                break


# Apartado numeros.
def cargar_imagenes_numeros(carpeta):
    imagenes = {}
    for i in range(10):  # Para los números del 0 al 9
        imagen = pygame.image.load(os.path.join(carpeta, f'numeros0{i}.png')).convert_alpha()
        imagen = escalar_img(imagen, 4)
        imagenes[i] = imagen
    return imagenes


# Muestra la vida del jugador.
def dibujar_vida(jugador, pantalla, x, y):
    vida = jugador.hp
    distancia_x = 0
    if vida >= 0:
        for digito in str(vida):
            imagen = imagenes_numeros[int(digito)]
            pantalla.blit(imagen, (x + distancia_x, y))
            distancia_x += imagen.get_width()


# Inicio del motor de pygame.
pygame.init()

# Estados del juego
game_paused, game_playing, game_menu, game_over = False, False, True, False

# Configuración de pantalla y del tiempo del juego.
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Sprites de enemigos y disparos enemigos.
sprites = pygame.sprite.Group()
disparo_list_en = pygame.sprite.Group()
disparo_list_player = pygame.sprite.Group()
enemigos_list = pygame.sprite.Group()
curaciones_list = pygame.sprite.Group()


imagenes_numeros = cargar_imagenes_numeros('graphics/Numeros')  # Carga los numeros usados para mostrar la vida del psj.
mouse_pos = (0, 0)  # Posición del mouse

# Clases de los menus
main_menu = menus.MainMenu(mouse_pos)
Pause_menu = menus.PauseMenu(mouse_pos)
Game_over_menu = menus.GameOverMenu(mouse_pos)
portal = pygame.sprite.GroupSingle()
portal.add(menus.Portal())


# Función que crea una lista con los fotogramas de animación del jugador.
def carpeta_a_lista_animaciones(path_carpeta):
    lista_return = []
    for frame in os.listdir(path_carpeta + '/Fotogramas'):
        img = pygame.image.load(path_carpeta + '/Fotogramas/' + frame).convert_alpha()
        lista_return.append(img)
    return lista_return


# SECCION ANIMACIONES DEL PERSONAJE PRINCIPAL
caminar_adelante = list(map(lambda img: escalar_img(img, 2),
                            carpeta_a_lista_animaciones('graphics/Personaje principal/Caminar - Adelante')))
caminar_atras = list(
    map(lambda img: escalar_img(img, 2), carpeta_a_lista_animaciones('graphics/Personaje principal/Caminar - Atras')))
caminar_izquierda = list(map(lambda img: escalar_img(img, 2),
                             carpeta_a_lista_animaciones('graphics/Personaje principal/Caminar - Izquierda')))
caminar_derecha = list(
    map(lambda img: escalar_img(img, 2), carpeta_a_lista_animaciones('graphics/Personaje principal/Caminar - Derecha')))
personaje_animaciones = [caminar_adelante, caminar_atras, caminar_izquierda, caminar_derecha]

# Estado del jefe
boss = Enemigo(enemigo_boss, 30)

# Imágenes de Fondo
img_gameover = pygame.image.load("graphics/Game Over/Sin menu/Gave Over - Sin Menu_0001.png").convert_alpha()
mainmenu_image = pygame.image.load(
    "graphics/Cambio de Nivel/Fondo solo/Fondo 835 x 532/Fondo 835 x 532.gif").convert_alpha()
fondo1 = pygame.image.load("graphics/Mapas/Prehistoria.png").convert_alpha()
fondo2 = pygame.image.load("graphics/Mapas/Guerra.png").convert_alpha()

# Sprite del jugador.
jugador = Jugador()
player_list = pygame.sprite.Group()
player_list.add(jugador)
sprites.add(jugador)

# Generación de niveles.
nivel = generar_nivel((3, 5), 20, nivel_1_coords, 7000)
disparando = False

# Variable que permite "reiniciar" el tiempo del juego.
last_time = 0
escenario = 1

while True:
    mouse_pos = pygame.mouse.get_pos()  # Posición del mouse

    # Se actualiza el tiempo transcurrido desde el último reseteo.
    current_time = pygame.time.get_ticks() - last_time

    if game_menu:  # En el menú principal
        menus.screen.blit(mainmenu_image, (0, 0))
        portal.draw(menus.screen)
        main_menu.update(mouse_pos)

        # Se reestablece la vida del jugador
        jugador.hp, player_hp = 50, 50

        # Se vacían todas las sprites.
        enemigos_list.empty()
        disparo_list_player.empty()
        disparo_list_en.empty()
        curaciones_list.empty()
        sprites.empty()

        # Se "reinicia" el tiempo de Pygame a 0
        last_time = pygame.time.get_ticks()

        # Se incluye al jugador
        sprites.add(jugador)

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
                    # Vuelta al menú principal
                    game_over = False
                    game_menu = True

    elif game_playing:  # El juego se ejecuta.
        if escenario == 1:
            # Dibujar fondo1
            screen.blit(fondo1, (0, 0))
        elif escenario == 2:
            # Dibujar fondo2
            screen.blit(fondo2, (0, 0))

        # Dibujar sprites
        sprites.draw(screen)

        # Actualizar posición del Jugador
        jugador.update()

        # Generación Boss
        if jugador.score >= 3:
            enemigos_list.add(boss)
            for ene in nivel:
                if ene.tiempo_aparicion >= current_time:
                    nivel.remove(ene)
            for ene in nivel:
                if current_time >= ene.tiempo_aparicion:
                    ene.spawn(enemigos_list, jugador)
            boss.spawn(enemigos_list, jugador)

            if boss.hp == 0:
                jugador.hp, player_hp = 50, 50

                # Se vacían todas las sprites.
                enemigos_list.empty()
                disparo_list_player.empty()
                disparo_list_en.empty()
                curaciones_list.empty()
                sprites.empty()

                # Se "reinicia" el tiempo de Pygame a 0
                last_time = pygame.time.get_ticks()

                # Se incluye al jugador
                sprites.add(jugador)

                escenario += 1
                jugador.score = 0

        elif jugador.score < 3:
            for ene in nivel:
                if current_time >= ene.tiempo_aparicion:
                    ene.spawn(enemigos_list, jugador)

        # Actualizar posición del disparo
        disparo_list_en.update(player_list)
        disparo_list_player.update(enemigos_list)

        # Actualizar curaciones
        curaciones_list.update(jugador)

        # dibujar vida
        dibujar_vida(jugador, screen, 10, 40)

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
                    # Vuelta al menú principal
                    game_over = False
                    game_menu = True

    # Actualizar pantalla
    pygame.display.flip()
    clock.tick(60)  # Limitar la velocidad de fotogramas a 60 FPS
