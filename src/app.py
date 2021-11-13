import os

from flask import Flask, render_template, redirect

from forms import RegistroCliente

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
	if form.validate_on_submit():
    	# return redirect('/api')
		print('ok')
	return render_template("registroCliente.html", form = form)

if __name__ == '__main__':
	app.run()
