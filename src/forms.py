from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, DateField, SelectField, TextAreaField, StringField
from wtforms.validators import InputRequired, EqualTo, DataRequired

class RegistroCliente(FlaskForm):    
	cedula = StringField('Cedula*', validators=[DataRequired()])
	nombres = StringField('Nombres')
	apellidos = StringField('Apellidos')
	sexo = SelectField(u'Sexo', choices=[('Masculino'), ('Femenino'), ('NS / NR')], option_widget=None)
	f_nacimiento = DateField('Fecha de Nacimiento', format='%d/%m/%Y')
	direccion = StringField('Direccion')
	ciudad = StringField('Ciudad')
	usuario = StringField('Usuario*', validators=[DataRequired()])
	clave = PasswordField('Clave*', validators=[DataRequired()])
	registrar = SubmitField('Registrar')

class ActualizaCliente(FlaskForm):    
	cedula = StringField('Cedula*', validators=[DataRequired()])
	nombres = StringField('Nombres')
	apellidos = StringField('Apellidos')
	sexo = SelectField(u'Sexo', choices=[('Masculino'), ('Femenino'), ('NS / NR')], option_widget=None)
	f_nacimiento = DateField('Fecha de Nacimiento')
	direccion = StringField('Direccion')
	ciudad = StringField('Ciudad')
	actualizar = SubmitField('Actualizar')

class CambioClave(FlaskForm):
	usuario = StringField('Usuario*', validators=[DataRequired()])
	clave = PasswordField('Clave actual*', validators=[DataRequired()])
	clave_nueva = PasswordField('Clave nueva*', validators=[DataRequired()])
	clave_confirma = PasswordField('Confirma clave*', validators=[DataRequired()])
	cambiar = SubmitField('Cambiar Clave')