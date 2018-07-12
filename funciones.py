import csv
from lectura_bd import lectura_de_bd

usuarios = "./csv/usuarios.csv"
bd = "./csv/farmacia.csv"

def encabezado():                              # Lista con el encabezado del csv
	encabezados = []
	if lectura_de_bd(bd) == True:
		with open(bd,'r',encoding='utf-8',errors='ignore') as archivo:
			lectura = csv.reader(archivo)
			primera_fila= next(lectura)
			encabezados.append(primera_fila)
	return encabezados

def datos():								#Lista con los registros del csv
	datos = []
	if lectura_de_bd(bd) == True:
		with open(bd,'r',encoding='utf-8',errors='ignore') as archivo:
			lectura = csv.reader(archivo)
			primera_fila= next(lectura)
			for x in lectura:
				datos.append(x)
	return datos


def indice_encabezado(nombre_campo):		 # Indice del campo ingresado
	registros = encabezado()
	indice = registros[0].index(nombre_campo)
	return indice


def registros_no_repetidos(campo):           #Lista no repetida
	indice = indice_encabezado(campo)
	registros = datos()
	lista_no_repet = []
	for x in registros:
		lista_no_repet.append(x[indice])
	lista_no_repet = list(set(lista_no_repet))
	lista_no_repet.sort()
	return lista_no_repet

def ultimas_vetas(cantidad):                   #Lista de los ultimos x registros de compra
	ultimas_ventas = []
	registros = datos()
	cont = -1
	for x in range(cantidad):
		ultimas_ventas.append(registros[cont]) 
		cont -= 1
	return ultimas_ventas

def productos_vendidos(cantidad):        		 #Lista de los productos mas vendidos
	lista_productos = registros_no_repetidos("PRODUCTO")
	registros = datos()
	indice_producto = indice_encabezado("PRODUCTO")
	indice_cantidad = indice_encabezado("CANTIDAD")
	lista_productos_vendidos = []
	for productos in lista_productos:
		cont = 0
		for reg in registros:			
			if productos == reg[indice_producto]:
				cant = reg[indice_cantidad]
				coma = cant.index(".")
				cont += int(cant[:coma])
		lista_productos_vendidos.append([productos,cont])

	lista_productos_vendidos = sorted(lista_productos_vendidos ,key=lambda student: student[1], reverse=True)   #Ordeno la lista de mayor a menor segun cantidad vendidas
	lista_productos_vendidos = lista_productos_vendidos[:cantidad]
	return lista_productos_vendidos

def clientes_consumo(cantidad):            #Lista de los clientes con el consumo total
	lista_clientes = registros_no_repetidos("CLIENTE")
	registros = datos()
	indice_cantidad = indice_encabezado("CANTIDAD")
	indice_cliente = indice_encabezado("CLIENTE")
	indice_precio = indice_encabezado("PRECIO")
	lista_clientes_consumo = []
	for clientes in lista_clientes:
		cont = 0
		for reg in registros:
			if clientes == reg[indice_cliente]:
				cont += float(reg[indice_cantidad]) * float(reg[indice_precio])
		lista_clientes_consumo.append([clientes,round(cont,2)])
	lista_clientes_consumo = sorted(lista_clientes_consumo ,key=lambda student: student[1], reverse=True)
	lista_clientes_consumo = lista_clientes_consumo[:cantidad]
	return lista_clientes_consumo

def agregar_venta(cliente,producto,cantidad):   # Agregar registro al archivo csv: farmacia.csv
	registros = datos()
	indice_producto = indice_encabezado("PRODUCTO")
	indice_codigo = indice_encabezado("CODIGO")
	indice_precio = indice_encabezado("PRECIO")
	cantidad_f = str(cantidad)
	cantidad_f = cantidad_f+'.00'
	registro_producto = []
	for reg in registros:
		if producto == reg[indice_producto]:
			registro_producto.append(reg)
			break

	with open(bd,"a") as archivo:
		archivo.writelines([cliente + ','+ registro_producto[0][indice_codigo] + ',' + producto + ',' + cantidad_f +','+ registro_producto[0][indice_precio] +'\n'])				
		return "Se agrego correctamente"



def consultar_usuario(usuario,password):
	estado = False
	with open(usuarios,'r') as archivo:
		usuarioss = csv.reader(archivo)
		for reg in usuarioss:
			if reg[0] == usuario and reg[1] == password:
				estado = True
	return estado

#def nuevo_usuario(usuario,pw,pw2)











