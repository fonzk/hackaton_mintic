import os

from flask import Flask, redirect, render_template, flash, request
from markupsafe import escape
from werkzeug.security import check_password_hash, generate_password_hash
from forms import RegistroCliente, ActualizaCliente

from db import accion, seleccion

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def hello_world():
    return render_template("construccion.html")

# Reinaldo test
@app.route("/api")
def api():
	return render_template("reinaldo.html")
# Reinaldo test

# Registro Clientes
@app.route("/registroCliente", methods=['GET', 'POST'])
def registro():
	form = RegistroCliente()
	if request.method == 'POST':
		try:
			cedula = escape(request.form.get('cedula')).lower()
			nombres = escape(request.form.get('nombres')).lower()
			apellidos = escape(request.form.get('apellidos')).lower()
			sexo = escape(request.form.get('sexo')).lower()
			f_nacimiento = escape(request.form.get('f_nacimiento')).lower()
			direccion = escape(request.form.get('direccion')).lower()
			ciudad = escape(request.form.get('ciudad')).lower()
			usuario = escape(request.form.get('usuario')).lower()
			clave = escape(request.form.get('clave')).lower()
			registrar = request.form.get('registrar')
			if registrar == 'Registrar':
				sql = f"INSERT INTO Person (id, Nombres, Apellidos, Sexo, Fecha, Direccion, Ciudad, username, contra) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
				pwd = generate_password_hash(clave)
				response = accion(sql, (cedula, nombres, apellidos, sexo, f_nacimiento, direccion, ciudad, usuario, pwd))
				if response != 0:
					flash('INFO: Datos almacenados con exito')
					return redirect('/actualizarCliente/')
				else:
					flash('ERROR: No se pudieron guardar los datos')
		except ValueError as ve:
			flash(f'La informacion ingresada no es valida o esta incompleta')
	return render_template("registroCliente.html", form = form, titulo = 'Registro')

# Actualizar datos Clientes
@app.route("/actualizarCliente", methods=['GET', 'POST'])
def actualizar():
	form = ActualizaCliente()
	if request.method == 'GET':
		# Obtener cedula ultimo registro (temporal) modificar por sesion
		ced = seleccion(f"SELECT id FROM Person ORDER BY rowid DESC LIMIT 1")[0][0]
		sql = f"SELECT id, Nombres, Apellidos, Sexo, DATE(Fecha), Direccion, Ciudad FROM Person WHERE id = { ced }"
		response = seleccion(sql)
		form.cedula.data = response[0][0]
		form.nombres.data = response[0][1]
		form.apellidos.data = response[0][2]
		form.sexo.data = response[0][3]
		# form.f_nacimiento.data = response[0][4]
		form.direccion.data = response[0][5]
		form.ciudad.data = response[0][6]
	if request.method == 'POST':
		try:			
			cedula = escape(request.form.get('cedula')).lower()
			nombres = escape(request.form.get('nombres')).lower()
			apellidos = escape(request.form.get('apellidos')).lower()
			sexo = escape(request.form.get('sexo')).lower()
			f_nacimiento = escape(request.form.get('f_nacimiento')).lower()
			direccion = escape(request.form.get('direccion')).lower()
			ciudad = escape(request.form.get('ciudad')).lower()
			usuario = escape(request.form.get('usuario')).lower()
			clave = escape(request.form.get('clave')).lower()
			registrar = request.form.get('registrar')
			if registrar == 'Registrar':
				sql = f"UPDATE Person (id, Nombres, Apellidos, Sexo, Fecha, Direccion, Ciudad, username, contra) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
				pwd = generate_password_hash(clave)
				response = accion(sql, (cedula, nombres, apellidos, sexo, f_nacimiento, direccion, ciudad, usuario, pwd))
				if response != 0:
					flash('INFO: Datos almacenados con exito')
					# return redirect('/registro/')
				else:
					flash('ERROR: No se pudieron guardar los datos')
		except ValueError as ve:
			flash(f'La informacion ingresada no es valida o esta incompleta')
	return render_template("actualizarCliente.html", form = form)

if __name__ == '__main__':
	app.run()
