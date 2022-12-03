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
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("/home/pi/display16x32/rpi-rgb-led-matrix/fonts/4x6.bdf")
        date_color = graphics.Color(45, 255, 45)
        time_color = graphics.Color(0, 145, 145)
        pos = offscreen_canvas.width
        my_text = self.args.text

        while True:
            today_out = time.ctime()[0:10]
            time_out = my_text + time.strftime("%I:%M%p")
            
            offscreen_canvas.Clear()
            
            graphics.DrawText(offscreen_canvas, font, 2, 15, time_color, time_out)
            
            len = graphics.DrawText(offscreen_canvas, font, pos, 7, date_color, today_out)
            pos -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width

            time.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
