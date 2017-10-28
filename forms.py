from flask_wtf import FlaskForm
from wtforms import Form
from wtforms import StringField, PasswordField, SubmitField



class LoginForm(FlaskForm):
	usuario = StringField('Usuario:')
	contraseña = PasswordField('Contraseña:')
	enviar = SubmitField('Enviar')