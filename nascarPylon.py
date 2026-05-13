# Importing required libraries
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import requests
import time

# CONFIGURATION SECTION OF CODE

# NASCAR live data endpoint
URL = "https://cf.nascar.com/cacher/live/leaderboard.json"

# Setup LED matrix options
options = RGBMatrixOptions()
options.rows = 32               # Each LED screen is 32 pixels tall
options.cols = 64               # Each LED screen is 64 pixels wide
options.chain_length = 5        # I'm chaining 5 LED screens vertically
options.parrallel = 1 
options.hardware_mapping = 'adafruit-hat'
options.brightness = 40         # Limits the brightness to reduce the power used

# Initialize matrix controller
matrix = RGBMatrix(options=options)

# Loading the font for the screens
font = graphics.Font()
font.LoadFont("fonts/6x10.bdf")

# DATA FETCHING FUNCTION

def get_data():
    """
    Fetch live NASCAR data from API.
    Returns JSON data or None if request fails.
    """
    try:
        response = requests.get(URL, timeout=5)
        return response.json()
    except Exception as e:
        print("Error fetching data:", e)
        
    
# DRAW FUNCTION. MAIN DISPLAY LOGIC

def draw_display(data):
    """
    Draws all content onto the LED panels:
    - Top panel: laps completed / laps remaining
    - Next panels: top 4 drivers
    """

    # Prevents flickering
    canvas = matrix.CreateFrameCanvas()

    #  TOP LED SCREEN - LAB INFO
    try:
        laps_completed = data["laps_completed"]
        laps_total = data["laps_total"]
        laps_left = laps_total - laps_completed

        #Display lap info
        graphics.DrawText(canvas, font, 2, 12, graphics.Color(0,255,0),
                          f"LAP {laps_completed}/{laps_total}"),

        graphics.DrawText(canvas, font, 2, 24, graphics.Color(255,255,0),
                          f"TO GO {laps_left}")
        
    except:
        # If data missing, show fallback
        graphics.DrawText(canvas, font, 2, 16, graphics.Color(255,0,0),
                          "NO DATA")

    # LED SCREENS 2 to 5 - TOP 4 DRIVERS
    drivers = data.get("leaderboard", [])

    for i in range(4):      # Top 4 Drivers
        if i >= len(drivers):
            break

        driver = drivers[i]

        position = driver.get("position", "?")
        car = driver.get("car_number", "??")
        name = driver.get("driver_name", "UNKNOWN")

        # Each LED screen is 32 pixels tall, offset by screen number
        y_offset = (i + 1) * 32

        # Draw position and car number
        graphics.DrawText(canvas, font, 2, y_offset + 12, 
                          graphics.Color(255,255,255),
                          f"{position:>2} #{car}")

        # Draw shortened driver name
        graphics.DrawText(canvas, font, 2, y_offset + 24,
                          graphics.Color(0,200,255),
                          name[:8])  #should limit the length to fit screen

    # display frame
    matrix.SwapOnVSync(canvas)

# MAIN LOOP
def main():
    """
    Main loop:
    - Fetch data every second
    - Update display
    """

    while True:
        data = get_data()

        if data:
            draw_display(data)

        time.sleep(1)   # Refresh rate

# Run the program
if __name__ == "__main__":
    main()                              