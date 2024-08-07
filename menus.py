import pygame
import Variables

screen = pygame.display.set_mode((Variables.ANCHOPANTALLA, Variables.ALTOPANTALLA))

pygame.display.set_caption("Jueguito Endless")


# Función para dibujar los textos cada vez que se necesiten
def draw_txt(text: str, font, txt_color, x: int, y: int):
    text_surface = font.render(text, True, txt_color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
    return text_rect


# Clase del menú principal
class MainMenu:
    def __init__(self, mouse_pos):
        self.mouse_pos = mouse_pos
        # Mostrando opciones del menú
        self.play_txt = draw_txt("JUGAR", Variables.text_options, Variables.txt_color_play, Variables.ANCHOPANTALLA // 2, Variables.txt_ops_y)
        self.quit_txt = draw_txt("SALIR", Variables.text_options, Variables.text_color, (Variables.ANCHOPANTALLA // 5) * 4 + 50, Variables.txt_ops_y)

    def menu(self):
        # Mostrando la superficie superpuesta y el portal
        # Mostrando texto principal del menu
        draw_txt("Menú Principal", Variables.text_titles, Variables.text_color, Variables.ANCHOPANTALLA // 2, Variables.ALTOPANTALLA // 8)

        # Cambiando de color los textos de las opciones ante un evento de colisión con mouse position
        if self.play_txt.collidepoint(self.mouse_pos):
            draw_txt("JUGAR", Variables.text_options, Variables.txt_color_colission, Variables.ANCHOPANTALLA // 2, Variables.txt_ops_y)
        elif self.quit_txt.collidepoint(self.mouse_pos):
            draw_txt("SALIR", Variables.text_options, Variables.txt_color_colission, (Variables.ANCHOPANTALLA // 5) * 4 + 50, Variables.txt_ops_y)

    def update(self, mouse_pos):
        self.__init__(mouse_pos)
        self.menu()


# Clase del menú de opciones
class PauseMenu:
    def __init__(self, mouse_pos):
        self.mouse_pos = mouse_pos
        self.quit_txt = draw_txt("SALIR AL MENÚ", Variables.text_options, Variables.text_color, Variables.ANCHOPANTALLA // 2, Variables.ALTOPANTALLA // 2 + 55)

    def menu(self):
        draw_txt("PRESIONA 'ESC' PARA REANUDAR", Variables.text_options, Variables.text_color, Variables.ANCHOPANTALLA // 2,Variables.ALTOPANTALLA // 4)

        if self.quit_txt.collidepoint(self.mouse_pos):
            draw_txt("SALIR AL MENÚ", Variables.text_options, Variables.txt_color_colission,Variables.ANCHOPANTALLA // 2, Variables.ALTOPANTALLA // 2 + 55)

    def update(self, mouse_pos):
        self.__init__(mouse_pos)
        self.menu()


''' class GameOverMenu:
    def __init__(self, mouse_pos):
        self.mouse_pos = mouse_pos
        self.rect = pygame.image.load("graphics/").convert_alpha()
        self.txt_game_over = draw_txt("VOLVER A JUGAR", Variables.text_options, Variables.text_color, Variables.ANCHOPANTALLA // 4, Variables.ALTOPANTALLA // 6 * 5)

    def menu(self):
        if self.txt_game_over.collidepoint(self.mouse_pos):
            draw_txt("VOLVER A JUGAR", Variables.text_options, Variables.txt_color_colission, Variables.ANCHOPANTALLA // 4, Variables.ALTOPANTALLA // 6 * 5)

    def update(self, mouse_pos):
        self.__init__(mouse_pos)
        self.menu() '''


class Portal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        portal_surf = pygame.image.load("graphics/portal_mainmenu.png").convert_alpha()
        portal_surf = pygame.transform.rotozoom(portal_surf, 0, 1.4)

        self.image = portal_surf
        self.rect = self.image.get_rect(center=(Variables.ANCHOPANTALLA // 2, Variables.ALTOPANTALLA // 2))

    def update(self):
        self.__init__()

