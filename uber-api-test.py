import json
import working
from uberpy import Uber
from pygeocoder import Geocoder

# Creates a new Uber instance using tokens

AUTH = Uber(working.client_id, working.server_token, working.secret)

# print AUTH

latitude = 51.5286416
longitude = -0.1015987

uber_products = AUTH.get_products(latitude, longitude)

# Prints JSON object in a format that won't make you insane

print json.dumps(uber_products, sort_keys=True, indent=4, separators=(',', ': '))

### This is a fix for the problem that arose from the geocode lbirary, fixes SSL restrictions. See site for more details: https://urllib3.readthedocs.org/en/latest/security.html#pyopenssl

# try:
# 	import urllib3.contrib.pyopenssl
# 	urllib3.contrib.pyopenssl.inject_into_urllib3()
# except ImportError:
#     pass

###

start_lat = Geocoder.geocode("180 Townsend Street, San Francisco, CA 94107")[0].coordinates[0]
start_long = Geocoder.geocode("180 Townsend Street, San Francisco, CA 94107")[0].coordinates[1]

end_lat = Geocoder.geocode("1737 Haight St, San Francisco, CA 94117")[0].coordinates[0]
end_long = Geocoder.geocode("1737 Haight St, San Francisco, CA 94117")[0].coordinates[1]

start_lat_test = Geocoder.geocode("poop").valid_address

print start_lat_test


estimate = AUTH.get_price_estimate(start_lat, start_long, end_lat, end_long)

print json.dumps(estimate, sort_keys=True, indent=4, separators=(',', ': '))

print estimate["prices"][0]["estimate"]