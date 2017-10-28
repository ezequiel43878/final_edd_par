from flask_wtf import FlaskForm
from wtforms import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required



class LoginForm(FlaskForm):
	usuario = StringField('Usuario:', validators=[Required()])
	password = PasswordField('Contraseña:',validators=[Required()])
	enviar = SubmitField('Enviar')