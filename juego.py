import pygame
import sys
import random
from pygame.locals import *

class Personaje(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.quieto = pygame.image.load('imagenes/Warrior_1/quieto.png')
        self.caminaDerecha = [
            pygame.image.load('imagenes/Warrior_1/caminar1.png'),
            pygame.image.load('imagenes/Warrior_1/caminar2.png'),
            pygame.image.load('imagenes/Warrior_1/caminar3.png'),
            pygame.image.load('imagenes/Warrior_1/caminar4.png'),
            pygame.image.load('imagenes/Warrior_1/caminar5.png'),
            pygame.image.load('imagenes/Warrior_1/caminar6.png'),
            pygame.image.load('imagenes/Warrior_1/caminar7.png')
        ]
        self.caminaIzquierda = [
            pygame.image.load('imagenes/Warrior_1/caminarI1.png'),
            pygame.image.load('imagenes/Warrior_1/caminarI2.png'),
            pygame.image.load('imagenes/Warrior_1/caminarI3.png'),
            pygame.image.load('imagenes/Warrior_1/caminarI4.png'),
            pygame.image.load('imagenes/Warrior_1/caminarI5.png'),
            pygame.image.load('imagenes/Warrior_1/caminarI6.png'),
            pygame.image.load('imagenes/Warrior_1/caminarI7.png')
        ]
        self.salta = [
            pygame.image.load('imagenes/Warrior_1/salto1.png'),
            pygame.image.load('imagenes/Warrior_1/salto2.png')
        ]

        # Posición y variables de movimiento
        self.x = 6
        self.px = 500
        self.py = 500
        self.ancho = 50
        self.velocidad_x = 1
        self.velocidad_y = 0.5  # Define la velocidad de salto
        self.gravedad = 1  # Define la gravedad

        # Pasos
        self.cuentaPasos = 0
        self.cuentaPasos_salto = 0

        # Dirección
        self.izquierda = False
        self.derecha = False

        # Salto
        self.salto = False
        self.cuentaSalto = 10

        self.image = self.quieto  # Imagen inicial
        self.rect = self.image.get_rect()

    def update(self):
        self.handle_movement()
        self.handle_jump()
        self.apply_gravity()
        self.limit_screen_bounds()
        self.update_position()
        self.update_sprite()

    def update_sprite(self):
        if self.izquierda:  # Si se está moviendo hacia la izquierda
            if self.cuentaPasos >= len(self.caminaIzquierda) * 3:
                self.cuentaPasos = 0
            self.image = self.caminaIzquierda[self.cuentaPasos // 3]
            self.cuentaPasos += 1
        elif self.derecha:  # Si se está moviendo hacia la derecha
            if self.cuentaPasos >= len(self.caminaDerecha) * 3:
                self.cuentaPasos = 0
            self.image = self.caminaDerecha[self.cuentaPasos // 3]
            self.cuentaPasos += 1
        else:  # Si no se está moviendo, se muestra la imagen de quieto
            self.image = self.quieto
            self.cuentaPasos = 0
    
    
    # Funciones refactorizadas para mejorar la modularidad y legibilidad


    def handle_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.move_sideways(-self.velocidad_x)
            self.set_direction(True, False)
        elif keys[pygame.K_d]:
            self.move_sideways(self.velocidad_x)
            self.set_direction(False, True)
        else:
            self.set_direction(False, False)

    def move_sideways(self, distance):
        self.px += distance
        self.check_horizontal_bounds()

    def check_horizontal_bounds(self):
        if self.px < 0:
            self.px = 0
        elif self.px > 1000 - self.ancho:
            self.px = 1000 - self.ancho

    def set_direction(self, left, right):
        self.izquierda = left
        self.derecha = right

    def handle_jump(self):
        if self.salto:
            if self.cuentaSalto >= -10:
                neg = 1 if self.cuentaSalto >= 1 else -1
                self.perform_jump(neg)
                self.animate_jump()
            else:
                self.finish_jump()

    def perform_jump(self, neg):
        self.py -= (self.cuentaSalto ** 1) * 0.5 * neg
        self.cuentaSalto -= 0.5

    def animate_jump(self):
        if self.cuentaSalto % 2 == 0:
            self.set_jump_image()

    def set_jump_image(self):
        self.image = self.salta[0] if self.image == self.salta[1] else self.salta[1]

    def finish_jump(self):
        self.salto = False
        self.cuentaSalto = 10
        self.image = self.quieto

    def apply_gravity(self):
        if not self.salto and self.py < 500:
            self.py += self.velocidad_y
            self.velocidad_y += self.gravedad

    def limit_screen_bounds(self):
        self.check_horizontal_bounds()

    def update_position(self):
        self.rect.x = self.px
        self.rect.y = self.py

    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect)

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, player, all_sprites, enemigos):
        super().__init__()
        self.player = player
        self.all_sprites = all_sprites
        self.enemigos = enemigos
        self.image = pygame.image.load('imagenes/enemigo/enemigo1.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.choice([0, 1000])
        self.rect.y = 500 

    def update(self):
        self.rect.x -= 1
        if pygame.sprite.collide_rect(self, self.player):
            self.player_die()

    def player_die(self):
        print("muerto :C")


class Juego:
    def __init__(self):
        pygame.init()
        self.PANTALLA = pygame.display.set_mode((1000, 667))
        pygame.display.set_caption('Vikingo')
        self.fondo = pygame.image.load("imagenes/paisaje.jpg")
        self.icono = pygame.image.load('imagenes/Warrior_1/quieto.png')
        pygame.display.set_icon(self.icono)
        self.personaje = Personaje()
        self.enemigos = pygame.sprite.Group()  # Grupo de enemigos

        # Crear grupo de todos los sprites y grupo de enemigos
        self.all_sprites = pygame.sprite.Group()
        self.enemigos = pygame.sprite.Group()

        # Agregar jugador y enemigos a los grupos respectivos
        self.personaje = Personaje()
        self.all_sprites.add(self.personaje)

        # Crear y agregar enemigos al grupo
        for _ in range(20):
            enemy = Enemigo(self.personaje, self.all_sprites, self.enemigos)
            self.enemigos.add(enemy)
            self.all_sprites.add(enemy)
        

    def manejar_eventos(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_a:
                    self.personaje.izquierda = True
                    self.personaje.derecha = False
                elif event.key == K_d:
                    self.personaje.derecha = True
                    self.personaje.izquierda = False
                elif event.key == K_SPACE:
                    self.personaje.salto = True

            elif event.type == KEYUP:
                if event.key == K_a or event.key == K_d:
                    self.personaje.izquierda = False
                    self.personaje.derecha = False
                    self.personaje.cuentaPasos = 0

    def actualizar_pantalla(self):
        self.PANTALLA.fill((0, 0, 0))
        self.PANTALLA.blit(self.fondo, (0, 0))
        self.personaje.update()
        self.personaje.dibujar(self.PANTALLA)

        # Actualizar y dibujar enemigos
        self.enemigos.update()
        self.enemigos.draw(self.PANTALLA)

        pygame.display.update()

    def ejecutar_juego(self):
        while True:
            self.manejar_eventos()
            self.actualizar_pantalla()

if __name__ == "__main__":
    juego = Juego()
    juego.ejecutar_juego()