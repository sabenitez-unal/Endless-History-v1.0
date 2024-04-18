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


game_playing = False
# psj_surf = pygame.image.load("images/psj.png").convert_alpha()
# psj_rect = psj_surf.get_rect(bottomleft=(200, 500))

# Bucle del juego
while True:
    # El juego corre
    if game_playing:
        menu_vars.screen.blit(menu_vars.screen_surf, (0, 0))

        # Creando bucle de eventos
        for event in pygame.event.get():
            # Evento de cierre
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    # Menú se muestra mientras el juego no corre
    else:
        # Mostrando la superficie superpuesta y el portal
        menu_vars.screen.blit(menu_vars.screen_surf, (0, 0))
        menu_vars.screen.blit(menu_vars.portal_surf, menu_vars.portal_rect)

        # Mostrando texto principal del menu
        main_title_txt_rect = draw_txt("Menú Principal", menu_vars.text_main_title, menu_vars.text_color, 500, 50)
        # pygame.draw.rect(screen, "Cyan", main_title_txt_rect,, 40 )
        # pygame.draw.rect(screen, "Cyan", main_title_txt_rect, 20, 40)

        # Mostrando opciones del menú
        play_txt_rect = draw_txt("Jugar", menu_vars.text_options, menu_vars.txt_color_play, 500, 230)
        opts_txt_rect = draw_txt("Opciones", menu_vars.text_options, menu_vars.text_color, 200, 230)
        quit_txt_rect = draw_txt("Salir", menu_vars.text_options, menu_vars.text_color, 850, 230)

        # Cambiando de color los textos de las opciones ante un evento de colisión con mouse position
        mouse_pos = pygame.mouse.get_pos()
        if play_txt_rect.collidepoint(mouse_pos):
            draw_txt("Jugar", menu_vars.text_options, menu_vars.txt_color_colission, 500, 230)
        elif opts_txt_rect.collidepoint(mouse_pos):
            draw_txt("Opciones", menu_vars.text_options, menu_vars.txt_color_colission, 200, 230)
        elif quit_txt_rect.collidepoint(mouse_pos):
            draw_txt("Salir", menu_vars.text_options, menu_vars.txt_color_colission, 850, 230)

        # Creando bucle de eventos
        for event in pygame.event.get():
            # Evento de cierre
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Evento de soltar botón del mouse
            if event.type == pygame.MOUSEBUTTONUP:
                # Evento de click sobre "Jugar"
                if play_txt_rect.collidepoint(mouse_pos):
                    # El juego corre
                    game_playing = True
                # Evento de click sobre "Opciones"
                elif opts_txt_rect.collidepoint(mouse_pos):
                    print("Opciones")
                # Evento de click sobre "Salir"
                elif quit_txt_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

    # Refrescando la screen surface a 60 FPS
    pygame.display.update()
    clock.tick(60)
