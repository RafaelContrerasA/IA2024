import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Cargar el dataset
file_path = 'C:/Users/avalo/Desktop/IA alcaraz/graficas phaser/datos_entrenamiento1.csv'
dataset = pd.read_csv(file_path)

# Crear una figura 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Definir los datos del CSV
x = dataset['DesplazamientoBala']
y = dataset['VelocidadBala']
z = dataset['EstatusAire']

# Graficar los puntos en 3D
ax.scatter(x, y, z, c='r', marker='o')

# Etiquetas de los ejes
ax.set_xlabel('DesplazamientoBala')
ax.set_ylabel('VelocidadBala')
ax.set_zlabel('EstatusAire')

# Mostrar la gráfica
plt.show()