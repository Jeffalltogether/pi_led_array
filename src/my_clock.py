#!/usr/bin/env python
# Display a runtext with double-buffering.
import sys
sys.path.append('/home/pi/display16x32/rpi-rgb-led-matrix/bindings/python/samples/')

from samplebase import SampleBase
from rgbmatrix import graphics
import time



class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)

    def run(self):
        ### for clock
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("/home/pi/display16x32/rpi-rgb-led-matrix/fonts/4x6.bdf")
        date_color = graphics.Color(45, 255, 45)
        time_color = graphics.Color(0, 145, 145)
        pos = offscreen_canvas.width
        
        ### for graphics
        sub_blocks = 16
        width = self.matrix.width
        height = self.matrix.height
        x_step = max(1, width / sub_blocks)
        y_step = max(1, height / sub_blocks)
        count = 0
        
        prev_min = 0
        
        while True:
            
            ### get date and time
            today_out = time.ctime()[0:10]
            time_out = time.strftime("%I:%M%p")

            ### clear LED matrix
            offscreen_canvas.Clear()
            
            ### triger graphics
            if (int(time_out[-3]) % 5 == 0) & (int(time_out[-3]) != prev_min):
                iters = 0
                while iters <= 7:
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

            ### Draw on LED matrix
            # display time as text
            graphics.DrawText(offscreen_canvas, font, 2, 15, time_color, time_out)
            
            # scroll through the date text
            len = graphics.DrawText(offscreen_canvas, font, pos, 7, date_color, today_out)
            pos -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width
            
            ### set delay time before entering loop again
            time.sleep(0.1)
            
            ### ???
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            
            ### set previous time to current time
            prev_min = int(time_out[-3])


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
