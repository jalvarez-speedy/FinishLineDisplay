# FinishLineDisplay

A live NASCAR race pylon display powered by a Raspberry Pi 4 and five 64x32 HUB75 RGB LED panels. Fetches real-time race data from the Sportradar NASCAR OT v3 API and displays lap info and the top 3 drivers on a chained LED matrix.

---

## Hardware

- Raspberry Pi 4 - 8GB RAM
- Adafruit RGB Matrix HAT + RTC
- 4x 64x32 HUB75 RGB LED panels (P2.5)
- 5V 15A Power Supply
- Tall GPIO stacking header (to clear Pi 4 heatsink and PoE header)
- IDC ribbon cables for panel chaining
- Female DC Power Adapter - 2.1mm
- 120mm Case Fan - Ultra Quiet 3 pin
- 3 Pin Fan Power Supply

### Wiring

```
Pi/HAT → Panel 1 → Panel 2 → Panel 3 → Panel 4
```

- Ribbon cable from HAT connects to the **IN (top) connector** of Panel 1
- Each panel's **OUT (bottom) connector** connects to the **IN (top) connector** of the next panel
- The last panel's OUT port is left unconnected
- Power (5V) connected directly to panels 2, 3, and 4 from the power supply (panel 1 is powered by Pi)
- Splicer used to connect two power cables into one female DC power adapter 2.1mm

---

## Software

### Requirements

- Python 3
- `requests` library
- `rgbmatrix` library (must be built from source — see below)
- Sportradar NASCAR OT v3 API key

### Installing the RGB Matrix Library

The hardware library must be built from source:

```bash
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
cd rpi-rgb-led-matrix
make build-python PYTHON=$(which python3)
sudo make install-python PYTHON=$(which python3)
```

### Installing Python Dependencies

```bash
pip install requests
```

### API Key Setup

Sign up at [developer.sportradar.com](https://developer.sportradar.com) and create a trial key for **NASCAR OT v3**. Store your key as an environment variable to keep it out of your code:

```bash
# Add to ~/.bashrc
export SPORTRADAR_KEY="your_api_key_here"
```

Then in your code:
```python
import os
API_KEY = os.environ.get("SPORTRADAR_KEY")
```

---

## Files

### `nascarPylon.py` — Main Display Script

The primary script that runs the live race display.

**What it does:**
- Pulls the Sportradar schedule endpoint every 60 seconds to find a live race
- When a race is found, fetches the leaderboard every 2 seconds
- Displays lap info on the first panel and the top 3 drivers on panels 2–4
- Shows `NO RACE` when no race is in progress

**Display layout:**
```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ LAP 37/400  │  1 #45      │  2 #20      │  3 #5       │
│ TO GO 363   │  Tyler Re   │  Christop   │  Kyle Lar   │
└─────────────┴─────────────┴─────────────┴─────────────┘
  Panel 1        Panel 2       Panel 3       Panel 4
```

**Running the script:**
```bash
sudo /home/jalvarez/Documents/github/FinishLineDisplay/.venv/bin/python nascarPylon.py
```

> `sudo` is required because the RGB matrix library needs direct GPIO access.

**Key configuration options at the top of the file:**
| Option | Description |
|---|---|
| `API_KEY` | Your Sportradar API key |
| `SERIES` | `mc` = Cup, `nx` = Xfinity, `ct` = Trucks |
| `options.chain_length` | Number of panels (currently 4) |
| `options.brightness` | LED brightness 0–100 (currently 40) |
| `options.gpio_slowdown` | Slow down GPIO for stability (currently 4) |

---

### `test_screens.py` — Static Screen Label Test

Tests that all panels are connected and displaying correctly by showing a static label on each panel in a different color.

**Display layout:**
```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│  SCREEN 1   │   SCREEN 2  │   SCREEN 3  │   SCREEN 4  │
│             │             │             │             │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

**Running the script:**
```bash
sudo /home/jalvarez/Documents/github/FinishLineDisplay/.venv/bin/python test_screens.py
```

Press `Ctrl+C` to stop.

---

### `test_race_sim.py` — Mock Race Simulation Test

Simulates a live race by counting up 10 laps from lap 22 and randomly shuffling the top 3 drivers each lap. Useful for testing the display without a live race.

**Display layout:**
```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│  LAP 22/400 │   1 #22     │   2 #5      │   3 #12     │
│  TO GO 378  │  Joey Log   │  Kyle Lar   │  Ryan Bla   │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

**What it does:**
- Starts at lap 22/400 and counts to lap 32
- Updates every 2 seconds
- Randomly shuffles Joey Logano, Kyle Larson, and Ryan Blaney each lap
- Prints the current order to the terminal

**Running the script:**
```bash
sudo /home/jalvarez/Documents/github/FinishLineDisplay/.venv/bin/python test_race_sim.py
```

Press `Ctrl+C` to stop.

---

## Testing Without Hardware (Mock Mode)

A mock `rgbmatrix.py` file can be placed in the project folder to simulate the display in the terminal on any PC or on the Pi without screens connected. The mock intercepts all draw calls and prints them as text output.

**To use mock mode:** Place `rgbmatrix.py` in the project root.  
**To use real hardware:** Delete `rgbmatrix.py` so the real library takes over.

Never deploy to real hardware with the mock file present.

---

## Notes

- The Sportradar free trial allows 1,000 API calls/month and 1 call/second. The script uses a 2-second sleep between cycles to stay within limits.
- `sudo` must always be used when running scripts with real LED panels.
- The `isolcpus=3` suggestion in the terminal output is optional but can improve display smoothness — add it to `/boot/cmdline.txt` and reboot.
- Disable onboard audio to prevent conflicts with the LED library: add `dtparam=audio=off` to `/boot/config.txt` and reboot.