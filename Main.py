def principal():
    menu()

def menu():
	
	while True:
		key = input("""
Menu:
1-Generar una sopa de letras
2-Mostrar una sopa de letras
3-Resolver una sopa de letras
(Ctrl+Z) -> salir

""")
		if key != "1" and key != "2" and key != "3":
			print ("\nLa tecla", key , "no es válida\n")

		if key == "1":
			generar()
		elif key == "2":
			mostrar()
		elif key == "3":
			resolver()

def generar():
	print("generarfunction")
def resolver():
	print("resolverfunction")
def archivoIn():
	archivo  = open(bdd.txt , mode = 'w')
def archivoOut():
	archivo  = open(bdd.txt , mode = 'r+')
def insertar():
	print("insertarfunction")
def rellenar():
	print("rellenarfunction")
def mostrar():
	print("mostrarfunction")
def buscar():
	print("buscarfunction")

principal()
