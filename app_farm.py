import csv
from flask import Flask, render_template, flash, session, redirect, url_for, request
from flask_bootstrap import Bootstrap
from forms import LoginForm, NombreCliente, NombreProducto, Cantidad_clientes , Cantidad_productos, Registrar
from lectura_bd import lectura_de_bd
import codecs

#BASE DE DATOS:
bd = "csv/farmacia.csv"

#BASE DE DATOS DE PRUEBA PARA COMPROBARA LAS EXCEPCIONES DEL CSV:
#bd = "csv/except_csv/campos_en_registros_invalidos.csv"
#bd = "csv/except_csv/campo_vacio.csv"
#bd = "csv/except_csv/campo_precio_sin_decimal.csv"
#bd = "csv/except_csv/campo_cantidad_con_valor_decimal.csv"

csv_farmacia = lectura_de_bd(bd)

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'key_secret'

@app.route("/")                 #Pagina de inicio
def index():
	if 'usuario' in session:
		return redirect (url_for("ultimas_ventas"))
	return render_template("index.html") 


@app.route("/login", methods = ['GET','POST'])          #Login de usuario 
def login():
	login = LoginForm()
	if login.validate_on_submit():							#Recibe los datos y crea session en caso de ser correcto Y redireccion a ultimas_ventas
		with open("csv/usuarios.csv","r") as archivo:
			usuarios = csv.reader(archivo)
			for x in usuarios:
				if login.usuario.data == x[0] and login.password.data == x[1]:
					session['usuario'] = login.usuario.data
					return redirect (url_for("ultimas_ventas"))
			else: 
				flash("Datos Incorrectos")
				return redirect (url_for("login"))
	return render_template("login.html", formulario = login)

@app.route("/logout")           # Destruyo la session y redirecciono a index 
def logout():
	if 'usuario' in session:
		session.pop('usuario')
	return redirect (url_for("index"))	


@app.route("/ultimas_ventas", methods=['GET','POST'])     # pagina de ultimas_ventas en caso de sesion iniciada sino redirecciono a indexx 
def ultimas_ventas():
	if 'usuario' in session:
		user = session['usuario']

		if csv_farmacia  == True:	                  # Pregunto si el csv no tiene ningun error
			with open(bd,"r",encoding='utf-8',errors='ignore') as archivo:				
				lectura = csv.reader(archivo)
				cabezera = next(lectura)
				lista_registross = []
				for columnas in lectura:                # guardo en una lista todos los registros del csv
					lista_registross.append(columnas)

				ultimos_registros = []    
				cont = -1	
				for x in range(5):        # guardo en una lista los ultimos 5 registros del csv y lo renderizo
					ultimos_registros.append(lista_registross[cont])
					cont -= 1
			return render_template("ultimas_ventas.html", usuario = user, cabezera = cabezera ,ultimos_registros = ultimos_registros )
			
	else:
		return redirect (url_for("index"))




@app.route("/consumos_clientes",methods=['GET','POST'])       # LISTAR TODOS LOS PRODUCTOS QUE COMPRO UN CLIENTE
def consumos_clientes():
	if 'usuario' in session:
		user = session['usuario']								# VERIFICO QUE ESTE INICIADA LA SESION, ENVIO EL FORMULARIO O GUARDO LOS DATOS RECIBIDOS POR EL FOMULARIO
		form_consumos_clientes = NombreCliente()			
		if form_consumos_clientes.validate_on_submit():
			nombre_cliente = form_consumos_clientes.cliente.data.upper()
			longitud_nombre = len(nombre_cliente)

			if csv_farmacia  == True:					# GUARDO EN UNA LISTA TODOS LOS CLIENTES 
				with open(bd,"r",encoding='utf-8',errors='ignore') as archivo:				
					lecturas = csv.reader(archivo)
					cabezera = next(lecturas)
					clientes = cabezera.index("CLIENTE")
					
					lista_columna_clientes = []
					for columnas in lecturas:
						lista_columna_clientes.append(columnas[clientes])

					lista_clientes = list(set(lista_columna_clientes))		


			lista_de_clientes = []          
			for x in lista_clientes:				# AÑADO A LA LISTA LOS CLIENTES Q SEAN IGUALES A EL DATO INTRODUCIDO
				if nombre_cliente == x[:longitud_nombre]:
					lista_de_clientes.append(x)            # ENVIO LA LISTA DE LOS CLIENTES Q COINCIDIERON 
			return render_template("lista_usuarios.html", nombre_campo = cabezera[clientes],lista_de_clientes = lista_de_clientes,usuario = user)
		
		return render_template("consumos_clientes.html", formulario = form_consumos_clientes, usuario = user)

@app.route("/lista_de_clientes",methods=['GET','POST'])			
def productos_de_clientes():
	if 'usuario' in session:
		nombre_cliente = request.form['cliente']			# RECIBO EL NOMBRE DEL CLIENTE QUE DESEO SABER LOS PRODUCTOS Q CONSUMIO
		if csv_farmacia  == True:
			with open(bd,"r",encoding='utf-8',errors='ignore') as archivo:			# AÑADO EN LISTA LOS PRUCTOS DE ESE CLIENTE
				lectura = csv.reader(archivo)
				cabezera = next(lectura)
				cliente = cabezera.index("CLIENTE")
				lista = []
				for columnas in lectura:
					if columnas[cliente] == nombre_cliente:
						lista.append(columnas)
					

		return render_template("ventas_por_cliente.html",cliente = nombre_cliente, lista = lista, cabezera = cabezera)

@app.route("/consumos_productos", methods=['GET','POST'])      # LISTAR TODOS LOS CLIENTES QUE COMPRARON UN DETERMINADO PRODUCTO
def consumos_productos():
	if 'usuario' in session:
		user = session['usuario']                         # VERIFICO QUE ESTE INICIADA LA SESION, ENVIO EL FORMULARIO O GUARDO LOS DATOS RECIBIDOS POR EL FOMULARIO
		form_consumos_productos = NombreProducto()
		if form_consumos_productos.validate_on_submit():
			nombre_producto = form_consumos_productos.producto.data.upper()
			longitud_nombre_producto = len(nombre_producto)

			if csv_farmacia  == True:											# GUARDO EN UNA LISTA TODOS LOS PRODUCTOS 	
				with open(bd,"r",encoding='utf-8',errors='ignore') as archivo:				
					lecturas = csv.reader(archivo)
					cabezera = next(lecturas)
					productos = cabezera.index("PRODUCTO")
					
					lista_todos_productos = []            
					for columnas in lecturas:
							lista_todos_productos.append(columnas[productos])

					lista_productos = list(set(lista_todos_productos))    # ELIMINO LOS PRODUCTOS REPETIDOS
					
			
			consulta_productos = []
			for x in lista_productos:								# AÑADO A LISTA LOS PROCUTOS QUE SEAN IGUALES A EL DATO INTRUCIDO Y ENVIO A LA PAGINA
				if nombre_producto == x [:longitud_nombre_producto]:
					consulta_productos.append(x)
			return render_template("lista_productos.html",usuario = user, lista_de_producto=consulta_productos,  nombre_campo = cabezera[productos])		

	return render_template("consumos_productos.html", formulario = form_consumos_productos, usuario = user)



@app.route("/lista_de_producto",methods=['GET','POST'])     
def clientes_de_productos():				
	if 'usuario' in session:
		nombre_producto = request.form['producto']
		if csv_farmacia  == True:
			with open(bd,"r",encoding='utf-8',errors='ignore') as archivo:     # RECIBO EL NOMBRE DEL PRODUCTO QUE DESEO SABER LA CANTIDAD DE CLIENTES Q LO COMPRARON
				lectura = csv.reader(archivo)
				cabezera = next(lectura)
				producto = cabezera.index("PRODUCTO")
				lista = []
				for columnas in lectura:								# AÑADO A LISTA Y LO ENVIO
					if columnas[producto] == nombre_producto:
						lista.append(columnas)
					

		return render_template("clientes_por_productos.html",producto = nombre_producto, lista = lista, cabezera = cabezera)
	return redirect (url_for("index"))



@app.route("/productos_mas_vendidos", methods=['GET', 'POST'])			# LISTAR LOS N PRODUCTOS MAS VENDIDOS
def productos_mas_vendidos():					
	if 'usuario' in session:								# VERIFICO QUE ESTE INICIADA LA SESION, ENVIO EL FORMULARIO O GUARDO LOS DATOS RECIBIDOS POR EL FOMULARIO
		user = session['usuario']
		formulario = Cantidad_productos()
		if formulario.validate_on_submit():
			cantidad_clientes = int(formulario.cantidad.data)
			if csv_farmacia  == True:
				with open(bd,"r",encoding='utf-8',errors='ignore') as archivo:		 	# ABRO LA BASE DE DATOS Y GUARDO EN UNA LISTA LOS NOMBRES DE TODOS LOS PRODUCTOS Y ELIMINO LOS QUE SE REPITEN
					lectura = csv.reader(archivo)
					cabezera = next(lectura)
					producto = cabezera.index("PRODUCTO")
					cantidad = cabezera.index("CANTIDAD")
					
					lista_de_productos = []
					
					for columnas in lectura:
						lista_de_productos.append(columnas[producto])						
																					
					lista = list(set(lista_de_productos))
					
				
				productos_cantidades = []                   
				for x in lista:
					with open(bd,"r",encoding='utf-8',errors='ignore') as archivo:		# RECORRO LA LISTA DE PRODUTOS Y LA COMPARO CON LA BASE DATOS
						lectura = csv.reader(archivo)
						
						contador_cantidad = 0
						for columnas in lectura:					# EN CASO DE SER IGUAL X PRODUCTO CON LA COLUMNA PRODUCTO DE LA BASE DE DATOS, SUMO AL CONTADOR LA CANTIDAD QUE SE VENDIO
							if x == columnas[producto]:
								z = columnas[cantidad]
								coma = z.index(".")
								parte_entera = int(z[:coma])
								
								contador_cantidad += parte_entera
						productos_cantidades.append([x,contador_cantidad])			# AÑADO A LA LISTA EL NOMBRE DE PRODUCTO CON LA CANTIDAD VENDIDAD
				

				productos_cantidades_ordenada = sorted(productos_cantidades ,key=lambda student: student[1], reverse=True)   # ORDENO LA LISTA DE PRODUCTO DE MAYOR A MENOS SEGUN LAS CANTIDADES VENDIDAS
					

				lista_render = productos_cantidades_ordenada[:cantidad_clientes]   # ENVIO A LA PAGINA LA LISTA DE N PRODUCTOS QUE DESEA SABER
				
					
				
			return render_template("lista_productos_vendidos.html", lista = lista_render, usuario = user , cantidad = cantidad_clientes )		
					
		return render_template("productos_mas_vendidos.html",formulario = formulario)

	return redirect(url_for("index"))





@app.route("/clientes_gastos", methods=['GET', 'POST'])       # LISTO LOS N CLIENTES QUE MAS PLATA GASTARON
def clientes_gastos():
	if 'usuario' in session:								# VERIFICO QUE ESTE INICIADA LA SESION, ENVIO EL FORMULARIO O GUARDO LOS DATOS RECIBIDOS POR EL FOMULARIO
		user = session['usuario']
		formulario = Cantidad_clientes()
		if formulario.validate_on_submit():
			cantidad_clientes = int(formulario.cantidad.data)
			if csv_farmacia  == True:
				with open(bd,"r",encoding='utf-8',errors='ignore') as archivo:	# ABRO LA BASE DE DATOS Y GUARDO EN UNA LISTA LOS NOMBRES DE TODOS LOS CLIENTES Y ELIMINO LOS QUE SE REPITEN			
					lectura = csv.reader(archivo)
					cabezera = next(lectura)
					cliente = cabezera.index("CLIENTE")
					cantidad = cabezera.index("CANTIDAD")
					precio = cabezera.index("PRECIO")
					
					lista_de_clientes = []
					
					for columnas in lectura:
						lista_de_clientes.append(columnas[cliente])						
																					
					lista = list(set(lista_de_clientes))
					
				
				cliente_gastos = []                                       
				for x in lista:														# RECORRO LA LISTA DE LOS CLIENTES Y LA COMPARO CON LA BASE DATOS
					with open(bd,"r",encoding='utf-8',errors='ignore') as archivo:
						lectura = csv.reader(archivo)
						
						contador_precio = 0
						for columnas in lectura:			# EN CASO DE SER IGUAL X CLIENTEDE LA LISTA DE CLIENTES CON LA COLUMNA DE CLIENTES DE LA BASE DE DATOS, MULTIPLICO LA CANTIDAD DE PRODUCTOS CON EL PRECIO Y LO SUMO A UN CONTADOR
							if x == columnas[cliente]:
								valor_precio = float(columnas[precio])
								cantidad_producto = columnas[cantidad] 
								coma = cantidad_producto.index(".")
								parte_entera = int(cantidad_producto[:coma])
								precio_total = valor_precio * parte_entera
								
								contador_precio += precio_total
						redondeo_contador_precio = round(contador_precio,2)
						cliente_gastos.append([x,redondeo_contador_precio])    # AGREGO A LA LISTA EL GASTO TOTAL DEL CLIENTE JUNTO CON EL NOMBRE
				

				cliente_gastos_ordenada = sorted(cliente_gastos ,key=lambda student: student[1], reverse=True)   # ORDENO LA LISTA DE CLIENTES CON SUS GASTOS DE MAYOR A MENOR SEGUN LA PLATA QUE GASTARON
					

				lista_render = cliente_gastos_ordenada[:cantidad_clientes]  # ENVIO A LA PAGINA LA CANTIDAD DE N CLIENTES QUE MAS GASTARON PLATA 
					
				
			return render_template("clientas_con_mas_gastos.html", lista = lista_render, usuario = user , cantidad = cantidad_clientes )		
					
		return render_template("productos_mas_vendidos.html",formulario = formulario)

	return redirect(url_for("index"))	


@app.errorhandler(404)							# ERROR 404 
def error_404(e):
	if 'usuario' in session:
		user = session['usuario']
		return render_template("404.html",usuario = user),404
	return render_template("404.html"),404	

@app.errorhandler(500)							#ERROR 500
def error_500(e):
	if 'usuario' in session:
		user = session['usuario']
		return render_template("500.html",usuario = user),500
	return render_template("500.html"),500


@app.route("/registrar",methods=['GET', 'POST'])    # PAGINA PARA REGISTRAR USUARIOS
def registrar():
	if 'usuario' in session:						#EN CASO DE HABERSE LOGUEADO REDIRECCIONO AL INDEX
		return redirect(url_for("index"))

	else:											#EN CASO CONTRARIO  MANDO EL FORMULARIO O GUARDO EN VARIABLES LOS DATOS RECIBIDOS DEL FORMULARIO
		formulario = Registrar()
		if formulario.validate_on_submit():				
			usuario = formulario.usuario.data
			pw = formulario.password.data
			pw2 = formulario.reingresar_password.data
			if pw == pw2:									# PREGUNTO SI LAS DOS CONTRASEÑAS INGRESADAS SON IGUALES
				existe = False
				with open("csv/usuarios.csv","r") as archivo:	#COMPRUEBO QUE NO EXISTA OTRO USUARIO CON EL MISMO NOMBRE
					lectura = csv.reader(archivo)
					for x in lectura:
						if x[0] == usuario:
							flash("Elija otro nombre de Usuario")
							existe = True
				if existe != True: 										# EN CASO DE NO EXISTIR AÑADO AL CSV EL USUARIO Y LA CONTRASEÑA Y REDIRECCIONO AL INDEX
					with open("csv/usuarios.csv","a") as archivo:
						archivo.writelines([usuario + ',' + pw + '\n'])				
						return redirect(url_for("index"))

			else:
				flash("Las contraseñas ingresadas no son iguales")

		return render_template("registrar.html",formulario = formulario)


if __name__ == ("__main__"):
	app.run(debug=True)