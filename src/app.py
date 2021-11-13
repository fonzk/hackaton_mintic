import os

from flask import Flask, redirect, render_template, flash, request
from markupsafe import escape
from werkzeug.security import check_password_hash, generate_password_hash
from forms import RegistroCliente, ActualizaCliente, CambioClave

from db import accion, seleccion

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.url_map.strict_slashes = False

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
		ced = seleccion(f"SELECT id FROM Person ORDER BY rowid LIMIT 1")[0][0]
		sql = f"SELECT id, Nombres, Apellidos, Sexo, Fecha, Direccion, Ciudad FROM Person WHERE id = { ced }"
		response = seleccion(sql)
		form.cedula.data = response[0][0]
		form.nombres.data = response[0][1]
		form.apellidos.data = response[0][2]
		form.sexo.data = response[0][3]
		# form.f_nacimiento. = '01/23/1982'
		print(response[0][4])
		form.direccion.data = response[0][5]
		form.ciudad.data = response[0][6]
	if request.method == 'POST':
		try:			
			cedula = escape(request.form.get('cedula')).lower()
			nombres = escape(request.form.get('nombres')).lower()
			print(nombres)
			apellidos = escape(request.form.get('apellidos')).lower()
			sexo = escape(request.form.get('sexo')).lower()
			f_nacimiento = escape(request.form.get('f_nacimiento')).lower()
			direccion = escape(request.form.get('direccion')).lower()
			ciudad = escape(request.form.get('ciudad')).lower()
			actualizar = request.form.get('Actualizar')
			if actualizar == 'Actualizar':
				print('entra a ahcer la query')
				sql = f"UPDATE Person SET id = ?, Nombres = ?, Apellidos = ?, Sexo = ?, Fecha = ?, Direccion = ?, Ciudad = ? WHERE id = { ced }"
				response = accion(sql, (cedula, nombres, apellidos, sexo, f_nacimiento, direccion, ciudad))
				if response != 0:
					flash('INFO: Datos actualizados con exito')
				else:
					flash('ERROR: No se pudieron guardar los datos')
		except ValueError as ve:
			flash(f'La informacion ingresada no es valida o esta incompleta')
	return render_template("actualizarCliente.html", form = form)

# Cambiar Clave
@app.route("/cambioClave", methods=['GET', 'POST'])
def cambiarClave():
	form = CambioClave()
	if request.method == 'GET':
		# Obtener cedula ultimo registro (temporal) modificar por sesion
		ced = seleccion(f"SELECT id FROM Person ORDER BY rowid LIMIT 1")[0][0]
		sql = f"SELECT username FROM Person WHERE id = { ced }"
		response = seleccion(sql)
		form.usuario.data = response[0][0]
	if request.method == 'POST':
		try:			
			usuario = escape(request.form.get('usuario')).lower()
			clave = escape(request.form.get('clave')).lower()
			clave_nueva = escape(request.form.get('clave_nueva')).lower()
			confirma_clave = escape(request.form.get('confirma_clave')).lower()
			pwd = generate_password_hash(clave_nueva)
			cambiar = request.form.get('Cambiar')
			if cambiar == 'Cambiar':
				sql = f"UPDATE Person SET username = ?, contra = ? WHERE id = { ced }"
				response = accion(sql, (usuario, pwd))
				if response != 0:
					flash('INFO: Datos actualizados con exito')
				else:
					flash('ERROR: No se pudieron guardar los datos')
		except ValueError as ve:
			flash(f'La informacion ingresada no es valida o esta incompleta')
	return render_template("cambioClave.html", form = form)

if __name__ == '__main__':
	app.run()
