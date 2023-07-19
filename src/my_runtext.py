#!/usr/bin/env python
# Display a runtext with double-buffering.
import sys
sys.path.append('/home/pi/display16x32/rpi-rgb-led-matrix/bindings/python/samples/')

from samplebase import SampleBase
from rgbmatrix import graphics
import time
import datetime



class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        scroll_font = graphics.Font()
        scroll_font.LoadFont("/home/pi/display16x32/rpi-rgb-led-matrix/fonts/5x8.bdf")
        timer_font = graphics.Font()
        timer_font.LoadFont("/home/pi/display16x32/rpi-rgb-led-matrix/fonts/4x6.bdf")
        
        name_color = graphics.Color(45, 255, 45)
        days_color = graphics.Color(0, 50, 255)
        time_color = graphics.Color(0, 145, 145)
        
        pos = offscreen_canvas.width
        my_text = self.args.text

        while True:
            time_delta = datetime.datetime(2023, 9, 19, 0, 0) - datetime.datetime.now()
            scroll_text = f"Days until Julian's Birthday:"

            dd = time_delta.days
            H = time_delta.seconds// 3600
            M = ( time_delta.seconds - (H*3600) ) // 60
            S = ( time_delta.seconds - (H*3600) - (M*60) )
            
            dd = str(dd) + ' days'
            hh_mm_ss = "{}:{}:{}".format(str(H).zfill(2), str(M).zfill(2), str(S).zfill(2))
            
            offscreen_canvas.Clear()
            
            graphics.DrawText(offscreen_canvas, timer_font, 0, 11, days_color, dd)
            graphics.DrawText(offscreen_canvas, timer_font, 0, 16, time_color, hh_mm_ss)
            
            len = graphics.DrawText(offscreen_canvas, scroll_font, pos, 6, name_color, scroll_text)
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
