import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Datos de entrenamiento
X = np.array([
    [0.9, 0.8, 0.2],
    [0.7, 0.6, 0.5],
    [0.4, 0.4, 0.8],
    [0.8, 0.9, 0.3],
    [0.5, 0.7, 0.6],
    [0.3, 0.5, 0.9]
])

Y = np.array([
    [1, 0, 0],  
    [0, 1, 0],  
    [0, 0, 1],  
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
])

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Crear el modelo de red neuronal multicapa
model = Sequential([
Dense(4, input_dim=3, activation='relu'), 
Dense(3, activation='sigmoid')
])

# Compilación del modelo
model.compile(optimizer='adam', 
              loss='categorical_crossentropy', 
              metrics=['accuracy'])

model.fit(X_train, y_train, epochs=20, batch_size=32, verbose=1)

# Evaluación del modelo
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"\nPrecisión en el conjunto de prueba: {accuracy:.2f}")

# Predicción con nuevos datos
pruebas = np.array([
    [0.1, 0.8, 0.2],
    [0.7, 0.6, 0.5],
    [0.4, 0.4, 0.8],
])

prediccion = model.predict(pruebas)
categorias = ['Riesgo Bajo', 'Riesgo Medio', 'Riesgo Alto']

for i, pred in enumerate(prediccion):
    print(f"Cliente {i+1}: {categorias[np.argmax(pred)]} - Probabilidades: {pred}")






