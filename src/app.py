from flask import Flask, render_template, request
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
  # numItemsFromDB = 15
  # return render_template("index.html", data = numItemsFromDB)
  return render_template("index.html")

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
		cantStandLote = request.form["cantStandLote"]

		descForm = request.form.get("descuento")
		if descForm == "on":
			descuento = True
		else:
			descuento = False

		# print(codigoProducto)
		# print(nombreProducto)
		# print(numeroLote)
		# print(tipoUnidad)
		# print(fechaEntrada)
		# print(porcPromo)
		# print(precioUni)
		# print(descuento)
		# print(cantStandLote)

	return render_template("punto2.html")

if __name__ == '__main__':
	app.run()