#!/usr/bin/env python
import time
import sys
import numpy as np
import math
import concurrent.futures
from PIL import Image

sys.path.append('/home/pi/display16x32/rpi-rgb-led-matrix/bindings/python/samples/')

from samplebase import SampleBase
from rgbmatrix import graphics


class GraphicsTest(SampleBase):
    """
    The graphics drawing options are as follows:
    
        * graphics.DrawLine()
        * graphics.DrawCircle()
        * graphics.DrawText()
        
    run them as follows:
        
        * DrawText
    font = graphics.Font()
    font.LoadFont("/home/pi/display16x32/rpi-rgb-led-matrix/fonts/7x13.bdf")
    blue = graphics.Color(0, 0, 255)
    graphics.DrawText(canvas, font, 2, 4, blue, "Julian")
        
        * DrawLine
    red = graphics.Color(255, 0, 0)
    graphics.DrawLine(canvas, 5, 5, 22, 13, red)
        
        * DrawCircle
    green = graphics.Color(0, 255, 0)
    graphics.DrawCircle(canvas, 15, 15, 10, green)
        
        
    To clear the LED matrix we run these lines of code:
    `
    for k in range(2):
        self.offscreen_canvas.Fill(0, 0, 0)
        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
    `

    There is something about projecting onto a montior (maybe 
    double buffering?) that makes the SwapOnVSync a difficult 
    command to get used too.
    """
    
    def __init__(self, *args, **kwargs):
        super(GraphicsTest, self).__init__(*args, **kwargs)
        
        
    def random_bars(self, colors, delay=10, num_iterations = 4):
        num_colors = len(colors)
        
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        
        iteration = 0
        prev = set()
        while iteration < num_iterations:
            i = np.random.choice(self.matrix.width)
            c = colors[np.random.choice(num_colors)]

            if i not in prev:
                for j in range(0,self.matrix.height,1):
                    self.offscreen_canvas.SetPixel(i, j, c[0], c[1], c[2])
                    for k in range(delay):
                        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
                        
                prev.add(i)

            if len(prev) >= self.matrix.width:
                prev.clear()
                while len(prev) < self.matrix.width:
                    i = np.random.choice(self.matrix.width)
                    if i not in prev:
                        for j in range(0,self.matrix.height,1):
                            self.offscreen_canvas.SetPixel(i, j, 0, 0, 0)
                            for k in range(delay):
                                self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
                        
                        prev.add(i) 

                prev.clear()
                iteration += 1
        return
        
    def fill_from_left(self, colors, delay=3, num_pixels=100):
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        
        pixel_counter = 0
        k = 0
        
        #while True:
        for i in range(0,self.matrix.width,1):
            for j in range(0,self.matrix.height,1):
                c = colors[k]
                self.offscreen_canvas.SetPixel(i, j, c[0], c[1], c[2])
                
                pixel_counter += 1
                if pixel_counter == num_pixels:
                    k += 1
                    if k > len(colors) - 1:
                        k = 0
                    pixel_counter = 0
                    
                for d in range(delay):
                    self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
        time.sleep(200)
        return
    
    def rain_drop(self, color, delay_options, twice_height, fade):
        '''
        pre-calculate as many arguments as possible to speed runtime
        ''' 
        #s=np.random.choice([0.25,0.5,0.75,1.0])  
        #time.sleep(s)
             
        i = np.random.choice(self.matrix.width)
        
        delay = np.random.choice(delay_options, 1)[0]

        for j in range(0,twice_height,1):
            for k in range(self.matrix.height):
                self.offscreen_canvas.SetPixel(i, j-k, color[0]-fade[k], color[1]-fade[k], color[2]-fade[k])

            for d in range(delay):
                self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
                
        return
        
    def rain(self, num_process=4, color=[255,255,255]):
        """
        this method of making multiple rain drops fall simultaneously 
        causes the Pi to crash 
        """
        delay_options = [3,4,5]
        twice_height=self.matrix.height*2
        fade=[np.min([25*k,255]) for k in range(self.matrix.height)]
        
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        with concurrent.futures.ThreadPoolExecutor(max_workers = num_process) as executor:
            while True:
                executor.submit(self.rain_drop, color, delay_options, twice_height, fade)
            
        return

    def rain_storm(self, num_drops=250, color=[255,255,255], delay = 0.05, dim_by=45, num_iterations = 2):
        ### compute the color gradient
        color_gradient = []
        for i in range(6):
            color_gradient.append([np.max([color[0]-(dim_by*i), 0]),
                                   np.max([color[1]-(dim_by*i), 0]),
                                   np.max([color[2]-(dim_by*i), 0])])

        ### create a matrix that represents a long vertical strip of rain
        rain_array = np.zeros([self.matrix.height*20, self.matrix.width, 3], dtype='uint8')
        
        for i in range(num_drops):
            x = np.random.choice(rain_array.shape[0])
            y = np.random.choice(rain_array.shape[1])
            for j in range(6):
                x_offset = x-j
                if x_offset > rain_array.shape[0]:
                    x_offset = x_offset - rain_array.shape[0]
        
                rain_array[x_offset,y,:] = color_gradient[j]
        
        self.rain_img = Image.fromarray(rain_array)
        
        double_buffer = self.matrix.CreateFrameCanvas()
        img_width, img_height = self.rain_img.size

        # let's scroll
        iteration = 0
        ypos = 0
        while iteration < num_iterations:
            ypos += 1
            if (ypos > img_height):
                ypos = 0
                iteration += 1

            double_buffer.SetImage(self.rain_img, 0, ypos)
            double_buffer.SetImage(self.rain_img, 0, ypos-img_height)
            
            double_buffer = self.matrix.SwapOnVSync(double_buffer)
            time.sleep(delay)
        
        # clear screen
        for k in range(2):
            double_buffer.Fill(0, 0, 0)
            double_buffer = self.matrix.SwapOnVSync(double_buffer)
            
        return
            
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
        
    def rotating_block(self, num_iterations = 6000):
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

        
    def run(self):
        #color_list = [ [205,3,254],
        #               [2,247,7],
        #               [247,27,2],
        #               [50,242,49],
        #               [5,25,242]]
                       
        temperature_colors = [[255,255,255],
                              [230,0,250],
                              [0,0,255],
                              [100,149,237],
                              [0,255,0],
                              [255,240,0],
                              [250,95,0],
                              [255,0,0]]
                              
        humidity_colors = [[255,128,0],
                            [255,255,0],
                            [51,255,51],
                            [102,255,255],
                            [102,178,255],
                            [0,128,255],
                            [0,51,255],
                            [0,0,255]]
  
        wind_colors = [[0,153,0],
                        [178,255,102],
                        [255,255,0],
                        [255,128,0],
                        [255,0,0]] 
                                                                         
        # self.random_bars(color_list, 8)
        self.fill_from_left(wind_colors, 3, 100)
        # self.rain()
        # self.rain_storm()
        # self.rotating_block()
        # self.gradient_fill()
        
        return

# Main function
if __name__ == "__main__":
    graphics_test = GraphicsTest()
    if (not graphics_test.process()):
        graphics_test.print_help()
