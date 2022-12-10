#!/usr/bin/env python
import requests
import re

def simple_weather_as_text(city):
	'''
	%c = atmospheric as symbol
	%C = atmospheric as text
	%e = 
	%f = temperature in F
	%h = humidity in %
	%l = longitude and latitude e.g.: 32.8295183,-96.9442177
	%m = moon phase as symbol
	%M = ??numeric moon phase (https://www.locationworks.com/sunrise/moon.html)
	%p = precipitation in mm
	%P = pressure in hPa
	%u = ?
	%w = wind speed mph
	%x = ?
	
	%20 = space character
	
	'''
	# Select city and parameters to query
	url = 'https://wttr.in/{}?AT&format="%c,%f,%h,%w,%P,%p,%m"'.format(city)
	
	# submit query and parse text
	res = requests.get(url)
	w_list = res.text.split(',')
	

	curr_values_dict = {
		'atmospheric_symbol': w_list[0].strip('" '),
		'temperature': w_list[1],
		'humidity': w_list[2] + 'RH',
		'wind_speed': w_list[3],
		'pressure': w_list[4],
		'precipitation': w_list[5],
		'moon_symbol': w_list[6].strip('" ')
		}
	
	return(curr_values_dict)

def complex_weather_as_text(city):
	# query wttr.in as text only
	url = 'https://wttr.in/{}?AT'.format(city)
	
	# submit query and parse output
	res = requests.get(url)
	w_list = res.text.split('\n')
		
	# see all the text
	#for s in w_list:
	#	print(s[14:])
	
	space_chr = re.compile(r'\s+')
	
	curr_values_dict = {
		'atmospheric_text': w_list[2][14:].strip(),
		'better_temperature': w_list[3][14:].strip(),
		'better_wind_speed': re.sub(space_chr, '', w_list[4][14:]),
		'high': 'temp',
		'low': 'temp'
		}
		
	return curr_values_dict

def wttr_weather(location):
	comp_weather_dict = complex_weather_as_text(location)
	simp_weather_dict = simple_weather_as_text(location)

	# merge dictionaries using new merge `|` operator
	weather_dict = (comp_weather_dict | simp_weather_dict)
	
	return weather_dict
	

if __name__ == '__main__':
	#my_report = wttr_weather('Irving,Texas,United States')
	my_report = wttr_weather('32.8295183,-96.9442177')
	print(my_report)
	
