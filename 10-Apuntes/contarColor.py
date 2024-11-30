import cv2 as cv

img = cv.imread('Pez.jpg', 1)
img2 = cv.cvtColor(img, cv.COLOR_BGR2RGB)
img3 = cv.cvtColor(img2, cv.COLOR_RGB2HSV)

umbralBajo=(0, 80, 80  )
umbralAlto=(10, 255, 255)
umbralBajoB=(170, 80,80)
umbralAltoB=(180, 255, 255)


mascara1 = cv.inRange(img3, umbralBajo, umbralAlto)
mascara2 = cv.inRange(img3, umbralBajoB, umbralAltoB)

mascara = mascara1 + mascara2

resultado = cv.bitwise_and(img, img, mask=mascara)

cv.imshow('resultado', resultado)
cv.imshow('mascara', mascara)
cv.imshow('img',img)
cv.imshow('img2', img2)
cv.imshow('img3', img3)

cv.waitKey(0)
cv.destroyAllWindows()




def contar_islas(mascara):
    contador_islas = 0

    islas = mascara

    for i in range(len(islas)):
        for j in range(len(islas[i])):
            if islas[i][j] == 255:
                # Si se detecta una isla, se empiezan a llenar todas sus celdas adyacentes con 2
                recorrer_isla(islas, i, j)
                # Una vez se termina de llenar toda la isla, se incrementa el contador
                contador_islas += 1

    print(f"Total de Islas: {contador_islas}")
    #imprimir_matriz(islas)


def imprimir_matriz(matriz):
    for fila in matriz:
        print(*fila)


def recorrer_isla(matriz, fila, columna):
    # Validar si se está accediendo a una posición válida de la matriz
    # Posteriormente, se valida aquí mismo si la celda es tierra (tiene valor de 1)
    if 0 <= fila < len(matriz) and 0 <= columna < len(matriz[0]) and matriz[fila][columna] == 255:
        # Al detectar tierra, se cambia su valor de 1 a 2 y se continúa buscando más celdas adyacentes
        matriz[fila][columna] = 2
        recorrer_isla(matriz, fila + 1, columna)
        recorrer_isla(matriz, fila - 1, columna)
        recorrer_isla(matriz, fila, columna + 1)
        recorrer_isla(matriz, fila, columna - 1)


contar_islas(mascara)




