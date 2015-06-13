from uberpy import Uber
from pygeocoder import Geocoder
import working

from flask import Flask, request, session, render_template, g, redirect, url_for, flash, jsonify
import os
import jinja2
import random
import json

app = Flask(__name__)

@app.route("/")
def start_here():
    return render_template("index.html")

@app.route("/results")
def determine_estimate():

	uber_prices = []
	uber_price = {}
	i = 0

### Gets addresses, converts them to coordinates, saves them, requests estimates from API

	try:
		import urllib3.contrib.pyopenssl
		urllib3.contrib.pyopenssl.inject_into_urllib3()
	except ImportError:
		pass

	start_lat = Geocoder.geocode(request.args.get("start_address"))[0].coordinates[0]
	start_long = Geocoder.geocode(request.args.get("start_address"))[0].coordinates[1]
	end_lat = Geocoder.geocode(request.args.get("end_address"))[0].coordinates[0]
	end_long = Geocoder.geocode(request.args.get("end_address"))[0].coordinates[1]

	AUTH = Uber(working.client_id, working.server_token, working.secret)

	estimate = AUTH.get_price_estimate(start_lat, start_long, end_lat, end_long)

	services_and_prices = estimate['prices']

	print services_and_prices

	# for item in services_and_prices:
	# 	print item

	# for item in services_and_prices:
	# 	uber_price['service'] = item['display_name']
	# 	uber_price['price'] = item['estimate']
	# 	uber_prices.append(uber_price)


	for i in range(len(services_and_prices)):
		print i
		uber_price['service'] = services_and_prices[i]['display_name']
		uber_price['price'] = services_and_prices[i]['estimate']
		uber_prices.append(uber_price)


	print uber_prices

	# uber_prices.append(uber_price)

	# print uber_prices 

	# print json.dumps(estimate, sort_keys=True, indent=4, separators=(',', ': '))

	return render_template("results.html")

### Performs BAC calculation, returns variable message determined by result of BAC


### Returns a dictionary = {'estimate': value, 'bac': value, 'dui': static value, 'message': value}

@app.route("/calculation")
def determine_bac():

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

	print bac

	return render_template(page)

@app.route('/comparison')
def response():

	dui_cost = "$15,000"
	user_response = request.args.get('user_response')

	print user_response

	print estimate

	if user_response == "But Ubers are expensive":
		message = {'how_expensive': "Not nearly as expensive as a DUI", 'uber': "The price of an Uber:", 'vs':"versus", 'dui': "The price of an average DUI: $15,000"}
	else:
		message = {'how_expensive': "Look at how much money you'll save!", 'uber': "The price of an Uber:", 'vs':"versus", 'dui': "The price of an average DUI: $15,000"}

	return render_template('comparison.html', message=message)

if __name__ == "__main__":
    app.run(debug=True, port=8000, host="0.0.0.0")
