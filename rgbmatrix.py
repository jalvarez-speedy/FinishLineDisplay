# rgbmatrix.py  —  hardware mock for testing in VS Code

class Color:
    def __init__(self, r, g, b):
        self.r, self.g, self.b = r, g, b

class Font:
    def LoadFont(self, path):
        pass

class Canvas:
    def __init__(self):
        self.content = []

    def clear(self):
        self.content = []

class RGBMatrix:
    def __init__(self, options=None):
        pass

    def CreateFrameCanvas(self):
        return Canvas()

    def SwapOnVSync(self, canvas):
        print("\n--- DISPLAY UPDATE ---")
        for line in canvas.content:
            print(line)
        print("----------------------")

class RGBMatrixOptions:
    rows = 32
    cols = 64
    chain_length = 1
    parallel = 1
    hardware_mapping = ''
    brightness = 100

# Mock the graphics module
class graphics:
    Font = Font
    Color = Color

    @staticmethod
    def DrawText(canvas, font, x, y, color, text):
        canvas.content.append(f"  [y={y:>3}] {text}")