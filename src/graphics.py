#!/usr/bin/env python
import time
import sys
import numpy as np
import concurrent.futures

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
        
    def random_bars(self, colors, delay=10):
        num_colors = len(colors)
        
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        
        prev = set()
        while True:
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
        return
        
    def fill_from_left(self, colors, delay=3):
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        
        while True:
            for c in colors:
                for i in range(0,self.matrix.width,1):
                    for j in range(0,self.matrix.height,1):
                        self.offscreen_canvas.SetPixel(i, j, c[0], c[1], c[2])
                        for k in range(delay):
                            self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
        return
    
    def rain_drop(self, color, delay_options, twice_height, fade):
        '''
        pre-calculate as many arguments as possible to speed runtime
        ''' 
        s=np.random.choice([0.25,0.5,0.75,1.0])  
        time.sleep(s)
             
        i = np.random.choice(self.matrix.width)
        
        #delay = np.random.choice(delay_options, 1)[0]

        for j in range(0,twice_height,1):
            for k in range(self.matrix.height):
                self.offscreen_canvas.SetPixel(i, j-k, color[0]-fade[k], color[1]-fade[k], color[2]-fade[k])

            #for d in range(delay):
            self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
                
        return
        
    def rain(self, color=[255,255,255]):
        delay_options = [4,5,6]
        twice_height=self.matrix.height*2
        fade=[np.min([25*k,255]) for k in range(self.matrix.height)]
        
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        with concurrent.futures.ThreadPoolExecutor(max_workers = 12) as executor:
            while True:
                executor.submit(self.rain_drop, color, delay_options, twice_height, fade)
            
        return
        
    def run(self):
        color_list = [ [205,3,254],
                       [2,247,7],
                       [247,27,2],
                       [50,242,49],
                       [5,25,242]]
        
        # self.random_bars(color_list, 2)
        # self.fill_from_left(color_list, 3)
        self.rain()
        
        return

# Main function
if __name__ == "__main__":
    graphics_test = GraphicsTest()
    if (not graphics_test.process()):
        graphics_test.print_help()
