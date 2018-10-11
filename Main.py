import random

def principal():
    menu()

def menu():
	
	while True:
		key = input("""
Menu:
1-Generar una sopa de letras
2-Resolver una sopa de letras
(Ctrl+Z) -> salir

""")
		if key != "1" and key != "2":
			print ("\nLa tecla", key , "no es válida\n")

		if key == "1":
			generar()
		elif key == "2":
			resolver()

def generar():
	palabras = archivo()
	
	maxPalabra = len ( max ( palabras , key=len ) )
	cantPalabras = len ( palabras )
	
	datos = generarTablero ( maxPalabra )
	tablero = datos[0]
	dimension = datos[1]

	temp = palabras [0]
	tempextra = agregarPalabra( tablero , palabras[0] )
	for palabra in range ( 1 , cantPalabras ):
		verificarCoincidencia( tablero , temp , palabras[palabra] , tempextra[0] , tempextra[1] )
		temp = palabras[palabra]

def verificarCoincidencia( tablero , palabrai , palabraj , posicion , direccion):
	for i  in range (len (palabrai) - 1):
		for j in range (len (palabraj) -1):
			if palabrai[i] == palabraj[j]:
				agregarPalabraCruzado( tablero , posicion , direccion , palabraj , i , j )
	agregarPalabra( tablero , palabraj )

def agregarPalabra( tablero , palabraj ):
	print("agregarPalabrafunction")
	#devuelve posicion y direccion de la ultima palabra agregada (pongo tuplas de prueba
	#para que no se rompa el programa)
	return(1,0)

def agregarPalabraCruzado( tablero , posicion , direccion , palabraj , i , j ):
	print("agregarPalabraCruzadofunction")
	#devuelve posicion y direccion de la ultima palabra agregada (pongo tuplas de prueba
	#para que no se rompa el programa)
	return(0,1)

def generarTablero( maxPalabra ):
	"""El tablero esta representado con una lista de tuplas en donde la primera posicion
	es un numero que representa la posicion y el segundo un numero que representa el valor
	en esa posicion"""
	dimension = random.randint ( 1.5 * maxPalabra , 2 * maxPalabra)
	tablero = []

	for i in range ( pow ( dimension , 2 ) ):
		tablero += [ ( i , -1 ) ]

	return ( tablero , dimension )


def resolver():
	print("resolverfunction")


def archivo():
	archivo  = open("bdd.txt" , "r+" )
	palabras = archivo.readlines()
	return palabras

def rellenar():
	print("rellenarfunction")


def mostrar( tablero ):

	print ( [tupla[0] for tupla in tablero] )


def buscar():
	print("buscarfunction")

principal()
