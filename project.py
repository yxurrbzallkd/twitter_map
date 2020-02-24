from flask import Flask, request, redirect, url_for
from flask import render_template

import folium

from geopy import Nominatim
locator = Nominatim(user_agent='suidiaucbsgaiu')

import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl
import os


# Code from https://www.py4e.com/code3/twitter1.py
TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def get_friends(acct):
    '''Returns locations and names of people user follows

    !WARNING! doctest may not work because people change their follows
    >>> result = get_friends('BillGates')
    >>> lst = [('trevormundel', 'Seattle, WA'),\
    ('rogerfederer', 'Switzerland'),\
    ('Trevornoah', 'New York, NY'),\
    ('matchinafrica', 'South Africa'),\
    ('GatesMiddleEast', '')]
    >>> lst == result
    True
    '''

    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '5'})
    connection = urllib.request.urlopen(url, context=ctx)

    data = connection.read().decode()  # get data string
    js = json.loads(data)  # turn data string into a dict
    js = js['users']  # leave only the data we need
    js = [(i['screen_name'], i['location']) for i in js]  # leave only the data we need
    return js
# ##############################################################


app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')

@app.route('/generate_map', methods=['GET', 'POST'])
def generate_map():
    '''Make a folium map, save it to html template and render template'''

    os.remove("templates/my_map.html")  # an attempt to stop caching

    acc = request.form['user']
    friends_data = get_friends(acc)

    folium_map = folium.Map()
    group = folium.FeatureGroup(name="Locations")

    for name, location in friends_data:
        loc = locator.geocode(location)  # get exact address with geopy.Nominatim locator from str
        if loc is not None:
            loc = (loc.latitude, loc.longitude)  # get latitude and longitude
            marker = folium.CircleMarker(location=loc, icon=folium.Icon(), popup=name, radius=5)
            marker.add_to(group)

    folium_map.add_child(group)
    folium_map.add_child(folium.LayerControl())
    mapname = "{}.html".format(acc)
    folium_map.save("templates/"+mapname)  # Saving a map with unique name (to avoid using cached map)
    return render_template(mapname)


if __name__ == '__main__':
    app.run(debug=True)
