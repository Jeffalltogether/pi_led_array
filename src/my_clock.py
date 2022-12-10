#!/usr/bin/env python
# Display a runtext with double-buffering.
import sys
import math
from weather_api import wttr_weather 

sys.path.append('/home/pi/display16x32/rpi-rgb-led-matrix/bindings/python/samples/')

from samplebase import SampleBase
from rgbmatrix import graphics
import time



class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        
    def gradient_fill(self, num_iterations = 4):
        ### for graphics
        sub_blocks = 16
        width = self.matrix.width
        height = self.matrix.height
        x_step = max(1, width / sub_blocks)
        y_step = max(1, height / sub_blocks)
        count = 0
        
        iters = 0
        while iters <= num_iterations:
            for y in range(0, height):
                for x in range(0, width):
                    c = sub_blocks * int(y / y_step) + int(x / x_step)
                    if count % 4 == 0:
                        self.matrix.SetPixel(x, y, c, c, c)
                    elif count % 4 == 1:
                        self.matrix.SetPixel(x, y, c, 0, 0)
                    elif count % 4 == 2:
                        self.matrix.SetPixel(x, y, 0, c, 0)
                    elif count % 4 == 3:
                        self.matrix.SetPixel(x, y, 0, 0, c)
            count += 1
            time.sleep(2)
            iters += 1
            
        return
        
    def rotating_block(self, num_iterations = 3000):
        def scale_col(val, lo, hi):
            if val < lo:
                return 0
            if val > hi:
                return 255
            return 255 * (val - lo) / (hi - lo)

        def rotate(x, y, sin, cos):
            return x * cos - y * sin, x * sin + y * cos

        cent_x = self.matrix.width / 2
        cent_y = self.matrix.height / 2

        rotate_square = min(self.matrix.width, self.matrix.height) * 1.41
        min_rotate = cent_x - rotate_square / 2
        max_rotate = cent_x + rotate_square / 2

        display_square = min(self.matrix.width, self.matrix.height) * 0.7
        min_display = cent_x - display_square / 2
        max_display = cent_x + display_square / 2

        deg_to_rad = 2 * 3.14159265 / 360
        rotation = 0

        # Pre calculate colors
        col_table = []
        for x in range(int(min_rotate), int(max_rotate)):
            col_table.insert(x, scale_col(x, min_display, max_display))

        offset_canvas = self.matrix.CreateFrameCanvas()

        # run graphics
        iters = 0
        while iters <= num_iterations:
            rotation += 1
            rotation %= 360

            # calculate sin and cos once for each frame
            angle = rotation * deg_to_rad
            sin = math.sin(angle)
            cos = math.cos(angle)

            for x in range(int(min_rotate), int(max_rotate)):
                for y in range(int(min_rotate), int(max_rotate)):
                    # Our rotate center is always offset by cent_x
                    rot_x, rot_y = rotate(x - cent_x, y - cent_x, sin, cos)

                    if x >= min_display and x < max_display and y >= min_display and y < max_display:
                        x_col = col_table[x]
                        y_col = col_table[y]
                        offset_canvas.SetPixel(rot_x + cent_x, rot_y + cent_y, x_col, 255 - y_col, y_col)
                    else:
                        offset_canvas.SetPixel(rot_x + cent_x, rot_y + cent_y, 0, 0, 0)

            offset_canvas = self.matrix.SwapOnVSync(offset_canvas)
            iters+=1
            
    def download_weather(self, location='Irving, Texas, United States', curr_wthr_dict=None):
        try:
            wthr_as_dict = wttr_weather(location)
        except:
            # typically a `requests.exceptions.ConnectionError` will occur
            if not curr_wthr_dict:
                # if it fals the first time, we generate an empty dict
                wthr_as_dict = {'atmospheric_text': '', 'temperature': '',
                                'humidity': '', 'better_wind_speed': ''}
            else:
                # if it fails a subsequent time, we return the current data
                return curr_wthr_dict
                           
        return wthr_as_dict
        

    def run(self):
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
        pos = offscreen_canvas.width
                
        # download weather
        wthr_dict = self.download_weather()
        # set minute counter
        prev_min = -1
        while True:
            
            ### get date and time
            day_mo_date = [i for i in time.ctime()[0:10].split()]
            time_out = time.strftime("%I:%M%p")
            
            ### update weather
            if prev_min in [5,35]:
                wthr_dict = self.download_weather('Irving, Texas, United States', wthr_dict)
                time.sleep(10)

            ### combine date and weather
            date_wthr_txt = day_mo_date[0] + ' ' + \
                            day_mo_date[1] + ', ' + \
                            day_mo_date[2] + ' ' + \
                            wthr_dict['atmospheric_text'] + ' ' + \
                            wthr_dict['temperature'] + ' ' + \
                            wthr_dict['humidity'] + ' ' + \
                            wthr_dict['better_wind_speed']
            
            ### clear LED matrix
            offscreen_canvas.Clear()
            
            ### triger graphics
            if (int(time_out[-4:-2]) in [15,45]) & (int(time_out[-4:-2]) != prev_min):
                self.gradient_fill()
                
            if (int(time_out[-4:-2]) in [0,30]) & (int(time_out[-4:-2]) != prev_min):
                self.rotating_block()

            ### Draw on LED matrix
            # display time as text
            graphics.DrawText(offscreen_canvas, clock_font, -1, 16, time_color, time_out[:-2])
            graphics.DrawText(offscreen_canvas, am_pm_font, 25, 16, time_color, time_out[-2:])
            
            # scroll through the date and weather text
            len = graphics.DrawText(offscreen_canvas, date_wthr_font, pos, 8, date_color, date_wthr_txt)
            pos -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width
            
            ### set delay time before entering loop again
            time.sleep(0.075)
            
            ### ???
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            
            ### set previous time to current time
            prev_min = int(time_out[-4:-2])


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
