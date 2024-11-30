import numpy as np
import cv2 as cv

# Cargar el clasificador de rostros de Haar, el archivo XML contiene datos preentrenados para la detección de rostros.
rostro = cv.CascadeClassifier('C:/Users/avalo/Desktop/IA Alcaraz/obtener_proporcion_rostro/haarcascade_frontalface_alt_tree.xml')

# Inicializar la captura de video desde la cámara (cámara con ID 0)
cap = cv.VideoCapture(0)

# Contador para nombrar las imágenes capturadas
i = 0

# Bucle principal para leer los fotogramas de la cámara en tiempo real
while True:
    # Leer un fotograma de la cámara
    ret, frame = cap.read()

    # Convertir el fotograma a escala de grises
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Detectar rostros en la imagen en escala de grises
    rostros = rostro.detectMultiScale(gray, 1.3, 5)

    # Recorrer todos los rostros detectados
    for (x, y, w, h) in rostros:
        # Dibujar un rectángulo alrededor del rostro detectado
        frame = cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Recortar el área del rostro
        frame2 = frame[y:y + h, x:x + w]
        frame4 = frame[y:y + h, x:x + w]

        # Redimensionar a 100x100 y 80x80 píxeles
        frame2_resized = cv.resize(frame2, (100, 100), interpolation=cv.INTER_AREA)
        frame4_resized = cv.resize(frame4, (80, 80), interpolation=cv.INTER_AREA)

        # Convertir ambas imágenes a escala de grises
        gray_100 = cv.cvtColor(frame2_resized, cv.COLOR_BGR2GRAY)
        gray_80 = cv.cvtColor(frame4_resized, cv.COLOR_BGR2GRAY)

        # Binarizar las imágenes (usar un umbral de 128)
        _, binarized_100 = cv.threshold(gray_100, 128, 255, cv.THRESH_BINARY)
        _, binarized_80 = cv.threshold(gray_80, 128, 255, cv.THRESH_BINARY)

        # Mostrar las imágenes originales y binarizadas
        #cv.imshow('Rostro 100x100 Grayscale', gray_100)
        cv.imshow('Rostro 100x100 Binarized', binarized_100)

        #cv.imshow('Rostro 80x80 Grayscale', gray_80)
        cv.imshow('Rostro 80x80 Binarized', binarized_80)

    # Incrementar el contador de imágenes guardadas
    i = i + 1

    # Esperar 1 milisegundo por la pulsación de una tecla; si la tecla 'Esc' (código ASCII 27) es presionada, romper el bucle
    k = cv.waitKey(1)
    if k == 27:
        break

# Liberar la cámara y cerrar todas las ventanas de OpenCV cuando se sale del bucle
cap.release()
cv.destroyAllWindows()