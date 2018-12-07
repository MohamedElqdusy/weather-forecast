from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

import json
import requests 
from .parse import parse_weather_data,parse_weather_by_timing
from .services import get_weather, get_weather_time

def ping(request):
    response_data = {}
    response_data['name'] = 'weatherservice'
    response_data['status'] = 'ok'
    response_data['version'] = '1.0.0'
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def forecast_by_city(request, city):
    time = request.GET.get('at')
    if((time != None)):
        return forcast_by_time(request,city,time)
    r = get_weather(city)
    if (r.status_code == 404):
        return country_not_found(city)
        
    response = r.json()
    result = parse_weather_data(response)
    return HttpResponse(result, content_type="application/json")

def forcast_by_time(request,city,time):
    response = get_weather_time(city).json()
    result = parse_weather_by_timing(response, time)
    if( result == None):
        return invalid_date_error()
    return HttpResponse(result, content_type="application/json")


def country_not_found(city):
    error = "Cannot find country %s" % city
    return error_page(error,"country_not_found",404)

def internal_server_error():
    return error_page("Something went wrong","internal_server_error",500)


def invalid_date_error():
    return error_page("Date is in the past","invalid date",400)

def error_page(error,error_code,status_code):
    result = {}
    result['error'] = error
    result['error_code'] = error_code
    content = json.dumps(result)
    return HttpResponse(content,status=status_code, content_type="application/json")