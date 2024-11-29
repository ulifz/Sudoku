import pygame
import menu_principal
import os
import json

pygame.init()

pantalla_x = 1600
pantalla_y = 900
pantalla = pygame.display.set_mode((pantalla_x,pantalla_y))
pygame.display.set_caption("Puntajes")
fuente = pygame.font.Font(None, 50)
puntajes = []
archivo = "puntajes.json"
    
def cargar_puntajes(archivo:json)->list:

    '''
    Abre un archivo .json para su lectura, o lo crea en caso de que sea inexistente. Retorna el archivo como una lista para facilitar su modificación.
    
    Arg:

    archivo = El archivo .json a abrir.

    Rtn:

    puntajes = list 
    '''

    if os.path.exists(archivo):
        with open(archivo, "r") as file:
            puntajes = json.load(file)
    else:
        puntajes = []
        with open(archivo, "w") as file:
            json.dump(puntajes, file)
    return puntajes

def mostrar_puntajes(pantalla:pygame.Surface, fondo_puntajes:pygame.Surface, puntajes:list)->None:
    '''
    Dibuja el título y los puntajes en la pantalla, tomando los valores que se le brindan por parámetro. No tiene retorno ya que solo dibuja lo indicado.

    Arg:

    pantalla = La superficie sobre la que se dibujan los textos.

    fondo_puntajes = El fondo a colocarle a la pantalla indicada.

    puntajes = La lista con los puntajes guardados.
    '''

    pantalla.fill((0, 0, 0))
    fuente = pygame.font.SysFont("unispace", 150, False, True)
    fuente_puntaje = pygame.font.SysFont("unispace", 100, False, True)
    titulo = fuente.render("Puntajes más altos", True, (181, 156, 29))
    pantalla.blit(fondo_puntajes, (0,0,pantalla_x,pantalla_y))
    pantalla.blit(titulo, (pantalla_x // 2 - titulo.get_width() // 2, 100))
    
    if len(puntajes) > 0:
        for i in range(len(puntajes)):
            texto = fuente_puntaje.render(f"{i + 1}. {puntajes[i]['nombre']} - {puntajes[i]['puntaje']}", True, (255, 255, 255))
            pantalla.blit(texto, (pantalla_x // 2 - texto.get_width() // 2, 300 + i * 85))

def iniciar_puntajes(fondo_puntajes: str) -> str:
    '''
    Inicia la pantalla de puntajes, utilizando mostrar_puntajes como auxiliar y agregandole los botones para interactuar con el sistema de estados del main. Retorna el estado para volver al menú principal.
    
    Arg:

    fondo_puntajes = La ruta donde está ubicada el fondo a utilizar en la pantalla.

    Rtn:

    estado = str para interactuar con el sistema de estados y volver al menú principal.
    
    '''

    pantalla_x = 1600
    pantalla_y = 900
    pantalla = pygame.display.set_mode((pantalla_x,pantalla_y))
    fondo_puntajes = pygame.image.load(fondo_puntajes)
    fondo_puntajes = pygame.transform.smoothscale(fondo_puntajes,(pantalla_x, pantalla_y))
    boton_volver_menu = menu_principal.crear_boton(100, "Menu", (255, 255, 255),None ,pantalla, 0.93, 0.90)
    puntajes = cargar_puntajes(archivo)
    
    pygame.mixer_music.load("sonidos/cancion_puntaje.mp3")
    pygame.mixer_music.play()
    pygame.mixer_music.set_volume(0.1)

    estado = "puntaje"

    while estado == "puntaje":

        mostrar_puntajes(pantalla, fondo_puntajes,puntajes)
        boton_volver_menu = menu_principal.crear_boton(100, "Menu", (255, 255, 255),None ,pantalla, 0.93, 0.90)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                estado = "salir"
            
            if event.type == pygame.MOUSEMOTION:
                if boton_volver_menu.collidepoint(pygame.mouse.get_pos()):
                    color_texto = (255, 30, 30)
                    boton_volver_menu = menu_principal.crear_boton(100, "Menu", color_texto,None ,pantalla, 0.93, 0.90)
                else:
                    color_texto = (255,255,255)
                    boton_volver_menu = menu_principal.crear_boton(100, "Menu", color_texto,None ,pantalla, 0.93, 0.90)
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                lista_botones_mouse = list(pygame.mouse.get_pressed())
                if lista_botones_mouse[0] == True:
                    if boton_volver_menu.collidepoint(pygame.mouse.get_pos()):
                        estado = "menu"
        pygame.display.flip()        
    
    return estado
                    