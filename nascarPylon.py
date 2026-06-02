# Importing required libraries
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import requests
import time
import os

os.environ['REQUESTS_CA_BUNDLE'] = '/etc/ssl/certs/ca-certificates.crt'

# CONFIGURATION SECTION OF CODE

# NASCAR live data endpoint
API_KEY = "gjGTrXqctthrcZtfI0Z7DjjvAofErymvwWRbB5AC"
SERIES = "mc"       #mc = CUP Series | nx = XFINITY | ct = TRUCK

SCHEDULE_URL  = f"https://api.sportradar.com/nascar-ot3/{SERIES}/2026/races/schedule.json?api_key={API_KEY}"
LEADERBOARD_URL = "https://api.sportradar.com/nascar-ot3/{SERIES}/races/{RACE_ID}/results.json?api_key={API_KEY}"
# Setup LED matrix options
options = RGBMatrixOptions()
options.rows = 32               # Each LED screen is 32 pixels tall
options.cols = 64               # Each LED screen is 64 pixels wide
options.chain_length = 4        # I'm chaining 4 LED screens vertically
options.parallel = 1 
options.hardware_mapping = 'adafruit-hat'
options.brightness = 40         # Limits the brightness to reduce the power used
options.gpio_slowdown = 4


# Initialize matrix controller
matrix = RGBMatrix(options=options)

# Loading the font for the screens
font = graphics.Font()
font.LoadFont("fonts/6x10.bdf")

# DATA FETCHING FUNCTION

def get_live_race_id():
    """
    Finds the race ID for the currently live (in-progress) race.
    Returns a race ID string, or None if no race is live.
    """
    try:
        response = requests.get(SCHEDULE_URL, timeout=5)
        data = response.json()
        for event in data.get("events", []):          # loop through events first
            for race in event.get("races", []):        # then races inside each event
                if race.get("status") == "inprogress":
                    return race["id"]
    except Exception as e:
        print("Error fetching schedule:", e)
    return None

def get_leaderboard(race_id):
    """
    Fetches live leaderboard data for a given race ID.
    Returns parsed JSON or None on failure.
    """
    try:
        url = LEADERBOARD_URL.format(SERIES=SERIES, RACE_ID=race_id, API_KEY=API_KEY)
        response = requests.get(url, timeout=5)
        return response.json()
    except Exception as e:
        print("Error fetching leaderboard:", e)
    return None
    
# DRAW FUNCTION. MAIN DISPLAY LOGIC

def draw_display(data):
    canvas = matrix.CreateFrameCanvas()

    try:
        results = data.get("results", [])
        laps_completed = results[0]["laps_completed"]
        laps_total = data.get("race", {}).get("laps", 400)
        laps_left = laps_total - laps_completed

        graphics.DrawText(canvas, font, 194, 12, graphics.Color(0, 255, 0),
                          f"LAP {laps_completed}/{laps_total}")
        graphics.DrawText(canvas, font, 194, 24, graphics.Color(255, 255, 0),
                          f"TO GO {laps_left}")
    except Exception as e:
        print("Error drawing lap info:", e)

    drivers = data.get("results", [])

    for i in range(3):
        if i >= len(drivers):
            break

        driver   = drivers[i]
        position = driver.get("position", "?")
        car      = driver.get("car", {}).get("number", "??")
        name     = driver.get("driver", {}).get("full_name", "UNKNOWN")

        x_offset = (options.chain_length - 2 - i) * 64  # panel 3, 2, 1 for drivers 1, 2, 3

        graphics.DrawText(canvas, font, x_offset + 2, 12,
                          graphics.Color(255, 255, 255),
                          f"{position:>2} #{car}")
        graphics.DrawText(canvas, font, x_offset + 2, 24,
                          graphics.Color(0, 200, 255),
                          name[:8])

    matrix.SwapOnVSync(canvas)
    
def draw_waiting(message="WAITING"):
    """Shown on screen when no live race is found."""
    canvas = matrix.CreateFrameCanvas()
    graphics.DrawText(canvas, font, 2, 20, graphics.Color(255, 100, 0), message)
    matrix.SwapOnVSync(canvas)    

# MAIN LOOP
def main():
    race_id = None
    race_id_refresh_timer = 0

    while True:
        now = time.time()

        # Re-check for a live race ID every 60 seconds
        # (avoids hammering the schedule endpoint)
        if race_id is None or (now - race_id_refresh_timer) > 60:
            race_id = get_live_race_id()
            race_id_refresh_timer = now

        if race_id:
            data = get_leaderboard(race_id)
            if data:
                draw_display(data)
            else:
                draw_waiting("NO DATA")
        else:
            draw_waiting("NO RACE")

        time.sleep(2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped.")                    