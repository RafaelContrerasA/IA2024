import numpy as np
import cv2 as cv
import os

# Función para contar píxeles blancos y negros y calcular proporción
def calcular_proporcion(imagen):
    pixeles_blancos = np.sum(imagen == 255)
    pixeles_negros = np.sum(imagen == 0)
    proporcion_blanco_negro = pixeles_blancos / pixeles_negros if pixeles_negros != 0 else float('inf')
    return proporcion_blanco_negro

# Función para procesar imágenes de una carpeta y calcular el promedio de proporciones
def procesar_carpeta(ruta_carpeta):
    imagenes = [archivo for archivo in os.listdir(ruta_carpeta) if archivo.endswith('.jpg') or archivo.endswith('.png')]
    
    suma_proporciones = 0
    total_imagenes = 0

    for imagen_archivo in imagenes:
        # Cargar la imagen
        imagen_ruta = os.path.join(ruta_carpeta, imagen_archivo)
        imagen = cv.imread(imagen_ruta, cv.IMREAD_GRAYSCALE)

        # Verificar si la imagen es válida (no nula)
        if imagen is not None:
            # Calcular la proporción blanco/negro
            proporcion = calcular_proporcion(imagen)
            suma_proporciones += proporcion
            total_imagenes += 1

    # Calcular el promedio de proporciones
    if total_imagenes > 0:
        promedio_proporcion = suma_proporciones / total_imagenes
        return promedio_proporcion, total_imagenes
    else:
        return None, 0

# Captura de imágenes desde la cámara
def capturar_imagenes():
    # Cargar el clasificador de rostros
    rostro = cv.CascadeClassifier('C:/Users/avalo/Desktop/IA alcaraz/obtener_proporcion_rostro/haarcascade_frontalface_alt_tree.xml')

    # Iniciar la captura de video
    cap = cv.VideoCapture(0)
    imagenes_guardadas = 0

    while imagenes_guardadas < 20:
        ret, frame = cap.read()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        rostros = rostro.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in rostros:
            # Extraer el rostro detectado
            frame2 = frame[y:y+h, x:x+w]

            # Redimensionar la imagen a 100x100 píxeles
            imagen_100x100 = cv.resize(frame2, (100, 100), interpolation=cv.INTER_AREA)

            # Convertir la imagen a escala de grises
            imagen_gris_100x100 = cv.cvtColor(imagen_100x100, cv.COLOR_BGR2GRAY)

            # Binarizar la imagen (convertir a blanco y negro)
            _, imagen_binaria_100x100 = cv.threshold(imagen_gris_100x100, 127, 255, cv.THRESH_BINARY)

            # Guardar la imagen binaria en 100x100
            cv.imwrite(f'C:/Users/avalo/Desktop/IA alcaraz/obtener_proporcion_rostro/caras100/rostro_binario_{imagenes_guardadas}.jpg', imagen_binaria_100x100)

            # Redimensionar la imagen a 80x80 píxeles
            imagen_80x80 = cv.resize(imagen_binaria_100x100, (80, 80), interpolation=cv.INTER_AREA)

            # Guardar la imagen binaria en 80x80
            cv.imwrite(f'C:/Users/avalo/Desktop/IA alcaraz/obtener_proporcion_rostro/caras80/rostro_binario_{imagenes_guardadas}.jpg', imagen_80x80)

            imagenes_guardadas += 1
            if imagenes_guardadas >= 20:
                break

        # Mostrar el video con los rostros detectados
        cv.imshow('Rostros', frame)

        # Salir al presionar 'Esc'
        if cv.waitKey(1) == 27:
            break

    # Liberar la captura de video y cerrar las ventanas
    cap.release()
    cv.destroyAllWindows()

# Procesar imágenes después de la captura
def procesar_imagenes():
    ruta_carpeta_100 = 'C:/Users/avalo/Desktop/IA alcaraz/obtener_proporcion_rostro/caras100'
    ruta_carpeta_80 = 'C:/Users/avalo/Desktop/IA alcaraz/obtener_proporcion_rostro/caras80'

    # Obtener promedio de proporciones para las imágenes 100x100
    promedio_100x100, total_100x100 = procesar_carpeta(ruta_carpeta_100)
    if promedio_100x100 is not None:
        print(f"Promedio de la proporción blanco/negro para {total_100x100} imágenes de 100x100: {promedio_100x100}")
    else:
        print("No se encontraron imágenes válidas en la carpeta 100x100.")

    # Obtener promedio de proporciones para las imágenes 80x80
    promedio_80x80, total_80x80 = procesar_carpeta(ruta_carpeta_80)
    if promedio_80x80 is not None:
        print(f"Promedio de la proporción blanco/negro para {total_80x80} imágenes de 80x80: {promedio_80x80}")
    else:
        print("No se encontraron imágenes válidas en la carpeta 80x80.")

# Primero capturamos las imágenes
capturar_imagenes()

# Luego procesamos las imágenes para calcular las proporciones
procesar_imagenes()
