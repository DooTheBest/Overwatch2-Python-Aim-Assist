import pydirectinput
from PIL import ImageGrab
import time
import math

target_color = (200, 20, 22)
tolerance = 15

screen_width, screen_height = pydirectinput.size()
mid_x = screen_width // 2
mid_y = screen_height // 2

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def match_color(pixel_color, target_color, tolerance):
    r_diff = abs(pixel_color[0] - target_color[0])
    g_diff = abs(pixel_color[1] - target_color[1])
    b_diff = abs(pixel_color[2] - target_color[2])
    return r_diff <= tolerance and g_diff <= tolerance and b_diff <= tolerance

right_button_pressed = False

try:
    while True:
        screenshot = ImageGrab.grab()

        best_match_position = None
        best_color_diff = float('inf')

        for x in range(mid_x - 200, mid_x + 200, 4):
            for y in range(mid_y - 200, mid_y + 200, 4):
                pixel_color = screenshot.getpixel((x, y))
                if match_color(pixel_color, target_color, tolerance):
                    color_diff = sum(abs(pixel_color[i] - target_color[i]) for i in range(3))
                    if color_diff < best_color_diff:
                        best_color_diff = color_diff
                        best_match_position = (x, y)

        if best_match_position:
            print('Found Color')
            move_x = int((best_match_position[0] - mid_x) / 18)
            move_y = int((best_match_position[1] - mid_y) / 40 + 0.3)
            new_x = int(mid_x + move_x)
            new_y = int(mid_y + move_y)
            distance = calculate_distance(mid_x, mid_y, new_x, new_y)
            pydirectinput.mouseDown()
            pydirectinput.move(move_x, move_y, relative=True)

        else:
            time.sleep(0.01)
            pydirectinput.mouseUp()
except KeyboardInterrupt:
    print("\nScript stopped by user.")
