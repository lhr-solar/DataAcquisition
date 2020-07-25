from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import json
import geocoder
import requests
import geopy
from pprint import pprint
from math import radians, sin, cos, acos
from collections import OrderedDict
from geopy.distance import geodesic
import numpy as np


#function returns data in the form of a json objects with weather, slope and road data
#listfile2.txt contains elevation data per function call
#listfile.txt contains latitude longitude data per function call in the order lat, long
#if you get this error: /usr/local/lib/python3.8/site-packages/geopy/point.py:471:
#UserWarning: Latitude normalization has been prohibited in the newer versions of geopy,
# because the normalized value happened to be on a different pole, which is probably not what was meant.
# If you pass coordinates as positional args,
# please make sure that the order is (latitude, longitude) or (y, x) in Cartesian terms.
# To resolve, clear all positional and elevation data except initial data and set cursor right after initial values
def json_weather_data():
    lstcoord =[]
    elevationlst=[] #defines list data and reads the data into list from text files
    with open('listfile.txt', 'r') as filehandle:
        for line in filehandle:
            # remove linebreak which is the last character of the string
            currentPlace = line[:-1]
            # add item to the list
            lstcoord.append(currentPlace)
    with open('listfile2.txt', 'r') as filehandle:
        for line in filehandle:
            # remove linebreak which is the last character of the string
            currentPlace = line[:-1]
            # add item to the list
            elevationlst.append(currentPlace)
    #get position data and add to list of data
    myloc = geocoder.ip('me')
    lati = myloc.lat
    longi = myloc.lng
    lstcoord.append(lati)
    lstcoord.append(longi)
    #keep bounds of latitude and longitude within [-90, 90] and [-180, 180]
    longibot = longi - 2
    latibot = lati - 2
    while (longibot < -180):
        longibot = longi + 4
    while (latibot < -90):
        latibot = lati + 4
    #set up APIs for weather, elevation, and traffic
    API_key = "770fdaded25c020b900de22ab272b41a"
    base_url = "http://api.openweathermap.org/data/2.5/weather?" #roughly only 45 requests per min for location api #1500 requests per day for the traffic api
    f_url = base_url + "appid=" + API_key + "&lat=" + str(lati) + "&lon=" + str(longi)
    weather_data = requests.get(f_url).json()
    elevation = "https://elevation-api.io/api/elevation?points=(" + str(lati) + "," + str(longi) + ")&key=Kde9kv2R5fWy8u9erNj7pRpf9ErD2d"
    elev_data = requests.get(elevation).json()
    l = elev_data['elevations'][0]['elevation']
    elevationlst.append(l)
    nav_url = "http://www.mapquestapi.com/traffic/v2/incidents" + "?key=" + "D0WyZccmV3Zg6KyQh4wlD8TB5fCiReHw" + "&boundingBox=" + str(latibot) + "," + str(longibot) + "," + str(lati) + "," + str(longi) + "&filters=construction,incidents,event,congestion"
    nav_data = requests.get(nav_url).json()
    #temperature data is returned in Kelvin so converted to Fahrenheit
    max_temp = weather_data['main']['temp_max']
    max_temp = ((max_temp - 273) * 1.8) + 32
    min_temp = weather_data['main']['temp_min']
    min_temp = ((min_temp - 273) * 1.8) + 32
    temp = weather_data['main']['temp']
    temp = ((min_temp - 273) * 1.8) + 32
    x = 0
    coord = {}
    #iterate through the dictionary response of the traffic API
    for y in nav_data['incidents']:
        loc = nav_data['incidents'][x]['fullDesc']
        val1 = nav_data['incidents'][x]['parameterizedDescription']
        rname = val1['roadName']
        if "crossRoad1" in val1:
            r1 = val1['crossRoad1'] #select intersection road
        if "crossRoad2" in val1:
            r2 = val1['crossRoad2'] #select intersection road
        gpslat = nav_data['incidents'][x]['lat']
        gpslng = nav_data['incidents'][x]['lng']
        #get lat and long for data values and convert them to find radians
        rlati = radians(lati)
        rgpslat = radians(gpslat)
        rlongi = radians(longi)
        rgpslng = radians(gpslng)
        #this formula helps us convert lat and long to dist in miles
        dist = 6371.01 * acos(sin(rlati)*sin(rgpslat) + cos(rlati)*cos(rgpslat)*cos(rlongi - rgpslng))
        lst = []
        #append data values to a list inside dictionary to group them together where the distance is the key
        lst.append(loc)
        lst.append(r1)
        lst.append(r2)
        lst.append(rname)
        lst.append(gpslat)
        lst.append(gpslng)
        if (dist <= 25): #sort by distance being within 25 miles of the vehicle
            coord.update({dist: lst})
        x = x + 1
    coord1 = OrderedDict(sorted(coord.items())) #sort in order of closest to furthest traffic data
    #grab length of data lists
    coordlen = len(lstcoord)
    coordlen = coordlen * -1
    elevationlen = len(elevationlst)
    elevationlen = elevationlen * -1
    latix = lstcoord[-4]
    longix = lstcoord[-3]
    latiy = lstcoord[-2]
    longiy = lstcoord[-1]
    #resolves base case of two elements inside the list
    if (elevationlen != 2):
        elevx = elevationlst[-2]
    else:
        elevx = elevationlst[1]
    elevy = elevationlst[-1]
    #format for geodesic library used to get distance traveled in meters
    init = (latix, longix)
    final = (latiy, longiy)
    distx = geodesic(init, final).meters
    disty = float(elevy) - float(elevx)
    slope = 0.0
    if (distx != 0): # resolves slope base case where run is 0 in slope = rise/ run
        slope = disty / distx
    slope = slope * 100 # slope in percentage
    with open('listfile.txt', 'w') as filehandle:
        for listitem in lstcoord:
            filehandle.write('%s\n' % listitem)
    with open('listfile2.txt', 'w') as filehandle:
        for listitem in elevationlst:
            filehandle.write('%s\n' % listitem)
    #append new values in text file for next call to function
    #return json with values inside
    return json.dumps({
        "region": weather_data['name'],
        "latitude": weather_data['coord']['lat'],
        "longitude": weather_data['coord']['lon'],
        "weather": {
             "max_temp": max_temp,
             "min_temp": min_temp,
             "current_temp": temp,
             "humidity": weather_data['main']['humidity'],
             "status": weather_data['weather'][0]['description'],
             "wind speed": weather_data['wind']['speed'],
        },
        "road_cond": coord1,
        "distchange": distx,
        "elevationchange": disty,
        "slope": slope
    })


if __name__ == '__main__':
    json_weather_data()