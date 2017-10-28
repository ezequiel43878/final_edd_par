from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from forms import LoginForm

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'key_secret'

@app.route("/")
def index():
	return render_template("index.html") 

@app.route("/login")
def login():
	login = LoginForm()
	return render_template("login.html", formulario = login)

if __name__ == ("__main__"):
	app.run(debug=True)
