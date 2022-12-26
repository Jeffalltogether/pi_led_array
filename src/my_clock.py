#!/usr/bin/env python
import sys
import math
import time
import re
from matplotlib import cm
from weather_api import wttr_weather 
from animations import GraphicsTest
sys.path.append('/home/pi/display16x32/rpi-rgb-led-matrix/bindings/python/samples/')

from samplebase import SampleBase
from rgbmatrix import graphics




class RunText(GraphicsTest, SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        
            
    def download_weather(self, location='Irving, Texas, United States', curr_wthr_dict=None, curr_color_dict=None):
        try:
            wthr_as_dict = wttr_weather(location)
        except:
            # typically a `requests.exceptions.ConnectionError` will occur
            if not curr_wthr_dict:
                # if it fails the first time, we generate an empty dict
                wthr_as_dict = {'atmospheric_text': '', 'better_temperature': '',
                                'humidity': '', 'better_wind_speed': ''}
                                
                color_dict = {'temp_color': [255,255,255], 'humid_color': [255,255,255], 'wind_color': [255,255,255]}
                
                return wthr_as_dict, color_dict
            else:
                # if it fails, but the variables curr_[...] are not None, we return the curr_[...] variables
                return curr_wthr_dict, curr_color_dict
                
                
        # get color values:
        temp_as_int = int(re.findall(r'\d+',wthr_as_dict['better_temperature'])[0])
        humid_as_int = int(re.findall(r'\d+',wthr_as_dict['humidity'])[0])
        wind_as_int = int(re.findall(r'\d+',wthr_as_dict['better_wind_speed'])[0])
        # print('as_int:{}, {}, {}'.format(temp_as_int, humid_as_int, wind_as_int))
        
        color_dict = {'temp_color': self.get_rgb_from_colormap(temp_as_int,15,110,'temp'),
                      'humid_color': self.get_rgb_from_colormap(humid_as_int,0,100,'humid'),
                      'wind_color': self.get_rgb_from_colormap(wind_as_int,-10,25,'wind')}
        #print(color_dict)
        
        return wthr_as_dict, color_dict
        
    def get_rgb_from_colormap(self, scalar, minimum, maximum, colormap='temp'):
        if scalar <= minimum: 
            value = minimum
        elif scalar >= maximum:
            value = maximum
        else:
            value = (scalar-minimum) * (1/(maximum-minimum))
        #print('scalar {}, minimum {}, maximum {}, value {}'.format(scalar, minimum, maximum, value))
            
        if colormap == 'temp':
            bgra = cm.rainbow(value) # values returned are RGBa ordered where a is the alpha (transparency)
            return [int(255*v) for v in bgra[:-1]]
            
        if colormap == 'humid':
            bgra = cm.Spectral(value)
            return [int(255*v) for v in bgra[:-1]]            
            
        if colormap == 'wind':
            bgra = cm.rainbow(value)
            return [int(255*v) for v in bgra[:-1]]             

            
    def run(self):
        ### define some colors
        watermellon_color_list = [[243,85,136],[255,187,180],[113,169,90],[0,121,68]]
        
        ### run a graphic
        self.random_bars(watermellon_color_list, delay = 5,  num_iterations = 1)
        
        ### for clock
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        
        clock_font = graphics.Font()
        clock_font.LoadFont("/home/pi/display16x32/rpi-rgb-led-matrix/fonts/5x7.bdf")
        
        am_pm_font = graphics.Font()
        am_pm_font.LoadFont("/home/pi/display16x32/rpi-rgb-led-matrix/fonts/4x6.bdf")
        
        date_wthr_font = graphics.Font()
        date_wthr_font.LoadFont("/home/pi/display16x32/rpi-rgb-led-matrix/fonts/6x9.bdf")
        
        date_color = graphics.Color(45, 255, 45)
        time_color = graphics.Color(0, 145, 145)
        
        # get date
        day_mo_date = [i for i in time.ctime()[0:10].split()]
        
        # download weather
        wthr_dict, color_dict = self.download_weather()
        
        # generate text 
        date_atmosphere = day_mo_date[0] + ' ' + \
                            day_mo_date[1] + ', ' + \
                            day_mo_date[2] + ' ' + \
                            wthr_dict['atmospheric_text'] + ' '
                            
        temperature_txt = wthr_dict['better_temperature'] + ' '
        rel_humidity = wthr_dict['humidity'] + ' '
        wind_speed = wthr_dict['better_wind_speed']
            
        # set minute counter
        prev_min = -1
        
        pos = offscreen_canvas.width
        while True:
            
            ### get time
            time_out = time.strftime("%I:%M%p")
            
            ### update date, weather, and text
            if (int(time_out[-4:-2]) in [1,16,31,46]) & (int(time_out[-4:-2]) != prev_min):
                day_mo_date = [i for i in time.ctime()[0:10].split()]
                wthr_dict, color_dict = self.download_weather('Irving, Texas, United States', wthr_dict, color_dict)

                date_atmosphere = day_mo_date[0] + ' ' + \
                                  day_mo_date[1] + ', ' + \
                                  day_mo_date[2] + ' ' + \
                                  wthr_dict['atmospheric_text'] + ' '
                            
                temperature_txt = wthr_dict['better_temperature'] + ' '
                rel_humidity = wthr_dict['humidity'] + ' '
                wind_speed = wthr_dict['better_wind_speed']
                time.sleep(2)
        
            ### clear LED matrix
            offscreen_canvas.Clear()
            
            ### triger graphics
            if (int(time_out[-4:-2]) in [15,45]) & (int(time_out[-4:-2]) != prev_min):
                self.random_bars(watermellon_color_list, delay = 5,  num_iterations = 1)

            if (int(time_out[-4:-2]) in [30]) & (int(time_out[-4:-2]) != prev_min):
                self.rain_storm(num_drops=350, delay = 0.05, color=[255,255,255], dim_by=45)
                                
            if (int(time_out[-4:-2]) in [0]) & (int(time_out[-4:-2]) != prev_min):
                self.rotating_block()

            ### Draw on LED matrix
            # display time as text
            graphics.DrawText(offscreen_canvas, clock_font, -1, 16, time_color, time_out[:-2])
            graphics.DrawText(offscreen_canvas, am_pm_font, 25, 16, time_color, time_out[-2:])
            
            # scroll through the date and weather text
            Len_1 = graphics.DrawText(offscreen_canvas, date_wthr_font, pos, 8, date_color, date_atmosphere)
            Len_2 = graphics.DrawText(offscreen_canvas, date_wthr_font, pos+Len_1, 8, 
                                      graphics.Color(color_dict['temp_color'][0],color_dict['temp_color'][1],color_dict['temp_color'][2]), 
                                      temperature_txt)
            Len_3 = graphics.DrawText(offscreen_canvas, date_wthr_font, pos+Len_1+Len_2, 8, 
                                      graphics.Color(color_dict['humid_color'][0],color_dict['humid_color'][1],color_dict['humid_color'][2]), 
                                      rel_humidity) 
            Len_4 = graphics.DrawText(offscreen_canvas, date_wthr_font, pos+Len_1+Len_2+Len_3, 8, 
                                      graphics.Color(color_dict['wind_color'][0],color_dict['wind_color'][1],color_dict['wind_color'][2]), 
                                      wind_speed)

            # iterate position var
            pos -= 1
            if (pos + Len_1 + Len_2 + Len_3 + Len_4 < 0):
                pos = offscreen_canvas.width
            
            ### set delay time before entering loop again
            time.sleep(0.05)
            
            ### ???
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            
            ### set previous time to current time
            prev_min = int(time_out[-4:-2])
        
        return

# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
