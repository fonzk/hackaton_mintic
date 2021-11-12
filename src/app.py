from flask import Flask, render_template
from forms import RegistroCliente
import os

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
@app.route("/registroCliente")
def registro():
	frm = RegistroCliente()
	return render_template("registroCliente.html")

if __name__ == '__main__':
	app.run()