from flask import Flask, render_template, request, flash
from db import accion, seleccion
import os, requests, re

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
  # numItemsFromDB = 15
  # return render_template("index.html", data = numItemsFromDB)
  return render_template("index.html")

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
	savedLote = False
	savedProd = False
	toShow = False
	buscarQue = None

	if request.method == "POST":
		buscar = request.form.get("buscar", False)
		enviar = request.form.get("enviar", False)

		codProd = request.form["codigoProducto"]
		nomProd = request.form["nombreProducto"]
		if len(re.findall("\d+", codProd)) != 0:
			codigoProducto = int(request.form["codProd"])
			print('codigoProducto')
		else if len(re.findall("^(?!\s*$).+", nomProd)) != 0:
			nombreProducto = request.form["nomProd"].lower()
			print('nombreProducto')
		
		if enviar:
			try:
				numeroLote = int(request.form["numeroLote"])
				tipoUnidad = request.form["tipoUnidad"].lower()
				fechaEntrada = request.form["fechaEntrada"].lower()
				porcPromo = int(request.form["porcPromo"])
				precioUni = int(request.form["precioUni"])
				cantidad = int(request.form["cantidad"])
			except ValueError as ve:
				flash(f'La informacion ingresada no es valida o esta incompleta')
			
			codigoProducto
			nombreProducto
			numeroLote
			tipoUnidad
			fechaEntrada
			porcPromo
			precioUni
			cantidad

		try:
			url = "https://www.random.org/integers/?num=1&min=1&max=10000&col=1&base=10&format=plain&rnd=new"
			referencia = requests.get(url).json()

			if buscar:
				buscarQue = seleccion(f"SELECT * FROM Producto WHERE referencia = '{codigoProducto}'")

				if len(buscarQue) > 0:
					#PENDIENTE, aplicar update
					toShow = True
				else:
					toShow = False
					print('NO existe')

				if len(nombreProducto) > 0:
					'''
					sql = f"SELECT usuarios.nombre, usuarios.apellido, comentarios.comentario, comentarios.calificacion, habitaciones.numero_habitacion, habitaciones.caracteristicas FROM comentarios INNER JOIN usuarios ON comentarios.identificacion = usuarios.numero_documento INNER JOIN habitaciones ON habitaciones.numero_habitacion = comentarios.habitacion"
					'''
					matchQue = seleccion(f"SELECT * FROM Producto WHERE nombre LIKE '%{nombreProducto}%'")
					if len(matchQue) > 0:
						print(f'matchQue {matchQue}')
					else:
						print(f'matchQue ELSE')
			
			elif enviar:
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

		except Exception as e:
			print(e)

	context = {
		'toShow' : toShow,
		'data' : buscarQue
	}

	return render_template("punto2.html", **context)

if __name__ == '__main__':
	app.run()