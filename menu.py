import pygame
import sys
from pygame.locals import *

# Inicialización de Pygame
pygame.init()

# Creación de la pantalla del menú
W, H = 800, 600
PANTALLA = pygame.display.set_mode((W, H))
pygame.display.set_caption('Menú Principal')

# Cargar el fondo del menú
try:
    fondo_menu = pygame.image.load("imagenes/paisaje.jpg")  # Ruta a tu imagen de fondo
    fondo_menu = pygame.transform.scale(fondo_menu, (W, H))  # Ajusta el tamaño al de la pantalla
except pygame.error as e:
    print("Error al cargar el fondo del menú:", e)
    fondo_menu = pygame.Surface((W, H))
    fondo_menu.fill((255, 255, 255))  # Un fondo blanco en caso de error

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)

# Fuente para el texto
fuente = pygame.font.Font('fuente/8-bitOut.ttf', 35)  # Ajusta el tamaño de la fuente

def mostrar_menu():
    texto_instrucciones = ("Bienvenido a VIKINGO\n"
                           "Sobrevive la mayor cantidad de tiempo posible\n"
                           "muevete con a y d\n "
                           "salta con el espacio\n"
                           "Presiona el número de la opción que deseas\n"
                           "1 Iniciar\n"
                           "2 Salir")
    
    while True:
        # Mostrar el fondo del menú
        PANTALLA.blit(fondo_menu, (0, 0))

        # Renderizar el texto en múltiples líneas
        lineas_texto = texto_instrucciones.split('\n')
        for i, linea in enumerate(lineas_texto):
            texto = fuente.render(linea, True, NEGRO)
            # Mostrar texto en la pantalla
            PANTALLA.blit(texto, (W // 2 - texto.get_width() // 2, H // 2 - len(lineas_texto) * 15 + i * 30))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_1:  # Si presiona la tecla '1'
                    return True
                elif event.key == K_2:  # Si presiona la tecla '2'
                    return False

if __name__ == "__main__":
    juego_iniciado = False

    while True:
        iniciar_juego = mostrar_menu()

        if iniciar_juego:
            import juego  # Importa tu juego principal

            if not juego_iniciado:
                pygame.init()
                juego_iniciado = True

            juego_principal = juego.Juego()
            juego_principal.ejecutar_juego()
        else:
            pygame.quit()
            sys.exit()