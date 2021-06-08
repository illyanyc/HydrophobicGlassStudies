import pyowm

def pressure():
    owm = pyowm.OWM('21bdaf3be2d8b2337030d788aae5d434')

    # Have a pro subscription? Then use:
    # owm = pyowm.OWM(API_key='your-API-key', subscription_type='pro')

    # Search for current weather in London (Great Britain)
    observation = owm.weather_at_place('Staten Island,US')
    w = observation.get_weather()

    print(w.get_wind())

pressure()
