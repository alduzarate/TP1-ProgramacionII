import random
import math

DEFAULT = 1

def principal():
    """Funcion princial: inicia el programa."""
    palabras = archivo()
    menu( palabras )

def menu( palabras ):
    """Funcion menu: muestra el menu e invoca a las funciones troncales del programa."""
    while True:
        key = input("""
Menu:
1-Generar una sopa de letras
2-Resolver una sopa de letras
(Ctrl+Z) -> salir
Ingrese una opción: """)
        print ()

        if key != "1" and key != "2":
            print ("\nLa tecla", key , "no es válida\n")
        if key == "1":
            generar( palabras )
        elif key == "2":
            resolver( palabras ) #ver como pasar la sopa

def generar( palabras ):
    """Funcion generar: toma una lista de palabras e invoca a verificarCoincidencia tomando palabras de a pares.
    Luego invoca a rellenar y por último muestra el tablero. La función devuelve el tablero."""
    
    maxPalabra = len ( max ( palabras , key=len ) )
    cantPalabras = len ( palabras )
    
    tablero = generarTablero ( maxPalabra )
    dimension = dimen ( tablero )

    temp = palabras[0]
    tempextra = agregarPalabra( tablero , temp )
    for palabra in range ( 1 , cantPalabras ):
        tempextra = verificarCoincidencia( tablero , temp , palabras[palabra] , tempextra[0] , tempextra[1] )
        temp = palabras[palabra]

    rellenar( tablero , palabras )
    mostrar( tablero )
    
    return tablero

def verificarCoincidencia( tablero , palabrai , palabraj , posicion , direccion):
    """Funcion verificarCoincidencia: toma el tablero, la ultima palabra ingresada, la que se desea ingresar
    y la posicion y direccion de ésta última. Si las palabras tienen algun punto de coincidencia, se invoca
    a la funcion agregarPalabraCruzado, caso contrario se invoca a agregarPalabra. La funcion devuelve una tupla
    en donde las componentes son la posicion y la direccion de la última palabra agregada respectivamente, 
    independientemente de cúal función la agrega."""
    for i  in range (len (palabrai)):
        for j in range (len (palabraj)):
            if palabrai[i] == palabraj[j]:
                retorno = agregarPalabraCruzado( tablero , posicion , direccion , palabraj , i , j )
                return retorno
    retorno = agregarPalabra( tablero , palabraj )
    return retorno

def agregarPalabra( tablero , palabra ):
    """Funcion agregarPalabra: toma el tablero y la palabra a agregar y devuelve una tupla en donde las 
    componentes son la posicion y la direccion de la palabra agregada. En el caso que la palabra no se pueda
    agregar, se lanza un error"""
    dimension = dimen ( tablero )

    for i in range ( len ( tablero )):
        if tablero[i] == DEFAULT:
            direcciones = [ "horiz" , "horizr" , "vert" , "vertr" , "diag" ]
            for j in range ( 1 , len( palabra ) ):


                if "horiz" in direcciones:
                    iterador = i + j
                    if ( not dentroDeLimites( tablero , iterador ) ) or ( not mismaFila( tablero , i , iterador ) ):
                        direcciones.remove("horiz")
                    elif tablero[iterador] != DEFAULT:
                        direcciones.remove("horiz")

                    
                if "horizr" in direcciones:
                    iterador = i - j
                    if ( not dentroDeLimites( tablero , iterador ) ) or ( not mismaFila( tablero , i , iterador ) ):
                        direcciones.remove("horizr")
                    elif tablero[iterador] != DEFAULT:
                        direcciones.remove("horizr")


                if "vert" in direcciones:
                    iterador = i + ( j * dimension )
                    if ( not dentroDeLimites( tablero , iterador ) ) or ( not mismaCol( tablero , i , iterador ) ):
                        direcciones.remove("vert")
                    elif tablero[iterador] != DEFAULT:
                        direcciones.remove("vert")


                if "vertr" in direcciones:
                    iterador = i - ( j * dimension )
                    if ( not dentroDeLimites( tablero , iterador ) ) or ( not mismaCol( tablero , i , iterador ) ):
                        direcciones.remove("vertr")
                    elif tablero[iterador] != DEFAULT:
                        direcciones.remove("vertr")


                if "diag" in direcciones:
                    if ((( dimension - ( i%dimension ) ) < len (palabra) ) or
                        (( dimension - ( i//dimension ) ) < len (palabra))):
                        direcciones.remove("diag")

            if direcciones != []:
                posicion = i
                direc = random.choice( direcciones )
                insertar ( tablero , posicion , direc , palabra )
                return(posicion,direc)

    errorMessage = ( "No se pudo agregar la palabra, checkear que la cantidad de palabras no"
                " sea mucho mayor que el tamaño de la palabra máxima" )
    raise ValueError( errorMessage )
    return(-1,-1)
    

def agregarPalabraCruzado( tablero , posicion , direccion , palabra , i , j ):
    """Funcion agregarPalabraCruzado: toma el tablero , la posicion y direccion de la última palabra agregada, 
    la palabra a agregar y el punto en el que coinciden las palabras respecto a cada una de las palabras.
    La función devuelve una tupla en donde las componentes son la posicion y la direccion de la palabra agregada."""
    dimension = dimen( tablero )
    largo = len ( palabra )
    direcciones = [ "horiz" , "horizr" , "vert" , "vertr" , "diag" ]

    #Preprocesamiento
    if direccion == "vert" or direccion == "vertr":
        direcciones.remove("vert")
        direcciones.remove("vertr")
    elif direccion == "horiz" or direccion == "horizr":
        direcciones.remove("horiz")
        direcciones.remove("horizr")
    elif direccion == "diag":
        direcciones.remove("diag")

    interseccion = pivot ( tablero , posicion , direccion , i )
    retorno = cruzar( tablero , palabra , interseccion , direcciones , j )
    return retorno


def pivot ( tablero , posicion , direccion , i ):
    """Funcion pivot: toma el tablero, la posicion y direccion de la última palabra agregada, y la posicion
    relativa a la palabra agregada en donde coincide con la palabra que se desea agregar. La función devuelve
    la posicion absoluta de coincidencia entre ambas palabras"""
    dimension = dimen( tablero )

    if direccion == "horiz":
        return ( posicion + i )
    if direccion == "horizr":
        return ( posicion - i )
    if direccion == "vert":
        return ( posicion + ( i * dimension ) )
    if direccion == "vertr":
        return ( posicion - ( i * dimension ) )
    if direccion == "diag":
        return ( posicion + ( i * dimension ) + i )

def cruzar ( tablero , palabra , inter , direcciones , j):
    """Funcion cruzar: toma el tablero, la palabra a agregar, la posicion absoluta en donde las palabras 
    coinciden, una lista con direcciones posibles y la posicion relativa a la palabra que se quiere agregar 
    en donde las palabras coinciden. La función devuelve una tupla en donde las componentes son la posicion y la 
    direccion de la palabra agregada."""
    dimension = dimen( tablero )
    largo = len ( palabra )

    while direcciones != []:
        flag = 1
        direccion = random.choice ( direcciones )
        posVal = posicionesValidas( tablero , direccion , j , inter , palabra)
        if (type( posVal[0] ) == str) and ( posVal[0] in direcciones ):
            direcciones.remove( posVal[0] )
        else:
            tupla = posVal[0]
            inicio = tupla[0]
            fin = tupla[1]
            salto = tupla[2]

            for h in range ( inicio , fin , salto ):
                if ( tablero [h] != DEFAULT ) and ( h != inter ):
                    flag = 0

            if flag == 0:
                direcciones.remove( direccion )
            else:
                if ( direccion[-1:] == 'r' ):
                    posicion = fin - 1
                else:
                    posicion = inicio
                insertar ( tablero , posicion , direccion , palabra )
                return ( posicion , direccion )

    retorno = agregarPalabra ( tablero , palabra )
    return retorno

def posicionesValidas( tablero , direccion , j , inter , palabra ):
    """Funcion posicionesValidas: toma el tablero, una direccion perteneciente a la lista de posiciones
    válidas( hasta este momento ), la posicion de coincidencia relativa a la palabra que se desea ingresar,
    la posicion absoluta de coincidencia y la palabra que se desea ingresar. La función devuelve una lista 
    con un solo elemento: en el caso que la dirección elegida no sea válida debido a límites del tablero, 
    límites de la fila o límites de la columna, el elemento es un string con la dirección no válida. Caso
    contrario, el elemento es una 3-upla en donde las componentes son el inicio, el fin y el salto del 
    rango en donde se insertaría la palabra."""
    dimension = dimen ( tablero )
    largo = len( palabra )

    if direccion == "horiz":
        inicio = inter - j
        fin = inter + largo - j
        salto = 1
        if ( ( not ( mismaFila( tablero , inter , inicio ) and mismaFila( tablero , inter , fin ) ) ) or
            ( not ( dentroDeLimites ( tablero , inicio ) and dentroDeLimites ( tablero , fin ) ) ) ):
            return ["horiz"]
            
    if direccion == "horizr":
        inicio = inter + j
        fin = inter + j - ( largo - 1 )
        salto = 1
        if ( ( not ( mismaFila( tablero , inter , inicio ) and mismaFila( tablero , inter , fin ) ) ) or
            not ( dentroDeLimites ( tablero , inicio ) and dentroDeLimites ( tablero , fin ) ) ):
            return ["horizr"]

    if direccion == "vert":
        inicio = inter - ( j * dimension )
        fin = inter + dimension * ( ( largo - 1 ) - j )
        salto = dimension
        if ( not ( mismaCol( tablero , inter , inicio ) and ( mismaCol( tablero , inter , fin ))) or
            not ( dentroDeLimites ( tablero , inicio ) and dentroDeLimites ( tablero , fin ) ) ):
            return ["vert"]

    if direccion == "vertr":
        inicio = inter + ( j * dimension )
        fin = inter + dimension * ( j - ( largo - 1 ) )
        salto = dimension
        if ( ( not ( mismaCol( tablero , inter , inicio ) and mismaCol( tablero , inter , fin ) ) ) or
            not ( dentroDeLimites ( tablero , inicio ) and dentroDeLimites ( tablero , fin ) ) ):
            return ["vertr"]

    if direccion == "diag":
        inicio = inter - ( ( j * dimension ) + j )
        fin = inter + dimension * ( largo - j ) + j
        salto = dimension + 1
        if ( not ((dentroDeLimites( tablero , inicio )) and (dentroDeLimites( tablero , fin ))) or
            ((( dimension - ( inicio%dimension ) ) < largo ) or (( dimension - ( inicio//dimension ) ) < largo ))):
            return ["diag"]

    if ( inicio < fin ):
        return [ ( inicio , fin , salto ) ]
    else:
        return [ ( fin , inicio + 1 , salto ) ]

def dentroDeLimites ( tablero , posicion ):
    """Funcion dentroDeLimites: toma un tablero y una posicion y devuelve True si la posición pertenece
    al tablero."""
    if ( posicion >= 0 ) and ( posicion <= len( tablero ) ):
        return True
    return False

def insertar ( tablero , posicion , direccion , palabra ):
    """Funcion insertar: toma el tablero, la posición y dirección de la palabra que se desea ingresar y la
    palabra. La función inserta la palabra en el tablero y devuelve NULL. En el caso que se le pase una direccion
    no válida, se lanza un error"""
    dimension = dimen ( tablero )
    largo = len ( palabra )

    if direccion == "horiz":
        for i in range ( largo ):
            tablero[ posicion + i ] = palabra[i].upper()

    elif direccion == "horizr":
        for i in range ( largo ):
            tablero[ posicion - i ] = palabra[i].upper()

    elif direccion == "vert":
        for i in range ( largo ):
            tablero[ posicion + ( i * dimension ) ] = palabra[i].upper()

    elif direccion == "vertr":
        for i in range ( largo ):
            tablero[ posicion - ( i * dimension ) ] = palabra[i].upper()

    elif direccion == "diag":
        for i in range ( largo ):
            tablero[ posicion + ( i * ( dimension + 1 ) ) ] = palabra [i].upper()

    else:
        raise ValueError('Se pretende insertar una palabra con una dirección no válida')


def generarTablero( maxPalabra ):
    """Función generarTablero: toma el tamaño de la palabra de mayor tamaño y devuelve un tablero de nxn en
    donde el n es un número aleatorio en [1.5*maxPalabra,2*maxPalabra]. El tablero esta representado con una 
    lista de n^2 elementos en donde los elementos que la componenen representan las letras de la sopa de 
    letras. De manera arbitraria se decició que el valor que representa "vacío" es el número 1"""
    dimension = random.randint ( int(1.5 * maxPalabra) , int(2 * maxPalabra) )
    tablero = []

    for i in range ( pow ( dimension , 2 ) ):
        tablero += [ DEFAULT ]

    return ( tablero )

def archivo():
    """Función archivo: lee el archivo bdd.txt y devuelve una lista con las palabras pertenecientes al archivo"""
    archivo  = open("bdd.txt" , "r+" )
    palabras = []
    for linea in archivo:
        palabras += [ linea[:-1] ]
    return palabras

def rellenar( tablero , palabras ):
    """Función rellenar: toma el tablero y la lista de palabras del archivo y completa los casilleros
    vacíos del tablero con letras elegidas de fora aleatoria del conjunto de letras pertenecientes a las
    palabras"""
    u = ''.join(palabras)
    universo = set ( u )
    for i in range ( len ( tablero ) ):
        if tablero[i] == DEFAULT:
            temp = random.sample( universo , 1 )
            tablero[i] = temp[0].upper()

def mostrar( tablero ):
    """Función mostrar: toma el tablero y lo imprime de manera que quede una grilla nxn"""
    dimension = dimen( tablero )

    for i in range ( len ( tablero ) ):
        print ( " " , tablero[i] , end = '' )
        if i%dimension == (dimension - 1):
            print ()

def dimen( tablero ):
    """Función dimen: toma el tablero y calcula la dimensión n del mismo"""
    return int ( math.sqrt ( len ( tablero ) ) )

def mismaFila( tablero , pos1 , pos2 ):
    """Función mismaFila: toma el tablero y dos posiciones pertenecientes a el y devuelve True en el caso
    que las posiciones estén en la misma fila"""
    dimension = dimen ( tablero )
    if ( pos1//dimension ) == ( pos2//dimension ):
        return True
    return False

def mismaCol( tablero , pos1 , pos2 ):
    """Función mismaCol: toma el tablero y dos posiciones pertenecientes a el y devuelve True en el caso
    que las posiciones estén en la misma columna"""
    dimension = dimen ( tablero )
    if ( pos1%dimension ) == ( pos2%dimension ):
        return True
    return False

def resolver( palabras , tablero ):
    for palabra in palabras:
        res = buscar ( palabra , tablero )
        print("La palabra " ,palabra, " está en la posición ", res[0], " del tablero en dirección ",res[1])

def buscar(tablero,palabra):
    n = dimen(tablero)
    l = len(palabra)
    j = 1 #inicializado en 1 ya que es innecesario volver a chequear la primer letra de la palabra
    i = 0
    #si la primer letra coincide, ahora queda chequear si: 1) hacia la derecha sigue salto +1 2) hacia la izq salto: -1
    # 3) hacia arriba sigue salto: -n 4) hacia abajo sigue salto +n 5) hacia la diagonal sigue: salto + n+1
    for e in range( len( tablero ) ):
        if tablero[e] == palabra[0]:
                 #busco hacia la derecha
            if (e % n) + (l-1) <= (n-1):
                for elementoi in tablero[ (e+1) : (e+l) ]:
                        if elementoi != palabra[j]:
                            break
                        else:
                            i+=1
                            j+=1
            if i == (l-1):
                return ( e, "horizontal hacia la derecha" )
            i=0
            j=len(palabra)-1
           #busco hacia la izquierda
            if (e % n) >= (l-1):
                for elementoi in tablero[e-(l-1):e]:
                    if elementoi != palabra[j]:
                        break
                    else:
                        i+=1
                        j-=1
            if i == (l-1):
                return(e,"horizontal hacia la izquierda")
            i=0
            j=1
           #busco hacia arriba
            if e // n >= (l-1):
                for elementoi in range(e-n,e-(n*(l-1))-1,(-1)*n):
                    if tablero[elementoi] != palabra[j]:
                        break
                    else:
                        i+=1
                        j+=1
            if i == (l-1):
                return (e,"vertical hacia arriba")
            i=0
            j=1
           #busco hacia abajo
            if (e // n) + (l-1) <= (n-1):
                for elementoi in range(e+n,e+(n*(l-1))+1,n):
                    if tablero[elementoi] != palabra[j]:
                        break
                    else:
                        i+=1
                        j+=1
            if i == (l-1):
                return (e,"vertical hacia abajo")
            i=0
            j=1
                #busco hacia la diagonal
            if (e % n) + (l-1) <= (n-1):
                for elementoi in range(e+(n+1),e+(n*l),(n+1)):
                    if tablero[elementoi] != palabra[j]:
                        break
                    else:
                        i+=1
                        j+=1
            if i == (l-1):
                return (e,"diagonal")

principal()
