from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time
import random

options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 4
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'
options.brightness = 40
options.gpio_slowdown = 4

matrix = RGBMatrix(options=options)

font = graphics.Font()
font.LoadFont("fonts/6x10.bdf")

# Race state
START_LAP = 22
TOTAL_LAPS = 400

drivers = [
    {"car": "#22", "name": "Joey Log"},
    {"car": "#5",  "name": "Kyle Lar"},
    {"car": "#12", "name": "Ryan Bla"},
]

def draw_race(lap, drivers):
    canvas = matrix.CreateFrameCanvas()
    laps_left = TOTAL_LAPS - lap

    # LAP INFO - Panel 1 (furthest from Pi)
    graphics.DrawText(canvas, font, 194, 12, graphics.Color(0, 255, 0),
                      f"LAP {lap}/{TOTAL_LAPS}")
    graphics.DrawText(canvas, font, 194, 24, graphics.Color(255, 255, 0),
                      f"TO GO {laps_left}")

    # DRIVERS - Panels 2, 3, 4
    x_positions = [130, 66, 2]
    for i, (x, driver) in enumerate(zip(x_positions, drivers)):
        graphics.DrawText(canvas, font, x, 12, graphics.Color(255, 255, 255),
                          f"{i+1:>2} {driver['car']}")
        graphics.DrawText(canvas, font, x, 24, graphics.Color(0, 200, 255),
                          driver["name"])

    matrix.SwapOnVSync(canvas)

try:
    for lap in range(START_LAP, START_LAP + 11):
        # Randomly shuffle drivers each lap
        random.shuffle(drivers)
        draw_race(lap, drivers)
        print(f"Lap {lap} | 1st: {drivers[0]['name']} | 2nd: {drivers[1]['name']} | 3rd: {drivers[2]['name']}")
        time.sleep(2)

    print("\nSimulation complete!")
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    matrix.Clear()
    print("\nDone.")