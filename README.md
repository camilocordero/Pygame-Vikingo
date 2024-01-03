# Juego de Vikingo

Este es un simple juego desarrollado en Python utilizando Pygame. El juego presenta un personaje vikingo que puede moverse horizontalmente y realizar saltos en un paisaje de fondo. mientras recibe ataques de otros personajes
El objetivo es durar la mayor cantidad de tiempo posible en juego

![Menú de Inicio](imagenes/menu.png)

## Contenido

- [Requisitos](#requisitos)
- [Instrucciones de Uso](#instrucciones-de-uso)
- [Descripción del Código](#descripción-del-código)
- [Cómo Ejecutar](#cómo-ejecutar)
- [Créditos](#créditos)
- [Licencia](#licencia)

## Requisitos

- Python 3.x
- Pygame (instalable con `pip install pygame`)

## Instrucciones de Uso

1. Asegúrate de tener Python instalado.
2. Instala Pygame utilizando `pip install pygame`.
3. Ejecuta el juego mediante el archivo `main.py`.

## Descripción del Código

El código consiste en dos clases principales:
- `Personaje`: define las propiedades y comportamientos del personaje vikingo, como movimientos, saltos y límites de pantalla.
- `Juego`: inicializa la ventana del juego, maneja eventos y actualiza la pantalla.

El personaje puede moverse hacia la izquierda y derecha con las teclas 'A' y 'D' respectivamente, y saltar con la tecla 'ESPACIO'. La lógica de movimiento, salto y gravedad se encuentra en la clase `Personaje`.

## Cómo Ejecutar

Para ejecutar el juego, asegúrate de tener instalado Python y Pygame. Luego, sigue estos pasos:

1. Abre una terminal.
2. Navega al directorio donde se encuentra el código.
3. Ejecuta el comando: `python menu.py`.

## Créditos

Este juego fue creado por Camilo Cordero como parte de una prueba tecnica asignada al tutor.
