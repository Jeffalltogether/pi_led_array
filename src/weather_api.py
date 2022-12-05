#!/usr/bin/env python
import requests
import re

def get_weather_as_text(city):
	url = 'https://wttr.in/{}?AT'.format(city)
	res = requests.get(url)
	return(res.text)

def get_values(w_str):
	w_list = w_str.split('\n')

	# see all the text
	#for s in w_list:
	#	print(s[14:])
	space_chr = re.compile(r'\s+')
	
	curr_values_dict = {
		'atmospheric_weather': w_list[2][14:].strip(),
		'temperature': w_list[3][14:].strip(),
		'wind_speed_dir': re.sub(space_chr, '', w_list[4][14:])
		}
		
	return curr_values_dict

def wttr_weather(location):
	weather_str = get_weather_as_text(location)
	
	curr_weather_params = get_values(weather_str)
	
	return curr_weather_params
	

if __name__ == '__main__':
	my_report = wttr_weather('Irving, Texas, United States')
	print(my_report)
	
