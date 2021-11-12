from flask import Flask, render_template
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    return render_template("index.html")

if __name__ == '__main__':
	app.run()