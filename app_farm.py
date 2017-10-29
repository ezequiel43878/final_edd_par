import csv
from flask import Flask, render_template, flash, session, redirect, url_for
from flask_bootstrap import Bootstrap
from forms import LoginForm

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'key_secret'

@app.route("/")                 #Pagina de inicio
def index():
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


@app.route("/ultimas_ventas", methods=['GET','POST'])     # pagina de ultimas_ventas en caso de sesion iniciada sino redirecciono a indexx 
def ultimas_ventas():
	if 'usuario' in session:
		user = session['usuario']		
		return render_template("ultimas_ventas.html", usuario = user )
	else:
		return redirect (url_for("index"))

@app.route("/logout")           # Destruyo la session y redirecciono a index 
def logout():
	if 'usuario' in session:
		session.pop('usuario')
	return redirect (url_for("index"))	

if __name__ == ("__main__"):
	app.run(debug=True)
