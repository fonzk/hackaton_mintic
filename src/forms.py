from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField

class ProductoForm(FlaskForm):
	codigoProducto = TextField('Codigo del producto')
	nombreProducto = TextField('Nombre del producto')
	numeroLote = TextField('Numero de lote')
	tipoUnidad = TextField('Tipo de unidad')
	fechaEntrada = TextField('Fecha entrada')
	porcPromo = TextField('Porcentaje promocion')
	precioUni = TextField('Precio Unidad')
	cantidad = TextField('Cantidad')
	buscar = SubmitField('Buscar')
	enviar = SubmitField('Enviar')