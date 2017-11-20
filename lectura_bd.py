import csv 
import codecs




class LongituCamposInvalidos(Exception):
	pass

class CampoVacio(Exception):
	pass	

class CampoEnteroError(Exception):
	pass

def lectura_de_bd(basededatos):
	basededatos = basededatos
	try:
		with codecs.open(basededatos,"r",encoding='utf-8',errors='ignore') as archivo:
			cont = 0
			lectura = csv.reader(archivo)
			cabezera = next(lectura)            #GUARDO LA CABEZERA DE CSV 
			
			cantidad_campos = len(cabezera)    #CANTIDAD DE CAMPOS EN LA CABEZERA

			verificar_campo_vacio = "CODIGO"          #INGRESO EL NOMBRE DEL CAMPO QUE QUIERO VERIFICAR QUE NO ESTE VACIO, EN ESTE CASO ES EL CAMPO "CODIGO"
			indice_campo_vacio = cabezera.index(verificar_campo_vacio)    #BUSCO EL INDICE DEL CAMPO EN LA LISTA DE CABEZERA
			
			campo_entero = "CANTIDAD"
			indice_campo_entero = cabezera.index(campo_entero)

			campo_valor_decimal = "PRECIO"
			indice_campo_decimal = cabezera.index(campo_valor_decimal)

			
			for columnas in lectura:
				cont += 1

				campo_enteros = columnas[indice_campo_entero]
				coma = campo_enteros.index(".")
				decimal = int(campo_enteros[coma+1:])

				campo_decimal = columnas[indice_campo_decimal]
				coma_decimal = campo_decimal.index(".")

				if len(columnas) != cantidad_campos:        #VERIFICO QUE CADA REGISTRO TENGA LA CANTIDAD DE CAMPOS CORRECTAS, EN CASO DE NO TENER LA CANTIDAD CREO LA EXCENCION "LongituCamposInvalidos"
					raise LongituCamposInvalidos()

			
				elif len(columnas[indice_campo_vacio]) == 0:      #VERIFICO QUE CADA CAMPO "CODIGO" NO SE ENCUENTRE VACIO, EN CASO DE ESTAR VACIO CREO LA EXCEPCION "CAMPO VACIO"
					raise CampoVacio()

				elif decimal > 0:
					raise CampoEnteroError()
					#elif type(columnas[indice_campo_decimal]) != float:
				
			return True 			


	except FileNotFoundError:
		print ("Ruta de archivo invalida")

	except LongituCamposInvalidos:
		print ("Cantidad de campos invalidos en el Registro N°: '{}'".format(cont))

	except CampoVacio:
		print ("Campo: '{}' vacio en el Registro N°: '{}'".format(verificar_campo_vacio, cont))

	except CampoEnteroError:
		print ("Campo: '{}' debe ser un numero entero en el Registro N°: '{}'".format(campo_entero, cont))	


	except ValueError:
		print ("Campo: '{}' debe ser un numero decimal en el Registro N°: '{}'".format(campo_valor_decimal, cont))



