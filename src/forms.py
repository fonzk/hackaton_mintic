from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, DateField, SelectField, TextAreaField
# from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, EqualTo

class RegistroCliente(FlaskForm):    
	nombre = TextAreaField('Nombre')
	apellido = TextAreaField('Apellido')
	tipoDoc = SelectField(u'Tipo de documento', choices=[('Cedula'), ('Pasaporte'), ('Cedula de extranjeria')])
	documento = TextAreaField('Documento')
	guardar = SubmitField('Guardar')
	actuali = SubmitField('Actualizar')