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
	archivo  = open("bdd.txt" , "r+" )
	palabras = archivo.readlines()
	for palabra in palabras:
		res=buscar(palabra,tablero)
		print("La palabra" ,palabra, "está en la posición", res[0], "del tablero en dirección",res[1])


def archivo():
	archivo  = open("bdd.txt" , "r+" )
	palabras = archivo.readlines()
	return palabras

def rellenar(tablero):
	i=0
	l=len(listaletras)
	for tupla in tablero:
		if tupla[2] == -1:
			tablero[i]=(i,listaletras[random(0,l)])
		i++	
	#return tablero

	print()



def mostrar( tablero ):

	print ( [tupla[0] for tupla in tablero] )


def buscar(tablero,palabra):
	n=sqrt(len(tablero)
	l=len(palabra)
	j=1
	i=0
	#si la primer letra coincide, ahora queda chequear si: 1) hacia la derecha sigue ++ 2) hacia la izq sigue --
	# 3) hacia arriba sigue -n 4) hacia abajo sigue +n 5) hacia la diagonal sigue n+1
	for tupla in tablero:
		if tupla[1] == palabra[0]:
			for tupla in tablero if i < l:
				if tupla[1]!=palabra[j]:
					break 
				elif:
					i++
		if i=l:
			return (tupla[0],horizontal hacia la derecha)
	for tupla in tablero:
		if tupla[1] == palabra[0]:
			for tupla in range(tablero[tupla],tablero,-1) if i < l:
				if tupla[1]!=palabra[j]:
					break 
				elif:
					i++
					j++
		if i=l:
			return (tupla[0],horizontal hacia la izquierda)
	for tupla in tablero:
		if tupla[1] == palabra[0]:
			for tupla in range(tablero[tupla],tablero,-n) if i < l:
				if tupla[1]!=palabra[j]:
					break 
				elif:
					i++
					j++
		if i=l:
			return (tupla[0],vertical hacia arriba)
	for tupla in tablero:
		if tupla[1] == palabra[0]:
			for tupla in range(tablero[tupla],tablero,n) if i < l:
				if tupla[1]!=palabra[j]:
					break 
				elif:
					i++
					j++
		if i=l:
			return (tupla[0],vertical hacia abajo)
	for tupla in tablero:
		if tupla[1] == palabra[0]:
			for tupla in range(tablero[tupla],tablero,n+1) if i < l:
				if tupla[1]!=palabra[j]:
					break 
				elif:
					i++
					j++
		if i=l:
			return (tupla[0],diagonal)

principal()