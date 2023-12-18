# Tetris

Este juego de tetris sigue las instrucciones del siguiente desafío: https://docs.google.com/document/d/1EJ0zanHbVCQM4bZ33vZvyaV7TAmXLKkc9KG6UpBDhPc/edit

## Descripción

Este programa es una implementación del clásico juego de Tetris, donde el objetivo es organizar y eliminar bloques que caen para acumular la mayor cantidad de puntos posible.

## Requisitos del Sistema

Asegúrate de tener instalado Python 3 y la librería pygame. Si no la tienes, puedes instalarla con:
` ` ` 
pip install pygame
` ` ` 

## Instrucciones de Uso

Clona este repositorio en tu máquina local:
` ` ` 
git clone [https://github.com/tu-usuario/tetris-game.git](https://github.com/saflores2/tetris.git)
` ` `   
Navega al directorio del juego:
` ` ` 
cd tetris
` ` ` 
Ejecuta el juego:
` ` ` 
python main.py
` ` ` 
## Características

Controles Sencillos: Utiliza las teclas de flecha para mover y girar las piezas, la barra espaciadora para hacer que las piezas caigan más rápido, Z o Left Control para la rotación en otro sentido y C o Shift para retener una pieza y usarla más tarde.

Puntuación: Cada vez que se elimininan fila suma puntos, si se hace de a más de una a la vez es mejor. También puedes sumar puntos con soft drop(flecha hacia abajo) y hard drop (barra espaciadora)

Niveles de Dificultad: Si completas 10 filas subes de nivel y la velocidad del juego aumenta.
