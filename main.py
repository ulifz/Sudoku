import puntaje
import menu_principal
import sudoku

def main():
    '''
    Maneja los estados del programa, cambiando entre las distintas pantallas y verificando que esté corriendo a menos que se seleccione la opción "Salir".
    No recibe argumentos, ni devuelve nada.
    '''
    corriendo_programa = True
    estado = "menu"
    lista_dificultad = ["facil"]

    while corriendo_programa == True:
        if estado == "menu":
            estado = menu_principal.iniciar_menu("imagenes/navidad.webp",lista_dificultad)
        elif estado == "jugar":
            estado = sudoku.iniciar_sudoku(lista_dificultad[0])
        elif estado == "puntuacion":
            estado = puntaje.iniciar_puntajes("imagenes/fondo_puntajes.jpg")
        elif estado == "salir":
            corriendo_programa = False
                 
main()