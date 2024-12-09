import pygame
import math
from queue import PriorityQueue

# Configuraciones iniciales
ANCHO_VENTANA = 600
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Visualización de A*")

# Inicializar pygame
pygame.init()

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)
AZUL = (0, 0, 255)

COSTO_HORIZONTAL_VERTICAL = 10
COSTO_DIAGONAL = 14



# Control de delay (en milisegundos)
DELAY = 500  # Ajusta este valor para aumentar/disminuir la velocidad


class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.vecinos = []
        self.g = float("inf")
        self.h = float("inf")
        self.f = float("inf")
        self.padre = None

    def get_pos(self):
        return self.fila, self.col

    def es_pared(self):
        return self.color == NEGRO

    def es_inicio(self):
        return self.color == NARANJA

    def es_fin(self):
        return self.color == PURPURA

    def restablecer(self):
        self.color = BLANCO

    def hacer_inicio(self):
        self.color = NARANJA

    def hacer_pared(self):
        self.color = NEGRO

    def hacer_fin(self):
        self.color = PURPURA

    def hacer_cerrado(self):
        self.color = ROJO

    def hacer_abierto(self):
        self.color = VERDE

    def hacer_camino(self):
        self.color = AZUL

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))
        if self.g != float("inf"):
            fuente = pygame.font.SysFont('Arial', 10)
            g_val = int(self.g) if self.g != float('inf') else " "
            f_val = int(self.f) if self.f != float('inf') else " "
            h_val = int(self.h) if self.h != float('inf') else " "
            texto = fuente.render(f"G:{g_val} F:{f_val} H:{h_val}", True, GRIS)
            ventana.blit(texto, (self.x + 2, self.y + 2))

    def actualizar_vecinos(self, grid):
        self.vecinos = []
        for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            fila, col = self.fila + i, self.col + j
            if 0 <= fila < self.total_filas and 0 <= col < self.total_filas and not grid[fila][col].es_pared():
                self.vecinos.append(grid[fila][col])


def heuristica(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return (abs(x1 - x2) + abs(y1 - y2))*COSTO_HORIZONTAL_VERTICAL


def reconstruir_camino(nodo_actual, dibujar):
    camino = []
    camino.append(nodo_actual.get_pos()) #Agregar el final al camino, estetico

    while nodo_actual.padre:
        nodo_actual = nodo_actual.padre
        nodo_actual.hacer_camino()
        camino.append(nodo_actual.get_pos())
        dibujar()

    # Imprimir la ruta final
    print("Ruta Final:")
    camino.reverse()
    for pos in camino:
        print(pos)
    

def a_estrella(dibujar, grid, inicio, fin):
    cont = 0
    open_set = PriorityQueue()
    open_set.put((0, cont, inicio))
    open_set_hash = {inicio}
    closed_set = set()

    inicio.g = 0
    inicio.f = heuristica(inicio.get_pos(), fin.get_pos())

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        nodo_actual = open_set.get()[2]
        open_set_hash.remove(nodo_actual)
        closed_set.add(nodo_actual)

        # Imprimir las listas abierta y cerrada
        print("Lista Abierta:", [n.get_pos() for n in open_set_hash])
        print("Lista Cerrada:", [n.get_pos() for n in closed_set])

        # Verificar si llegamos al nodo final
        if nodo_actual == fin:
            reconstruir_camino(fin, dibujar)
            return True

        # Recalcular los valores de los vecinos del nodo actual
        for vecino in nodo_actual.vecinos:
            if vecino in closed_set:
                continue

            # Determinar el costo del movimiento
            peso = (
                COSTO_DIAGONAL
                if abs(vecino.fila - nodo_actual.fila) + abs(vecino.col - nodo_actual.col) == 2
                else COSTO_HORIZONTAL_VERTICAL
            )
            temp_g = nodo_actual.g + peso

            # Solo actualizar si encontramos un camino mejor
            if temp_g < vecino.g:
                vecino.padre = nodo_actual
                vecino.g = temp_g
                vecino.h = heuristica(vecino.get_pos(), fin.get_pos())
                vecino.f = vecino.g + vecino.h

                # Agregar a open_set si no está ya en él
                if vecino not in open_set_hash:
                    cont += 1
                    open_set.put((vecino.f, cont, vecino))
                    open_set_hash.add(vecino)
                    if vecino != fin:
                        vecino.hacer_abierto()

        # Dibujar y retrasar para observar el algoritmo
         # Pausa para observar los pasos
        if nodo_actual != inicio:
            nodo_actual.hacer_cerrado()

        #Aca abajo pa que se imprima tambien el mov    
        dibujar()
        pygame.time.delay(DELAY) 

    return False



def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas)
            grid[i].append(nodo)
    return grid


def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))


def dibujar(ventana, grid, filas, ancho):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)

    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()


def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col


def main(ventana, ancho):
    FILAS = 9
    grid = crear_grid(FILAS, ancho)

    inicio = None
    fin = None

    corriendo = True

    while corriendo:
        dibujar(ventana, grid, FILAS, ancho)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            if pygame.mouse.get_pressed()[0]:  # Click izquierdo
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                if not inicio and nodo != fin:
                    inicio = nodo
                    inicio.hacer_inicio()

                elif not fin and nodo != inicio:
                    fin = nodo
                    fin.hacer_fin()

                elif nodo != fin and nodo != inicio:
                    nodo.hacer_pared()

            elif pygame.mouse.get_pressed()[2]:  # Click derecho
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                nodo.restablecer()
                if nodo == inicio:
                    inicio = None
                elif nodo == fin:
                    fin = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and inicio and fin:
                    for fila in grid:
                        for nodo in fila:
                            nodo.actualizar_vecinos(grid)

                    a_estrella(lambda: dibujar(ventana, grid, FILAS, ancho), grid, inicio, fin)

                if event.key == pygame.K_r:
                    inicio = None
                    fin = None
                    grid = crear_grid(FILAS, ancho)

    pygame.quit()


main(VENTANA, ANCHO_VENTANA)
