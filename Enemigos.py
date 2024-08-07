import Variables
import pygame
import random


class Slime(pygame.sprite.Sprite):
    def __init__(self, image, energia, velocidad):
        super().__init__()
        self.energia_maxima = energia
        self.energia_actual = self.energia_maxima
        self.image = image
        self.rect = self.image.get_rect()
        self.velocidad = velocidad
        self.rect.x = random.randint(0, Variables.ANCHOPANTALLA - self.rect.width)
        self.rect.y = random.randint(-100, -50)

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.top > Variables.ALTOPANTALLA:
            self.rect.x = random.randint(0, Variables.ANCHOPANTALLA - self.rect.width)
            self.rect.y = random.randint(-100, -50)

    def recibir_dano(self, cantidad):
        self.energia_actual -= cantidad
        if self.energia_actual == 0:
            self.kill()

    def dibujo(self, pantalla):
        pantalla.blit(self.image, self.rect)
