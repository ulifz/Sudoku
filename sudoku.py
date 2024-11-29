import pygame as pg
import calculos_sudoku as calculos 
import copy
import funciones_puntaje as pj
import funciones_sudoku as fs

pg.init()
def iniciar_sudoku(dificultad:str):
    '''
    Inicializa la pantalla del sudoku, dibujando el mismo con todos sus valores.

    Arg:

    dificultad = str con la dificultad a asignarle al tablero.
    '''

    modo_oscuro = False
    nombre = ""
    puntuacion = 0
    sudoku = calculos.generar_tablero_sudoku()
    sudoku_copia = calculos.generar_sudoku_con_dificultad(sudoku,dificultad)
    sudoku_sin_tocar = copy.deepcopy(sudoku_copia)
    calculos.mostrar_tablero(sudoku)
    color_lineas = pg.Color("black")
    color_numeros_normales = pg.Color("black")
    color_numero_colocado = pg.Color("blue")
    color_numero_erroneo = pg.Color("red")
    color_revisar_cuadrante = pg.Color(160, 201, 227)
    color_fondo_pantalla = pg.Color("gray")
    color_ayuda = pg.Color(185, 213, 227)
    color_fondo_cuadrados = pg.Color(215,232,232)
    fondo = pg.image.load("imagenes/dia.jpg")
    color_cositas = pg.Color(128,9,9)
    color_rojo = pg.Color(128,9,9)

    #Variables y eventos
    
    tablero_ancho = 700
    tablero_alto = 700
    pantalla_ancho = 1600
    pantalla_alto = 900
    cuadrado_numeros_ancho = 360
    tamaño_cuadrado_numeros = cuadrado_numeros_ancho // 3
    punto_cuadrado_numeros = (900,455)
    rect_cuadrados_numeros = pg.Rect(punto_cuadrado_numeros[0],punto_cuadrado_numeros[1],cuadrado_numeros_ancho,cuadrado_numeros_ancho)
    punto_tablero_gigante = pg.Vector2(120,120) #ACAAAAAAA
    pantalla = pg.display.set_mode((pantalla_ancho, pantalla_alto))
    celda_seleccionada = None
    celda_ayuda = []
    lista_numeros_agregados = []
    lista_numeros = [[1,2,3],[4,5,6],[7,8,9]]
    fila = None
    fila2,columna2 = -1,-1
    x_inicial2,y_inicial2 = 0,0
    vidas = 3
    lista_cantidad_errores = []
    encima_de = None
    pausa = False
    perdiste = False
    ganaste = False
    musica_on = True
    evento_segundo = pg.USEREVENT + 1
    un_segundo = 1000
    pg.time.set_timer(evento_segundo,un_segundo)
    evento_5segundos = pg.USEREVENT + 2
    cincosegundos = 5000
    pg.time.set_timer(evento_5segundos,cincosegundos)
    contador = 0
    pg.display.set_caption("Sudoku")
    fuente = pg.font.SysFont("Bahnschrift", 30)
    fuente_grande = pg.font.SysFont("Bahnschrift", 50)
    fuente_palabras = pg.font.SysFont("Bahnschrift",35)
    grillas = 9
    tamaño_casilla = tablero_ancho // grillas #Divido el ancho del tablero por la cantida de cuadrantes para tener un numero redondo y usarlo siempre.
    numeros = [pg.K_1,pg.K_2,pg.K_3,pg.K_4,pg.K_5,pg.K_6,pg.K_7,pg.K_8,pg.K_9]
    numerospad = {pg.K_KP_1:"1",pg.K_KP_2:"2",pg.K_KP_3:"3",pg.K_KP_4:"4",pg.K_KP_5:"5",pg.K_KP_6:"6",pg.K_KP_7:"7",pg.K_KP_8:"8",pg.K_KP_9:"9"}
    rect_rectangulo = pg.Rect(punto_tablero_gigante.x,punto_tablero_gigante.y,tablero_ancho-5,tablero_alto-5)

    #Cargar imagenes, transformarlas y guardar su rect.
    reiniciar = pg.image.load("imagenes/reiniciar.png")
    home = pg.image.load("imagenes/casita.png")
    reiniciar = pg.transform.smoothscale(reiniciar,(50,35))
    home = pg.transform.smoothscale(home,(50,35))
    punto_home = pg.Vector2(950,370) #ACAAAAAAAAA
    punto_reiniciar = pg.Vector2(punto_home.x+75,punto_home.y)
    rect_reiniciar = pg.Rect(punto_reiniciar.x, punto_reiniciar.y,reiniciar.get_width(),reiniciar.get_height())
    rect_home = pg.Rect(punto_home.x,punto_home.y,home.get_width(),home.get_height())
    eliminar = pg.image.load("imagenes/eliminar.png")
    eliminar = pg.transform.smoothscale(eliminar,(50,35))
    pausar = pg.image.load("imagenes/pausar.png")
    pausar = pg.transform.smoothscale(pausar,(50,35))
    punto_pausar = pg.Vector2(punto_reiniciar.x+75,punto_home.y)
    punto_eliminar = pg.Vector2(punto_pausar.x+75,punto_home.y-8)
    rect_eliminar = pg.Rect(punto_eliminar.x,punto_eliminar.y,eliminar.get_width()+15,eliminar.get_height()+15)
    rect_pausar = pg.Rect(punto_pausar.x,punto_pausar.y,pausar.get_width(),pausar.get_height())
    reanudar = pg.image.load("imagenes/reanudar.png")
    reanudar = pg.transform.smoothscale(reanudar,(50,35))
    fondo = pg.transform.smoothscale(fondo,(pantalla_ancho,pantalla_alto))
    boton_oscuro = pg.image.load("imagenes/sol.png")
    boton_oscuro = pg.transform.scale(boton_oscuro,(90,90))
    rect_boton_oscuro = pg.Rect(pantalla_ancho-90,pantalla_alto-90,boton_oscuro.get_width(),boton_oscuro.get_height())
    boton_claro = pg.image.load("imagenes/luna.png")
    boton_claro = pg.transform.smoothscale(boton_claro,(90,90))
    musica_encendida = pg.image.load("imagenes/volumen_on.png")
    musica_encendida = pg.transform.smoothscale(musica_encendida,(95,90))
    musica_apagada = pg.image.load("imagenes/volumen_off.png")
    musica_apagada = pg.transform.smoothscale(musica_apagada,(125,95))
    rect_musica = pg.Rect(pantalla_ancho-195,pantalla_alto-95,musica_apagada.get_width(),musica_apagada.get_height())

    pg.mixer.music.load("sonidos/my christmas old carol, happy holiday!.mp3")
    pg.mixer.music.set_volume(0.2)
    pg.mixer.music.play()
    estado = "jugar"
    while estado == "jugar":
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                pg.quit()
            if evento.type == pg.MOUSEMOTION:
                if rect_cuadrados_numeros.collidepoint(pg.mouse.get_pos()):
                    columna2 = (pg.mouse.get_pos()[0]-punto_cuadrado_numeros[0]) // tamaño_cuadrado_numeros
                    fila2 = (pg.mouse.get_pos()[1]-punto_cuadrado_numeros[1]) // tamaño_cuadrado_numeros
                    x_inicial2 = (columna2 * tamaño_cuadrado_numeros) + punto_cuadrado_numeros[0]
                    y_inicial2 = (fila2 * tamaño_cuadrado_numeros) + punto_cuadrado_numeros[1]
                else: 
                    fila2 = -1
                if rect_home.collidepoint(pg.mouse.get_pos()):
                    encima_de = rect_home
                elif rect_reiniciar.collidepoint(pg.mouse.get_pos()):
                    encima_de = rect_reiniciar
                elif rect_eliminar.collidepoint(pg.mouse.get_pos()):
                    encima_de = rect_eliminar
                elif rect_pausar.collidepoint(pg.mouse.get_pos()):
                    encima_de = rect_pausar
                else:
                    encima_de = None
            if evento.type == pg.MOUSEBUTTONDOWN:
                #Cada vez que hago click me guardo la columna,fila, su X e Y, y modifico celda_seleccionada que sirve para la funcion dibujar cuadrante.
                if pg.mouse.get_pressed()[0] and ganaste == False:
                    if rect_rectangulo.collidepoint(pg.mouse.get_pos()):
                        columna = (pg.mouse.get_pos()[0]-int(punto_tablero_gigante.x)) // tamaño_casilla
                        fila = (pg.mouse.get_pos()[1]-int(punto_tablero_gigante.y)) // tamaño_casilla
                        x_inicial = (columna * tamaño_casilla) + punto_tablero_gigante.x
                        y_inicial = (fila * tamaño_casilla) + punto_tablero_gigante.y
                        celda_seleccionada = [x_inicial, y_inicial, fila, columna]
                    if rect_cuadrados_numeros.collidepoint(pg.mouse.get_pos()):
                        numero = lista_numeros[fila2][columna2]
                        #Misma logica que al colocar un numero con el teclado. O sea, se repite codigo...
                        if fila != None and sudoku_copia[fila][columna] == 0 and pausa == False:
                            lista_numeros_agregados.append({"numero":int(numero),"fila":fila,"columna":columna,"x":x_inicial,"y":y_inicial,"error":False})
                            if int(numero) != sudoku[fila][columna]: 
                                lista_cantidad_errores.append("error")
                        elif fila != None and sudoku_sin_tocar[fila][columna] == 0 and pausa == False and int(numero) != sudoku_copia[fila][columna]: #Reemplazar numero ya puesto. Lo borro y agrego el nuevo al mismo tiempo.
                            fs.borrar_numero(fila,columna,lista_numeros_agregados, sudoku_copia)
                            lista_numeros_agregados.append({"numero":int(numero),"fila":fila,"columna":columna,"x":x_inicial,"y":y_inicial,"error":False})
                            if int(numero) != sudoku[fila][columna]:
                                lista_cantidad_errores.append("error")
                    if not rect_rectangulo.collidepoint(pg.mouse.get_pos()) and not rect_cuadrados_numeros.collidepoint(pg.mouse.get_pos()) and not rect_eliminar.collidepoint(pg.mouse.get_pos()):
                        celda_seleccionada = None
                        celda_ayuda = []
                        fila = None
                    if rect_home.collidepoint(pg.mouse.get_pos()):
                        estado = "menu"
                    if rect_reiniciar.collidepoint(pg.mouse.get_pos()):
                        contador = fs.reiniciar_juego(sudoku,sudoku_copia,sudoku_sin_tocar,dificultad,lista_cantidad_errores,celda_ayuda,lista_numeros_agregados)
                    if rect_pausar.collidepoint(pg.mouse.get_pos()):
                        pausa = not pausa
                    if rect_eliminar.collidepoint(pg.mouse.get_pos()) and fila != None:
                        if sudoku_sin_tocar[fila][columna] == 0:
                            fs.borrar_numero(fila,columna,lista_numeros_agregados, sudoku_copia)
                    if rect_boton_oscuro.collidepoint(pg.mouse.get_pos()):
                        modo_oscuro = not modo_oscuro
                        fs.definir_modo_oscuro(modo_oscuro,color_lineas,color_numeros_normales,color_numero_colocado,color_numero_erroneo,color_revisar_cuadrante,color_fondo_pantalla,color_ayuda,color_fondo_cuadrados,fondo,color_cositas,pantalla_ancho,pantalla_alto,color_rojo)
                    if rect_musica.collidepoint(pg.mouse.get_pos()):
                        musica_on = not musica_on
                        if musica_on:
                            pg.mixer.music.unpause()
                        else:
                            pg.mixer.music.pause()
                    if perdiste == True:
                        estado = "menu"
            if evento.type == pg.KEYDOWN:
                if ganaste == True:
                    fila = None
                    if len(nombre) < 10:
                        if evento.key >= pg.K_a and evento.key <= pg.K_z:
                            if pg.key.get_mods() == 1 or pg.key.get_mods() == 4097 or pg.key.get_mods() == 12288:
                                nombre += chr(evento.key).upper()
                            else:
                                nombre += chr(evento.key)
                        elif evento.key == 32 and nombre[-1] != " ":
                            nombre += " "
                        elif evento.key == pg.K_BACKSPACE:
                            nombre = nombre[:-1]
                        elif evento.key == pg.K_RETURN:
                            datos = (nombre,puntuacion)
                            pj.actualizar_puntajes(datos)
                            estado = "menu"
                    else:
                        if evento.key == pg.K_BACKSPACE:
                            nombre = nombre[:-1]
                if ((evento.key in numeros) or (evento.key in numerospad)) and ganaste == False: #Filtro si el numero lo toque con el pad o los numeros de arriba.
                    if evento.key > 10000:
                        numero = numerospad[evento.key]
                    else:
                        numero = chr(evento.key)
                    if fila != None and sudoku_copia[fila][columna] == 0 and perdiste == False: # Si la casilla está vacía y escribo un numero, me guardo los datos de ese numero y lo dibujo en dibujar numeros
                        #De cada numero que quiero agregar, me guardo el numero que toco, la fila y columna con relacion al tablero, y su posicion (x,y).
                        #Para borrar tengo que eliminar su indice en esta lista.
                        lista_numeros_agregados.append({"numero":int(numero),"fila":fila,"columna":columna,"x":x_inicial,"y":y_inicial,"error":False})
                        if int(numero) != sudoku[fila][columna]: #Si el numero colocado es erroneo, a la lista le agrego un elemento, cuando el largo de la lista sea igual a la cantidad de vidas, perdiste.
                            print("ERROR 1")
                            lista_cantidad_errores.append("error")
                    elif fila != None and sudoku_sin_tocar[fila][columna] == 0 and perdiste == False and int(numero) != sudoku_copia[fila][columna]: #Reemplazar numero ya puesto. Lo borro y agrego el nuevo al mismo tiempo.
                        fs.borrar_numero(fila,columna,lista_numeros_agregados, sudoku_copia)
                        lista_numeros_agregados.append({"numero":int(numero),"fila":fila,"columna":columna,"x":x_inicial,"y":y_inicial,"error":False})
                        if int(numero) != sudoku[fila][columna] and sudoku_copia[fila][columna] != int(numero): #VERIFICAR ERROR...
                            calculos.mostrar_tablero(sudoku_copia)
                            lista_cantidad_errores.append("error")
                if (evento.key == 27 or evento.key == 8 or evento.key == 127) and fila != None: #Si la tecla es backspace o escape, borro el numero.
                    if sudoku_sin_tocar[fila][columna] == 0: #Si la casilla en el sudoku era 0, significa que es una casilla modificable, podes escribir y por ende borrar.
                        fs.borrar_numero(fila,columna,lista_numeros_agregados, sudoku_copia)
                if perdiste == True:
                    if evento.key == pg.K_RETURN:
                        estado = "menu"
            if evento.type == evento_segundo and pausa == False and perdiste == False and ganaste == False:
                contador += 1

        pantalla.blit(fondo,(0,0,fondo.get_width(),fondo.get_height()))
        fs.dibujar_fondo_cuadrados(pantalla,color_fondo_cuadrados,rect_rectangulo,rect_cuadrados_numeros)
        fs.dibujar_efecto_en_el_cuadrado(pantalla,fila2,color_ayuda,x_inicial2,y_inicial2,tamaño_cuadrado_numeros)
        fs.dibujar_cuadrado_numeros(pantalla,cuadrado_numeros_ancho,tamaño_cuadrado_numeros,color_lineas,punto_cuadrado_numeros)
        fs.dibujar_numeros_en_el_cuadrado(pantalla,fuente_grande,color_numeros_normales,punto_cuadrado_numeros,tamaño_cuadrado_numeros,cuadrado_numeros_ancho)
        fs.dibujar_cuadrante(pantalla, celda_seleccionada,celda_ayuda,color_revisar_cuadrante,tamaño_casilla,sudoku_copia)
        fs.dibujar_ayuda(pantalla,celda_ayuda,tamaño_casilla,color_revisar_cuadrante,color_ayuda, sudoku_copia,punto_tablero_gigante)
        fs.dibujar_cuadrado(pantalla,tablero_ancho,tamaño_casilla,color_lineas,tablero_alto,punto_tablero_gigante)
        fs.dibujar_numeros_fijos(pantalla,color_numeros_normales,tamaño_casilla,fuente,punto_tablero_gigante,sudoku_sin_tocar)
        fs.dibujar_numeros(pantalla,lista_numeros_agregados, color_numero_colocado, color_numero_erroneo, tamaño_casilla, sudoku_copia, sudoku,fuente)
        puntuacion = fs.dibujar_cositas(pantalla,reiniciar,punto_reiniciar,home,punto_home,rect_reiniciar,encima_de,color_cositas,color_ayuda,contador,rect_home,rect_pausar,rect_eliminar,eliminar,punto_eliminar,pausa,pausar,punto_pausar,reanudar,fuente_palabras,lista_cantidad_errores,vidas,color_rojo,dificultad,lista_numeros_agregados,punto_cuadrado_numeros,puntuacion,modo_oscuro,boton_oscuro,boton_claro,pantalla_ancho,pantalla_alto,musica_on,musica_encendida,musica_apagada)
        fs.pausar_el_juego(pantalla,pausa,color_revisar_cuadrante,rect_rectangulo)
        ganaste = fs.verificar_victoria(pantalla,sudoku,sudoku_copia,nombre,dificultad,contador,lista_cantidad_errores,puntuacion,fuente_palabras)
        perdiste = fs.verificar_derrota(pantalla,lista_cantidad_errores,vidas,color_revisar_cuadrante,rect_rectangulo)
        pg.display.flip()
    return estado