## Contar Islas

Este programa cuenta el número de islas en una matriz, donde las islas están formadas por celdas adyacentes que contienen el valor `1`.



```java
public class ContarIslas {

    public static void main(String[] args) {        
        
        int[][] islas = {
            {0, 0, 0, 0, 0, 1, 0, 0},
            {0, 1, 0, 0, 0, 0, 1, 1},
            {0, 1, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 1, 0, 0},
            {0, 0, 1, 0, 0, 1, 1, 1},
            {0, 1, 1, 1, 0, 1, 0, 0},
            {0, 0, 1, 0, 0, 1, 1, 0},
            {0, 0, 0, 0, 0, 0, 0, 0}
        };
```       
### Recorrido de Matriz
Se tiene una variable para ir contando las islas encontradas. Con un ciclo se va recorriendo la matriz de izquierda hasta encontrarse con un `1` (isla). Al encontrarla se llama a una funcion recursiva que va identificando a todas las celdas adyacentes que pertenecen a esa misma isla.
       
```java      
        int contadorIslas=0;
        
        for (int i = 0; i < islas.length; i++) {
            for (int j = 0; j < islas[i].length; j++) {
                if(islas[i][j]==1){
                    //Si se detecta una isla se empiezan a llenar todas sus celdas adyacentes con 2
                    recorrerIsla(islas, i, j);
                    
                    //Una vez se termino de llenar toda la isla se incrementa el contador
                    contadorIslas++;               
                }
                
            }
        }
        
        System.out.println("Total de Islas "+ contadorIslas);
        imprimirMatriz(islas);
        
    }
```  
### Función recursiva
Esta funcion va recorriendo la matriz buscando las celdas que contienen un `1` y se detiene cuando ya no hay ninguna celda adyacente con ese valor. Al recorrer la isla va marcando los puntos ya recorridos con el valor `2` de modo que al finalizar toda la isla se compondra de celdas con el numero `2`. Esto tambien sirve para que el ciclo que recorre la matriz no vuelva a intentar contar la misma isla varias veces.



```java     
    public static void recorrerIsla(int[][] matriz, int fila, int columna){
        
        //Validar si se esta accediendo a una posicion valida de la matriz
        //Posteriormente se valida aqui mismo si la celda es tierra (tiene valor de 1)
        if(fila<matriz.length && columna<matriz[0].length && fila>=0 && columna >=0 && matriz[fila][columna]==1){
            
            //al detectar tierra se cambia su valor de 1 a 2 y se continua buscando mas celdas adyacentes
            matriz[fila][columna]=2;
            
            recorrerIsla(matriz, fila+1, columna);
            
            recorrerIsla(matriz, fila-1, columna);
            
            recorrerIsla(matriz, fila, columna+1);
            
            recorrerIsla(matriz, fila, columna-1);           
        
        }
                    
    }
    
}
```

###Imprimir
Se imprime la matriz al acabar de identificar todas las islas.

```java 
    public static void imprimirMatriz(int[][] matriz) {
        for (int i = 0; i < matriz.length; i++) {
            for (int j = 0; j < matriz[i].length; j++) {
                System.out.print(matriz[i][j] + " ");
            }
            System.out.println();
        }
    }

``` 