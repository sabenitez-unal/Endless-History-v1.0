import sys

import pygame

import menu_vars

pygame.init()

# Título de la ventana
pygame.display.set_caption("PC Final Proyect")
clock = pygame.time.Clock()


# Función para dibujar los textos cada vez que se necesiten
def draw_txt(text: str, font, txt_color, x: int, y: int):
    text_surface = font.render(text, True, txt_color)
    text_rect = text_surface.get_rect(midtop=(x, y))
    menu_vars.screen.blit(text_surface, text_rect)
    return text_rect


# Estados del juego
game_paused = False
game_playing = False
game_in_menu = True
game_options = False
# psj_surf = pygame.image.load("images/psj.png").convert_alpha()
# psj_rect = psj_surf.get_rect(bottomleft=(200, 500))

# Bucle del juego
while True:
    # Posición del mouse
    mouse_pos = pygame.mouse.get_pos()

    # El juego corre
    if game_in_menu:
        # Mostrando la superficie superpuesta y el portal
        menu_vars.screen.blit(menu_vars.screen_surf, (0, 0))
        menu_vars.screen.blit(menu_vars.portal_surf, menu_vars.portal_rect)

        # Mostrando texto principal del menu
        draw_txt("Menú Principal", menu_vars.text_titles, menu_vars.text_color, 500, 40)
        # pygame.draw.rect(screen, "Cyan", main_title_txt_rect,, 40 )
        # pygame.draw.rect(screen, "Cyan", main_title_txt_rect, 20, 40)

        # Mostrando opciones del menú
        play_txt = draw_txt("JUGAR", menu_vars.text_options, menu_vars.txt_color_play, 500, menu_vars.txt_ops_y)
        opts_txt = draw_txt("OPCIONES", menu_vars.text_options, menu_vars.text_color, 200, menu_vars.txt_ops_y)
        quit_txt = draw_txt("SALIR", menu_vars.text_options, menu_vars.text_color, 850, menu_vars.txt_ops_y)

        # Cambiando de color los textos de las opciones ante un evento de colisión con mouse position
        if play_txt.collidepoint(mouse_pos):
            draw_txt("JUGAR", menu_vars.text_options, menu_vars.txt_color_colission, 500, menu_vars.txt_ops_y)
        elif opts_txt.collidepoint(mouse_pos):
            draw_txt("OPCIONES", menu_vars.text_options, menu_vars.txt_color_colission, 200, menu_vars.txt_ops_y)
        elif quit_txt.collidepoint(mouse_pos):
            draw_txt("SALIR", menu_vars.text_options, menu_vars.txt_color_colission, 850, menu_vars.txt_ops_y)

        # Creando bucle de eventos
        for event in pygame.event.get():
            # Evento de cierre
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Evento de soltar botón del mouse
            if event.type == pygame.MOUSEBUTTONUP:
                # Evento de click sobre "Jugar"
                if play_txt.collidepoint(mouse_pos):
                    # El juego corre
                    game_playing = True
                    game_in_menu = False
                # Evento de click sobre "Opciones"
                elif opts_txt.collidepoint(mouse_pos):
                    print("Opciones")
                # Evento de click sobre "Salir"
                elif quit_txt.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

    elif game_options:
        menu_vars.screen.blit(menu_vars.screen_surf, (0, 0))

        draw_txt("MENÚ DE OPCIONES", menu_vars.text_options, menu_vars.text_color, 500, 125)

        # Creando bucle de eventos
        for event in pygame.event.get():
            # Evento de cierre
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    elif game_playing:
        menu_vars.screen.blit(menu_vars.screen_surf, (0, 0))

        # Creando bucle de eventos
        for event in pygame.event.get():
            # Evento de cierre
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Evento de entrada a menú de pausa
                if event.key == pygame.K_ESCAPE:
                    game_paused = True
                    game_playing = False

    # Menú se muestra mientras el juego no corre
    if game_paused:
        menu_vars.screen.blit(menu_vars.screen_surf, (0, 0))
        draw_txt("PRESIONA 'ESC' PARA REANUDAR", menu_vars.text_options, menu_vars.text_color, 500, 125)
        opts_txt = draw_txt("OPCIONES", menu_vars.text_options, menu_vars.text_color, 500, 250)
        quit_txt = draw_txt("SALIR AL MENÚ", menu_vars.text_options, menu_vars.text_color, 500, 305)

        if opts_txt.collidepoint(mouse_pos):
            draw_txt("OPCIONES", menu_vars.text_options, menu_vars.txt_color_colission, 500, 250)
        elif quit_txt.collidepoint(mouse_pos):
            quit_txt = draw_txt("SALIR AL MENÚ", menu_vars.text_options, menu_vars.txt_color_colission, 500, 305)

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
                # Click sobre opciones
                if opts_txt.collidepoint(mouse_pos):
                    game_options = True
                    game_paused = False
                # clicl sobre salir al menú
                elif quit_txt.collidepoint(mouse_pos):
                    game_playing = False
                    game_in_menu = True


    # Refrescando la screen surface a 60 FPS
    pygame.display.update()
    clock.tick(60)
