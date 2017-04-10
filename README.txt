-- Jordan Bottrell--

- Make sure the 'aiml' and 'aiml_data' folders are in the same directory as 'chatbot.py', which holds the main functionality of the bot. 

- My program has two cache files -- 'darksky_chatbot_cache.json' and 'google_chatbot_cache.json'. Each of these files holds the data relative to it's api. Besides the functions built in to the aiml library, the bot responds intelligently to the following:

> What's the weather like in Ann Arbor?
> Is it going to rain in Ypsilanti today?
> How hot will it get in Detroit today?
> How cold will it get in Flint today?
> Is it going to rain in East Lansing this week?
> How hot will it get in Grand Rapids this week?
> How cold will it get in Kalamazoo this week?

- There are two functions named googleCaching() and darkSkyCaching() that check if the request url has already been used, allowing for faster access to cities information that has already been accessed (caching ftw).

- The getDarkSkyInfo() function finds the latitude and longitude of the city input and returns the weather information in a json formatted string. 

- The computeProbabilityForRain() function calculates the probability that it will rain based on the next 7 days and returns a different response based on the probability it will rain.

- The __main__() function holds the main flow loop of the program, it accepts user input while the input isn't 'exit', and responds based on the aiml responses. 
