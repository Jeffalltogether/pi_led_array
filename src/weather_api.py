#!/usr/bin/env python
'''
Weather forcast with python
By: Ayushi Rawat
'''

import requests

city = 'Irving, Texas, United States'
print(city)

url = 'https://wttr.in/{}?AT'.format(city)
res = requests.get(url)

print(res.text)

#print("23", chr(176), 'happy', sep = '')

#print(int(res.text[144:147].strip()))
#print('temperature: ', temperature, chr(176), 'F', sep='')
