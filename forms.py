from flask_wtf import FlaskForm
from wtforms import Form
from wtforms import StringField, PasswordField, SubmitField, RadioField, IntegerField, SelectField
from wtforms.validators import Required , InputRequired, Length

class LoginForm(FlaskForm):
	usuario = StringField('Usuario:', validators=[Required()])
	password = PasswordField('Contraseña:',validators=[Required()])
	enviar = SubmitField('Enviar')

class NombreCliente(FlaskForm):
	cliente = StringField('Nombre del Cliente:',validators=[Required(), Length(min=3)])
	enviar = SubmitField('Enviar')

class NombreProducto(FlaskForm):
	producto = StringField('Nombre del Producto:',validators=[Required(), Length(min=3)])
	enviar = SubmitField('Enviar')

class Cantidad_clientes(FlaskForm):
	cantidad = IntegerField('Ingrese la cantidad de clientes:',validators=[Required()])
	enviar = SubmitField('Enviar')

class Cantidad_productos(FlaskForm):
	cantidad = IntegerField('Ingrese la cantidad de productos:',validators=[Required()])
	enviar = SubmitField('Enviar')

class Registrar(FlaskForm):
	usuario = StringField('Ingrese nombre de usuario:',validators=[Required()])
	password = PasswordField('Ingrese una Contraseña:',validators=[Required()])
	reingresar_password = PasswordField('Repita la Contraseña:',validators=[Required()])
	enviar = SubmitField('Enviar')

class AgregarVenta(FlaskForm):
	cliente = SelectField('Cliente:', choices=[])
	producto = SelectField('Producto:',choices=[])
	cantidad = IntegerField('Cantidad',validators=[Required()])
	enviar = SubmitField('Enviar')
