# Raspberry Pi Adafruit LED Array
Code for displaying things on my Raspberry Pi 3b adafruit 16x32 LED array  

# Dependencies
Hardware I'm running on:   
* (Raspberry Pi 3 Model B Board)[https://www.raspberrypi.com/products/raspberry-pi-3-model-b/]  
* (Adafruit RGB Matrix HAT + RTC for Raspberry Pi)[https://www.adafruit.com/product/2345?ref=steemhunt&gclid=CjwKCAiAp7GcBhA0EiwA9U0mti9TTRHq5IobsEF6d39YgTzA8DdIzhaXKJIFPbTcRqm9GX-0Flj_xBoCj8YQAvD_BwE]  
* (Medium 16x32 RGB LED matrix panel - 6mm Pitch)[https://www.adafruit.com/product/420?gclid=CjwKCAiAp7GcBhA0EiwA9U0mtt0btEnOEC1WdJ8tYHpE_FYioES_b7oKZh3J45_BUw-lZe8_KYRY5hoCG5sQAvD_BwE]  

The library that drives the display must be installed  
https://github.com/hzeller/rpi-rgb-led-matrix  

# Run clock
sudo python my_clock.py -r=16 --led-cols=32 -b=15
