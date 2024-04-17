import sys

import pygame

pygame.init()

screen = pygame.display.set_mode((1000, 500))

pygame.display.set_caption("PC Final Proyect")
clock = pygame.time.Clock()

text_main_title = pygame.font.Font('freesansbold.ttf', 50)
text_options = pygame.font.Font('freesansbold.ttf', 25)

text_color = (0, 0, 0)
txt_color_play = (255, 255, 255)
txt_color_colission = (115, 192, 182)


def draw_txt(text: str, font, txt_color, x: int, y: int):
    text_surface = font.render(text, True, txt_color)
    text_rect = text_surface.get_rect(midtop=(x, y))
    screen.blit(text_surface, text_rect)
    return text_rect


screen_surf = pygame.Surface((1000, 500))
screen_surf.fill((255, 255, 255))

portal_surf = pygame.image.load("images/portal_mainmenu.png").convert_alpha()
portal_rect = portal_surf.get_rect(center=(500, 250))

psj_surf = pygame.image.load("images/psj.png").convert_alpha()
psj_rect = psj_surf.get_rect(bottomleft=(200, 500))

while True:
    screen.blit(screen_surf, (0, 0))
    screen.blit(portal_surf, portal_rect)

    main_title_txt_rect = draw_txt("Menú Principal", text_main_title, text_color, 500, 50)
    # pygame.draw.rect(screen, "Cyan", main_title_txt_rect,, 40 )
    # pygame.draw.rect(screen, "Cyan", main_title_txt_rect, 20, 40)

    play_txt_rect = draw_txt("Jugar", text_options, txt_color_play, 500, 230)
    opts_txt_rect = draw_txt("Opciones", text_options, text_color, 200, 230)
    quit_txt_rect = draw_txt("Salir", text_options, text_color, 850, 230)

    mouse_pos = pygame.mouse.get_pos()
    if play_txt_rect.collidepoint(mouse_pos):
        draw_txt("Jugar", text_options, txt_color_colission, 500, 230)
    elif opts_txt_rect.collidepoint(mouse_pos):
        draw_txt("Opciones", text_options, txt_color_colission, 200, 230)
    elif quit_txt_rect.collidepoint(mouse_pos):
        draw_txt("Salir", text_options, txt_color_colission, 850, 230)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.key == pygame.K_ESCAPE:
                print("a")

    pygame.display.update()
    clock.tick(60)
