import json
import iso8601
import re

def parse_humidity(humidity):
    return str(humidity) + '%'

"""
convert from Kelvin to Celsius
"""
def parse_temperature(temp):
    celsius = temp - 273.15
    return str(round(celsius,1)) + 'C'

def parse_pressure(pressure):
    return str(pressure) + ' hPa'

def parse_weather_data(response):
    result = {}
    temperature = response['main']['temp']
    parsed_temp = parse_temperature(temperature)
    result['temperature'] = parsed_temp

    pressure = response['main']['pressure']
    parsed_pressure = parse_pressure(pressure)
    result['pressure'] = parsed_pressure

    humidity = response['main']['humidity']
    parsed_humidity = parse_humidity(humidity)
    result['humidity'] = parsed_humidity

    clouds = response['weather'][0]['description']
    result['clouds'] = clouds
    return json.dumps(result)


def parse_weather_by_timing(response, time):
    timings = response['list']
    for t in timings:
        current_time = t['dt']
        if(is_valid_date(time, current_time)):
            return parse_weather_data(t)
    return None                    

"""
takes t1 in ISO8601 format and t2 as unix timestamp
return true if the the difference within 3 hours from the query timestamp
return false for invalid timestamp
"""
def is_valid_date(t1,t2):
    try:
        t1_unix_timestamp = parse_iso8601_to_timestamp(t1)
        diff = time_diff(t1_unix_timestamp,t2)
        has_nearest_diff = (diff < 6) & (diff >= 3) 
        if(has_nearest_diff):
            return True
    except:
        return False        
    return False

def parse_iso8601_to_timestamp(t):
    parsed_t = iso8601.parse_date(t)
    return parsed_t.strftime('%s')

"""
takes two times in unix timestamps, returns the differnece in hours
"""
def time_diff(t1,t2):
    t = int(t1) - int(t2)
    hours = t / (3600)
    return int(hours)
