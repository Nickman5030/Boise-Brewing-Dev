import pygame as pg
import numpy as np
import sys
from freenect import sync_get_depth as get_depth


def make_gamma():
    """
    Create a gamma table
    """
    num_pix = 2048 # There's 2048 different possible depth values
    npf = float(num_pix)
    _gamma = np.empty((num_pix, 3), dtype=np.uint16)
    for i in range(num_pix):
        v = i / npf
        v = pow(v, 3) * 6
        pval = int(v * 6 * 256)
        lb = pval & 0xff
        pval >> 8
        if pval == 0:
            a = np.array([255, 255 - lb, 255 - lb], dtype=np.uint8)
        elif pval == 1:
            a = np.array([255, lb, 0], dtype=np.uint8)
        elif pval == 2:
            a = np.array([255 - lb, lb, 0], dtype=np.uint8)
        elif pval == 3:
            a = np.array([255 - lb, 255, 0], dtype=np.uint8)
        elif pval == 4:
            a = np.array([0, 255 - lb, 255], dtype=np.uint8)
        elif pval == 5:
            a = np.array([0, 0, 255 - lb], dtype=np.uint8)
        else:
            a = np.array([0, 0, 0], dtype=np.uint8)

        _gamma[i] = a
    return _gamma


gamma = make_gamma()

if __name__=="__main__":
    fpsClock = pg.time.Clock()
    FPS = 30 # Kinect only ouputs 30 fps
    disp_size = (640, 480)
    pg.init()
    screen = pg.display.set_mode(disp_size)
    font = pg.font.SysFont("comicsansms", 32) # Provide own font
    while True:
        events = pg.event.get()
        for e in events:
            if e.type == pg.QUIT:
                sys.exit()
        fps_text = f"FPS: {fpsClock.get_fps():.2f}"
        # draw the pixels

        depth = np.rot90(get_depth()[0])  # get the depth readings from the camera
        pixels = gamma[depth]  # The color pixels are the depth readings overlayed onto the gamma table
        temp_surface = pg.Surface(disp_size)
        pg.surfarray.blit_array(temp_surface, pixels)
        pg.transform.scale(temp_surface, disp_size, screen)
        screen.blit(font.render(fps_text, 1, (255, 255, 255)), (30, 30))
        pg.display.flip()
        fpsClock.tick(FPS)
