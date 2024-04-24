import pygame, sys

VERDE = (0, 255, 0)
NEGRO = (0, 0, 0)
ANCHOPANTALLA = 832
ALTOPANTALLA = 512


class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('idle_abajo.png').convert()
        self.image.set_colorkey(VERDE)
        self.rect = self.image.get_rect()
        self.rect.center = (ANCHOPANTALLA // 2, ALTOPANTALLA // 2)
        self.velocidad_x = 0
        self.velocidad_y = 0

    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        if self.rect.left < 64:
            self.rect.left = 64
        if self.rect.right > ANCHOPANTALLA - 64:
            self.rect.right = ANCHOPANTALLA - 64
        if self.rect.top < 40:
            self.rect.top = 40
        if self.rect.bottom > ALTOPANTALLA - 70:
            self.rect.bottom = ALTOPANTALLA - 70


class DisparoAR(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('laser.png').convert()
        self.image.set_colorkey(NEGRO)
        self.rect = self.image.get_rect()

    def update(self):
        
        self.rect.y -= 5
class DisparoAB(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('laser.png').convert()
        self.image.set_colorkey(NEGRO)
        self.rect = self.image.get_rect()

    def update(self):
        
        self.rect.y += 5

class DisparoIZ(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('laser.png').convert()
        self.image.set_colorkey(NEGRO)
        self.rect = self.image.get_rect()


    def update(self):
        
        self.rect.x -= 5

class DisparoDER(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('laser.png').convert()
        self.image.set_colorkey(NEGRO)
        self.rect = self.image.get_rect()

    def update(self):
        
        self.rect.x += 5


pygame.init()
screen = pygame.display.set_mode((ANCHOPANTALLA, ALTOPANTALLA))
clock = pygame.time.Clock()

fondo = pygame.image.load("mapa.png")

jugador = Jugador()

sprites = pygame.sprite.Group()
disparo_list = pygame.sprite.Group()

sprites.add(jugador)

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                jugador.velocidad_x = -5
            
            elif event.key == pygame.K_d:
                jugador.velocidad_x = 5
            
            elif event.key == pygame.K_w:
                jugador.velocidad_y = -5
            
            elif event.key == pygame.K_s:
                jugador.velocidad_y = 5
            
            elif event.key == pygame.K_SPACE:
            
                if jugador.velocidad_x != 0:
                    jugador.velocidad_x *= 2
            
                if jugador.velocidad_y != 0:
                    jugador.velocidad_y *= 2

            # Disparar
            if event.key == pygame.K_UP:
                nuevo_disparo = DisparoAR()  # Crear una nueva instancia de Disparo
                nuevo_disparo.rect.x = jugador.rect.x + 25
                nuevo_disparo.rect.y = jugador.rect.y - 20
                sprites.add(nuevo_disparo)  # Agregar la nueva instancia al grupo de sprites
                disparo_list.add(nuevo_disparo)
            if event.key == pygame.K_DOWN:
                nuevo_disparo = DisparoAB()  # Crear una nueva instancia de Disparo
                nuevo_disparo.rect.x = jugador.rect.x + 25
                nuevo_disparo.rect.y = jugador.rect.y + 20
                sprites.add(nuevo_disparo)  # Agregar la nueva instancia al grupo de sprites
                disparo_list.add(nuevo_disparo)
            if event.key == pygame.K_RIGHT:
                nuevo_disparo = DisparoDER()  # Crear una nueva instancia de Disparo
                nuevo_disparo.rect.x = jugador.rect.x + 40
                nuevo_disparo.rect.y = jugador.rect.y 
                sprites.add(nuevo_disparo)  # Agregar la nueva instancia al grupo de sprites
                disparo_list.add(nuevo_disparo)
            if event.key == pygame.K_LEFT:
                nuevo_disparo = DisparoIZ()  # Crear una nueva instancia de Disparo
                nuevo_disparo.rect.x = jugador.rect.x - 20
                nuevo_disparo.rect.y = jugador.rect.y 
                sprites.add(nuevo_disparo)  # Agregar la nueva instancia al grupo de sprites
                disparo_list.add(nuevo_disparo)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                jugador.velocidad_x = 0
            elif event.key == pygame.K_w or event.key == pygame.K_s:
                jugador.velocidad_y = 0

    # Actualizar posición del Jugador
    jugador.update()

    # Actualizar posición del disparo
    disparo_list.update()

    # Dibujar fondo
    screen.blit(fondo, (0, 0))

    # Dibujar sprites
    sprites.draw(screen)
    disparo_list.draw(screen)

    # Actualizar pantalla
    pygame.display.flip()

# Salir del juego
pygame.quit()