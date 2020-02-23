from flask import Flask, request, redirect, url_for
from flask import render_template

import folium

from geopy import Nominatim
locator = Nominatim(user_agent='suidiaucbsgaiu')

import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def get_friends(acct):
    '''Returns locations and names of people user follows'''

    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '5'})
    print('Retrieving', url)
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)
    js = js['users']
    js = [(i['screen_name'], i['location']) for i in js]
    print(js)
    return js



Message = {'User account': ''}
messages=[]

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')

@app.route('/generate_map', methods=['GET', 'POST'])
def generate_map():
    '''Make a folium map, save it to html template and render template'''

    friends = get_friends(request.form['user'])

    folium_map = folium.Map()
    group = folium.FeatureGroup(name="Locations")

    for name, location in friends:
        loc = locator.geocode(location)
        if loc is not None:
            loc = (loc.latitude, loc.longitude)
            marker = folium.CircleMarker(location=loc, icon=folium.Icon(), popup=name, radius=5)
            marker.add_to(group)

    folium_map.add_child(group)
    folium_map.add_child(folium.LayerControl())
    folium_map.save("templates/my_map.html")
    return render_template('my_map.html')


if __name__ == '__main__':
    app.run(debug=True)
