
public class ContarIslas {

    public static void main(String[] args) {
        
        int contadorIslas=0;

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
    
    
    public static void imprimirMatriz(int[][] matriz) {
        for (int i = 0; i < matriz.length; i++) {
            for (int j = 0; j < matriz[i].length; j++) {
                System.out.print(matriz[i][j] + " ");
            }
            System.out.println();
        }
    }
    
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
