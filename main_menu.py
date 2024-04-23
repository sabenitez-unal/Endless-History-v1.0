import sys
import pygame


# Ajustar resoluciones
class Resolution:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))

    def draw_screen(self):
        self.screen.fill((203, 162, 220))


# Inicia el motor de pygame
pygame.init()

# Título de la ventana
pygame.display.set_caption("PC Final Proyect")
clock = pygame.time.Clock()

# Resolución inicial
resolution = Resolution(1000, 500)


# Creando el objeto de Portal
class Portal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        portal_surf = pygame.image.load("images/portal_mainmenu.png").convert_alpha()
        portal_surf = pygame.transform.rotozoom(portal_surf, 0, 1.4)

        self.image = portal_surf
        self.rect = self.image.get_rect(center=(resolution.width // 2, resolution.height // 2))

    def update(self):
        self.__init__()


portal = pygame.sprite.GroupSingle()
portal.add(Portal())

# Asignando colores a los textos
text_color = (0, 0, 0)
txt_color_play = (255, 255, 255)
txt_color_colission = (245, 176, 65)
# Creando fuentes de textos de opciones y título
text_titles = pygame.font.Font('fonts/PixelifySans-Regular.ttf', 60)
text_options = pygame.font.Font('fonts/PixelifySans-Regular.ttf', 35)

# VARIABLES MENU PRINCIPAL


# Función para dibujar los textos cada vez que se necesiten
def draw_txt(text: str, font, txt_color, x: int, y: int):
    text_surface = font.render(text, True, txt_color)
    text_rect = text_surface.get_rect(center=(x, y))
    resolution.screen.blit(text_surface, text_rect)
    return text_rect


# Resolución de ventana seleccionada
res_1_use = False
res_2_use = True

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
    # Distancia del texto de las opciones desde TOP
    txt_ops_y = resolution.height // 2
    resolution.draw_screen()

    # En el menú principal
    if game_in_menu:
        # Mostrando la superficie superpuesta y el portal
        portal.draw(resolution.screen)

        # Mostrando texto principal del menu
        draw_txt("Menú Principal", text_titles, text_color, resolution.width // 2, resolution.height // 8)
        # pygame.draw.rect(screen, "Cyan", main_title_txt_rect,, 40 )
        # pygame.draw.rect(screen, "Cyan", main_title_txt_rect, 20, 40)

        # Mostrando opciones del menú
        play_txt = draw_txt("JUGAR", text_options, txt_color_play, resolution.width // 2, txt_ops_y)
        opts_txt = draw_txt("OPCIONES", text_options, text_color, resolution.width // 5, txt_ops_y)
        quit_txt = draw_txt("SALIR", text_options, text_color, (resolution.width // 5)*4 + 50, txt_ops_y)

        # Cambiando de color los textos de las opciones ante un evento de colisión con mouse position
        if play_txt.collidepoint(mouse_pos):
            draw_txt("JUGAR", text_options, txt_color_colission, resolution.width // 2, txt_ops_y)
        elif opts_txt.collidepoint(mouse_pos):
            draw_txt("OPCIONES", text_options, txt_color_colission, resolution.width // 5, txt_ops_y)
        elif quit_txt.collidepoint(mouse_pos):
            draw_txt("SALIR", text_options, txt_color_colission, (resolution.width // 5)*4 + 50, txt_ops_y)

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
                    game_paused = False
                # Evento de click sobre "Opciones"
                elif opts_txt.collidepoint(mouse_pos):
                    game_options = True
                    game_in_menu = False
                # Evento de click sobre "Salir"
                elif quit_txt.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

    # Durante el menú de opciones
    elif game_options:
        draw_txt("MENÚ DE OPCIONES", text_options, text_color, resolution.width // 2, resolution.height // 5)
        draw_txt("Resolución:", text_options, text_color, resolution.width // 4, resolution.height // 2)

        # Mostrando opciones de resolución, resaltando la resolución en uso
        if res_1_use:
            res_1 = draw_txt("800 x 400", text_options, txt_color_colission, resolution.width // 2, resolution.height // 2)
            res_2 = draw_txt("1000 x 500", text_options, text_color, resolution.width // 4 * 3, resolution.height // 2)
        elif res_2_use:
            res_1 = draw_txt("800 x 400", text_options, text_color, resolution.width // 2, resolution.height // 2)
            res_2 = draw_txt("1000 x 500", text_options, txt_color_colission, resolution.width // 4 * 3, resolution.height // 2)
        draw_txt("Presiona 'ESC' para volver", text_options, text_color, resolution.width // 2, resolution.height // 5 * 4)

        # Resaltando resolución donde se pasa el puntero del mouse
        if res_1.collidepoint(mouse_pos):
            draw_txt("800 x 400", text_options, txt_color_colission, resolution.width // 2, resolution.height // 2)
        elif res_2.collidepoint(mouse_pos):
            draw_txt("1000 x 500", text_options, txt_color_colission, resolution.width // 4 * 3, resolution.height // 2)

        # Creando bucle de eventos
        for event in pygame.event.get():
            # Evento de cierre
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not game_playing:
                        game_in_menu = True
                    else:
                        game_paused = True
                    game_options = False
            if event.type == pygame.MOUSEBUTTONUP:
                if res_1.collidepoint(mouse_pos):
                    resolution = Resolution(800, 400)
                    res_1_use = True
                    res_2_use = False

                if res_2.collidepoint(mouse_pos):
                    resolution = Resolution(1000, 500)
                    res_1_use = False
                    res_2_use = True
                portal.update()

    # Menú se muestra mientras el juego no corre
    elif game_paused:
        draw_txt("PRESIONA 'ESC' PARA REANUDAR", text_options, text_color, resolution.width // 2, resolution.height // 4)
        opts_txt = draw_txt("OPCIONES", text_options, text_color, resolution.width // 2, resolution.height // 2)
        quit_txt = draw_txt("SALIR AL MENÚ", text_options, text_color, resolution.width // 2, resolution.height // 2 + 55)

        if opts_txt.collidepoint(mouse_pos):
            draw_txt("OPCIONES", text_options, txt_color_colission, resolution.width // 2, resolution.height // 2)
        elif quit_txt.collidepoint(mouse_pos):
            quit_txt = draw_txt("SALIR AL MENÚ", text_options, txt_color_colission, resolution.width // 2, resolution.height // 2 + 55)

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

    # Durante el juego
    elif game_playing:
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

    # Refrescando la screen surface a 60 FPS
    pygame.display.update()
    clock.tick(60)
