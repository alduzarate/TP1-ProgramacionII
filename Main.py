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
	#print (palabras)
	
	maxPalabra = len ( max ( palabras , key=len ) )
	cantPalabras = len ( palabras )
	
	datos = generarTablero ( maxPalabra )
	tab = datos[0]
	dim = datos[1]

	mostrar ( tab , dim )

def generarTablero( maxPalabra ):
	"""El tablero esta representado con una lista de tuplas en donde la primera posicion
	es un numero que representa la posicion y el segundo un numero que representa el valor
	en esa posicion"""
	dimension = random.randint ( 1.5 * maxPalabra , 2 * maxPalabra)
	print (dimension)
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


def insertar():
	print("insertarfunction")
def rellenar():
	print("rellenarfunction")


def mostrar( tablero , dimension ):

	print (tablero)

#	for i in tablero:
#		print ( " " , tablero[i][0] , end = '')
#		if i[0] % dimension == dimension - 1:
#			print ()

def buscar():
	print("buscarfunction")

principal()
