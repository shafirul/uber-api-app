from uberpy import Uber
from pygeocoder import Geocoder
import working

from flask import Flask, request, session, render_template, g, redirect, url_for, flash, jsonify
from flask.ext.session import Session
import os
import jinja2
import json

SESSION_TYPE = 'filesystem'

app = Flask(__name__)
sess = Session()

@app.route("/")
def start_here():
    return render_template("index.html")

@app.route("/location")
def determine_estimate():

### Gets addresses, converts them to coordinates, saves them, requests estimates from API

	uber_prices = []

	app_start_address = request.args.get('start_address')
	app_end_address = request.args.get('end_address')

	try:
		import urllib3.contrib.pyopenssl
		urllib3.contrib.pyopenssl.inject_into_urllib3()
	except ImportError:
		pass

	if Geocoder.geocode(app_start_address).valid_address and Geocoder.geocode(app_end_address).valid_address is True:
	
		start_lat = Geocoder.geocode(app_start_address)[0].coordinates[0]
		start_long = Geocoder.geocode(app_start_address)[0].coordinates[1]
	
		end_lat = Geocoder.geocode(app_end_address)[0].coordinates[0]
		end_long = Geocoder.geocode(app_end_address)[0].coordinates[1]

		AUTH = Uber(working.client_id, working.server_token, working.secret)

		estimate = AUTH.get_price_estimate(start_lat, start_long, end_lat, end_long)

		services_and_prices = estimate['prices']

		for i in range(len(services_and_prices)):
			uber_price = {}
			uber_price['service'] = services_and_prices[i]['display_name']
			uber_price['price'] = services_and_prices[i]['estimate']
			uber_prices.append(uber_price)

		session['user_travel'] = uber_prices

		return render_template("results.html")

	else:

		message = "Something went wrong. Please make sure you entered valid addresses."

		return render_template("index.html",  message=message)

### Returns a dictionary = {'estimate': value, 'bac': value, 'dui': static value, 'message': value}

@app.route("/calculation")
def determine_bac():

### Performs BAC calculation, returns variable message determined by result of BAC

	try:

		drinks = float(request.args.get('drinks')) * .6
		weight = float(request.args.get('weight'))
		sex = request.args.get('sex')
		hours = float(request.args.get('hours'))

		if sex == "female":
			ratio = .66
		else:
			ratio = .73

		bac = float((drinks * 5.14/weight * ratio) - .015 * hours) 

		if bac >= .08:
			page = "get-uber.html"
		else:
			page = "no-uber.html"

		return render_template(page)

	except:

		message = "Something went wrong. Please make sure you entered valid inputs."

		return render_template("results.html", message=message)

@app.route('/comparison')
def response():

	user_response = request.args.get('user_response')
	user_estimate = session.get('user_travel')

	dui_cost = "$15,000"

	print user_estimate

	print 

	if user_response == "But Ubers are expensive":
		message = {'how_expensive': "Not nearly as expensive as a DUI!", 'uber': "The price of an Uber:", 'vs':"versus", 'dui': "The price of an average DUI: $15,000"}
	else:
		message = {'how_expensive': "Look at how much money you'll save!", 'uber': "The price of an Uber:", 'vs':"versus", 'dui': "The price of an average DUI: $15,000"}

	return render_template('comparison.html', message=message, user_estimate=user_estimate)

if __name__ == "__main__":

	app.secret_key = working.secret_key
	app.config['SESSION_TYPE'] = 'filesystem'

	sess.init_app(app)

	app.debug = True
	app.run(debug=True, port=8000, host="0.0.0.0")