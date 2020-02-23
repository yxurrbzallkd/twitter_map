# Project Description
a web application that displays a map with locations of all people a given user follows on Twitter

# Features
display a map with markers for locations of people a given user follows


# Files
## my_project.py
main file of the project: takes account as input and generates map.
uses code from www.py4e.com/code3/twitter2.py to obtain data on given user's follows

## oauth.py & twurl.py
from www.py4e.com/code3

## templates/index.html
Main page template. Containes a simple form for asking user name.

# Packages used
```bash
folium
```
```bash
geopy
```
```bash
flask
```

# Issues
can't overwrite html map with locations, app uses cached map
