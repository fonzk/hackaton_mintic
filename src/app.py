
from flask import Flask, render_template, request, jsonify, redirect, session, url_for, flash
from flask.helpers import flash, url_for
from markupsafe import escape
from werkzeug.utils import secure_filename
from werkzeug.wrappers import response
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms.i18n import messages_path
from formularios import FormPart, Login, RegistroCliente, ActualizaCliente, CambioClave
from db import accion, seleccion
from db import consult_action, consult_select
import os, requests, re

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.url_map.strict_slashes = False

@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
  # numItemsFromDB = 15
  # return render_template("index.html", data = numItemsFromDB)

  return render_template("index.html", prods= loadProds())

@app.route("/login")
def loginForm():
    frm = Login()
    return render_template("login.html",form=frm)

@app.route('/validarLogin',methods=["GET","POST"])
def validarLogin():
    #recuperacion de datos
	if request.method == "POST" :
		user = escape(request.form['username'].strip()).lower()
		pwd = escape(request.form['password'].strip())
		#preparamos para consultar si el usuario existe
		sql = f"SELECT * FROM Person WHERE username = '{user}'"
		#realizamos la consulta
		res = consult_select(sql)
		#si el usuario existe traemos los datos para crear la sesion
		if len(res)!=0:
			sql2 = f"SELECT * FROM Person WHERE username = '{user}'"
			res2 = consult_select(sql2)
			passw = res2[0][8]
			activo = res2[0][11]
			confirmPassword = check_password_hash(passw,pwd)
			if confirmPassword == True and activo == '1':
				#si el usuario y la password son correctos creamos la session y lo enviamos al dashboard
				session['name'] = res2[0][1]
				session['userName'] = res2[0][4]
				session['rol'] = res2[0][5]
				datos = [()]
				return render_template('admin.html',datos=res)
				# sql = "SELECT * FROM Producto"
				# res = consult_select(sql)
				# if len(res)!= 0:
				# 	return render_template('contents/home.html',datos=res)
				# else :
				# 	messageRes = "No existen productos registrados"
				# 	return render_template('admin.html',messageRes=messageRes)
			else :
				#si el usuario no existe lo redirigimos al login
				flash('Usuario o Contraseña incorrectos')
				return redirect('/login')
		else :
			#si el usuario no existe lo redirigimos al login
			flash('Usuario o Contraseña incorrectos')
			return redirect('/login')
	else :
		if 'userName' and 'rol' in session :
			sql = "SELECT * FROM Producto"
			res = consult_select(sql)
			if len(res)!= 0:
				return render_template('contents/home.html',datos=res)
			else:
				messageRes = " No existen productos registrados"
				return render_template('admin.html',messageRes=messageRes)
		else :
			return redirect(url_for('/login'))

@app.route("/user")
def user():
    if 'userName' and 'rol' in session :
        sql =  "SELECT * FROM Person"
        res = consult_select(sql)
        if len(res)!=0 :
            frm = FormPart()
            return render_template('usuarios.html',form=frm, data=res)
    else :
        res = [()]
        frm = FormPart()
        return render_template('usuarios.html',form=frm, data=res)
        # return redirect(url_for('loginForm'))

@app.route('/form/crear',methods=["GET"])
def formUser():
    frm = FormPart()
    return render_template('formUser.html',form=frm)
    # if 'userName' and 'name' in session :
    #     frm = FormPart()
    #     return render_template('formUser.html',form=frm)
    # else :
    #     return redirect(url_for('index'))

@app.route('/usuarios/edit/<string:id>',methods=["GET"])
def userEdit(id):
    if 'userName' and 'name' in session :
        sql = f"SELECT * FROM Person id = '{id}'"
        res = consult_select(sql)
        frm = FormPart()
        return render_template('editUser.html',form=frm,datos=res)
    else :
        return redirect(url_for('index'))

def deleteUsuarios(id):
    if 'userName' and 'name' in session :
        sql =  f"SELECT Nombres, activo FROM Person WHERE id = {id}"
        res = consult_select(sql)
        name = res[0][0]
        if res[0][1] == 'si' :
            activo = 'no'
        else :
            activo = 'si'

        sql = f"UPDATE Person SET nombres =?, activo =? WHERE id = {id} "
        res = consult_action(sql,(name,activo))
        return redirect(url_for('user'))
    else :
        return redirect(url_for('loginForm'))


@app.route('/username/',methods=["POST"])
def username():
    username = request.form['username'].lower()
    sql = f"SELECT * FROM Persona WHERE username = '{username}'"
    res = consult_select(sql)
    if len(res)==0 :
        response = 'username free'
        return response;
    else :
        response = 'username busy'
        return response;

#ruta para salir del dashboard
@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route("/admin")
def admin():
    return render_template("admin.html")
# Reinaldo test
@app.route("/api")
# START Reinaldo test
@app.route("/api", methods=["GET", "POST"])
def api():
	if request.method == "POST":
		url = "https://www.random.org/integers/?num=1&min=1&max=1000&col=1&base=10&format=plain&rnd=new"
		response = requests.get(url).json()
		print(f"response: {response}")

		fin = request.form['fin']
		fou = request.form['fou']

		print(f"data: {request.form['texto']}")
		print(f"data: {fin}")
		print(f"data: {fou}")

		try:
			ins = f"INSERT INTO fechasPrueba (fechainicial, fechaFinal) VALUES (?, ?)"
			insRes = accion(ins, (fin, fou))

			if res != 0:
				print("guardado")
			else:
				print("error guardando")
		except Exception as e:
			print(e)

		print("---------")

		queRes = '' # ('2021-11-02', '2021-11-05')
		try:
			queRes = seleccion(f"SELECT fechainicial, fechaFinal FROM fechasPrueba")

			if queRes != 0:
				print("leido")
				print(queRes)
			else:
				print("error leer")
		except Exception as e:
			print(e)

	return render_template("reinaldo.html")
# END Reinaldo test

@app.route("/producto", methods=["GET", "POST"])
def producto():

	savedLote, savedProd, toShow = False, False, False
	codigoProducto, nombreProducto, buscarQue = None, None, None

	if request.method == "POST":
		buscar = request.form.get("buscar", False)
		enviar = request.form.get("enviar", False)

		codProd = escape(request.form["codigoProducto"])
		nomProd = escape(request.form["nombreProducto"])
		if len(re.findall("\d+", codProd)) != 0:
			codigoProducto = int(codProd)
		if len(re.findall("^(?!\s*$).+", nomProd)) != 0:
			nombreProducto = nomProd.lower()
		
		if enviar and codigoProducto != None and nombreProducto != None:
			try:
				numeroLote = int(escape(request.form["numeroLote"]))
				tipoUnidad = escape(request.form["tipoUnidad"].lower())
				fechaEntrada = escape(request.form["fechaEntrada"].lower())
				porcPromo = int(escape(request.form["porcPromo"]))
				precioUni = int(escape(request.form["precioUni"]))
				cantidad = int(escape(request.form["cantidad"]))

				f = request.files['file']
      			# f.save(secure_filename(f.filename))

				url = "https://www.random.org/integers/?num=1&min=1&max=10000&col=1&base=10&format=plain&rnd=new"
				referencia = requests.get(url).json()

				insertLote = f"INSERT INTO Lotes (codProducto, fechaEntrada, cantidad) VALUES (?, ?, ?)"
				resultLote = accion(insertLote, (codigoProducto, fechaEntrada, cantidad))

				if resultLote != 0:
					savedLote = True

				# categoria esta en la tabla pero se debe calcular no se lee
				insertProd = f"INSERT INTO Producto (nombre, tipo, precio, promocion,  referencia) VALUES (?, ?, ?, ?, ?)"
				resultProd = accion(insertProd, (nombreProducto, tipoUnidad, precioUni, porcPromo, referencia))

				if insertProd != 0:
					savedProd = True

				if savedLote and savedProd:
					flash(f"Datos guardados con exito")
				else:
					flash(f"Error al guardar los datos")

			except ValueError as ve:
				flash(f'La informacion ingresada no es valida o esta incompleta')

		elif buscar and codigoProducto != None:
			try:
				buscarQue = seleccion(f"SELECT * FROM Producto WHERE referencia = '{codigoProducto}'")

				if len(buscarQue) > 0:
					#PENDIENTE, aplicar update
					toShow = True
					print('SI existe')
				else:
					toShow = False
					print('NO existe')

			except Exception as e:
				print(e)

		elif buscar and nombreProducto != None:
			try:
				'''
				sql = f"SELECT usuarios.nombre, usuarios.apellido, comentarios.comentario, comentarios.calificacion, habitaciones.numero_habitacion, habitaciones.caracteristicas FROM comentarios INNER JOIN usuarios ON comentarios.identificacion = usuarios.numero_documento INNER JOIN habitaciones ON habitaciones.numero_habitacion = comentarios.habitacion"
				'''
				buscarQue = seleccion(f"SELECT * FROM Producto WHERE nombre LIKE '%{nombreProducto}%'")
				if len(buscarQue) > 0:
					toShow = True
					print(f'matchQue {buscarQue}')
				else:
					toShow = False
					print(f'matchQue ELSE')
			except Exception as e:
				print(e)
				
		else:
			flash(f'La informacion ingresada no es valida o esta incompleta')

	context = {
		'toShow' : toShow,
		'data' : buscarQue
	}

	return render_template("punto2.html", **context)




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

#function load prods :AlfonsoD
def loadProds():
	
	try:

		products = seleccion(f"SELECT * FROM Producto")
		if len(products) > 0:
			print(f'Products: {products}')
		else:
			print(f'products ELSE')
	except Exception as e:
				print(e)
	return products

if __name__ == '__main__':
	app.run(debug=True)

