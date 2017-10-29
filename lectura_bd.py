import csv 
import codecs

#bd = "csv/farmacia.csv"
bd = "csv/except_csv/campos_en_registros_invalidos.csv"
class LongituCamposInvalidos(Exception):
	pass

try:
	with codecs.open(bd,"r",encoding='utf-8',errors='ignore') as archivo:
		lectura = csv.reader(archivo)
		cabezera = next(lectura)
		print (cabezera)
		cantidad_campos = len(cabezera)
		cont = 0
		for columnas in lectura:
			cont += 1
			if len(columnas) != cantidad_campos:
				raise LongituCamposInvalidos()	
		

except FileNotFoundError:
	print ("Ruta de archivo invalida")
except LongituCamposInvalidos:
	print ("Cantidad de campos invalidos en el registro N°: {}".format(cont))



