import urllib2, urllib, json
def getForecast():
    url    = 'http://api.openweathermap.org/data/2.5/forecast?q=Bandung&appid=ab09346d9a9123104405c6a84ad48c19'
    result = urllib2.urlopen(url).read()
    data   = json.loads(result)
    return data;
