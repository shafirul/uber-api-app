
from flask import Flask, request, session, render_template, g, redirect, url_for, flash, jsonify
import os
import jinja2
import random
import json

app = Flask(__name__)

@app.route("/")
def start_here():
    return render_template("index.html")

@app.route("/input")
def determine_bac():

	drinks = (float(request.args.get("drinks"))) * 12
	weight = float(request.args.get("weight"))
	sex = request.args.get("sex")
	hours = float(request.args.get("hours"))

	if sex == "female":
		ratio = .66
	else:
		ratio = .73

	bac = (drinks * 5.14/weight * ratio) - .015 * hours 

	return render_template("results.html", drinks=drinks, weight=weight, sex=sex, hours=hours, bac=bac)

if __name__ == "__main__":
    app.run(debug=True, port=8000, host="0.0.0.0")
