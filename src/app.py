from flask import Flask, render_template, request
import os, requests

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def hello_world():
    return render_template("construccion.html")

# Reinaldo test
@app.route("/api", methods=["GET", "POST"])
def api():
	if request.method == "POST":
		print("test")
		url = "https://www.random.org/integers/?num=1&min=1&max=1000&col=1&base=10&format=plain&rnd=new"
		response = requests.get(url).json()
		print(response)

	return render_template("reinaldo.html")
# Reinaldo test

if __name__ == '__main__':
	app.run()