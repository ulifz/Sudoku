import pygame

def crear_boton(tamano_fuente: int, text: str, color: tuple | str, color_background : tuple | None, pantalla: pygame.Surface,pos_x: float, pos_y: float) -> pygame.Rect:
    """
    Crea un botón a partir de los parametros que se le brindan por argumento. Retorna un rect con el botón creado y ubicado en pantalla.

    Arg:

    tamano_fuente = tamaño de las letras.

    text = texto que imprime.

    color = color de las letras.

    color_background = color del fondo de las letras.

    pantalla = Surface en el cual imprimir.

    pos_x = posicion x en la cual escribir.

    pos_y = posicion y en la cual escribir.

    Rtn:

    boton_modificado = Rect

    """
    # Uso los screen como refencia para sacar el porcentaje para el tamaño de las letras.
    pantalla_x = 1600
    pantalla_y = 900
    porcentaje_letras = tamano_fuente / (pantalla_x + pantalla_y)         
    
    tamano_pantalla = list(pantalla.get_size())
    tamano_fuente = (tamano_pantalla[0] + tamano_pantalla[1]) * porcentaje_letras 
        
    fuente = pygame.font.SysFont("unispace", int(tamano_fuente), False, True)
    #fuente = pygame.font.Font("unispace", int(tamano_fuente))
    texto = fuente.render(str(text), True, color, color_background)

    tamano_texto = list(texto.get_size()) # Me da la una tupla con el tamaño del texto, me sirve para centralizarlo en el eje x,y
    posicion_en_pantalla_x =  (tamano_pantalla[0] * pos_x) - (tamano_texto[0] / 2) 
    posicion_en_pantalla_y =  (tamano_pantalla[1] * pos_y) #- (tamano_texto[1] / 2)
    
    boton_modificado = pantalla.blit(texto, (posicion_en_pantalla_x, posicion_en_pantalla_y))

    return boton_modificado

def iniciar_menu(fondo: str, dificultad: list) -> str:
    """
    Inicializa el menú pricipal y la dibuja. También recibe y modifica la dificultad del juego a través de una lista. Retorna el estado al que va a pasar el programa cuando se clickee un botón.

    Arg:

    fondo = Recibe la imagen de fondo del menu principal.

    dificultad = Recibe lista con str de dificultad Facil, Medio o Dificil.
    
    Rtn: 
    
    estado = str

    """
    pygame.init()

    pantalla_x = 1600
    pantalla_y = 900
    pantalla = pygame.display.set_mode((pantalla_x,pantalla_y))
    pygame.display.set_caption("Sudoku")
    icono = pygame.image.load("imagenes\icono.png")
    pygame.display.set_icon(icono)
    fondo_principal = pygame.image.load(fondo)
    fondo_principal = pygame.transform.scale(fondo_principal,(pantalla_x,pantalla_y))
    imagen_musica = pygame.image.load("imagenes/renito.jpeg")
    imagen_musica = pygame.transform.scale(imagen_musica,(150,150))
    pygame.mixer.music.load("sonidos/musica_navidad.mp3")
    
    color_texto = (255,255,255)
    jugar_y = 0.50
    estado = "menu"
    musiquita = True
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.1)
    
    while estado == "menu":
        
        pantalla.blit(fondo_principal,(0,0))
        boton_dificultad = crear_boton(100, dificultad[0], color_texto,None ,pantalla, 0.93, 0.90)
        boton_musica = pantalla.blit(imagen_musica,(pantalla_x * 0.03, pantalla_y * 0.80))
        crear_boton(400, "Sudoku", (0,0,0), None, pantalla, 0.50, 0.10)
        jugar = crear_boton(200, "Jugar", color_texto, None,pantalla, 0.50, jugar_y)
        puntuacion = crear_boton(200, "Puntajes", color_texto,None , pantalla, 0.50, (jugar_y + 0.15))
        salir = crear_boton(200, "Salir", color_texto, None,pantalla, 0.50, (jugar_y + 0.30))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                estado = "salir"
            if event.type == pygame.MOUSEMOTION:
                if jugar.collidepoint(pygame.mouse.get_pos()):
                    color_texto = (255, 30, 30)
                    jugar = crear_boton(200, "Jugar", color_texto, None,pantalla, 0.50, jugar_y)
                else:
                    color_texto = (255,255,255)
                    jugar = crear_boton(200, "Jugar", color_texto, None,pantalla, 0.50, jugar_y)
                if puntuacion.collidepoint(pygame.mouse.get_pos()):
                    color_texto = (255, 30, 30)
                    puntuacion = crear_boton(200, "Puntajes", color_texto,None , pantalla, 0.50, (jugar_y + 0.15))
                else:
                    color_texto = (255,255,255)
                    puntuacion = crear_boton(200, "Puntajes", color_texto,None , pantalla, 0.50, (jugar_y + 0.15))
                if boton_dificultad.collidepoint(pygame.mouse.get_pos()):
                    color_texto = (255, 30, 30)
                    boton_dificultad = crear_boton(100, dificultad[0], color_texto,None ,pantalla, 0.93, 0.90)
                else:
                    color_texto = (255,255,255)
                    boton_dificultad = crear_boton(100, dificultad[0], color_texto,None,pantalla, 0.93, 0.90)
                if salir.collidepoint(pygame.mouse.get_pos()):   
                    color_texto = (255, 30, 30) 
                    salir = crear_boton(200, "Salir", color_texto, None,pantalla, 0.50, (jugar_y + 0.30))
                else:
                    color_texto = (255,255,255)
                    salir = crear_boton(200, "Salir", color_texto, None,pantalla, 0.50, (jugar_y + 0.30))

            if event.type == pygame.MOUSEBUTTONDOWN:
                lista_botones_mouse = list(pygame.mouse.get_pressed())
                if lista_botones_mouse[0] == True:
                    if jugar.collidepoint(pygame.mouse.get_pos()):
                        estado = "jugar"
                        pygame.mixer.music.pause()
                    elif puntuacion.collidepoint(pygame.mouse.get_pos()):
                        estado = "puntuacion"
                        pygame.mixer.music.pause()
                    elif boton_dificultad.collidepoint(pygame.mouse.get_pos()):
                        if dificultad[0] == "facil":
                            dificultad.clear()
                            dificultad.append("medio")
                            estado = "menu"
                        elif dificultad[0] == "medio":
                            dificultad.clear()
                            dificultad.append("dificil")
                            estado = "menu"
                        elif dificultad[0] ==  "dificil":
                            dificultad.clear()
                            dificultad.append("facil")
                            estado = "menu"
                    elif boton_musica.collidepoint(pygame.mouse.get_pos()):
                        if musiquita == True:
                            pygame.mixer.music.pause()
                            musiquita = False
                        else:
                            pygame.mixer.music.play()
                            pygame.mixer.music.set_volume(0.1)
                            musiquita = True
                    elif salir.collidepoint(pygame.mouse.get_pos()):
                        estado = "salir"
            pygame.display.flip()
    return estado