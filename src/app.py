from flask import Flask, render_template, request
from db import accion, seleccion
import os, requests

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
	if request.method == "POST":
		codigoProducto = request.form["codigoProducto"]
		nombreProducto = request.form["nombreProducto"]
		numeroLote = request.form["numeroLote"]
		tipoUnidad = request.form["tipoUnidad"]
		fechaEntrada = request.form["fechaEntrada"]
		porcPromo = request.form["porcPromo"]
		precioUni = request.form["precioUni"]
		cantidad = request.form["cantidad"]

	#PENDIENTE, HAY QUE VALIDAR PRIMERO SI EXISTE O NO???

	try:
		url = "https://www.random.org/integers/?num=1&min=1&max=10000&col=1&base=10&format=plain&rnd=new"
		referencia = requests.get(url).json()

		insertLote = f"INSERT INTO Lotes (codProducto, fechaEntrada, cantidad) VALUES (?, ?, ?)"
		resultLote = accion(insertLote, (codigoProducto, fechaEntrada, cantidad))

		if resultLote != 0:
			print("guardadoR")
		else:
			print("error guardandoR")

		# categoria esta en la tabla pero se debe calcular no se lee
		insertProd = f"INSERT INTO Producto (nombre, tipo, precio, promocion,  referencia) VALUES (?, ?, ?, ?, ?)"
		resultProd = accion(insertProd, (nombreProducto, tipoUnidad, precioUni, porcPromo, referencia))

		if insertProd != 0:
			print("guardadoP")
		else:
			print("error guardandoP")
	except Exception as e:
		print(e)

	return render_template("punto2.html")

if __name__ == '__main__':
	app.run()