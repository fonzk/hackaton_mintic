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

	return render_template("punto2.html")

if __name__ == '__main__':
	app.run()