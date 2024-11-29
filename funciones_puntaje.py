import os
import json

ARCHIVO = "puntajes.json"

puntajes = []

def calcular_puntaje(errores:int, tiempo:int, dificultad:str,lista_numeros:list)->int:
    '''
    Calcula el puntaje conseguido por el usuario en base a los parametros que recibe. Retorna el puntaje redondeado para no tener flotantes.

    Arg:

    errores = La cantidad de errores que tuvo el usuario en el juego.

    tiempo = La cantidad de tiempo invertida en el juego.

    dificultad = La dificultad seleccionada para jugar.

    lista_numeros = Los números ingresados durante el juego.

    Rtn:

    puntaje = El entero resultante del cálculo de la función.
    '''
    aciertos = 0
    if len(lista_numeros) > 0:
        for numero in lista_numeros:
            if numero["error"] == False:
                aciertos += 1

    puntos_base = 1000
    penalizacion_error = 75
    penalizacion_tiempo = 50
    acierto = 15

    multiplicadores = {"facil": 0.75, "medio": 1, "dificil": 1.25}
    multiplicador = multiplicadores[dificultad]
    minutos = tiempo // 30
    puntaje = ((puntos_base - (errores * penalizacion_error + (2*errores))) * multiplicador) + aciertos*acierto - (minutos * penalizacion_tiempo)
    return round(puntaje)

if os.path.exists(ARCHIVO):
    with open(ARCHIVO, "r") as archivo:
        puntajes = json.load(archivo)
else:
    with open(ARCHIVO, "w") as archivo:
        json.dump({}, archivo)
    
def guardar_puntajes(puntajes:list,ARCHIVO:str)->None:
    '''
    Guarda los puntajes que se le brindan por parámetro en el archivo .json. Retorna None ya que solo guarda los datos en el archivo.

    Arg:

    puntajes = La lista de puntajes.

    ARCHIVO = La ruta de ubicación del archivo a modificar.
    '''
    with open(ARCHIVO, "w") as archivo:
        json.dump(puntajes, archivo)
    
def buscar_nombre_existente(nombre:str, puntajes:list)->bool:
    '''
    Busca si el nombre ingresado por el usuario ya existe en la lista de puntajes, retorna un booleano indicando si es correcto o no.

    Arg:

    nombre = El nombre ingresado por el usuario

    puntajes = La lista de puntajes.

    Rtn:

    nombre_encontrado = True si encontró el nombre, False si no existía.
    '''
    nombre_encontrado = False

    for jugador in puntajes:
        if jugador["nombre"] == nombre:
            nombre_encontrado = True

    return nombre_encontrado
    
def actualizar_puntajes(datos:tuple,puntajes:list=puntajes):
    '''
    Actualiza los puntajes de la lista, recibiendolos por una tupla y verificando con ayuda del auxiliar buscar_nombre_existente. Modifica la lista, la ordena y se asegura que no haya más valores que los 5 mayores. Guarda los valores utilizando el auxiliar guardar_puntajes. No tiene retorno ya que solo actualiza la lista.

    Arg:

    datos = Tupla con los datos (nombre y puntaje) del usuario.

    puntajes = Lista con los puntajes ingresados hasta el momento.
    '''
    nombre = datos[0]
    puntaje = datos[1]

    if buscar_nombre_existente(nombre, puntajes) == True:

        for jugador in puntajes:
            if jugador["nombre"] == nombre:
                if puntaje > jugador["puntaje"]:
                    puntajes.remove(jugador)
                    puntajes.append({"nombre": nombre, "puntaje": puntaje})
    else:
        puntajes.append({"nombre": nombre, "puntaje": puntaje})

    puntajes.sort(key=lambda x: x["puntaje"], reverse=True) 
    #Se utiliza la función lambda para no tener que hacer una función auxiliar de una sola línea.
    del puntajes[5:]
    guardar_puntajes(puntajes,ARCHIVO)