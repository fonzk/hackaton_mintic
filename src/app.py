from flask import Flask, render_template
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

if __name__ == '__main__':
	app.run()