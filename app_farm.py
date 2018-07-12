import csv
import io
import pyexcel
from flask import Flask, render_template, flash, session, redirect, url_for, request,make_response
from flask_bootstrap import Bootstrap
from forms import *
from lectura_bd import lectura_de_bd
from datetime import datetime , date, time, timedelta
import codecs
from funciones import *



app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = '12345678'

@app.route("/")                 #Pagina de inicio
def index():
	if 'usuario' in session:
		return redirect (url_for("ultimas_ventas"))
	return render_template("index.html") 

#--------------------------

@app.route("/login", methods = ['GET','POST'])          #Login de usuario 
def login():
	if 'usuario' in session:						
		return redirect(url_for("index"))
	else:
		login = LoginForm()
		if login.validate_on_submit():							#Recibe los datos y crea session en caso de ser correcto Y redireccion a ultimas_ventas
			usuario = login.usuario.data
			password = login.password.data
			consulta = consultar_usuario(usuario,password)
			
			if consulta == True:
				session['usuario'] = usuario
				return redirect (url_for("ultimas_ventas"))
			else: 
				flash("Datos Incorrectos")
				return redirect (url_for("login"))

		return render_template("login.html", formulario = login)


@app.route("/logout")           # Cierro la session y redirecciono a index 
def logout():
	if 'usuario' in session:
		session.pop('usuario')
	return redirect (url_for("index"))	


#------------------------------------------REGISTRAR NUEVO USUARIO--------------------------------------------------

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


# --------------------------  ULTIMAS VENTAS -----------------------------------------

@app.route("/ultimas_ventas", methods=['GET','POST'])     # pagina de ultimas_ventas en caso de sesion iniciada sino redirecciono a indexx 
def ultimas_ventas():

	if 'usuario' in session:					
		user = session['usuario']
		cabezera = encabezado()
		ultimos_registros = ultimas_vetas(5)
		return render_template("ultimas_ventas.html", usuario = user, cabezera = cabezera ,ultimos_registros = ultimos_registros )

	else:
		return redirect (url_for("index"))


# --------------------------   CONSUMOS DE CLIENTES-----------------------------------

@app.route("/consumos_clientes",methods=['GET','POST'])       # RECIBE VALOR DEL FORMULARIO Y ENVIA LISTA CON LOS CLIENTES QUE COINDICEN
def consumos_clientes():
	
	if 'usuario' in session:
		user = session['usuario']								
		form_consumos_clientes = NombreCliente()			
		if form_consumos_clientes.validate_on_submit():
			nombre_cliente = form_consumos_clientes.cliente.data.upper()
			longitud_nombre = len(nombre_cliente)
			lista_de_clientes = registros_no_repetidos("CLIENTE")
			lista_de_clientess = []          
			for x in lista_de_clientes:				# AÑADO A LA LISTA LOS CLIENTES Q SEAN IGUALES A EL DATO INTRODUCIDO
				if nombre_cliente == x[:longitud_nombre]:
					lista_de_clientess.append(x)            # ENVIO LA LISTA DE LOS CLIENTES Q COINCIDIERON 
			return render_template("lista_usuarios.html", nombre_campo = "CLIENTES",lista_de_clientes = lista_de_clientess,usuario = user)
		
		return render_template("consumos_clientes.html", formulario = form_consumos_clientes, usuario = user)
	
	else:
		return redirect (url_for("index"))

@app.route("/lista_de_clientes",methods=['GET','POST'])		#  RECIBO EL NOMBRE DEL CLIENTE Y ENVIO  LA LISTA DE LOS PRODUCTO Q ADQUIRIO	
def productos_de_clientes():
	if 'usuario' in session:
		nombre_cliente = request.form['cliente']			
		cabezera = encabezado()
		lectura = datos()
		cliente = indice_encabezado("CLIENTE")
		lista = []
		for columnas in lectura:
			if columnas[cliente] == nombre_cliente:
				lista.append(columnas)
			
		return render_template("ventas_por_cliente.html",cliente = nombre_cliente, lista = lista, cabezera = cabezera)
	else:
		return redirect (url_for("index"))

# ------------------------------------- CONSUMO DE PRODUCTOS -------------------------------------

@app.route("/consumos_productos", methods=['GET','POST'])      # LISTAR TODOS LOS CLIENTES QUE COMPRARON UN DETERMINADO PRODUCTO
def consumos_productos():
	if 'usuario' in session:
		user = session['usuario']                        
		form_consumos_productos = NombreProducto()
		if form_consumos_productos.validate_on_submit():
			nombre_producto = form_consumos_productos.producto.data.upper()
			longitud_nombre_producto = len(nombre_producto)
			lista_productos = registros_no_repetidos("PRODUCTO")	
			consulta_productos = []
			for x in lista_productos:								# AÑADO A LISTA LOS PROCUTOS QUE SEAN IGUALES A EL DATO INTRUCIDO Y ENVIO A LA PAGINA
				if nombre_producto == x [:longitud_nombre_producto]:
					consulta_productos.append(x)
			return render_template("lista_productos.html",usuario = user, lista_de_producto=consulta_productos,  nombre_campo = "PRODUCTOS")		

		return render_template("consumos_productos.html", formulario = form_consumos_productos, usuario = user)
	else: 
		return redirect (url_for("index"))


@app.route("/lista_de_producto",methods=['GET','POST'])     
def clientes_de_productos():				
	if 'usuario' in session:
		nombre_producto = request.form['producto']
		cabezera = encabezado()
		lectura = datos()
		producto = indice_encabezado("PRODUCTO")
		lista = []
		for columnas in lectura:								
			if columnas[producto] == nombre_producto:
				lista.append(columnas)	
  
		return render_template("clientes_por_productos.html",producto = nombre_producto, lista = lista, cabezera = cabezera)
	else:
		return redirect (url_for("index"))
         
#----------------------------------------PRODUCTOS MAS VENDIDOS-------------------------------------------------

@app.route("/productos_mas_vendidos", methods=['GET', 'POST'])			
def productos_mas_vendidos():					
	if 'usuario' in session:								
		user = session['usuario']
		formulario = Cantidad_productos()
		if formulario.validate_on_submit():
			cantidad_clientes = int(formulario.cantidad.data)
			lista = productos_vendidos(cantidad_clientes)
			return render_template("lista_productos_vendidos.html", lista = lista, usuario = user , cantidad = cantidad_clientes )		
					
		return render_template("productos_mas_vendidos.html",formulario = formulario)
	
	else:
		return redirect(url_for("index"))


#----------------------------------------CLIENTES CON MAS CONSUMOS------------------------------------------------

@app.route("/clientes_gastos", methods=['GET', 'POST'])       # LISTO LOS N CLIENTES QUE MAS PLATA GASTARON
def clientes_gastos():
	if 'usuario' in session:								
		user = session['usuario']
		formulario = Cantidad_clientes()
		if formulario.validate_on_submit():
			cantidad_clientes = int(formulario.cantidad.data)
			lista = clientes_consumo(cantidad_clientes)
			return render_template("clientas_con_mas_gastos.html", lista = lista, usuario = user , cantidad = cantidad_clientes )		
					
		return render_template("productos_mas_vendidos.html",formulario = formulario)
	
	else:
		return redirect(url_for("index"))	


#----------------------------------------------NUEVA VENTA-------------------------------------------------------

@app.route('/agregar_registro', methods=['GET','POST'])   # AGREGO UN NUEVO REGISTRO
def agregar_registro():
	if 'usuario' in session:								
		user = session['usuario']
		agregar_registro = AgregarVenta()
		lista_clientes = registros_no_repetidos("CLIENTE")
		lista_productos = registros_no_repetidos("PRODUCTO")

		if request.method == 'POST':  
			cliente = agregar_registro.cliente.data
			producto = agregar_registro.producto.data
			cantidad = str(agregar_registro.cantidad.data)
			agregar = agregar_venta(cliente,producto,cantidad)
			return redirect (url_for("index"))
		else:			
			agregar_registro.cliente.choices = [(x,x) for x in lista_clientes]
			agregar_registro.producto.choices = [(y,y) for y in lista_productos]
			return render_template("agregar_venta.html", formulario = agregar_registro)

	else:
		return redirect(url_for("index"))
#----------------------------------------------------------------------------------------


@app.route('/csv', methods= ['POST','GET'])  
def download_csv():
    titulo = request.form['producto']
    csv = request.form['lista']
    lista = csv.replace("], [","\n")
    lista = lista.replace("'","")
    lista = lista.replace("[","")
    lista = lista.replace("]","")
    response = make_response(titulo+'\n'+ lista)

    ahora = datetime.now()
    nombre_archivo = 'attachment; filename=resultados_{}{}{}_{}{}{}.csv'.format(ahora.year,ahora.month,ahora.day,ahora.hour,ahora.minute,ahora.second)
    response.headers['Content-Disposition'] = nombre_archivo 
    response.mimetype='text/csv'

    return response


#-----------------------------------------------ERROR----------------------------------------------------------

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

#------------------------------------------------------------------------------------------------------------
	

if __name__ == ("__main__"):
	app.run(debug=True)

