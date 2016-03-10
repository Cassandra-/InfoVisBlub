import urllib2
import ast
import json
import cPickle as pickle
import os
from geopy.geocoders import Nominatim
import sys

if not os.path.exists('save.p'):
    with open('../ALL_GEMEENTES.txt', 'r') as infile:
        read_data = infile.read()
        read_data = ast.literal_eval(read_data)
    infile.close()

    pickle.dump(read_data, open('save.p', 'wb'))

cities = pickle.load(open('save.p', 'rb'))

geolocator = Nominatim()

with open('data.json', 'a') as outfile:
    outfile.write('{')
    print len(cities)

    while len(cities) > 0:
        try:
            for city in cities:
                if len(city) > 2:
                    location = geolocator.geocode(str(city + ', Netherlands'))

                    if location is not None:
                        lat = location.latitude
                        lng = location.longitude
                        data = {city: [lat, lng]}

                        outfile.write("\"" + city + '\":[' + str(lat) + ',' + str(lng) + '],')
                        cities.remove(city)
                    else:
                        print "location: ", location# city
        finally:
            pickle.dump(cities, open('save.p', 'wb'))
            outfile.write('}')
            outfile.close()
