from bottle import Bottle, request
from datetime import date, timedelta
import requests
import requests_toolbelt.adapters.appengine
from collections import OrderedDict

requests_toolbelt.adapters.appengine.monkeypatch()

today = date.today()
start_date = today - timedelta(days=1)
end_date = today - timedelta(days=7)
dates = [start_date - timedelta(days=x) for x in range((start_date-end_date).days + 1)]

app = Bottle()

@app.get('/')
def hello():
    return "Hello!"

@app.get('/location')
def location():
    return '''
        <form action="/location" method="post">
            latitude: <input name="latitude" type="text" />
            longitude: <input name="longitude" type="text" />
            <input value="Submit" type="submit" />
        </form>
    '''

@app.post('/location')
def do_location():
    latitude = request.forms.get('latitude')
    longitude = request.forms.get('longitude')

    weather_days = dict()
    for dt in dates:
        url = 'https://api.darksky.net/forecast/****/' + latitude + ',' + longitude + ',' + str(dt) + 'T00:00:00?exclude=currently,minutely,hourly,flags'
        r = requests.get(url)
        weather_days[str(dt)] = r.json()
    return OrderedDict(sorted(weather_days.items(), key=lambda t: t[0], reverse=True))
