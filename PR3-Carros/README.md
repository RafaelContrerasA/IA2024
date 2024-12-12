# Proyecto 3: CNN Carros.
Programa para entrenar una CNN que sea capaz de reconcer 5 modelos distintos de carros
- Cheyenne (Clase 0)
- Hummer (Clase 1)
- Lamborghini (Clase 2)
- Tsuru (Clase 3)
- Vocho (Clase 4)

## Graficas de entrenamiento
![Graficas de entrenamiento](Graficas.png)

## Precision del modelo por clase
![Precision del modelo por clase](Precision.png)

## Ejemplo de output del modelo
![Ejemplo](Ejemplo.png)

## Codigo completo
```python

import numpy as np
import os
import re
import matplotlib.pyplot as plt
%matplotlib inline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import keras
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from keras.models import Sequential,Model
from tensorflow.keras.layers import Input
from keras.layers import Dense, Dropout, Flatten
#from keras.layers import Conv2D, MaxPooling2D
#from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    BatchNormalization, SeparableConv2D, MaxPooling2D, Activation, Flatten, Dropout, Dense, Conv2D
)
from keras.layers import LeakyReLU

print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

# Leer imágenes 

Este código está diseñado para recorrer un directorio específico y sus subdirectorios, leer todas las imágenes con extensiones .jpg, .jpeg, .png, .bmp, o .tiff, y almacenar información sobre estas imágenes y los directorios donde se encuentran.
from PIL import Image
import os
import re

dirname = os.path.join(os.getcwd(), r'C:\Users\avalo\Desktop\CNN carros\Dataset2')
imgpath = dirname + os.sep 

images = []
directories = []
dircount = []
prevRoot = ''
cant = 0

print("Leyendo imágenes de", imgpath)

for root, dirnames, filenames in os.walk(imgpath):
    for filename in filenames:
        if re.search(r"\.(jpg|jpeg|png|bmp|webp|tiff)$", filename, re.IGNORECASE):
            filepath = os.path.join(root, filename)
            try:
                with Image.open(filepath) as img:
                    if img.mode in ["RGB", "RGBA"]:
                        images.append(img.copy())
                    cant += 1
            except Exception as e:
                print(f"Error al leer el archivo {filepath}: {e}")
            if prevRoot != root:
                directories.append(root)
                dircount.append(cant)
                cant = 0
                prevRoot = root
dircount.append(cant)
dircount = dircount[1:]
dircount[0] += 1

print('Directorios leídos:', len(directories))
print("Imágenes en cada directorio:", dircount)
print('Suma total de imágenes en subdirs:', sum(dircount))

# Generación de Etiquetas 

Esta sección del código está asignando una etiqueta numérica a cada imagen basada en el directorio del que proviene. Si un directorio tiene 5 imágenes, todas esas imágenes tendrán la misma etiqueta (por ejemplo, 0), y luego la etiqueta cambiará para el próximo directorio. Esto es útil para clasificar las imágenes según sus directorios de origen.
labels=[]
indice=0
for cantidad in dircount:
    for i in range(cantidad):
        labels.append(indice)
    indice=indice+1
print("Cantidad etiquetas creadas: ",len(labels))
Esta sección del código permite identificar y almacenar los nombres de los subdirectorios de manera organizada, lo cual puede ser útil para el análisis posterior o para referenciar los datos procesados.
sriesgos=[]
indice=0
for directorio in directories:
    name = directorio.split(os.sep)
    print(indice , name[len(name)-1])
    sriesgos.append(name[len(name)-1])
    indice=indice+1
Esta sección del código convierte las listas de etiquetas e imágenes en arreglos de NumPy para facilitar su manipulación. Luego, identifica las clases únicas presentes en las etiquetas y calcula el número total de clases, imprimiendo esta información. Esto es útil para entender la distribución de las clases en el conjunto de datos y preparar los datos para análisis o entrenamiento de modelos.
y = np.array(labels)
X = np.array(images, dtype=np.uint8) #convierto de lista a numpy

classes = np.unique(y)
nClasses = len(classes)
print('Total number of outputs : ', nClasses)
print('Output classes : ', classes)
Esta sección del código divide el conjunto de datos en dos partes: datos de entrenamiento (80%) y datos de prueba (20%). Luego, imprime las dimensiones de estos conjuntos de datos. Esta división es crucial en el proceso de entrenamiento y evaluación de modelos de aprendizaje automático, ya que permite evaluar el rendimiento del modelo en datos no vistos durante el entrenamiento.
train_X,test_X,train_Y,test_Y = train_test_split(X,y,test_size=0.2)
print('Training data shape : ', train_X.shape, train_Y.shape)
print('Testing data shape : ', test_X.shape, test_Y.shape)
Esta sección del código utiliza Matplotlib para mostrar las primeras imágenes de los conjuntos de datos de entrenamiento y de prueba, junto con sus etiquetas correspondientes.
plt.figure(figsize=[5,5])

# Display the first image in training data
plt.subplot(121)
plt.imshow(train_X[0,:,:], cmap='gray')
plt.title("Ground Truth : {}".format(train_Y[0]))

# Display the first image in testing data
plt.subplot(122)
plt.imshow(test_X[0,:,:], cmap='gray')
plt.title("Ground Truth : {}".format(test_Y[0]))
Esta sección del código convierte los datos de imágenes a tipo de dato float32 y normaliza los valores de píxel para que estén en el rango [0, 1]. Luego, visualiza una imagen del conjunto de datos de prueba. La normalización es crucial para el entrenamiento efectivo de modelos de aprendizaje automático.
rain_X = train_X.astype('float32')
test_X = test_X.astype('float32')
train_X = train_X/255.
test_X = test_X/255.
plt.imshow(test_X[0,:,:])
Esta sección del código convierte las etiquetas de clase en formato entero a un formato de codificación one-hot. Esto es importante porque muchos algoritmos de aprendizaje automático, especialmente las redes neuronales, funcionan mejor con etiquetas en formato one-hot. Luego, se imprime una etiqueta antes y después de la conversión para verificar el proceso.
train_Y_one_hot = to_categorical(train_Y)
test_Y_one_hot = to_categorical(test_Y)
print('Original label:', train_Y[0])
print('After conversion to one-hot:', train_Y_one_hot[0])
Esta sección del código toma el conjunto de datos de entrenamiento y lo divide en dos conjuntos: uno para continuar el entrenamiento y otro para la validación. La validación es una parte crucial del proceso de entrenamiento de modelos de aprendizaje automático porque permite evaluar el rendimiento del modelo en datos no vistos durante el entrenamiento, ayudando a prevenir el sobreajuste.
#Mezclar todo y crear los grupos de entrenamiento y testing
train_X,valid_X,train_label,valid_label = train_test_split(train_X, train_Y_one_hot, test_size=0.2, random_state=13)
Esta sección del código es útil para verificar que los conjuntos de datos se han dividido correctamente y que las formas de los datos son las esperadas. Esto asegura que los datos estén listos para ser utilizados en el entrenamiento y validación del modelo.
print(train_X.shape,valid_X.shape,train_label.shape,valid_label.shape)
Esta sección del código define y configura varios parámetros importantes para el entrenamiento de una red neuronal. Estos parámetros incluyen la tasa de aprendizaje inicial, el número de épocas y el tamaño del lote.
#declaramos variables con los parámetros de configuración de la red
INIT_LR = 0.001 # Valor inicial de learning rate. El valor 1e-3 corresponde con 0.001
epochs = 95 # Cantidad de iteraciones completas al conjunto de imagenes de entrenamiento
batch_size = 16 # cantidad de imágenes que se toman a la vez en memoria
Esta sección del código define un modelo de red neuronal convolucional (CNN) utilizando la API de Keras. La red consta de varias capas, incluyendo capas convolucionales, de activación, de pooling, de normalización (Dropout) y densas (fully connected).
riesgo_model = Sequential()
riesgo_model.add(Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same', input_shape=(21,28,3)))
riesgo_model.add(BatchNormalization())
riesgo_model.add(MaxPooling2D((2, 2), padding='same'))
riesgo_model.add(Dropout(0.3))

riesgo_model.add(Conv2D(128, kernel_size=(3, 3), activation='relu', padding='same'))
riesgo_model.add(BatchNormalization())
riesgo_model.add(MaxPooling2D((2, 2), padding='same'))
riesgo_model.add(Dropout(0.3))

riesgo_model.add(Flatten())
riesgo_model.add(Dense(64, activation='relu'))
riesgo_model.add(Dropout(0.3))
riesgo_model.add(Dense(nClasses, activation='softmax'))
riesgo_model.summary()
Esta sección del código configura la función de pérdida, el optimizador y las métricas que se utilizarán durante el entrenamiento del modelo. La compilación del modelo es un paso crucial que prepara el modelo para ser entrenado con los datos.
riesgo_model.compile(loss=keras.losses.categorical_crossentropy, optimizer=tf.keras.optimizers.SGD(learning_rate=INIT_LR, decay=INIT_LR / 100),metrics=['accuracy'])

Esta sección del código entrena el modelo de red neuronal convolucional utilizando los datos de entrenamiento. Durante el entrenamiento, el modelo se ajusta iterativamente a los datos, actualizando sus parámetros para minimizar la función de pérdida. El conjunto de datos de validación se utiliza para monitorear el rendimiento del modelo y prevenir el sobreajuste.
riesgo_train = riesgo_model.fit(train_X, train_label, batch_size=batch_size,epochs=epochs,verbose=1,validation_data=(valid_X, valid_label))
riesgo_model.save(r'C:\Users\avalo\Desktop\CNN carros\ModeloGenerado\carros.h5')
test_eval = riesgo_model.evaluate(test_X, test_Y_one_hot, verbose=1)
print('Test loss:', test_eval[0])
print('Test accuracy:', test_eval[1])
accuracy = riesgo_train.history['accuracy']
val_accuracy = riesgo_train.history['val_accuracy']
loss = riesgo_train.history['loss']
val_loss = riesgo_train.history['val_loss']
epochs = range(len(accuracy))
plt.plot(epochs, accuracy, 'bo', label='Training accuracy')
plt.plot(epochs, val_accuracy, 'b', label='Validation accuracy')
plt.title('Training and validation accuracy')
plt.legend()
plt.figure()
plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()
plt.show()
predicted_classes2 = riesgo_model.predict(test_X)
predicted_classes=[]
for predicted_riesgo in predicted_classes2:
    predicted_classes.append(predicted_riesgo.tolist().index(max(predicted_riesgo)))
predicted_classes=np.array(predicted_classes)
predicted_classes.shape, test_Y.shape
correct = np.where(predicted_classes==test_Y)[0]
print("Found %d correct labels" % len(correct))
for i, correct in enumerate(correct[0:9]):
    plt.subplot(3,3,i+1)
    plt.imshow(test_X[correct].reshape(21,28,3), cmap='gray', interpolation='none')
    plt.title("{}, {}".format(sriesgos[predicted_classes[correct]],
                                                    sriesgos[test_Y[correct]]))

    plt.tight_layout()
incorrect = np.where(predicted_classes!=test_Y)[0]
print("Found %d incorrect labels" % len(incorrect))
for i, incorrect in enumerate(incorrect[0:9]):
    plt.subplot(3,3,i+1)
    plt.imshow(test_X[incorrect].reshape(21,28,3), cmap='gray', interpolation='none')
    plt.title("{}, {}".format(sriesgos[predicted_classes[incorrect]],
                                                    sriesgos[test_Y[incorrect]]))
    plt.tight_layout()
target_names = ["Class {}".format(i) for i in range(nClasses)]
print(classification_report(test_Y, predicted_classes, target_names=target_names))
import os
from PIL import Image
from rembg import remove
import numpy as np
from keras.models import load_model

# Cargar el modelo h5
modelo_h5 = r'C:\Users\avalo\Desktop\CNN carros\ModeloGenerado\carros.h5'
riesgo_model = load_model(modelo_h5)

images = []

# ESPECIFICAMOS UNAS IMÁGENES
filenames = [    
    r'C:\Users\avalo\Downloads\Tsuru1.jpg',
    r'C:\Users\avalo\Downloads\cheyenne1.webp',
    r'C:\Users\avalo\Downloads\lambo1.webp',
    r'C:\Users\avalo\Downloads\hummer1.jpg',
    r'C:\Users\avalo\Downloads\vocho1.jpg',    
]

# Crear la carpeta temp si no existe
os.makedirs("temp", exist_ok=True)

for filepath in filenames:
    # Abrimos la imagen con Pillow
    try:
        with Image.open(filepath) as img:
            # Cargar la imagen
            with open(filepath, 'rb') as file:
                input_image = file.read()
            
            # Eliminar el fondo
            output_image = remove(input_image)
                
            # Guardar temporalmente la imagen sin fondo
            temp_image_path = os.path.join("temp", os.path.basename(filepath))  # Usar solo el nombre del archivo
            with open(temp_image_path, 'wb') as temp_file:
                temp_file.write(output_image)
            
            # Cargar la imagen sin fondo, redimensionarla y convertirla a RGB si es necesario
            with Image.open(temp_image_path) as img:
                # Convertir a RGB si tiene canal alfa
                img_rgb = img.convert('RGB')
                img_resized = img_rgb.resize((21, 28))  # Asegúrate de que estas dimensiones sean correctas para tu modelo

                # Convertimos a array numpy
                image_array = np.array(img_resized)
                images.append(image_array)

    except Exception as e:
        print(f"Error al procesar la imagen {filepath}: {e}")

# Convertimos de lista a numpy array
X = np.array(images, dtype=np.uint8)

# Normalizamos los datos
test_X = X.astype('float32')
test_X = test_X / 255.0

# Realizamos la predicción
predicted_classes = riesgo_model.predict(test_X)

# Asegúrate de tener una lista de etiquetas o categorías en 'sriesgos'
sriesgos = ['Cheyenne','Hummer', 'Lamborghini', "Tsuru", 'Vocho']  # Reemplaza con tus etiquetas reales

for i, img_tagged in enumerate(predicted_classes):
    print(f"{filenames[i]} -> {sriesgos[np.argmax(img_tagged)]}")



```