import pygame
import sys
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("PC Final Proyect")
clock = pygame.time.Clock()

text_font = pygame.font.Font('freesansbold.ttf', 50)

text_color = (255, 255, 255)


def draw_font(text: str, font, txt_color, x: int, y: int):
    text_surface = font.render(text, True, txt_color)
    screen.blit(text_surface, (x, y))


a_surface = pygame.Surface((50, 50))
a_surface.fill("Red")
a_x_pos = -50

b_surface = pygame.Surface((1000, 500))
b_surface.fill((234, 140, 194))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("a")

    a_x_pos += 3
    if a_x_pos >= 1000:
        a_x_pos = -50

    screen.blit(b_surface, (0, 0))
    draw_font("Menú Principal", text_font, text_color, 340, 50)
    screen.blit(a_surface, (a_x_pos, 0))

    pygame.display.update()
    clock.tick(60)
