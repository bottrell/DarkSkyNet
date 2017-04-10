#Jordan Bottrell
#1250 6284
#section 009
import aiml
import os
import requests
import json

#Should respond to the following querys
#What's the weather like in Ann Arbor?
#Is it going to rain in Ypsilanti today?
#How hot will it get in Detroit today?
#How cold will it get in Flint today?
#Is it going to rain in East Lansing this week?
#How hot will it get in Grand Rapids this week?
#How cold will it get in Kalamazoo this week?


# kernel is responsible for responding to users
kernel = aiml.Kernel()

# load every aiml file in the 'standard' directory
# use os.listdir and a for loop to do this
kernel.learn(os.path.join('aiml_data', 'std-hello.aiml'))
aiml_list = [os.path.join('aiml_data',x) for x in os.listdir('aiml_data')]
for x in aiml_list:
    kernel.learn(x)

#checking if the file 'google_chatbot_cache.json' exists, if it does, load it
GOOGLE_CACHE_FNAME = 'google_chatbot_cache.json'
DARKSKY_CACHE_FNAME = 'darksky_chatbot_cache.json'

try:
    google_cache_file = open(GOOGLE_CACHE_FNAME, 'r')
    google_cache_contents = google_cache_file.read()
    GOOGLE_CACHE_DICTION = json.loads(google_cache_contents)
    #print 'google_chatbot_cache.json exists'
    google_cache_file.close()
except:
    GOOGLE_CACHE_DICTION = {}
    #print 'google_chatbot_cache.json does not exist'

#checking if the file 'darksky_chatbot_cache.json' exists, if it does, load it
DARKSKY_CACHE_FNAME = 'darksky_chatbot_cache.json'
try:
    darksky_cache_file = open(DARKSKY_CACHE_FNAME, 'r')
    darksky_cache_contents = darksky_cache_file.read()
    DARKSKY_CACHE_DICTION = json.loads(darksky_cache_contents)
    #print 'darksky_chatbot_cache.json exists'
    darksky_cache_file.close()
except:
    DARKSKY_CACHE_DICTION = {}
    #print 'darksky_chatbot_cache.json does not exist'



    

#Jordan's actual project
    
def googleCaching(baseURL):
    req = requests.Request(method = 'GET', url = baseURL)
    prepped = req.prepare()
    fullURL = prepped.url
  
  # if we haven't seen this URL before
    if fullURL not in GOOGLE_CACHE_DICTION:
      # make the request and store the response
        response = requests.get(fullURL)
        GOOGLE_CACHE_DICTION[fullURL] = json.loads(response.text)

      # write the updated cache file
        cache_file = open(GOOGLE_CACHE_FNAME, 'w')
        cache_file.write(json.dumps(GOOGLE_CACHE_DICTION))
        cache_file.close()

  # if fullURL WAS in the cache, CACHE_DICTION[fullURL] already had a value
  # if fullRUL was NOT in the cache, we just set it in the if block above, so it's there now
    return GOOGLE_CACHE_DICTION[fullURL]


def darkSkyCaching(baseURL):
    req = requests.Request(method = 'GET', url = baseURL)
    prepped = req.prepare()
    fullURL = prepped.url
  
  # if we haven't seen this URL before
    if fullURL not in DARKSKY_CACHE_DICTION:
      # make the request and store the response
        response = requests.get(fullURL)
        DARKSKY_CACHE_DICTION[fullURL] = json.loads(response.text)

      # write the updated cache file
        cache_file = open(DARKSKY_CACHE_FNAME, 'w')
        cache_file.write(json.dumps(DARKSKY_CACHE_DICTION))
        cache_file.close()

  # if fullURL WAS in the cache, CACHE_DICTION[fullURL] already had a value
  # if fullRUL was NOT in the cache, we just set it in the if block above, so it's there now
    return DARKSKY_CACHE_DICTION[fullURL]


#Essentially the main function of the program that accesses both the google maps API and Dark Sky API and returns
#"dark_sky_object" or a json object with the cities weather information
def getDarkSkyInfo(city_name):
    google_full_url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + city_name.replace(' ', '+') + '&key=AIzaSyAcuMDv-HMLZWf9bPOfFO3VtBITAyH6X0s'
    google_cache = googleCaching(google_full_url)
    #print google_cache
    #print json.dumps(google_object, indent = 4)
    google_latitude = google_cache['results'][0]['geometry']['location']['lat']
    google_longitude = google_cache['results'][0]['geometry']['location']['lng']
    #print google_latitude
    #print google_longitude
    
    darksky_full_url = 'https://api.darksky.net/forecast/0cb3e1ca1a088491e91916b13c795c16/' + str(google_latitude) + ',' + str(google_longitude)
    darksky_cache = darkSkyCaching(darksky_full_url)
    #print json.dumps(darksky_cache, indent = 4)
    return darksky_cache

def computeProbabilityForRain(city):  
#When the user asks "is it going to rain in XXX this week", your code should compute a rain probability by taking:
#1-((probability it will NOT rain on day 1) * (probability it will NOT rain on day 2)
#* ... * (probability it will NOT rain on day 7))
    try:
        info = getDarkSkyInfo(city)
        day1 = 1 - info['daily']['data'][0]['precipProbability']
        day2 = 1 - info['daily']['data'][1]['precipProbability']
        day3 = 1 - info['daily']['data'][2]['precipProbability']
        day4 = 1 - info['daily']['data'][3]['precipProbability']
        day5 = 1 - info['daily']['data'][4]['precipProbability']
        day6 = 1 - info['daily']['data'][5]['precipProbability']
        day7 = 1 - info['daily']['data'][6]['precipProbability']
        precipResult = (1- day1 * day2 * day3 * day4 * day5 * day6 * day7)
        #If the resulting probabiility is < 0.1, respond with:
        if (precipResult) < 0.1:
            return 'It almost definitely will not rain in {}'.format(city)
        #If the resulting probability is >= 0.1 and < 0.5, your chatbot should respond with:
        if (precipResult >= .1) and (precipResult < 0.5):
            return 'It probably will not rain in {}'.format(city)
        #If the resulting probability is >= 0.5 and < 0.9, your chatbot should respond with:
        if (precipResult >= .5) and (precipResult < 0.9):
            return 'It probably will rain in {}'.format(city)
        #If the resulting probability is >= 0.9, your chatbot should respond with:
        if (precipResult >= .9):
            return 'It will almost definitely rain in {}'.format(city)
    except:
        return "Sorry, I don't know"


def whatWeatherLike(city):
    try:
        info = getDarkSkyInfo(city)
        cityName = city
        temperature = info['currently']['temperature']
        weather = info['currently']['summary']
        return 'In {}, it is {} and {}'.format(cityName, temperature, weather)
    except:
        return "Sorry, I don't know"

kernel.addPattern("What's the weather like in {city}?", whatWeatherLike)

def isGoingToRainToday(city):
    try:
        info = getDarkSkyInfo(city)
        precipProbability = info['currently']['precipProbability']
        if (precipProbability) < 0.1:
            return 'It almost definitely will not rain in {}'.format(city)
        #If the resulting probability is >= 0.1 and < 0.5, your chatbot should respond with:
        if (precipProbability >= .1) and (precipProbability < 0.5):
            return 'It probably will not rain in {}'.format(city)
        #If the resulting probability is >= 0.5 and < 0.9, your chatbot should respond with:
        if (precipProbability >= .5) and (precipProbability < 0.9):
            return 'It probably will rain in {}'.format(city)
        #If the resulting probability is >= 0.9, your chatbot should respond with:
        if (precipProbability >= .9):
            return 'It will almost definitely rain in {}'.format(city)
    except:
        return "Sorry, I don't know"

kernel.addPattern("Is it going to rain in {city} today?", isGoingToRainToday)
                  
def howHotToday(city):
    try:
        info = getDarkSkyInfo(city)
        maxTemperature = info['daily']['data'][0]['apparentTemperatureMax']
        return "In {} it will reach {}".format(city, maxTemperature)
    except:
        return "Sorry, I don't know"

kernel.addPattern("How hot will it get in {city} today?", howHotToday)

def howColdToday(city):
    try:
        info = getDarkSkyInfo(city)
        lowTemperature = info['daily']['data'][0]['apparentTemperatureMin']
        return "In {} it drop to {}".format(city, lowTemperature)
    except:
        return "Sorry, I don't know"

kernel.addPattern("How cold will it get in {city} today?", howColdToday)
                  
def isGoingToRainWeek(city):
    try:
        return computeProbabilityForRain(city)
    except:
        return "Sorry, I don't know"

kernel.addPattern("Is it going to rain in {city} this week?", isGoingToRainWeek)


def howHotWeek(city):
    try:
        info = getDarkSkyInfo(city)
        currentHigh = float(info['daily']['data'][0]['apparentTemperatureMax'])
        for day in info['daily']['data']:
            if float(day['apparentTemperatureMax']) > currentHigh:
                currentHigh = float(day['apparentTemperatureMax'])
        return "In {} it will reach a high of {} this week".format(city, currentHigh)
    except:
        return "Sorry, I don't know"

kernel.addPattern("How hot will it get in {city} this week?", howHotWeek)
                  
def howColdWeek(city):
    try: 
        info = getDarkSkyInfo(city)
        currentLow = float(info['daily']['data'][0]['apparentTemperatureMin'])
        for day in info['daily']['data']:
            if float(day['apparentTemperatureMin']) > currentLow:
                currentLow = float(day['apparentTemperatureMin'])
        return "In {} it will reach a low of {} this week".format(city, currentLow)
    except:
        return "Sorry, I don't know"
    
kernel.addPattern("How cold will it get in {city} this week?", howColdWeek)


def __main__():
    query = raw_input('> ')
    while query != 'exit':
        print('...{}\n'.format(kernel.respond(query)))
        query = raw_input('> ')
    
    return

__main__()

