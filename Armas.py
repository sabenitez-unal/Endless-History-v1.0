import math

import pygame

import Variables


class Sniper:
    def __init__(self, image, imagen_bala):
        self.imagen_bala = imagen_bala
        self.imagen_original = image
        self.imagen = self.imagen_original
        self.angulo = 0
        self.forma = self.imagen_original.get_rect()
        self.dispara = False
        self.last_shoot = pygame.time.get_ticks()

    def update(self, Jugador):
        disparo_cooldown = Variables.COOLDOWN_BALAS_SNIPER
        bala = None
        self.forma.center = Jugador.forma.center
        self.forma.x += 10
        self.forma.y += 5
        keys = pygame.key.get_pressed()
        if any(keys[key] for key in
               (pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT)) and self.dispara == False and (
                pygame.time.get_ticks() - self.last_shoot >= disparo_cooldown):
            if keys[pygame.K_UP]:
                self.angulo = 90
            elif keys[pygame.K_DOWN]:
                self.angulo = -90
            elif keys[pygame.K_RIGHT]:
                self.angulo = 0
            elif keys[pygame.K_LEFT]:
                self.angulo = 180
            self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo)

            bala = Disparo(self.imagen_bala, self.forma.centerx, self.forma.centery, self.angulo)
            self.dispara = True
            self.last_shoot = pygame.time.get_ticks()

        # reset
        if not any(keys[key] for key in (pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT)):
            self.angulo = 0
            self.dispara = False
            self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo)

        return bala

    def dibujo(self, interfaz):
        interfaz.blit(self.imagen, self.forma)
        # pygame.draw.rect(interfaz, Variables.ROJO, self.forma, 1)

    def rotar_arma(self, rotar):
        if rotar:
            imagen_flip = pygame.transform.flip(self.imagen_original, True, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)
        else:
            imagen_flip = pygame.transform.flip(self.imagen_original, False, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)


class Shotgun:
    def __init__(self, image, imagen_bala):
        self.imagen_bala = imagen_bala
        self.imagen_original = image
        self.imagen = self.imagen_original
        self.angulo = 0
        self.forma = self.imagen_original.get_rect()
        self.dispara = False
        self.last_shoot = pygame.time.get_ticks()

    def update(self, Jugador):
        disparo_cooldown = Variables.COOLDOWN_BALAS_SHOTGUN
        balas = []
        bala = None
        self.forma.center = Jugador.forma.center
        self.forma.x += 10
        self.forma.y += 5
        keys = pygame.key.get_pressed()
        if any(keys[key] for key in
               (pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT)) and self.dispara == False and (
                pygame.time.get_ticks() - self.last_shoot >= disparo_cooldown):
            if keys[pygame.K_UP]:
                self.angulo = 90
            elif keys[pygame.K_DOWN]:
                self.angulo = -90
            elif keys[pygame.K_RIGHT]:
                self.angulo = 0
            elif keys[pygame.K_LEFT]:
                self.angulo = 180
            self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo)
            angulos = [self.angulo, self.angulo + 5, self.angulo - 5, self.angulo + 10, self.angulo - 10]

            for angulo in angulos:
                bala = Disparo(self.imagen_bala, self.forma.centerx, self.forma.centery, angulo)
                balas.append(bala)

            self.dispara = True
            self.last_shoot = pygame.time.get_ticks()

        # reset
        if not any(keys[key] for key in (pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT)):
            self.angulo = 0
            self.dispara = False
            self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo)

        return balas

    def dibujo(self, interfaz):
        interfaz.blit(self.imagen, self.forma)
        # pygame.draw.rect(interfaz, Variables.ROJO, self.forma, 1)

    def rotar_arma(self, rotar):
        if rotar:
            imagen_flip = pygame.transform.flip(self.imagen_original, True, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)
        else:
            imagen_flip = pygame.transform.flip(self.imagen_original, False, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)


class Gun:
    def __init__(self, image, imagen_bala):
        self.imagen_bala = imagen_bala
        self.imagen_original = image
        self.imagen = self.imagen_original
        self.angulo = 0
        self.forma = self.imagen_original.get_rect()
        self.dispara = False
        self.last_shoot = pygame.time.get_ticks()

    def update(self, Jugador):
        disparo_cooldown = Variables.COOLDOWN_BALAS_GUN
        bala = None
        self.forma.center = Jugador.forma.center
        self.forma.x += 10
        self.forma.y += 5
        keys = pygame.key.get_pressed()
        if any(keys[key] for key in
               (pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT)) and not self.dispara and (
                pygame.time.get_ticks() - self.last_shoot >= disparo_cooldown):
            if keys[pygame.K_UP]:
                self.angulo = 90
            elif keys[pygame.K_DOWN]:
                self.angulo = -90
            elif keys[pygame.K_RIGHT]:
                self.angulo = 0
            elif keys[pygame.K_LEFT]:
                self.angulo = 180
            self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo)
            bala = Disparo(self.imagen_bala, self.forma.centerx, self.forma.centery, self.angulo)

            self.dispara = True
            self.last_shoot = pygame.time.get_ticks()

        # reset
        if not any(keys[key] for key in (pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT)):
            self.angulo = 0
            self.dispara = False
            self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo)

        return bala

    def dibujo(self, interfaz):
        interfaz.blit(self.imagen, self.forma)
        # pygame.draw.rect(interfaz, Variables.ROJO, self.forma, 1)

    def rotar_arma(self, rotar):
        if rotar:
            imagen_flip = pygame.transform.flip(self.imagen_original, True, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)
        else:
            imagen_flip = pygame.transform.flip(self.imagen_original, False, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)


class Disparo(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angulo):
        pygame.sprite.Sprite.__init__(self)
        self.imagen_original = image
        self.angulo = angulo
        self.image = pygame.transform.rotate(self.imagen_original, self.angulo)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.delta_x = math.cos(math.radians(self.angulo)) * Variables.VELOCIDAD_BALA
        self.delta_y = -math.sin(math.radians(self.angulo)) * Variables.VELOCIDAD_BALA
        self.distancia_recorrida = 0

    def update(self):
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y
        self.distancia_recorrida += math.sqrt(self.delta_x ** 2 + self.delta_y ** 2)
        if Variables.ARMA_SEGUN_LEVEL == 1:
            if self.rect.right < 0 or self.rect.left > Variables.ANCHOPANTALLA or self.rect.bottom < 0 or self.rect.top > Variables.ALTOPANTALLA:
                self.kill()
        if Variables.ARMA_SEGUN_LEVEL == 2:
            if self.distancia_recorrida >= Variables.DISTANCIA_MAXIMA_BALA:
                self.kill()
                if self.rect.right < 0 or self.rect.left > Variables.ANCHOPANTALLA or self.rect.bottom < 0 or self.rect.top > Variables.ALTOPANTALLA:
                    self.kill()

    def dibujo(self, interfaz):
        interfaz.blit(self.image, self.rect)
