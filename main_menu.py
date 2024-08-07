import sys
import pygame
import Variables
import menus
from Armas import Sniper, Shotgun, Gun
from Enemigos import Slime
from Jugador import Jugador

pygame.init()


# Funcion de escalar imagen
def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, (w * scale, h * scale))
    return nueva_imagen


# Importar imagenes
# Jugador
Jugador_image = pygame.image.load("graphics/Personajes/Jugador/Caballero.png").convert_alpha()
Jugador_image = escalar_img(Jugador_image, Variables.ESCALA_PERSONAJE)

# Armas:
# Sniper
Sniper_image = pygame.image.load("graphics/Armas/Guns/Sniper.png").convert_alpha()
Sniper_image = escalar_img(Sniper_image, Variables.ESCALA_ARMA)
# Escopeta
Shotgun_image = pygame.image.load("graphics/Armas/Guns/Shotgun.png").convert_alpha()
Shotgun_image = escalar_img(Shotgun_image, Variables.ESCALA_ARMA)
# Pistola
Gun_image = pygame.image.load("graphics/Armas/Guns/Gun.png").convert_alpha()
Gun_image = escalar_img(Gun_image, Variables.ESCALA_ARMA)

# Disparo
Disparo_image = pygame.image.load("graphics/Armas/Balas/laser.png").convert_alpha()
Disparo_image = escalar_img(Disparo_image, Variables.ESCALA_DISPARO)

# Enemigos
Enemy_image = pygame.image.load("graphics/Personajes/Enemigos/Enemy.png").convert_alpha()
Enemy_image = escalar_img(Enemy_image, Variables.ESCALA_ENEMIGO)

boss_image = pygame.image.load("graphics/Personajes/Enemigos/Enemy.png").convert_alpha()
boss_image = escalar_img(Enemy_image, Variables.ESCALA_BOSS)

fondo = pygame.image.load("graphics/Mapas/Prehistoria.png").convert_alpha()
# img_gameover = pygame.image.load("graphics/").convert_alpha()

# Reloj
clock = pygame.time.Clock()

# Crear Jugador
jugador = Jugador(Variables.ANCHOPANTALLA // 2, Variables.ALTOPANTALLA // 2, Jugador_image)

# Crear Arma
# sniper
sniper = Sniper(Sniper_image, Disparo_image)
# Shotgun
shotgun = Shotgun(Shotgun_image, Disparo_image)
# Gun
gun = Gun(Gun_image, Disparo_image)

# grupo de sprites
# Balas
grupo_disparo = pygame.sprite.Group()

# Enemigos
grupo_enemigos = pygame.sprite.Group()

Move_Up, Move_Down, Move_Left, Move_Right = False, False, False, False

# Estados del juego
game_paused, game_playing, game_menu, game_over = False, False, True, False

boss_state = False
boss = Slime(boss_image, 15, 1.4)
hp_jugador = 10000

mouse_pos = (0, 0)

score = 0

main_menu = menus.MainMenu(mouse_pos)
Pause_menu = menus.PauseMenu(mouse_pos)
# Game_over_menu = menus.GameOverMenu(mouse_pos)
portal = pygame.sprite.GroupSingle()
portal.add(menus.Portal())

# Inicio del bucle

while True:
    mouse_pos = pygame.mouse.get_pos()  # Posición del mouse

    # En el menú principal
    if game_menu:
        menus.screen.fill((123, 245, 113))
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

    # Menú de pausa durante el juego
    elif game_paused:
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
                # clicl sobre salir al menú
                if Pause_menu.quit_txt.collidepoint(mouse_pos):
                    game_playing = False
                    game_menu = True

    # El juego corre
    elif game_playing:
        menus.screen.blit(fondo, (0, 0))

        # Jugador
        # Dibujar Jugador
        jugador.dibujo(menus.screen)

        # Direcciones
        Delta_x, Delta_y = 0, 0

        # Cambio de Deltas
        if Move_Right:
            Delta_x = Variables.VELOCIDAD
        if Move_Left:
            Delta_x = -Variables.VELOCIDAD
        if Move_Up:
            Delta_y = -Variables.VELOCIDAD
        if Move_Down:
            Delta_y = Variables.VELOCIDAD

        # Llenar datos de jugador movimiento
        jugador.movimiento(Delta_x, Delta_y)

        # Enemigos
        # Aparicion
        if score == 25:
            grupo_enemigos.add(boss)
        elif score < 25:
            if pygame.time.get_ticks() % 60 == 0:
                nuevo_slime = Slime(Enemy_image, 10, 1)
                grupo_enemigos.add(nuevo_slime)

        if pygame.time.get_ticks() % 60 == 0:
            score += 1

        # Dibujar enemigo
        for enemigo in grupo_enemigos:
            enemigo.update()
            enemigo.dibujo(menus.screen)

        # Arma
        # Dibujar Arma
        if Variables.ARMA_SEGUN_LEVEL == 1:
            sniper.dibujo(menus.screen)
            balas = sniper.update(jugador)
            damage_weapon = Variables.DANO_SNIPER
        elif Variables.ARMA_SEGUN_LEVEL == 2:
            shotgun.dibujo(menus.screen)
            balas = shotgun.update(jugador)
            damage_weapon = Variables.DANO_SHOTGUN
        elif Variables.ARMA_SEGUN_LEVEL == 3:
            gun.dibujo(menus.screen)
            balas = gun.update(jugador)
            damage_weapon = Variables.DANO_GUN

        if balas:
            grupo_disparo.add(balas)
        for bala in grupo_disparo:
            bala.update()

        # Dibujar Disparo
        for bala in grupo_disparo:
            bala.dibujo(menus.screen)

        # Colisiones
        if Variables.ARMA_SEGUN_LEVEL == 1:
            for bala in grupo_disparo:
                enemigos_golpeados = pygame.sprite.spritecollide(bala, grupo_enemigos, True)
                if enemigos_golpeados:
                    for enemigo in enemigos_golpeados:
                        enemigo.recibir_dano(damage_weapon)
        if Variables.ARMA_SEGUN_LEVEL >= 2:
            for bala in grupo_disparo:
                enemigos_golpeados = pygame.sprite.spritecollide(bala, grupo_enemigos, True)
                if enemigos_golpeados:
                    for enemigo in enemigos_golpeados:
                        enemigo.recibir_dano(damage_weapon)
                        bala.kill()

        if hp_jugador == 0:
            game_over = True
            game_playing = False

        # Controles
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Evento de entrada a menú de pausa
                    game_paused = True
                if event.key == pygame.K_a:
                    Move_Left = True
                elif event.key == pygame.K_d:
                    Move_Right = True
                elif event.key == pygame.K_w:
                    Move_Up = True
                elif event.key == pygame.K_s:
                    Move_Down = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    Move_Left = False
                elif event.key == pygame.K_d:
                    Move_Right = False
                elif event.key == pygame.K_w:
                    Move_Up = False
                elif event.key == pygame.K_s:
                    Move_Down = False

    '''elif game_over:
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
                    game_over = False'''

    pygame.display.update()
    clock.tick(40)  # Limitar la velocidad de fotogramas a 60 FPS
