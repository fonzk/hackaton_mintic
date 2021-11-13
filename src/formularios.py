from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, validators, SubmitField, SelectField, RadioField, FileField, FloatField, TextAreaField
from markupsafe import Markup
from datetime import date
from wtforms.validators import InputRequired , Regexp 
from wtforms.fields.html5 import EmailField,DateField
from flask_wtf.file import FileField, FileAllowed, FileRequired

class Login(FlaskForm):
    username_value = Markup('<span class="text-light"><i class="fas fa-user-tie p-2"></i>Usuario</span>')
    username = TextField(username_value,validators = [InputRequired(message='Campo obligatorio'),validators.Regexp('\w+', flags=0, message='caracteres no permitidos')])
    password_value = Markup('<span class="text-light"><i class="fas fa-key p-2"></i>Contraseña</span>')

    password = PasswordField(password_value, validators = [InputRequired(message='Campo obligatorio')])

    ingresar = SubmitField('Ingresar')

class FormPart(FlaskForm):
    date = DateField('Fecha',default=date.today)
    nombres = TextField('Nombres',validators = [InputRequired(message='Campo obligatorio'),validators.Regexp('/^[A-Za-z0-9\s]+$/g', flags=0, message='caracteres no permitidos')])
    apellidos = TextField('Apellidos',validators = [InputRequired(message='Campo obligatorio'),validators.Regexp('/^[A-Za-z0-9\s]+$/g', flags=0, message='caracteres no permitidos')])
    ciudad = TextField('Ciudad',validators = [InputRequired(message='Campo obligatorio'),validators.Regexp('/^[A-Za-z0-9\s]+$/g', flags=0, message='caracteres no permitidos')])
    cargo = TextField('Cargo',validators = [InputRequired(message='Campo obligatorio'),validators.Regexp('/^[A-Za-z0-9\s]+$/g', flags=0, message='caracteres no permitidos')])
    tipo_documento = RadioField('Sexo', choices=[('Femenino','femenino'),('Masculino','masculino'),('No Especifica','No Especifica')],default='Masculino')
    numero_documento = TextField('No Documento',validators = [InputRequired(message='Campo obligatorio'),validators.Regexp('/^[A-Za-z0-9\s]+$/g', flags=0, message='caracteres no permitidos')])
    email = EmailField('Email',validators = [InputRequired(message='Campo obligatorio'),validators.Regexp("^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$", flags=0, message='correo no valido')])
    celular = TextField('Celular',validators = [InputRequired(message='Campo obligatorio'),validators.Regexp('^(\d{10})$', flags=0, message='caracteres no permitidos')])
    direccion = TextField('Dirección',validators = [InputRequired(message='Campo obligatorio')],default='ingrese la dirección')
    username = TextField('Nombre de Usuario',validators = [InputRequired(message='Campo obligatorio'),validators.Regexp('\w+', flags=0, message='caracteres no permitidos')])
    password = PasswordField('Contraseña', validators = [InputRequired(message='Campo obligatorio'),validators.Regexp('^(?=\w*\d)(?=\w*[A-Z])(?=\w*[a-z])\S{8,16}$', flags=0, message='caracteres no permitidos')])
    confirm_password = PasswordField('Confirmar Contraseña', validators = [InputRequired(message='Campo obligatorio'),validators.Regexp('^(?=\w*\d)(?=\w*[A-Z])(?=\w*[a-z])\S{8,16}$', flags=0, message='caracteres no permitidos')])
    roles = SelectField('Asignar Rol', choices=[(1,'Super Administrador'), (2,'Administrador'),(3,'Usuario Final') ],default=3)
    autorizacion = RadioField('Autorizacion de Datos', choices=[('si','Autorizo el manejo y almacenamiento de datos personales')],default='si')
    crear = SubmitField('Crear Usuario')
    actualizar = SubmitField('Actualizar Usuario')

    #proveedor
    nombresProveedor = TextField('Nombre Proveedor',validators = [InputRequired(message='Campo obligatorio'),validators.Regexp('/^[A-Za-z0-9\s]+$/g', flags=0, message='caracteres no permitidos')])
    logo = FileField('Logo Proveedor', validators=[FileAllowed(['jpg', 'png'])])
    actualizarProveedor = SubmitField('Actualizar Proveedor')
    #producto
    nombresProducto = TextField('Nombre Producto',validators = [InputRequired(message='Campo obligatorio'),validators.Regexp('/^[A-Za-z0-9\s]+$/g', flags=0, message='caracteres no permitidos')])
    cantidadMinima = FloatField('Cantidad Mínima del producto',validators = [InputRequired(message='Campo obligatorio')])
    cantidadDisponible = FloatField('Cantidad Disponible del producto',validators = [InputRequired(message='Campo obligatorio')])
    descripcion = TextAreaField('Descripción del Producto')
    img1 = FileField('Primera imagen del producto', validators=[FileAllowed(['jpg', 'png'])])
    img2 = FileField('Segunda imagen del producto', validators=[FileAllowed(['jpg', 'png'])])
    img3 = FileField('Tercera imagen del producto', validators=[FileAllowed(['jpg', 'png'])])
    actualizarProducto = SubmitField('Actualizar Producto')