# coding: latin-1
import os
import sys

#################################################################################################
#Delfin Martin - Aldana Zarate                                                                  #
# Comentarios generales:                                                                        #
#   -El tablero está representado con una lista de n^2 elementos en donde los elementos         #
#   que la componenen representan las letras de la sopa de letras.                              #
#   -De manera arbitraria se decició que el valor que representa "vacío" es el número 1         #
#   -Las posiciones en las que se pueden agregar las palabras son:                              #
#       -vertical de arriba hacia abajo: vert                                                   #
#       -vertical de abajo hacia arriba: vertr                                                  #
#       -horizontal de izquierda a derecha: horiz                                               #
#       -horizontal de derecha a izquierda: horizr                                              #
#       -diagonal de arriba hacia abajo y de izquierda a derecha: diag                          #
#   -El archivo bdd.txt que funciona a modo de base de datos constituye la entrada de generar() #
#   y debe terminar en endline, lo mismo ocurre con el archivo que recibe resolver(): sopa.txt  #
#   El archivo bdd.txt debe contener palabras en mayúscula separadas por un endline             #
#   EL archivo sopa.txt debe contener la sopa de letras en donde cada                           #
#   fila del tablero está representada por una linea en el archivo en las cualas las letras     #
#   deben estar separadas por espacios (ver sopa.txt una vez que se corre generar() a modo de   #
#   ejemplo).                                                                                   #
#   -bdd.txt debe tener al menos dos palabras.                                                  #
#   -resolver() resuelve matrices cuadradas, es decir donde la cantidad de filas es igual a la  #
#   cantidad de columnas.                                                                       #
#   -Una posición no es válida para una palabra cuando no entra en el trablero debido a su      #
#   distancia relativa a los "márgenes" del mismo o cuando existen casillas ya ocupadas en al   #
#   menos una de las posiciones en donde se la quiere agregar.                                  #
#   -En rasgos generales, la función que genera la sopa de letras se comporta de la             #
#   siguiente manera:                                                                           #
#       Una vez extraídas las palabras de un archivo de texto, éstas se comparan de a           #
#       pares de manera que se verfique si poseen alguna letra en comun. En el caso que         #
#       coincidan en alguna letra, se analiza si la palabra que se quiere agregar se            #
#       puede agregar de forma cruzada (teniendo en cuenta la posición y dirección de la        #
#       palabra ya agregada). Si la disposión de las letras del tablero en ese momento no       #
#       permite que la palabra se agregue de manera cruzada, entonces se procede a agregarla    #
#       de la siguiente manera (el mismo método se usa para agregar palabras cuando no hay      #
#       coincidencia): se recorre el tablero hasta encontrar un espacio vacio. Una vez          #
#       encontrada esa posición, se descartan las posiciones no válidas. Luego, del conjunto    #
#       de posiciones válidas restantes, se eligeuna de manera aleatoria y la palabra           #
#       efectivamente se inserta en esa posicion.                                               #
#   -Por otro lado, el funcionamiento de la función que resuelve una sopa de letras se          #
#   caracteriza por:                                                                            #
#    Una vez extraídas las palabras a buscar y la sopa de letras a resolver de sus              #
#    respectivos archivos de texto, se llama a la función buscar que se ejecutará un número     #
#    de veces igual a la cantidad de palabras a buscar. En esta función, se va recorriendo      #
#    el tablero buscando una coincidencia con la primer letra de la palabra que se busca.       #
#    Si encuentra una coincidencia, luego procede a verificar si el resto de la palabra se      #
#    encuentra en alguna de las 5 direcciones posibles nombradas anteriormente. Cada dirección  #
#    tiene su propia "subsección" de tablero a recorrer. Si buscamos hacia la derecha, se       #
#    avanza de a 1 elemento, si se busca hacia la izquierda se retrocede el largo de la palabra #
#    y se avanza de a 1, si se busca en vertical hacia abajo se avanza de saltos de tamaño      #
#    de la dimensión, en vertical hacia arriba se retrocede en pasos de tamaño de la dimensión  #
#    y si se busca en diagonal se avanza en saltos de tamaño dimensión+1. Si cuando empieza a   #
#    buscar en alguna de estas direcciones, encuentra una letra que no coincide con la          #
#    esperada perteneciente a la palabra, se sale de la función. Si esto no sucede, quiere      #
#    decir que se ha encontrado la palabra y salimos en este punto volviendo a buscar,          #
#    retornando la posición y orientación de la palabra.                                        #
#   -Para adquirir aun mas posibilidades a la hora de insertar una palabra de la manera más     #
#   aleatoria posible, se pueden realizar una serie de transposiciones de la matriz que forma   #
#   la sopa de letras. Hay 7 posibles transposiciones a realizar:                               #
#       1) Rotar las columnas desde la última hacia adelante, quedando así ahora la primer      #
#       columna como última columna                                                             #
#       2) Poner los elementos de las filas en lugar de las columnas anteriores                 #
#       (transposición más clásica)                                                             #
#       3) El caso 2), inviertiendo el orden de las filas                                       #
#       4) Invertir el orden de las filas                                                       #
#       5) Invertir el orden de la totalidad de los elementos (el último elemento pasa          #
#       a ser el primero, el penultimo a segundo...)                                            #
#       6) Reemplazar los elementos de las filas por los de las columnas, empezando por la      #
#       ultima columna, desde el ultimo elemento hacia arriba                                   #
#       7) 6) invirtiendo el orden de los elementos de las columnas resultantes                 #
#################################################################################################

import random
import math

DEFAULT = 1  # Valor que representa posición vacía, declarada como cte


def principal():
    """Función princial: inicia el programa."""
    menu()


def menu():
    """Función menu: muestra el menu e invoca a las funciónes troncales del programa."""
    while True:
        key = input("""
Menu:
1-Generar una sopa de letras
2-Resolver una sopa de letras
(Ctrl+Z) -> salir
Ingrese una opcion: """)

        print ("\n")

        if key != "1" and key != "2":
            print ("#####\nLa tecla", key, "no es valida\n#####")

        if key == "1":
            generar()
        elif key == "2":
            resolver("sopa.txt", "bdd.txt")


def generar():
    """Función generar: invoca a verificarCoincidencia tomando palabras de a pares.
    Luego invoca a rellenar y por último invoca a guardar."""

    palabras = archivoGenerar("bdd.txt")
    maxPalabra = len(max(palabras, key=len))
    cantPalabras = len(palabras)

    tablero = generarTablero(maxPalabra)
    dimension = dimen(tablero)

    temp = palabras[0]
    tempextra = agregarPalabra(tablero, temp)
    for palabra in range(1, cantPalabras):
        tempextra = redireccionar(
            tablero,
            temp,
            tempextra[0],
            tempextra[1],
            palabras[palabra])
        temp = palabras[palabra]

    rellenar(tablero, palabras)

    transposicion = random.randint(0, 6)
    print(transposicion)
    tablero = manipular(tablero, transposicion)
    guardar(tablero)

#manipular: str list -> str list
def manipular(tablero, transposicion):
    """Funcion transponerIzq: toma un tablero y lo devuelve con alguna de las 7 transposiciones posibles"""
    dimension = dimen(tablero)
    largo = len(tablero)
    retorno = []

    for i in range(dimension):
        for j in range(0, largo, dimension):
            
        	if transposicion == 0:
        		indice = ((dimension - 1) - int(j / dimension)) + (i * dimension)
        	elif transposicion == 1:
        		indice = i + j
        	elif transposicion == 2:
        		indice = j + (dimension - 1) - i
        	elif transposicion == 3:
        		indice = int(j / dimension) + ((dimension - 1) - i) * dimension
        	elif transposicion == 4:
        		indice = (dimension - 1) - int(j / dimension) + (dimension - 1 - i) * dimension
        	elif transposicion == 5:
        		indice = ((dimension - 1) - int(j / dimension)) * dimension + (dimension - 1 - i)
        	else:
        		indice = (dimension - 1 - (int(j / dimension))) * dimension + i

        	retorno += [tablero[indice]]

    return retorno

#archivoGenerar: File -> str list
def archivoGenerar(nombreArchivo):
    """Función archivo: lee el archivo bdd.txt y devuelve una lista con las palabras pertenecientes al archivo"""
    archivo = open(nombreArchivo, "r+")
    palabras = []
    for linea in archivo:
        palabras += [linea[:-1]]

    if palabras == []:
        raise ValueError("El archivo no contiene palabras")

    return palabras

#generarTablero: int -> int list
def generarTablero(maxPalabra):
    """Función generarTablero: toma el tamaño de la palabra de mayor tamaño y devuelve un tablero de n filas por n
    columnas en donde el n es un número aleatorio en el intervalo: [1.5*maxPalabra,2*maxPalabra]."""
    dimension = random.randint(int(1.5 * maxPalabra), int(2 * maxPalabra))
    tablero = []

    for i in range(pow(dimension, 2)):
        tablero += [DEFAULT]

    return (tablero)

# redireccionar: list , str , int , int , str -> ( int , int )


def redireccionar(tablero, palabrai, posicion, direccion, palabraj):
    """Función redireccionar: toma el tablero, la ultima palabra ingresada en conjunto con su posición y
    direccion y la palabra que se desea ingresar. Si las palabras tienen algun punto de coincidencia, se invoca
    a la función agregarPalabraCruzado, caso contrario se invoca a agregarPalabra. La función devuelve una tupla
    en donde las componentes son la posicion y la direccion de la última palabra agregada."""
    coincidencia = verificarCoincidencia(palabrai, palabraj)

    if coincidencia == []:
        retorno = agregarPalabra(tablero, palabraj)
    else:
        tupla = coincidencia[0]
        retorno = agregarPalabraCruzado(
            tablero, posicion, direccion, palabraj, tupla[0], tupla[1])

    return retorno

#verificarCoincidencia: str, str -> (int , int) list
def verificarCoincidencia(palabrai, palabraj):
    """Función verificarCoincidencia: toma dos palabras y devuelve una lista en la que el primer elemento es una tupla
    en la cual las componentes representan la posicion de coincidencia relativa a ambas palabras. Caso contrario,
    devuelve la lista vacía."""

    largo1 = len(palabrai)
    largo2 = len(palabraj)

    for i in range(largo1):
        for j in range(largo2):
            if palabrai[i] == palabraj[j]:
                return [(i, j)]

    return []

#agregarPalabra: List , str -> (int , str)
def agregarPalabra(tablero, palabra):
    """Función agregarPalabra: toma el tablero y la palabra a agregar y devuelve una tupla en donde las
    componentes representan la posicion y direccion de la palabra agregada. En el caso que la palabra no se pueda
    agregar, se lanza un error"""
    dimension = dimen(tablero)

    for i in range(len(tablero)):
        if tablero[i] == DEFAULT:
            direcciones = ["horiz", "horizr", "vert", "vertr", "diag"]
            for j in range(1, len(palabra)):

                if "horiz" in direcciones:
                    iterador = i + j
                    if (not dentroDeLimites(tablero, iterador)) or (
                            not mismaFila(tablero, i, iterador)):
                        direcciones.remove("horiz")
                    elif tablero[iterador] != DEFAULT:
                        direcciones.remove("horiz")

                if "horizr" in direcciones:
                    iterador = i - j
                    if (not dentroDeLimites(tablero, iterador)) or (
                            not mismaFila(tablero, i, iterador)):
                        direcciones.remove("horizr")
                    elif tablero[iterador] != DEFAULT:
                        direcciones.remove("horizr")

                if "vert" in direcciones:
                    iterador = i + (j * dimension)
                    if (not dentroDeLimites(tablero, iterador)) or (
                            not mismaCol(tablero, i, iterador)):
                        direcciones.remove("vert")
                    elif tablero[iterador] != DEFAULT:
                        direcciones.remove("vert")

                if "vertr" in direcciones:
                    iterador = i - (j * dimension)
                    if (not dentroDeLimites(tablero, iterador)) or (
                            not mismaCol(tablero, i, iterador)):
                        direcciones.remove("vertr")
                    elif tablero[iterador] != DEFAULT:
                        direcciones.remove("vertr")

                if "diag" in direcciones:
                    iterador = i + (j * (dimension + 1))
                    if ((((dimension - (i % dimension)) < len(palabra)) or
                         ((dimension - (i // dimension)) < len(palabra))) or
                            (tablero[iterador] != DEFAULT)):
                        direcciones.remove("diag")

            if direcciones != []:
                posicion = i
                direc = random.choice(direcciones)
                insertar(tablero, posicion, direc, palabra)
                return(posicion, direc)

    errorMessage = (
        "No se pudo agregar la palabra, checkear que la cantidad de palabras no"
        " sea mucho mayor que el tamaño de la palabra máxima")
    raise ValueError(errorMessage)
    return(-1, -1)

#agregarPalabraCruzado: List , int , str , str , int , int -> ( int , str )
def agregarPalabraCruzado(tablero, posicion, direccion, palabra, i, j):
    """Función agregarPalabraCruzado: toma el tablero , la posicion y direccion de la última palabra agregada,
    la palabra a agregar y el punto en el que coinciden las palabras relativo a las posiciones de cada una de ellas.
    Se invoca a la funcion preprocesar y luego se eliminan las direcciones
    La función devuelve una tupla en donde las componentes representan la posicion y direccion de la palabra agregada."""
    dimension = dimen(tablero)
    largo = len(palabra)
    direcciones = ["horiz", "horizr", "vert", "vertr", "diag"]

    direccionesAEliminar = preprocesar(direcciones, direccion)
    for direc in direccionesAEliminar:
        direcciones.remove(direc)

    interseccion = pivot(tablero, posicion, direccion, i)
    retorno = cruzar(tablero, direcciones, palabra, interseccion, j)
    return retorno

#preprocesar: str List, str -> str List 
def preprocesar(direcciones, direccion):
    """Función preprocesar: toma una lista de direcciones y una dirección y devuelve una lista con las posiciones
    no válidas de la siguiente manera:
            -si la palabra anterior se insertó en dirección vertical (en cualquiera de los dos sentidos) la siguiente
            no se podrá insertar de manera vertical, ya que algunos caracteres coincidirían con la anterior.
            -si la palabra anterior se insertó en dirección horizontal (en cualquiera de los dos sentidos), la siguiente
            no se podrá insertar de manera horizontal
            -si la palabra anterior se inserto en dirección diagonal entonces la siguiente no se podrá insertar en
            dirección diagonal."""

    if direccion == "vert" or direccion == "vertr":
        return ["vert", "vertr"]
    elif direccion == "horiz" or direccion == "horizr":
        return ["horiz", "horizr"]
    elif direccion == "diag":
        return ["diag"]
    else:
        raise ValueError(
            'Se pretende insertar una palabra en una dirección no válida')

#pivot: List, int , str , int ->  int
def pivot(tablero, posicion, direccion, i):
    """Función pivot: toma el tablero, la posicion y direccion de la última palabra agregada, y la posicion
    relativa a la palabra agregada en donde coincide con la palabra que se desea agregar. La función devuelve
    la posicion absoluta de coincidencia entre ambas palabras"""
    dimension = dimen(tablero)

    if direccion == "horiz":
        return (posicion + i)
    if direccion == "horizr":
        return (posicion - i)
    if direccion == "vert":
        return (posicion + (i * dimension))
    if direccion == "vertr":
        return (posicion - (i * dimension))
    if direccion == "diag":
        return (posicion + (i * dimension) + i)

#cruzar: List , str List , str , int , int -> ( int , str )
def cruzar(tablero, direcciones, palabra, inter, j):
    """Función cruzar: toma el tablero, una lista con direcciones posibles, la palabra a agregar, la posicion absoluta
    en donde las palabras coinciden, y la posicion de coincidencia relativa a la palabra que se quiere agregar.
    La función devuelve una tupla en donde las componentes representan la posicion y direccion de la palabra agregada."""
    dimension = dimen(tablero)
    largo = len(palabra)

    while direcciones != []:
        flag = 1
        direccion = random.choice(direcciones)
        posVal = posicionesValidas(tablero, direccion, j, inter, palabra)
        if (isinstance(posVal[0], str)) and (posVal[0] in direcciones):
            direcciones.remove(posVal[0])
        else:
            tupla = posVal[0]
            inicio = tupla[0]
            fin = tupla[1]
            salto = tupla[2]

            for h in range(inicio, fin, salto):
            	if (tablero[h] != DEFAULT) and (h != inter):
            		flag = 0

            if flag == 0:
                direcciones.remove(direccion)
            else:
                if (direccion[-1:] == 'r'):
                    posicion = fin - 1
                else:
                    posicion = inicio
                insertar(tablero, posicion, direccion, palabra)
                return (posicion, direccion)

    retorno = agregarPalabra(tablero, palabra)
    return retorno

#posicionesValidas: List, str , int , int , str -> List
def posicionesValidas(tablero, direccion, j, inter, palabra):
    """Función posicionesValidas: toma el tablero, una direccion perteneciente a la lista de posiciones
    válidas( hasta este momento ), la posicion de coincidencia relativa a la palabra que se desea ingresar,
    la posicion absoluta de coincidencia y la palabra que se desea ingresar. La función devuelve una lista
    con un solo elemento: en el caso que la dirección elegida no sea válida debido a límites del tablero,
    límites de la fila o límites de la columna, el elemento de la lista es un string con la dirección no válida;
    caso contrario, el elemento es una 3-upla en donde las componentes representan el inicio, el fin y el salto del
    rango en donde se insertaría la palabra( suponiendo que todas las posiciones en ese rango estén vacías)."""
    dimension = dimen(tablero)
    largo = len(palabra)

    if direccion == "horiz":
        inicio = inter - j
        fin = inter + largo - j
        salto = 1
        if ((not (mismaFila(tablero, inter, inicio) and mismaFila(tablero, inter, fin))) or
                (not (dentroDeLimites(tablero, inicio) and dentroDeLimites(tablero, fin)))):
            return ["horiz"]

    if direccion == "horizr":
        inicio = inter + j
        fin = inter + j - (largo - 1)
        salto = 1
        if ((not (mismaFila(tablero, inter, inicio) and mismaFila(tablero, inter, fin)))
                or not (dentroDeLimites(tablero, inicio) and dentroDeLimites(tablero, fin))):
            return ["horizr"]

    if direccion == "vert":
        inicio = inter - (j * dimension)
        fin = inter + dimension * ((largo - 1) - j)
        salto = dimension
        if (not (mismaCol(tablero, inter, inicio) and (mismaCol(tablero, inter, fin))) or
                not (dentroDeLimites(tablero, inicio) and dentroDeLimites(tablero, fin))):
            return ["vert"]

    if direccion == "vertr":
        inicio = inter + (j * dimension)
        fin = inter + dimension * (j - (largo - 1))
        salto = dimension
        if ((not (mismaCol(tablero, inter, inicio) and mismaCol(tablero, inter, fin))) or
                not (dentroDeLimites(tablero, inicio) and dentroDeLimites(tablero, fin))):
            return ["vertr"]

    if direccion == "diag":
        inicio = inter - ((j * dimension) + j)
        fin = inter + dimension * (largo - j) + j
        salto = dimension + 1
        if (not ((dentroDeLimites(tablero, inicio)) and (dentroDeLimites(tablero, fin))) or (
                ((dimension - (inicio % dimension)) < largo) or ((dimension - (inicio // dimension)) < largo))):
            return ["diag"]

    if (inicio < fin):
        return [(inicio, fin + 1, salto)]
    else:
        return [(fin, inicio + 1, salto)]

#insertar: List , int , str , str -> None
def insertar(tablero, posicion, direccion, palabra):
    """Función insertar: toma el tablero, la posición y dirección de la palabra que se desea ingresar y la
    palabra. La función inserta la palabra en el tablero y devuelve NULL. En el caso que se le pase una direccion
    no válida, se lanza un error"""
    dimension = dimen(tablero)
    largo = len(palabra)

    if direccion == "horiz":
        for i in range(largo):
            tablero[posicion + i] = palabra[i].upper()

    elif direccion == "horizr":
        for i in range(largo):
            tablero[posicion - i] = palabra[i].upper()

    elif direccion == "vert":
        for i in range(largo):
            tablero[posicion + (i * dimension)] = palabra[i].upper()

    elif direccion == "vertr":
        for i in range(largo):
            tablero[posicion - (i * dimension)] = palabra[i].upper()

    elif direccion == "diag":
        for i in range(largo):
            tablero[posicion + (i * (dimension + 1))] = palabra[i].upper()

    else:
        raise ValueError(
            'Se pretende insertar una palabra en una dirección no válida')

#rellenar: List , str List -> str List
def rellenar(tablero, palabras):
    """Función rellenar: toma el tablero y la lista de palabras del archivo y completa los casilleros
    vacíos del tablero con letras elegidas de forma aleatoria del conjunto de letras pertenecientes a las
    palabras"""
    u = ''.join(palabras)
    universo = set(u)
    for i in range(len(tablero)):
        if tablero[i] == DEFAULT:
            temp = random.sample(universo, 1)
            tablero[i] = temp[0].upper()

#guardar: str List -> None
def guardar(tablero):
    """Función guardar: toma el tablero y lo imprime de manera que quede una grilla nxn. Si se desea ver el resultado
    del tablero generado en pantalla, quitarle el comentario a "print" """
    dimension = dimen(tablero)

    sopa = open("sopa.txt", "r+")
    sopa.truncate(0)

    letras = []
    for i in range(len(tablero)):
        sopa.write(tablero[i] + " ")
        letras.append(tablero[i])

        if i % dimension == (dimension - 1):
            print (str.join(" ", letras))
            letras = []
            sopa.write("\n")

    sopa.close()

#dimen: List -> int
def dimen(tablero):
    """Función dimen: toma el tablero y calcula la dimensión n del mismo"""
    return int(math.sqrt(len(tablero)))

#dentroDeLimites: List , int -> Bool
def dentroDeLimites(tablero, posicion):
    """Función dentroDeLimites: toma un tablero y una posicion y devuelve True si la posición pertenece
    al tablero."""
    if (posicion >= 0) and (posicion <= len(tablero)):
        return True
    return False

#mismaFila: List, int , int -> Bool
def mismaFila(tablero, pos1, pos2):
    """Función mismaFila: toma el tablero y dos posiciones pertenecientes a el y devuelve True en el caso
    que las posiciones estén en la misma fila"""
    dimension = dimen(tablero)
    if (pos1 // dimension) == (pos2 // dimension):
        return True
    return False

#mismaCol: List, int , int -> Bool
def mismaCol(tablero, pos1, pos2):
    """Función mismaCol: toma el tablero y dos posiciones pertenecientes a el y devuelve True en el caso
    que las posiciones estén en la misma columna"""
    dimension = dimen(tablero)
    if (pos1 % dimension) == (pos2 % dimension):
        return True
    return False

#coordenadas: List, int -> ( int , int )
"""Función coordenadas: toma el tablero y una posicion del mismo y devuelve una tupla cuya primer componente es la fila
y la segunda es la columna donde está ubicado"""
def coordenadas(tablero, pos):
    dimension = dimen(tablero)
    return (pos // dimension, pos % dimension)

# resolver: file , file -> None


def resolver(nombreArchivoSopa, nombreArchivoPalabras):
    """Función resolver: la función toma una sopa de letras y una lista de palabras e imprime la posición de cada una en la sopa"""
    tablero = archivoResolver(nombreArchivoSopa)
    palabras = archivoGenerar(nombreArchivoPalabras)
    for palabra in palabras:
        res = buscar(tablero, palabra)
        coord = res[0]
        print(
            "La palabra ",
            palabra,
            " está en la fila ",
            coord[0],
            " columna ",
            coord[1],
            "en direccion",
            res[1])


# archivoResolver: file -> list
def archivoResolver(nombreArchivo):
    """Función archivoResolver: lee el archivo sopa.txt y devuelve una lista representando los caracteres de la sopa de letras
    escrita en el archivo"""
    archivo = open(nombreArchivo, "r+")
    filas = []
    tablero = []
    filas = archivo.read().splitlines()
    for fila in filas:
        tablero += fila.split()

    return tablero

# buscar: list , string -> ( ( int , int ) , string  )


def buscar(tablero, palabra):
    """Función buscar: toma un tablero y una palabra y devuelve una tupla cuya primera componente es otra tupla con el numero y de
    fila y de columna, y como segunda componenente la orientacion de la palabra"""
    dimension = dimen(tablero)
    largo = len(palabra)
    # si la primer letra coincide, ahora queda chequear si: 1) hacia la derecha sigue salto +1 2) hacia la izq salto: -1
    # 3) hacia arriba sigue salto: -n 4) hacia abajo sigue salto +n 5) hacia
    # la diagonal sigue: salto + n+1
    for e in range(len(tablero)):
        if tablero[e] == palabra[0]:

            # busco en direccion horiz

            if mismaFila(tablero, e, e + (largo - 1)
                         ) and dentroDeLimites(tablero, e + (largo - 1)):
                inicio = e + 1
                fin = e + largo
                salto = 1
                if buscarGeneral(
                    tablero,palabra,inicio,fin,salto):
                    return (
                        coordenadas(
                            tablero,
                            e),
                        "horizontal hacia la derecha")

            # busco en direccion horizr

            if mismaFila(tablero, e, e - (largo - 1)
                         ) and dentroDeLimites(tablero, e - largo):
                inicio = e - 1
                fin = e - largo
                salto = -1
                if buscarGeneral(
                        tablero,palabra,inicio,fin,salto):
                    return (
                        coordenadas(
                            tablero,
                            e),
                        "horizontal hacia la izquierda")

            # busco en direccion vertr

            if ((e // dimension) >= (largo - 1)
                ) and (dentroDeLimites(tablero, e - (dimension * (largo - 1)))):
                inicio = e - dimension
                fin = e - (dimension * largo - 1) - 1
                salto = (-1) * dimension
                if buscarGeneral(
                    tablero,palabra,inicio,fin,salto):
                    return (coordenadas(tablero, e), "vertical hacia arriba")

            # busco en direccion vert

            if (e // dimension) + (largo - 1) <= (dimension - \
                1) and dentroDeLimites(tablero, e + (dimension * (largo - 1))):
                inicio = e + dimension
                fin = e + (dimension * (largo - 1)) + 1
                salto = dimension
                if buscarGeneral(
                    tablero,palabra,inicio,fin,salto):
                    return (coordenadas(tablero, e), "vertical hacia abajo")

            # busco en las 4 direcciones en diagonal (debido a las transposiciones)
            # diagonal de arriba a abajo y de izq a der
            if (e % dimension) + (largo - 1) <= (dimension - \
                1) and dentroDeLimites(tablero, e + ((largo - 1) * (dimension + 1))):
                inicio = e + dimension + 1
                fin = e + (largo * dimension)
                salto = dimension + 1
                if buscarGeneral(
                    tablero,palabra,inicio,fin,salto):
                    return (coordenadas(tablero, e), "diagonal(de arriba a abajo de izq a der)")

            # diagonal de arriba a abajo y de der a izq
            if (e % dimension) - (largo - 1) >= 0  \
             and dentroDeLimites(tablero, e + ((largo - 1) * (dimension - 1))):
                inicio = e + dimension - 1
                fin = e + ((largo-1) * dimension)
                salto = dimension - 1
                if buscarGeneral(
                    tablero,palabra,inicio,fin,salto):
                    return (coordenadas(tablero, e), "diagonal(de arriba a abajo de der a izq)")
            
            #diagonal de abajo a arriba y de der a izq
            if (e % dimension) - (largo - 1) >= 0 \
             and dentroDeLimites(tablero, e - ((largo - 1) * (dimension + 1))):
                inicio = e - dimension - 1
                fin = e - (largo * dimension)
                salto = -(dimension + 1)
                if buscarGeneral(
                    tablero,palabra,inicio,fin,salto):
                    return (coordenadas(tablero, e), "diagonal(de abajo a arriba de der a izq)")
            
            #diagonal de abajo a arriba y de izq a der
            if (e % dimension) + (largo - 1) <= (dimension - \
                1) and dentroDeLimites(tablero, e - ((largo - 1) * (dimension - 1))):
                inicio = e - dimension + 1
                fin = e - ((largo-1) * dimension)
                salto = -dimension + 1
                if buscarGeneral(
                    tablero,palabra,inicio,fin,salto):
                    return (coordenadas(tablero, e), "diagonal(de abajo a arriba de izq a der)")

    raise ValueError("La palabra",palabra," no está en el tablero")

# buscarGeneral: list , string , int , int , int -> bool


def buscarGeneral(tablero, palabra, inicio, fin, salto):
    """Función buscarGeneral: toma como parámetro un tablero (lista), una palabra (string), un entero indicando el inicio de la lista
    a iterar, el fin de la lista a iterar y el salto al ir recorriendola y devuelve True si la palabra está en el modo de recorrido
    a la dirección correspondiente o False si no está en el recorrido de la dirección correspondiente"""
    letrapos = 1
    for i in range(inicio, fin, salto):
        if tablero[i] != palabra[letrapos]:
            return False
        else:
            letrapos += 1
    return True

principal()
