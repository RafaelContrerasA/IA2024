//////Enfoques de la IA
- Sistema que piensa como humano
- Sistemas que piensan racionalmente
- Sistemas que actuan como humanos
- Sistemas que actuan racionalmente

//////Tipos de IA
- Suave: Se especializa en un solo problema
- Dura: Puede tomar decisiones en varios contextos.

//capitulo 1,2,26 y 27
//Ia un enfoque moderno Russell


///Agentes inteligentes



////Medidas de rendimiento


///Racionalidad
Se define por 4 factores
-La medida de rendimineto que define el criterio de exito
-El conocimiento del medio en el que habota acumulado por el Agentes
-Las acciones que el agente puede llevar a cabo
-La secuencia de percepciones que...

////heuristica
Problema A*

Lista abierta: Mientras tengo la lista abierta esta la posibilidad de saltar
a dicha posicion. Posiciones a los que no hemos ido.

Lista cerrada: Por donde ya pase. La lista cerrada me va a dar la solucion

F= G + H 

-G: es el costo que te lleva al vecino mas cercano
-H: la  heurista o distancia que conozco del punto que estoy al punto final. 
es la distancia mas directa. Costo total al destino (sin contar muros)

Ej
Moverse diagonal 10
moverse vertical 10
en diagonal 14 (raiz de 200)


LA: O,K.L,P,U,T
LC:O


Se salta al vecino con F menor
(En el ejercicio se salta hacia P, y luego esta se coloca en la lista cerrada)

LA: O,K,L,~P,U,T
LC:O, P

Se salta hacia LA

LA: O,K,~L,~P,U,T
LC:O, P, L

Para f y g se calculan los valores a partir del nodo LA


No ocupas estar contiguo para moverte a esa casilla
La siguinte F mas pequeña es la letra U (porque todavia no esta en lista cerrada)

Despues de movernos a U se calculan los valores de Y y Z

Si hay varios valores con la misma H se elige la que este primero en la lista abierta
(Y, Z, K tienen H=50 se elige K porque esta antes en la lista)

Al saltar a K se vuelve a calcular los valores de T pero tomando como nodo base la K
(La G de F cambia de 28 a 20)

Saltamos a T
Se recalcula los valores de Y y Z otra vez pero tomando como nodo base a T
(G de Y cambia de 28 a 20)

Saltamos a G 
Se calculan los valores para A, B, C

Saltamos a Z
Se calculan los valores para 4,5,6

Saltamos a F
Se recalcula A (G pasa de 34 a 30)

Saltamos a y
Se recalcula 4 (G pasa de 38 a 30)

Saltamos a C
Se calculan los valores para D, I

Saltamos a I
Se calculan los valores para E, J, N, Ñ

Saltamos a Ñ
Se calculan los valores para S, R


Saltamos a S


Se calcula la solucion, de la S se hace backtracking de quien es el padre de la letra

Solucion final es: O L G C I N S


//Espacio de estados
Es espacio de estados es un grafo cuyos nodos representan las configuraciones alcanzables

Problema arriero puma lechuga

APCL 
inicial   final
(iiii)    (dddd)


//Ejercicio de monjes y canibales
Pueden cruzar dos al mismo tiempo, si hay mas canibales que monjes de algun lado pierdes


inicial
(ccc mmm)  (vvv vvv)

->
(cvv mmm)  (ccv vvv)

<-
(ccv mmm)  (cvv vvv)

->
(vvv mmm)  (cccvvv)

<-
(vvc mmm)  (ccvvvv)

->
(vvc mvv)  (ccmmvv)

<-
(vcc mmv)  (cmvvvv)

->
(vcc vvv)  (cmmmvv)

<-
(ccc vvv)  (vmmmvv)

->
(cvv vvv)  (ccmmmv)

<-
(ccv vvv)  (cvmmmv)

->
(vvv vvv)  (cccmmm)



(iii iii)
(idd iii)
(iid iii)
(ddd iii)
(idd iii)


//busqueda profundo

Se hace en preorden la busqueda del arbol hasta que encuentra la solucion


// Ejercicio Ranas
Ninguna rana se puede regresar
7 espacios
3 azules
3 rojas
QUieren cruzar al lafo opuesto, pueden saltar uno o dos espacios
Generar arbol de derivacion


//Aprendizaje supervisado
Requiere de etiquetas

//Operador puntual
Solo afectan a un solo pixel


//operador de caja
Tambien afectan los pixeles adyacentes

// Modelos de color


//Problema linealmente separable
QUe los datos pueden ser separados simplemente por una sola linea

//Dataset para el juego de esquivar bola
La altura de la bola es constante, la velocidad 


//23 oct
//Perceptron (redes neuronales)
-- Epocas (cuantas veces se hace)

Flujo general
Entradas (x1, x2) --> Funcion sumadora --> Funcion de activacion --> Salida --> target


Entradas- pesos sinapticos (cambian a partir del error que se va calculando)
Funciones de activacion: Relu, sigmoide y tangente hiperbolica

    sigmoide valores entro 0 y 1, 1 significaria que estra sobreajustado, si se queda en numeros s
    cercanos a 0.5 signfica que no sabe que hacer, no esta aprendiendo, el problema no es linealmente
    separable


Capas ocultas: ayudan a que problemas que normalmente son linearmente no separables sean capaces de 
ser separados.

Mientras mas capas mas "especialista" se vuelve la neurona, mientras que las primeras capas tiene conocimiento
mas general.


//Redes neuronales convolucionales
-Capas de convolucion 
-Capas de pooling 
-Capas de conexion
