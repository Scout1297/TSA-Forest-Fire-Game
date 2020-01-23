from cs1lib import *

WINDOW_HEIGHT = 811
WINDOW_WIDTH = 1012



def main():
    img = load_image("TSAgame.png")
    x = 100
    y = 10
    xl = 0
    xr = 100
    yt = 0
    yb = 100
    while not window_closed():
        clear()
            
        advanced_draw_image(img, x, y, xl, xr, yt, yb)
        request_redraw()
        
        sleep(0.005)

start_graphics(main, "Dartmouth Map", WINDOW_WIDTH, WINDOW_HEIGHT)