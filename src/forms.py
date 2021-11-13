from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, DateField, SelectField, TextAreaField, StringField
from wtforms import validators
from wtforms.validators import InputRequired, EqualTo, DataRequired

class RegistroCliente(FlaskForm):    
	cedula = StringField('Cedula', validators=[DataRequired()])
	nombre = StringField('Nombre y Apellido', validators=[DataRequired()])
	sexo = StringField('Sexo', validators=[DataRequired()])
	f_nacimiento = DateField('Fecha de Nacimiento', validators=[DataRequired()])
	direccion = StringField('Direccion', validators=[DataRequired()])
	ciudad = StringField('Ciudad', validators=[DataRequired()])
	usuario = StringField('Usuario', validators=[DataRequired()])
	clave = PasswordField('Clave', validators=[DataRequired()])
	registrar = SubmitField('Registrar')