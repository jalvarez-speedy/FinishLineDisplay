from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time

options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 4   # testing 4 screens
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'
options.brightness = 40
options.gpio_slowdown = 4

matrix = RGBMatrix(options=options)

font = graphics.Font()
font.LoadFont("fonts/6x10.bdf")

canvas = matrix.CreateFrameCanvas()
canvas.Clear()

# Default chained canvas is 256 wide x 32 tall:
# Panel 1 = x 0-63
# Panel 2 = x 64-127
# Panel 3 = x 128-191
# Panel 4 = x 192-255

screens = [
    (graphics.Color(255, 255, 0), "SCREEN 4"),
    (graphics.Color(0, 0, 255),   "SCREEN 3"),
    (graphics.Color(255, 0, 0),   "SCREEN 2"),
    (graphics.Color(0, 255, 0),   "SCREEN 1"),
]

for i, (color, label) in enumerate(screens):
    x_offset = i * 64
    graphics.DrawText(canvas, font, x_offset + 2, 20, color, label)

matrix.SwapOnVSync(canvas)

print("Displaying 4-screen test. Press Ctrl+C to stop.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    matrix.Clear()
    print("\nDone.")