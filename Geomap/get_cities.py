import urllib2
import ast
import json
import cPickle as pickle
import os
from geopy.geocoders import Nominatim
import sys
import argparse
import urllib2


def get_cities(geopy=True):
    if not os.path.exists('save.p'):
        with open('../ALL_GEMEENTES.txt', 'r') as infile:
            read_data = infile.read()
            read_data = ast.literal_eval(read_data)
        infile.close()

        pickle.dump(read_data, open('save.p', 'wb'))

    cities = pickle.load(open('save.p', 'rb'))

    if geopy:
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
                                print "location: ", city
                finally:
                    pickle.dump(cities, open('save.p', 'wb'))
                    outfile.write('}')
                    outfile.close()
    else:
        with open('data.json', 'a') as outfile:
            outfile.write('{')
            print len(cities)

            while len(cities) > 0:
                try:
                    for city in cities:
                        print city
                        if len(city) > 2:
                            new_city = city.replace(' ', '+')
                            response = urllib2.urlopen(str('http://maps.googleapis.com/maps/api/geocode/json?address=' +
                                                           new_city + ',+netherlands&sensor=false'))
                            read_data = response.read()
                            try:
                                read_data = ast.literal_eval(read_data)
                            except:
                                continue

                            if len(read_data['results']) > 0:
                                lat = read_data['results'][0]['geometry']['location']['lat']
                                lng = read_data['results'][0]['geometry']['location']['lng']

                                outfile.write("\"" + city + '\":[' + str(lat) + ',' + str(lng) + '],')
                                cities.remove(city)
                            else:
                                print "location: ", city
                finally:
                    pickle.dump(cities, open('save.p', 'wb'))
                    outfile.write('}')
                    outfile.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--geopy', dest='geopy', type=int, help='pass 0 to undo geopy')
    args = parser.parse_args()

    geo = True
    if args.geopy is not None:
        geo = False

    get_cities(geopy=geo)

