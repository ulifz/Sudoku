import random
import copy

def mostrar_tablero(sudoku:list, separador:str=" ")->None:
    '''
    Muestra el sudoku completo, separando cada numero por el separador recibido.

    Arg:

    sudoku = La matriz 9x9.
    separador = El str que va a separar las filas.
    '''
    for i in range(len(sudoku)):
        for j in range(len(sudoku[i])):
            print(sudoku[i][j], end=separador)
        print()

def validar_numero(tablero:list, fila:int, columna:int, numero:int)->bool:
    '''
    Recibe el tablero sudoku, la fila, columna y el numero a validar.
    Valida si el numero está repetido dentro de la fila, columna y cuadrado del mismo.
    Retorna True si el número está repetido dentro de una de las tres especificaciones.

    Arg:

    tablero = La matriz 9x9 del tablero.

    fila = La fila a validar.

    columna = La columna a validar.

    numero = El número a validar.

    Rtn:

    retorno = True si no está repetido, False si lo está.
    '''
    retorno = True
    for i in range(9):
        if numero == tablero[i][columna]:
            retorno = False
        if numero == tablero[fila][i]:
            retorno = False
    inicio_fila = (fila // 3) * 3
    inicio_columna = (columna // 3) * 3
    for i in range(inicio_fila, inicio_fila + 3):
        for j in range(inicio_columna, inicio_columna + 3):
            if tablero[i][j] == numero:
                retorno = False
    return retorno

def llenar_sudoku(tablero:list)->bool:
    '''
    Llena el tablero vacío, generando un sudoku de cero.
    Se recorre el tablero, si el numero es igual a 0, significa que se le puede colocar un numero, se crea una lista de numeros aleatorios y se validan esos numeros con respecto a la 
    fila y columna donde se ubica el bucle.
    Si el numero es valido, se coloca ese numero y es llama a esta misma funcion provocando una recursividad.
    Si se probaron todos los numeros y ninguno fue valido para esa posicion, se retorna un False, provocando que es la anterior llamada se coloque un 0 y pruebe con un numero distinto.
    Al terminar el tablero, se retornar una serie de True, para cortar con todos los llamados recursivos.

    Arg:

    tablero = La matriz 9x9 del sudoku.
    
    Rtn:

    retorno = True si todavía faltan casillas por llenar en el tablero, False si ya están llenas (se probaron todos los números).
    '''
    retorno = True
    exito = False
    for fila in range(9):
        for columna in range(9):
            if tablero[fila][columna] == 0:  # Espacio vacío | Si ya no quedan numeros, retorna True.
                numeros = list(range(1, 10))
                random.shuffle(numeros)
                for i in range(len(numeros)):
                    if validar_numero(tablero, fila, columna, numeros[i]):
                        tablero[fila][columna] = numeros[i]
                        if llenar_sudoku(tablero): #Aca se llama a si mismo, lo de abajo no se lee.
                            exito = True #Aca entra cuando el último numero fue colocado, las llamadas entran aca y tienen que retornar True sucesivamente.
                            retorno = True 
                            break
                        else:
                            tablero[fila][columna] = 0  # Si la llamada del siguiente numero dio False, se vuelve y modifica el numero a 0 para intentarlo con otro.
                    elif validar_numero(tablero, fila, columna, numeros[i]) == False and i == len(numeros)-1:
                        retorno = False #Si el numero no es valido y ya se probaron todos los numeros, se retorna un False, para que se modifique el anterior.
                        break           #Haciendo que entre al else de llenar_sudoku donde se pone un 0 para intentar con otro numero.

            if not retorno or exito:  #Aca rompo los bucles para que al momento de que el numero no sea valido, o ya esten todos los numeros puestos no
                break                 #itere mas y devuelva el True o False de una.
        if not retorno or exito:
            break
    return retorno

def generar_sudoku_con_dificultad(sudoku:list,dificultad:str)->list:
    '''
    Recibe el sudoku completo y la dificultad seleccionada.
    Se crea una copia del sudoku, la cual se modifica colocando 0 aleatorios, la cantidad de 0 colocados depende de la dificultad recibida.
    Se hace un Bucle for que itera la cantidad de veces asignada a la dificultad, y se colocan ceros validando que no se repitan las posiciones.
    Se retorna una copia del sudoku modificado.
    '''
    sudoku_copia = copy.deepcopy(sudoku)
    if dificultad == "facil":
        cantidad = 16
    elif dificultad == "medio":
        cantidad = 32
    else:
        cantidad = 48
    for _ in range(cantidad):
            i = random.randint(0,8)
            j = random.randint(0,8)
            while sudoku_copia[i][j] == 0:
                i = random.randint(0,8)
                j = random.randint(0,8)
            sudoku_copia[i][j] = 0
    return sudoku_copia

def generar_tablero_sudoku()->list:
    "Esta funcion crea una matriz 9x9, donde se rellena con un sudoku creado desde cero y se retorna este mismo."
    tablero = []
    for _ in range(9):
        fila = [0]*9
        tablero += [fila]
    llenar_sudoku(tablero)
    return tablero