import pygame as pg
import calculos_sudoku as calculos
import funciones_puntaje as pj
import copy
def definir_modo_oscuro(modo_oscuro:bool, color_lineas:pg.Color, color_numeros_normales:pg.Color,color_numero_colocado:pg.Color,color_numero_erroneo:pg.Color,color_revisar_cuadrante:pg.Color,color_fondo_pantalla:pg.Color,color_ayuda:pg.Color,color_fondo_cuadrados:pg.Color,fondo:pg.Surface,color_cositas:pg.Color,pantalla_ancho:int,pantalla_alto:int,color_rojo:pg.Color)->None:
    '''
    Esta función recibe por parametro: El modo oscuro, que determina si el juego va a estar en modo oscuro.
    Recibe todos los colores y un Surface a cambiar.
    Actualiza los colores y carga la imagen correspondiente.
    '''
    #Los colores al hacer asignacion, se pierde la referencia, no le tengo que poner un nuevo valor, si no que lo tengo que actualizar, por eso uso el update, para no perder la referencia de la variable.
    if modo_oscuro == False:
        color_lineas.update(pg.Color("black"))
        color_numeros_normales.update(pg.Color("black"))
        color_numero_colocado.update(pg.Color("blue"))
        color_numero_erroneo.update(pg.Color("red"))
        color_revisar_cuadrante.update(160, 201, 227)
        color_fondo_pantalla.update(pg.Color("gray"))
        color_ayuda.update(pg.Color(185, 213, 227))
        color_fondo_cuadrados.update(pg.Color(215,232,232))
        aux = pg.image.load("imagenes/dia.jpg")
        aux = pg.transform.smoothscale(aux,(pantalla_ancho,pantalla_alto))
        fondo.blit(aux,(0,0))
        color_cositas.update(pg.Color(128,9,9))
        color_rojo.update(pg.Color(128,9,9))
    else:
        color_lineas.update(24, 91, 53)
        color_numeros_normales.update(pg.Color("black"))
        color_numero_colocado.update(pg.Color(32, 134, 248))
        color_numero_erroneo.update(pg.Color("red"))
        color_revisar_cuadrante.update(87, 196, 85)
        color_fondo_pantalla.update(pg.Color("gray"))
        color_ayuda.update(pg.Color(168, 255, 170))
        color_fondo_cuadrados.update(pg.Color(198, 200, 167))#(248, 250, 217)
        aux = pg.image.load("imagenes/navidad.jpg")
        aux = pg.transform.smoothscale(aux,(pantalla_ancho,pantalla_alto))
        fondo.blit(aux,(0,0))
        color_cositas.update(pg.Color(223, 112, 112))
        color_rojo.update(pg.Color(225,66,66))

def verificar_victoria(pantalla:pg.Surface, sudoku:list[list], sudoku_copia:list[list],nombre:str,dificultad:str,contador:int,lista_cantidad_errores:list,puntaje:int,fuente:pg.font.Font)->bool:
    '''
    Esta función recibe por parametro la pantalla, el sudoku completo y el sudoku_copia que se modifica mediante transcurre la partida, un string vació que se actualiza mediante escribimos,
    la dificultad en la que se está jugando, el tiempo, la cantidad de errores, el puntaje y la fuente con la que se va a escribir el texto.
    Compara el sudoku_copia con el sudoku completo, si todos los elementos son iguales, ganaste.
    Al ganar se muetra una pantalla con los datos recibidos por parametro, y se permite ingresar el nombre por teclado, todo finaliza al presionar Enter.
    Retorna un booleano, que sirve para entrar en el modo victoria, donde solamente se puede escribir tu nombre e ignorar el sudoku.
    '''
    #Si los numeros del tablero sudoku_copia (es el tablero que modifico) es igual al tablero original, win.
    ganaste = True
    for i in range(len(sudoku_copia)):
        for j in range(len(sudoku_copia)):
            if sudoku_copia[i][j] != sudoku[i][j]:
                ganaste = False
        if ganaste == False:
            break
    if ganaste:
        fondo_victoria = pg.image.load("imagenes/1.jpg")
        fondo_victoria = pg.transform.smoothscale(fondo_victoria,(900,500))
        pantalla.blit(fondo_victoria,(300,200))
        errores = len(lista_cantidad_errores)
        minuto = 0
        minuto = contador // 60
        contador -= 60 * minuto
        estadisticas = [
            "¡Ganaste!",
            f"Errores: {errores}",
            f"Tiempo: {str(minuto).zfill(2)}:{str(contador).zfill(2)}",
            f"Dificultad: {dificultad.capitalize()}",
            f"Puntaje: {puntaje}",
            "Ingresa tu nombre: " + nombre,
            ]
            
        for i in range(len(estadisticas)):
            render = fuente.render(estadisticas[i], True, pg.Color("white"))
            pantalla.blit(render, (350, 250 + i * 60))
    return ganaste


def verificar_derrota(pantalla:pg.Surface, lista_cantidad_errores:list, vidas:int, color_revisar_cuadrante:pg.Color,rect_rectangulo:pg.Rect)->bool:
    '''
    Esta función recibe la pantalla, la cantidad de errores que se determina por el largo de la lista, la cantidad de vidas, el color a usar, y un rect.
    Al igualarse el largo de la lista con la cantidad de vidas, se muestra un mensaje de Game Over.
    Devuelve un booleano que sirve para entrar en el modo derrota, que al retornar un True se activa un evento que dura 5 segundos, que al finalizar, se vuelve al inicio del juego.
    '''
    retorno = False
    if len(lista_cantidad_errores) == vidas:
        pausar_el_juego(pantalla,True,color_revisar_cuadrante,rect_rectangulo)
        pg.draw.rect(pantalla,pg.Color(0,0,0),(400,300,800,300),border_radius=60)
        bastones = pg.image.load("imagenes/bastones.png")
        bastones = pg.transform.smoothscale(bastones, (150,150))
        perdiste = pg.image.load("imagenes/gameover.jpg")
        perdiste = pg.transform.smoothscale(perdiste,(600,300))
        pantalla.blit(perdiste,(500,300))
        pantalla.blit(bastones,(330,370))
        pantalla.blit(bastones, (1120,370))
        retorno = True
    return retorno

def pausar_el_juego(pantalla:pg.Surface, pausa:bool, color_revisar_cuadrante:pg.Color, rect_rectangulo:pg.Rect): #Color revisar cuadrante
    '''
    Recibe la pantalla, el boolean de pausa, un color, y el rect.
    Cuando el booleano pausa es True, se dibuja en el rect, un rectangulo del color recibido, provocando que no se pueda utilizar el tablero.
    '''
    if pausa:
        pg.draw.rect(pantalla,color_revisar_cuadrante,rect_rectangulo)

def reiniciar_juego(sudoku:list[list], sudoku_copia:list[list], sudoku_sin_tocar:list[list], dificultad:str, lista_cantidad_errores:list,celda_ayuda:list,lista_numeros_agregados:list)->int:
    '''
    Recibe los 3 sudoku utilizados en el juego, la dificultad, la lista con la cantidad de errores, la celda ayuda y la lista de numeros agregados.
    La función reinicia los tres sudoku, sin perder la referencia y estando los tres conectados. Crea un Sudoku completo con la dificultad recibida,
    y se actualizan los otros dos en referencia al sudoku creado.
    Limpia las listas que contienen información sobre el juego, se reinicia la lista con la cantidad de errores, 
    la celda ayuda que contiene los datos de la ultima casilla seleccionada, y se reinicia la lista con los numeros agregados por el jugador.
    '''
    lista = calculos.generar_tablero_sudoku()
    sudoku.clear()
    sudoku.extend(lista) #sudoku = lista
    sudoku_copia.clear() #Que las funciones retornen la lista modificada asi no pierdo la referencia al asignar.
    lista = calculos.generar_sudoku_con_dificultad(sudoku,dificultad)
    sudoku_copia.extend(lista)
    sudoku_sin_tocar.clear()
    lista = copy.deepcopy(sudoku_copia)
    sudoku_sin_tocar.extend(lista)
    lista_cantidad_errores.clear()
    celda_ayuda.clear()
    lista_numeros_agregados.clear()
    return 0

def dibujar_cositas(pantalla:pg.Surface, reiniciar:pg.Surface, punto_reiniciar:pg.Vector2, home:pg.Surface, punto_home:pg.Vector2, rect_reiniciar:pg.Rect,encima_de:None|pg.Rect, color_cositas:pg.Color, color_ayuda:pg.Color, contador:int,rect_home:pg.Rect,rect_pausar:pg.Rect,rect_eliminar:pg.Rect,eliminar:pg.Surface,punto_eliminar:pg.Vector2,pausa:bool,pausar:pg.Surface,punto_pausar:pg.Vector2,reanudar:pg.Surface,fuente_palabras:pg.font.Font,lista_cantidad_errores:list,vidas:int,color_rojo:pg.Color,dificultad:str,lista_numeros_agregados:list,punto_cuadrado_numeros:tuple,puntuacion:int,modo_oscuro:bool,boton_oscuro:pg.Surface,boton_claro:pg.Surface,pantalla_ancho:int,pantalla_alto:int,musica_on:bool,musica_encendida:pg.Surface,musica_apagada:pg.Surface)->int:
    '''
    Esta funcion recibe todo lo necesario para dibujar los siguientes elementos: Los botones de reiniciar - ir al menu - pausar el juego y eliminar numero seleccionado.
    Tambien dibuja los botones visuales para cambiar el modo oscuro, mutear el juego y pausarlo, provocando un switch dependiendo del estado del booleano correspondiente.
    Escribe con la fuente recibida y actualiza constantemente la puntuación, la cantidad de errores y el tiempo transcurrido.
    Por último, provoca un efecto de seleccionamiento al dibujar de distinto color el circulo sobre el cual el mouse está encima.
    Calcula la puntuación según los errores, el tiempo y la cantidad de numeros agregados, y el resultado de ese calculo se retorna.
    '''
    pg.draw.circle(pantalla,color_cositas,rect_reiniciar.center,35)
    pg.draw.circle(pantalla,color_cositas,rect_home.center,35)
    pg.draw.circle(pantalla,color_cositas,rect_pausar.center,35)
    pg.draw.circle(pantalla,color_cositas,rect_eliminar.center,35)
    if encima_de != None: #Encima de, y me guardo el rect
        pg.draw.circle(pantalla,color_ayuda,encima_de.center,35)
    pantalla.blit(reiniciar,punto_reiniciar)
    pantalla.blit(home,punto_home)
    pantalla.blit(eliminar,(punto_eliminar.x+7,punto_eliminar.y+7))
    if modo_oscuro:
        pantalla.blit(boton_oscuro,(pantalla_ancho-90,pantalla_alto-90))
    else:
        pantalla.blit(boton_claro,(pantalla_ancho-90,pantalla_alto-90))
    if pausa == False:
        pantalla.blit(pausar,punto_pausar)  
    else:
        pantalla.blit(reanudar,punto_pausar)
    if musica_on:
        pantalla.blit(musica_encendida,(pantalla_ancho-165,pantalla_alto-90))
    else:
        pantalla.blit(musica_apagada,(pantalla_ancho-180,pantalla_alto-95))
    errores = fuente_palabras.render(f"Errores: {len(lista_cantidad_errores)}/{vidas}",True,color_rojo)
    puntuacion = pj.calcular_puntaje(len(lista_cantidad_errores),contador,dificultad,lista_numeros_agregados)
    puntuacion_palabra = fuente_palabras.render(f"Puntuación: {str(puntuacion)}",True,color_rojo)
    minuto = 0
    minuto = contador // 60
    contador -= 60 * minuto
    tiempo = fuente_palabras.render(f"Tiempo: {str(minuto).zfill(2)}:{str(contador).zfill(2)}",True,color_rojo)
    pantalla.blit(errores,(punto_cuadrado_numeros[0],150))
    pantalla.blit(tiempo,(punto_cuadrado_numeros[0],200))
    pantalla.blit(puntuacion_palabra,(punto_cuadrado_numeros[0],250))
    return puntuacion

def dibujar_fondo_cuadrados(pantalla:pg.Surface, color_fondo_cuadrados:pg.Color, rect_rectangulo:pg.Rect, rect_cuadrados_numeros:pg.Rect):
    '''
    Esta función recibe la pantalla, un color, el rect del tablero y el rect del cuadrado con los numeros.
    Pinta los dos cuadrados con el color recibido.
    '''
    pg.draw.rect(pantalla,color_fondo_cuadrados,rect_rectangulo)
    pg.draw.rect(pantalla,color_fondo_cuadrados,rect_cuadrados_numeros)

def dibujar_cuadrado_numeros(pantalla:pg.Surface, cuadrado_numeros_ancho:int, tamaño_cuadrado_numeros:int, color_lineas:pg.Color, punto_cuadrado_numeros:tuple, grosor_linea:int=5):
    '''
    Esta función recibe la pantalla, el ancho del cuadrado, el tamaño de cada cuadrante, el color de las líneas, el punto de origen para empezar y el grosor de las líneas (opcional).
    Dibuja las líneas internas y externas del cuadrado con los numeros seleccionables, el tamaño depende del ancho recibido, lo mismo con el tamaño de cada cuadrado.
    '''
    for x in range(0, cuadrado_numeros_ancho+1, tamaño_cuadrado_numeros):
        pg.draw.line(pantalla, color_lineas,(x+punto_cuadrado_numeros[0],punto_cuadrado_numeros[1]), (x+punto_cuadrado_numeros[0], punto_cuadrado_numeros[1]+cuadrado_numeros_ancho), grosor_linea)
        pg.draw.line(pantalla,color_lineas,(punto_cuadrado_numeros[0],punto_cuadrado_numeros[1]+x), (punto_cuadrado_numeros[0]+cuadrado_numeros_ancho, x+punto_cuadrado_numeros[1]),grosor_linea)
    
def dibujar_numeros_en_el_cuadrado(pantalla:pg.Surface, fuente_grande:pg.font.Font, color_numeros_normales:pg.Color, punto_cuadrado_numeros:tuple, tamaño_cuadrado_numeros:int, cuadrado_numeros_ancho:int):
    '''
    Esta función dibuja los numeros de manera ascendente dentro del cuadrado con los numeros seleccionables.
    Recibe la pantalla, la fuente para escribir los numeros, su punto (x,y) para empezar el dibujado, el tamaño del cuadrado total y el ancho de cada cuadradito que contiene un número.
    '''
    contador = 0
    for i in range(0 ,cuadrado_numeros_ancho, tamaño_cuadrado_numeros):
        imagen_numero1 = fuente_grande.render(str(contador+1),True,color_numeros_normales)
        imagen_numero2 = fuente_grande.render(str(contador+4),True,color_numeros_normales)
        imagen_numero3 = fuente_grande.render(str(contador+7),True,color_numeros_normales)
        x = i+punto_cuadrado_numeros[0]+40
        y = punto_cuadrado_numeros[1]+30
        pantalla.blit(imagen_numero1,(x,y),(0,0,tamaño_cuadrado_numeros,tamaño_cuadrado_numeros))
        pantalla.blit(imagen_numero2, (x, y + tamaño_cuadrado_numeros), (0,0,tamaño_cuadrado_numeros,tamaño_cuadrado_numeros))
        pantalla.blit(imagen_numero3, (x, (y + (tamaño_cuadrado_numeros*2))), (0,0,tamaño_cuadrado_numeros,tamaño_cuadrado_numeros))
        contador += 1

def dibujar_efecto_en_el_cuadrado(pantalla:pg.Surface, fila2:int, color_ayuda:pg.Color, x_inicial2:int, y_inicial2:int, tamaño_cuadrado_numeros:int):
    '''
    Esta función recibe la pantalla, la fila2 que se usa como condición para saber si dibujar o no, el punto X e Y del cuadrado con el mouse encima, y el tamaño del cuadrado.
    Pinta un cuadrado del color dentro de las coordenadas con el tamaño recibido.
    El fila2 se modifica cuando se coloca el mouse encima, cambiando su valor y provocando que se dibuje el cuadrado con los datos correspondientes.
    '''
    if fila2 != -1:
        pg.draw.rect(pantalla,color_ayuda,(x_inicial2,y_inicial2,tamaño_cuadrado_numeros,tamaño_cuadrado_numeros))

def dibujar_cuadrado(pantalla:pg.Surface, tablero_ancho:int, tamaño_casilla:int, color_lineas:pg.Color,tablero_alto:int,punto_tablero_gigante:pg.Vector2):
    '''
    La función recibe la pantalla, el ancho y alto del tablero, el tamaño de cada casilla, el color de las lineas, y el punto (x,y) del cuadrado.
    Se dibujan lineas de manera que se crea un tablero del ancho y alto, donde cada 3 lineas (contando la primera) el mas gruesa, dando el efecto que tienen los tableros del sudoku
    para diferenciar los cuadrantes grandes.
    Se utilizan los valores recibidos para crear un tablero al estilo Sudoku.
    '''
    for x in range(0, tablero_ancho, tamaño_casilla): #Empieza en 0 hasta el ancho de la pantalla, y salta lo mismo que mide cada casilla.
        ancho_linea = 5 if x % (tamaño_casilla * 3) == 0 else 1 #Cada 3 saltos hago una linea gruesa, cuenta el 0.
        pg.draw.line(pantalla, color_lineas, (x+punto_tablero_gigante.x, punto_tablero_gigante.y), (x+punto_tablero_gigante.x, tablero_alto+punto_tablero_gigante.y-5), ancho_linea) #Vertical
        pg.draw.line(pantalla, color_lineas, (punto_tablero_gigante.x, punto_tablero_gigante.y+x), (tablero_ancho+punto_tablero_gigante.x-5, punto_tablero_gigante.y+x), ancho_linea)

def dibujar_numeros_fijos(pantalla:pg.Surface, color_numeros_normales:pg.Color, tamaño_casilla:int, fuente:pg.font.Font, punto_tablero_gigante:pg.Vector2, sudoku_sin_tocar:list):
    '''
    Recibe la pantalla, el color y fuente para escribir los numeros, el tamaño de cada casilla, su punto (x,y) para saber donde empezar a dibujar y el sudoku
    Esta función dibuja los numeros fijos, no modificables del tablero.
    Determina si el numero es fijo si no se ocultó del tablero, es decir, si el numero es distinto a 0 se dibuja.
    '''
    for i in range(len(sudoku_sin_tocar)):
        for j in range(len(sudoku_sin_tocar[i])):
            if sudoku_sin_tocar[i][j] != 0:
                imagen_numero = fuente.render(str(sudoku_sin_tocar[i][j]),True,color_numeros_normales)
                pantalla.blit(imagen_numero, ((j*tamaño_casilla)+punto_tablero_gigante.x+30,(i*tamaño_casilla)+punto_tablero_gigante.y+23),(0,0,tamaño_casilla,tamaño_casilla))

def dibujar_cuadrante(pantalla:pg.Surface, celda_seleccionada:list|None, celda_ayuda:list, color_revisar_cuadrante:pg.Color, tamaño_casilla:int, sudoku_copia:list[list]):
    '''
    Recibe la pantalla, la celda_seleccionada, la celda ayuda, el color del rectangulo a resaltar, el tamaño de la casilla y el sudoku copia.
    Esta funcion se activa cuando la celda seleccionada es distinto a None, o sea, cuando hay una celda seleccionada.
    A partir de esa celda seleccionada, se dibuja el rectangulo con el color en la posicion de la casilla del sudoku, estos datos se albergan dentro de la lista celda seleccionada.
    Cuando hay una celda seleccionada, significa que tengo que mostrar una ayuda, se limpia la lista celda ayuda, y se ponen los datos que tiene la celda seleccionada, su numero, la fila y columna.
    '''
    if celda_seleccionada != None:
        pg.draw.rect(pantalla,color_revisar_cuadrante,(celda_seleccionada[0],celda_seleccionada[1],tamaño_casilla,tamaño_casilla))
        celda_ayuda.clear() #Limpio para que no se acumulen los numeros.
        celda_ayuda.append(sudoku_copia[celda_seleccionada[2]][celda_seleccionada[3]]) #El numero literal (int)
        celda_ayuda.append(celda_seleccionada[2]) # Fila
        celda_ayuda.append(celda_seleccionada[3]) # Columna

def dibujar_ayuda(pantalla:pg.Surface, celda_ayuda:list, tamaño_casilla:int, color_revisar_cuadrante:pg.Color, color_ayuda:pg.Color, sudoku_copia:list[list], punto_tablero_gigante:pg.Vector2):
    '''
    Recibe la pantalla, la lista de celda ayuda, el tamaño de cada casilla, el color para resaltar fila, columna y cuadrante, el color para resaltar a si mismo y los numeros iguales,
    el sudoku copia para analizar las posiciones de los cuadrados a dibujar, y el punto de origen del tablero.
    Al seleccionarse un cuadrante, la celda ayuda se completa con la información de la celda seleccionada, provocando que se active la función.
    Esta función resalta todos los cuadrantes que están dentro de la misma fila, misma columna, mismo cuadrante y que tengan el mismo numero, exceptuando cuando el numero 0,
    que solo dibuja el 0 seleccionado y no los otros 0.
    '''
    if len(celda_ayuda)>0: #Condicion para que esta funcion sirva, si la lista no está vacía, funciona.
        inicio_fila = (celda_ayuda[1] // 3) * 3
        inicio_columna = (celda_ayuda[2] // 3) * 3
        for i in range(inicio_fila, inicio_fila + 3):
            for j in range(inicio_columna, inicio_columna + 3):
                x_inicial = (j * tamaño_casilla) + punto_tablero_gigante.x
                y_inicial = (i * tamaño_casilla) + punto_tablero_gigante.y
                pg.draw.rect(pantalla,color_ayuda,(x_inicial,y_inicial,tamaño_casilla,tamaño_casilla))
        for i in range(len(sudoku_copia)):
            for j in range(len(sudoku_copia[i])):
                x_inicial = (j * tamaño_casilla) + punto_tablero_gigante.x
                y_inicial = (i * tamaño_casilla) + punto_tablero_gigante.y
                if i == celda_ayuda[1] or j == celda_ayuda[2]:
                    pg.draw.rect(pantalla,color_ayuda,(x_inicial,y_inicial,tamaño_casilla,tamaño_casilla))
                if sudoku_copia[i][j] == celda_ayuda[0] and celda_ayuda[0] != 0:
                    pg.draw.rect(pantalla,color_revisar_cuadrante,(x_inicial,y_inicial,tamaño_casilla,tamaño_casilla))
                if i == celda_ayuda[1] and j == celda_ayuda[2] and celda_ayuda[0] == 0:
                    pg.draw.rect(pantalla,color_revisar_cuadrante,(x_inicial,y_inicial,tamaño_casilla,tamaño_casilla))

def dibujar_numeros(pantalla:pg.Surface, lista_numeros_agregados:list[dict], color_numero_colocado:pg.Color, color_numero_erroneo:pg.Color, tamaño_casilla:int, sudoku_copia:list[list], sudoku:list[list], fuente:pg.font.Font):
    '''
    Esta función dibuja los numeros agregados por el usuario, que se albergan dentro de la lista, dependiendo del numero y su posicion, se usa el color para marcar la validez del numero.
    Recorre cada numero agregado, agrego el numero al sudoku copia, y al comparar ese numero con su posicion, con la misma posicion en el sudoku resuelto, determino si es correcto o no, cambiando
    el color del numero y modificando su clave "error" a True. (Este cambio sirve para calcular la puntuación).
    Con la fuente y tamaño de casilla recibido, se dibuja el numero en el centro del cuadrado donde fue colocado el numero por el jugador.
    '''
    if len(lista_numeros_agregados) > 0:
        for i in range(len(lista_numeros_agregados)):
            sudoku_copia[lista_numeros_agregados[i]["fila"]][lista_numeros_agregados[i]["columna"]] = lista_numeros_agregados[i]["numero"] #Modifico el tablero sudoku_copia con el numero colocado en la posicion colocada en el juego.
            if sudoku_copia[lista_numeros_agregados[i]["fila"]][lista_numeros_agregados[i]["columna"]] == sudoku[lista_numeros_agregados[i]["fila"]][lista_numeros_agregados[i]["columna"]]: #Si el numero es correcto.
                imagen_numero = fuente.render(str(lista_numeros_agregados[i]["numero"]),True,color_numero_colocado)
            else:
                imagen_numero = fuente.render(str(lista_numeros_agregados[i]["numero"]),True,color_numero_erroneo) #Si el numero es incorrecto.
                lista_numeros_agregados[i]["error"] = True
            pantalla.blit(imagen_numero, (lista_numeros_agregados[i]["x"]+30,lista_numeros_agregados[i]["y"]+23),(0,0,tamaño_casilla,tamaño_casilla))

def borrar_numero(fila:int|None, columna:int|None, lista_numeros_agregados:list[dict], sudoku_copia:list[list]):
    '''
    Esta función recibe la fila y columna del numero a borrar, la lista de numeros agregados y el sudoku copia.
    Esta funcion recorre cada numero dentro de la lista de numeros agregados, y compara su fila y columna con los recibidos, 
    al encontrar una igualdad, ese numero se borra del sudoku copia y se elimina el indice de la lista para que no se muestre más en dibujar numeros.
    '''
    for i in range(len(lista_numeros_agregados)): #De la lista de numeros que agregue, lo comparo con la ultima fila y columna seleccionada, el numero en esa fila y columna es el que tengo que borrar.
        if lista_numeros_agregados[i]["fila"] == fila and lista_numeros_agregados[i]["columna"] == columna: #Borro el indice de la lista en la que contiene la fila y columna del numero a borrar.
            sudoku_copia[lista_numeros_agregados[i]["fila"]][lista_numeros_agregados[i]["columna"]] = 0
            lista_numeros_agregados.pop(i)