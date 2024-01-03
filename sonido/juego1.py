import pygame
import sys
import random 
from pygame.locals import *

# Inicialización de Pygame
pygame.init()

# Creación de la pantalla
W, H = 1000, 667
PANTALLA = pygame.display.set_mode((W, H))
pygame.display.set_caption('Vikingo')
icono = pygame.image.load('imagenes\Warrior_1\quieto.png')
pygame.display.set_icon(icono)

# Fondo del juego
try:
    fondo = pygame.image.load("imagenes/paisaje.jpg")
    PANTALLA.blit(fondo, (0, 0))
except pygame.error as e:
    print("Error al cargar el fondo:", e)

#Música de fondo
pygame.mixer.music.load('sonido/song.ogg')
pygame.mixer.music.play(-1)


# personaje juego 
quieto = pygame.image.load('imagenes\Warrior_1\quieto.png')
caminaDerecha = [pygame.image.load('imagenes\Warrior_1\caminar1.png'), pygame.image.load('imagenes\Warrior_1\caminar2.png'),
                 pygame.image.load('imagenes\Warrior_1\caminar3.png'), pygame.image.load('imagenes\Warrior_1\caminar4.png'),
                 pygame.image.load('imagenes\Warrior_1\caminar5.png'), pygame.image.load('imagenes\Warrior_1\caminar6.png'),
                 pygame.image.load('imagenes\Warrior_1\caminar7.png')]
caminaIzquierda = [pygame.image.load('imagenes\Warrior_1\caminarI1.png'), pygame.image.load('imagenes\Warrior_1\caminarI2.png'),
                   pygame.image.load('imagenes\Warrior_1\caminarI3.png'), pygame.image.load('imagenes\Warrior_1\caminarI4.png'),
                   pygame.image.load('imagenes\Warrior_1\caminarI5.png'), pygame.image.load('imagenes\Warrior_1\caminarI6.png'),
                   pygame.image.load('imagenes\Warrior_1\caminarI7.png')]
salta = [pygame.image.load('imagenes\Warrior_1\salto1.png'), pygame.image.load('imagenes\Warrior_1\salto2.png')]

#Sonido
sonido_arriba = pygame.image.load('sonido/volume_up.png')
sonido_abajo = pygame.image.load('sonido/volume_down.png')
sonido_mute = pygame.image.load('sonido/volume_muted.png')
sonido_max = pygame.image.load('sonido/volume_max.png')

# Variables
x = 0
px = 50
py = 500
ancho = 50
velocidad = 10

# Control de FPS
reloj = pygame.time.Clock()

# Pasos
cuentaPasos = 0

# Variables dirección
izquierda = False
derecha = False

# Variables salto
salto = False
# Contador de salto
cuentaSalto = 10

class Personaje(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 50, 50)
        self.image = pygame.image.load('imagenes/Warrior_1/quieto.png')
        self.velocidad = 10
        self.salto = False

# Clase para el personaje
class Personaje(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 50, 50)
        self.image = pygame.image.load('imagenes/Warrior_1/quieto.png')
        self.velocidad = 10
        self.salto = False

    def actualizar(self):
        if self.salto:
            if self.rect.y >= 350:  # Altura del salto (ajustable según el juego)
                self.salto = False
            else:
                self.rect.y -= 10
        else:
            if self.izquierda:
                if self.rect.x > self.velocidad:
                    self.rect.x -= self.velocidad
            elif self.derecha:
                if self.rect.x < 900 - self.velocidad - 50:  # Límite derecho de la pantalla (ajustable según el juego)
                    self.rect.x += self.velocidad

    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect)

    def colisionar(self, otro_objeto):
        if self.rect.colliderect(otro_objeto.rect):
            return True
        else:
            return False


# Función para dibujar el personaje en la pantalla
def recargaPantalla():
    global cuentaPasos
    global izquierda
    global derecha

    PANTALLA.blit(fondo, (0, 0))  # Dibujar el fondo estático

    # Movimiento a la izquierda
    if izquierda:
        if cuentaPasos + 1 < len(caminaIzquierda):
            PANTALLA.blit(caminaIzquierda[cuentaPasos // 1], (int(px), int(py)))
            cuentaPasos += 1
        else:
            PANTALLA.blit(caminaIzquierda[-1], (int(px), int(py)))  # Mostrar la última imagen cuando termine la animación
            cuentaPasos = 0  # Reiniciar el contador de pasos

    elif derecha:
        if cuentaPasos + 1 < len(caminaDerecha):
            PANTALLA.blit(caminaDerecha[cuentaPasos // 1], (int(px), int(py)))
            cuentaPasos += 1
        else:
            PANTALLA.blit(caminaDerecha[-1], (int(px), int(py)))  # Mostrar la última imagen cuando termine la animación
            cuentaPasos = 0  # Reiniciar el contador de pasos
    # Salto
    elif salto + 1 >= 2:
        PANTALLA.blit(salta[cuentaPasos // 1], (int(px), int(py)))
        cuentaPasos += 1

    # Personaje quieto
    else:
        PANTALLA.blit(quieto, (int(px), int(py)))


# Definir la clase Enemigo
class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("imagenes/enemigo/enemigo1.png").convert()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(W)  # Posición x aleatoria dentro del ancho de la pantalla
        self.rect.y = random.randrange(H - 100)  # Posición y aleatoria dentro del alto de la pantalla (dejando espacio en la parte inferior)

# Crear al personaje principal (jugador)
personaje = Personaje()
grupo_personajes = pygame.sprite.Group()
grupo_personajes.add(personaje)

# Crear al enemigo
enemigo1 = Enemigo()
grupo_enemigos = pygame.sprite.Group()
grupo_enemigos.add(enemigo1)  # Agregar al grupo de enemigos

cantidad_enemigos = 5  # Puedes ajustar la cantidad de enemigos según lo necesites

# Agregar enemigos al grupo
for _ in range(cantidad_enemigos):
    enemigo = Enemigo()
    grupo_enemigos.add(enemigo)

# Bucle principal del juego
def main():
    global personaje
    global px
    global py
    global cuentaPasos
    global izquierda
    global derecha
    global salto
    global cuentaSalto  # Agregar esta línea para usar la variable 'salto' globalmente
    ejecuta = True
    salto = False  # Asignar un valor a 'salto' al inicio de la función
    while ejecuta:
        PANTALLA.fill((0, 0, 0))  # Limpia la pantalla con un color de fondo

        # FPS
        reloj.tick(18)
    
        # Opción tecla pulsada
        keys = pygame.key.get_pressed()

        # Tecla A - Movimiento a la izquierda
        if keys[pygame.K_a] and px > velocidad:
            px -= velocidad
            izquierda = True
            derecha = False

        # Tecla D - Movimiento a la derecha
        elif keys[pygame.K_d] and px < 900 - velocidad - ancho:
            px += velocidad
            izquierda = False
            derecha = True
        
        # Personaje quieto
        else:
            izquierda = False
            derecha = False
            cuentaPasos = 0

        # Tecla SPACE - Salto
        if not salto:
            if keys[pygame.K_SPACE]:
                salto = True
                izquierda = False
                derecha = False
                cuentaPasos = 0
        else:
            if cuentaSalto >= -10:
                py -= (cuentaSalto * abs(cuentaSalto)) * 0.5
                cuentaSalto -= 1
            else:
                cuentaSalto = 10
                salto = False

        # Procesa los eventos del usuario
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

        # Actualizar y dibujar los enemigos
        grupo_enemigos.update()
        grupo_enemigos.draw(PANTALLA)

        # Comprobar colisiones entre el jugador y los enemigos
        if pygame.sprite.spritecollide(enemigo1, grupo_enemigos, False):
            # Si hay colisión entre el personaje y algún enemigo, finalizar el juego
            print("Has sido alcanzado por un enemigo. ¡Juego terminado!")

        
        # Actualizar y dibujar los enemigos
        grupo_enemigos.update()
        grupo_enemigos.draw(PANTALLA)



        # Control del audio
        #Baja volumen
        if keys[pygame.K_9] and pygame.mixer.music.get_volume() > 0.0:
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.01)
            PANTALLA.blit(sonido_abajo, (850, 25))
        elif keys[pygame.K_9] and pygame.mixer.music.get_volume() == 0.0:
            PANTALLA.blit(sonido_mute, (850, 25))

        #Sube volumen
        if keys[pygame.K_0] and pygame.mixer.music.get_volume() < 1.0:
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.01)
            PANTALLA.blit(sonido_arriba, (850, 25))
        elif keys [pygame.K_0] and pygame.mixer.music.get_volume() == 1.0:
                PANTALLA.blit(sonido_max, (850, 25))

        #Desactivar sonido
        elif keys[pygame.K_m]:
            pygame.mixer.music.set_volume(0.0)
            PANTALLA.blit(sonido_mute, (850, 25))

        #Reactivar sonido
        elif keys[pygame.K_COMMA]:
            pygame.mixer.music.set_volume(1.0)
            PANTALLA.blit(sonido_max, (850, 25))


        # Llamar a la función para actualizar la pantalla con el fondo y el personaje
        recargaPantalla()

        # Actualizar la pantalla
        pygame.display.update()

# Comprobación para ejecutar 'main' si este script se ejecuta directamente
if __name__ == "__main__":
    main()  # Llama a la función principal del juego