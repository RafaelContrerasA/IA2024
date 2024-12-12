## Proyecto 2: Phaser
Este codigo usa la libreria pygames para simular un personaje que salta una bala. Se juega de forma manual y se recolectan los datos del juego. Posteriormente se entrenan 2 modelos, uno con red neuronal y otro con arbol de decision, para finalmente hacer que el juego se mueva de manera automatica en base a lo que aprendió.


# Codigo entrenar red neuronal 
```python
def entrenar_modelo():
    global modelo_entrenado, datos_modelo
    if len(datos_modelo) < 10:  # Verificar que hay suficientes datos
        print("Insuficientes datos para entrenar el modelo.")
        return
    
    datos = np.array(datos_modelo)
    X = datos[:, :2]
    y = datos[:, 2]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelo = Sequential([
        Dense(4, input_dim=2, activation='relu'),
        #Dense(8, activation='relu'),               
        Dense(4, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    
    modelo.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    modelo.fit(X_train, y_train, epochs=50, batch_size=32, verbose=1)
    loss, accuracy = modelo.evaluate(X_test, y_test, verbose=0)
    print(f"Modelo entrenado con precisión: {accuracy:.2f}")

```


# Codigo entrenar arbol decision
```python
def entrenar_modelo_arbol():
    global modelo_entrenado_arbol, datos_modelo
    if len(datos_modelo) < 10:  # Verificar que hay suficientes datos
        print("Insuficientes datos para entrenar el modelo.")
        return
    
    # Convertir datos en DataFrame para facilitar la manipulación
    dataset = pd.DataFrame(datos_modelo, columns=['Velocidad', 'Distancia', 'Salto'])
    X = dataset[['Velocidad', 'Distancia']]  # Características de entrada
    y = dataset['Salto']  # Etiquetas

    # Dividir datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=44)

    # Crear y entrenar el modelo
    clf = DecisionTreeClassifier(
        criterion='gini',          # Índice de Gini
        #class_weight='balanced',   # Ajustar pesos si las clases están desbalanceadas
        random_state=44
    )
    clf.fit(X_train, y_train)

    # Evaluar el modelo
    accuracy = clf.score(X_test, y_test)
    print(f"Modelo de árbol entrenado con precisión: {accuracy:.2f}")

    modelo_entrenado_arbol = clf

```

# Codigo predicir en base al modelo de red neuronal
```python
def decidir_salto():
    global modelo_entrenado, salto, en_suelo
    if modelo_entrenado is None:
        return
    
    distancia = abs(jugador.x - bala.x)
    entrada = np.array([[velocidad_bala, distancia]])

    #Hacer preddicion con el modelo
    prediccion = modelo_entrenado.predict(entrada)[0][0]
    
    if prediccion > 0.5 and en_suelo:
        salto = True
        en_suelo = False
        print("Decidio: Saltar")
    else:
        print("Decidio: NO saltar")
```


# Codigo predicir en base al modelo de arbol de decision
```python
def decidir_salto_arbol():
    global modelo_entrenado_arbol, salto, en_suelo
    if modelo_entrenado_arbol is None:
        print("Modelo no entrenado. No se puede decidir.")
        return

    distancia = abs(jugador.x - bala.x)
    entrada = pd.DataFrame([[velocidad_bala, distancia]], columns=['Velocidad', 'Distancia'])  # Formato: [[velocidad, distancia]]

    # Hacer predicción con el modelo
    prediccion = modelo_entrenado_arbol.predict(entrada)[0]

    if prediccion == 1 and en_suelo: 
        salto = True
        en_suelo = False
        print("Decidió: Saltar")
    else:
        print("Decidió: NO saltar")
```

## Codigo Completo
```python
import pygame
import random
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
#import graphviz

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego: Disparo de Bala, Salto, Nave y Menú")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Variables del jugador, bala, nave, fondo, etc.
jugador = None
bala = None
fondo = None
nave = None
menu = None

# Variables de salto
salto = False
salto_altura = 15  # Velocidad inicial de salto
gravedad = 1
en_suelo = True

# Variables de pausa y menú
pausa = False
fuente = pygame.font.SysFont('Arial', 20)
menu_activo = True
modo_auto = False  # Indica si el modo de juego es automático
modo_arbol = False

# Lista para guardar los datos de velocidad, distancia y salto (target)
datos_modelo = []
modelo_entrenado = None
modelo_entrenado_arbol = None

# Cargar las imágenes
jugador_frames = [
    pygame.image.load('assets/sprites/mono_frame_1.png'),
    pygame.image.load('assets/sprites/mono_frame_2.png'),
    pygame.image.load('assets/sprites/mono_frame_3.png'),
    pygame.image.load('assets/sprites/mono_frame_4.png')
]

bala_img = pygame.image.load('assets/sprites/purple_ball.png')
fondo_img = pygame.image.load('assets/game/fondo2.png')
nave_img = pygame.image.load('assets/game/ufo.png')
menu_img = pygame.image.load('assets/game/menu.png')

# Escalar la imagen de fondo para que coincida con el tamaño de la pantalla
fondo_img = pygame.transform.scale(fondo_img, (w, h))

# Crear el rectángulo del jugador y de la bala
jugador = pygame.Rect(50, h - 100, 32, 48)
bala = pygame.Rect(w - 50, h - 90, 16, 16)
nave = pygame.Rect(w - 100, h - 100, 64, 64)
menu_rect = pygame.Rect(w // 2 - 135, h // 2 - 90, 270, 180)  # Tamaño del menú

# Variables para la animación del jugador
current_frame = 0
frame_speed = 10  # Cuántos frames antes de cambiar a la siguiente imagen
frame_count = 0

# Variables para la bala
velocidad_bala = -10  # Velocidad de la bala hacia la izquierda
bala_disparada = False

# Variables para el fondo en movimiento
fondo_x1 = 0
fondo_x2 = w

intervalo_decidir_salto = 1  # Ejecutar decidir_salto cada 10 frames
contador_decidir_salto = 0

# Función para disparar la bala
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-11, -6)  # Velocidad aleatoria negativa para la bala
        bala_disparada = True

# Función para reiniciar la posición de la bala
def reset_bala():
    global bala, bala_disparada
    bala.x = w - 50  # Reiniciar la posición de la bala
    bala_disparada = False

# Función para manejar el salto
def manejar_salto():
    global jugador, salto, salto_altura, gravedad, en_suelo

    if salto:
        jugador.y -= salto_altura  # Mover al jugador hacia arriba
        salto_altura -= gravedad  # Aplicar gravedad (reduce la velocidad del salto)

        # Si el jugador llega al suelo, detener el salto
        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto = False
            salto_altura = 15  # Restablecer la velocidad de salto
            en_suelo = True

# Función para actualizar el juego
def update():
    global bala, velocidad_bala, current_frame, frame_count, fondo_x1, fondo_x2

    # Mover el fondo
    fondo_x1 -= 1
    fondo_x2 -= 1

    # Si el primer fondo sale de la pantalla, lo movemos detrás del segundo
    if fondo_x1 <= -w:
        fondo_x1 = w

    # Si el segundo fondo sale de la pantalla, lo movemos detrás del primero
    if fondo_x2 <= -w:
        fondo_x2 = w

    # Dibujar los fondos
    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

    # Animación del jugador
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0

    # Dibujar el jugador con la animación
    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))

    # Dibujar la nave
    pantalla.blit(nave_img, (nave.x, nave.y))

    # Mover y dibujar la bala
    if bala_disparada:
        bala.x += velocidad_bala

    # Si la bala sale de la pantalla, reiniciar su posición
    if bala.x < 0:
        reset_bala()

    pantalla.blit(bala_img, (bala.x, bala.y))

    # Colisión entre la bala y el jugador
    if jugador.colliderect(bala):
        print("Colisión detectada!")
        reiniciar_juego()  # Terminar el juego y mostrar el menú

# Función para guardar datos del modelo en modo manual
def guardar_datos():
    global jugador, bala, velocidad_bala, salto
    distancia = abs(jugador.x - bala.x)
    salto_hecho = 1 if salto else 0  # 1 si saltó, 0 si no saltó
    # Guardar velocidad de la bala, distancia al jugador y si saltó o no
    datos_modelo.append((velocidad_bala, distancia, salto_hecho))

# Función para pausar el juego y guardar los datos
def pausa_juego():
    global pausa
    pausa = not pausa
    if pausa:
        print("Juego pausado. Datos registrados hasta ahora:", datos_modelo)
    else:
        print("Juego reanudado.")

# Función para mostrar el menú y seleccionar el modo de juego
def mostrar_menu():
    global menu_activo, modo_auto, modo_arbol, datos_modelo, modelo_entrenado, modelo_entrenado_arbol
    pantalla.fill(NEGRO)
    texto = fuente.render("Presiona 'A' para Auto, 'M' para Manual, E para entrenar, L para limpiar,  G para graficar o 'Q' para Salir", True, BLANCO)
    pantalla.blit(texto, (w // 20, h // 2))
    texto2 = fuente.render(" 'T' para modo Arbol, 'R' para Reiniciar", True, BLANCO)
    pantalla.blit(texto2, (w // 20, h // 6))
    pygame.display.flip()

    while menu_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:
                    modo_auto = True
                    modo_arbol = False
                    menu_activo = False
                   # graficar_arbol()

                elif evento.key == pygame.K_m:
                    modo_auto = False
                    modo_arbol= False
                    menu_activo = False

                elif evento.key == pygame.K_t:
                    modo_auto = False
                    modo_arbol= True
                    menu_activo = False
                
                #limpiar modelo y datos
                elif evento.key == pygame.K_l:
                    print("Limpiando datos...")
                    datos_modelo = []
                    modelo_entrenado = None
                    modelo_entrenado_arbol = None
                    print("Datos y modelo limpiados...")

                #Hacer grafica
                elif evento.key == pygame.K_g:
                    # Cargar el dataset
                    dataset = datos_modelo

                    # Extraer datos individuales
                    x = [dato[0] for dato in dataset]  # Velocidad de la bala
                    y = [dato[1] for dato in dataset]  # Distancia entre el jugador y la bala
                    z = [dato[2] for dato in dataset]  # Salto hecho (1 si saltó, 0 si no)

                    print(x)
                    # Crear una figura 3D
                    fig = plt.figure()
                    ax = fig.add_subplot(111, projection='3d')

                    # Graficar los puntos en 3D
                    ax.scatter(x, y, z, c='r', marker='o')

                    # Etiquetas de los ejes
                    ax.set_xlabel('Velocidad')
                    ax.set_ylabel('Distancia')
                    ax.set_zlabel('Salto ')

                    # Mostrar la gráfica
                    plt.show()

                elif evento.key == pygame.K_q:
                    #print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()
                elif evento.key == pygame.K_e:
                    print("Entrenando red neuronal...")
                    entrenar_modelo()
                    print("Red entrenada")
                    print("Entrenando arbol...")
                    entrenar_modelo_arbol()
                    print("Arbol entrenado")
                    

# Función para reiniciar el juego tras la colisión
def reiniciar_juego():
    global menu_activo, jugador, bala, nave, bala_disparada, salto, en_suelo
    menu_activo = True  # Activar de nuevo el menú
    jugador.x, jugador.y = 50, h - 100  # Reiniciar posición del jugador
    bala.x = w - 50  # Reiniciar posición de la bala
    nave.x, nave.y = w - 100, h - 100  # Reiniciar posición de la nave
    bala_disparada = False
    salto = False
    en_suelo = True
    # Mostrar los datos recopilados hasta el momento
    #print("Datos recopilados para el modelo: ", datos_modelo)
    mostrar_menu()  # Mostrar el menú de nuevo para seleccionar modo

###### Entrenar modelo con los datos recolectados
def entrenar_modelo():
    global modelo_entrenado, datos_modelo
    if len(datos_modelo) < 10:  # Verificar que hay suficientes datos
        print("Insuficientes datos para entrenar el modelo.")
        return
    
    datos = np.array(datos_modelo)
    X = datos[:, :2]
    y = datos[:, 2]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelo = Sequential([
        Dense(4, input_dim=2, activation='relu'),
        #Dense(8, activation='relu'),               
        Dense(4, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    
    modelo.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    modelo.fit(X_train, y_train, epochs=50, batch_size=32, verbose=1)
    loss, accuracy = modelo.evaluate(X_test, y_test, verbose=0)
    print(f"Modelo entrenado con precisión: {accuracy:.2f}")
    modelo_entrenado = modelo

#####Funcion que predice si saltar o no con la red neuronal
def decidir_salto():
    global modelo_entrenado, salto, en_suelo
    if modelo_entrenado is None:
        return
    
    distancia = abs(jugador.x - bala.x)
    entrada = np.array([[velocidad_bala, distancia]])

    #Hacer preddicion con el modelo
    prediccion = modelo_entrenado.predict(entrada)[0][0]
    
    if prediccion > 0.5 and en_suelo:
        salto = True
        en_suelo = False
        print("Decidio: Saltar")
    else:
        print("Decidio: NO saltar")

#####Entrenar arbol de decision
def entrenar_modelo_arbol():
    global modelo_entrenado_arbol, datos_modelo
    if len(datos_modelo) < 10:  # Verificar que hay suficientes datos
        print("Insuficientes datos para entrenar el modelo.")
        return
    
    # Convertir datos en DataFrame para facilitar la manipulación
    dataset = pd.DataFrame(datos_modelo, columns=['Velocidad', 'Distancia', 'Salto'])
    X = dataset[['Velocidad', 'Distancia']]  # Características de entrada
    y = dataset['Salto']  # Etiquetas

    # Dividir datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=44)

    # Crear y entrenar el modelo
    clf = DecisionTreeClassifier(
        criterion='gini',          # Índice de Gini
        #class_weight='balanced',   # Ajustar pesos si las clases están desbalanceadas
        random_state=44
    )
    clf.fit(X_train, y_train)

    # Evaluar el modelo
    accuracy = clf.score(X_test, y_test)
    print(f"Modelo de árbol entrenado con precisión: {accuracy:.2f}")

    modelo_entrenado_arbol = clf

#####Funcion que usa el arbol para decidir si saltar o no
def decidir_salto_arbol():
    global modelo_entrenado_arbol, salto, en_suelo
    if modelo_entrenado_arbol is None:
        print("Modelo no entrenado. No se puede decidir.")
        return

    distancia = abs(jugador.x - bala.x)
    entrada = pd.DataFrame([[velocidad_bala, distancia]], columns=['Velocidad', 'Distancia'])  # Formato: [[velocidad, distancia]]

    # Hacer predicción con el modelo
    prediccion = modelo_entrenado_arbol.predict(entrada)[0]

    if prediccion == 1 and en_suelo: 
        salto = True
        en_suelo = False
        print("Decidió: Saltar")
    else:
        print("Decidió: NO saltar")

#def graficar_arbol():
    # # Convertir datos_modelo en un DataFrame
    # dataset = pd.DataFrame(datos_modelo, columns=['Velocidad', 'Distancia', 'Salto'])

    # # Definir características (X) y etiquetas (y)
    # X = dataset[['Velocidad', 'Distancia']]
    # y = dataset['Salto']

    # # Dividir los datos en conjunto de entrenamiento y prueba
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # # Crear el clasificador de Árbol de Decisión
    # clf = DecisionTreeClassifier()

    # # Entrenar el modelo
    # clf.fit(X_train, y_train)

    # # Exportar el árbol de decisión en formato DOT para su visualización
    # dot_data = export_graphviz(clf, out_file=None, 
    #                            feature_names=['Velocidad', 'Distancia'],  
    #                            class_names=['No Salto', 'Salto'],  
    #                            filled=True, rounded=True,  
    #                            special_characters=True)

    # # Crear el gráfico con graphviz
    # #graph = graphviz.Source(dot_data)

    # Mostrar el gráfico
    #graph.view()

def main():
    global salto, en_suelo, bala_disparada, contador_decidir_salto

    reloj = pygame.time.Clock()
    mostrar_menu()  # Mostrar el menú al inicio
    correr = True

    while correr:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo and not pausa:  # Detectar la tecla espacio para saltar
                    salto = True
                    en_suelo = False
                if evento.key == pygame.K_p:  # Presiona 'p' para pausar el juego
                    pausa_juego()
                if evento.key == pygame.K_r:  # Presiona 'p' para pausar el juego
                    reiniciar_juego()
                if evento.key == pygame.K_q:  # Presiona 'q' para terminar el juego
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()

        if not pausa:
            # Modo manual: el jugador controla el salto
            if not modo_auto or modo_arbol:
                if salto:
                    manejar_salto()
                # Guardar los datos si estamos en modo manual
                guardar_datos()

            if modo_auto:         
                
                if contador_decidir_salto >= intervalo_decidir_salto:
                    decidir_salto()
                    contador_decidir_salto = 0  # Reiniciar el contador
                else:
                    contador_decidir_salto += 1

                if salto:
                    manejar_salto()
            
            if modo_arbol:         
                
                if contador_decidir_salto >= intervalo_decidir_salto:
                    decidir_salto_arbol()
                    contador_decidir_salto = 0  # Reiniciar el contador
                else:
                    contador_decidir_salto += 1

                if salto:
                    manejar_salto()


            # Actualizar el juego
            if not bala_disparada:
                disparar_bala()
            update()

        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(60)  # Limitar el juego a 30 FPS

    pygame.quit()

if __name__ == "__main__":
    main()

```