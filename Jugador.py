import Variables
import pygame


class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.flip = False
        self.image = image
        self.forma = self.image.get_rect()
        self.forma.center = (x, y)

    def movimiento(self, delta_x, delta_y):
        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False

        if self.forma.left < 64:
            self.forma.left = 64
        if self.forma.right > Variables.ANCHOPANTALLA - 64:
            self.forma.right = Variables.ANCHOPANTALLA - 64
        if self.forma.top < 40:
            self.forma.top = 40
        if self.forma.bottom > Variables.ALTOPANTALLA - 70:
            self.forma.bottom = Variables.ALTOPANTALLA - 70

        self.forma.x = self.forma.x + delta_x
        self.forma.y = self.forma.y + delta_y

    def dibujo(self, interfaz):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(imagen_flip, self.forma)
        self.image.set_colorkey(Variables.VERDE)
