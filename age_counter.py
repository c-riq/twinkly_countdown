
from time import sleep
from xled_plus.discoverall import *
from xled_plus.highcontrol import HighControlInterface
from xled_plus.ledcolor import *
from xled_plus.shapes import *

import time
import random


devdict = controldict(discover_all())
if len(devdict.keys()) == 1:
    iplst = devdict[list(devdict.keys())[0]]

ctr = HighControlInterface(iplst[0])

cc = ControlInterface(iplst[0])

cc.set_mode("rt")

def place_text(scene, txt, size1=0.87, speed=2, line_thickness=0.26):
    # Adapted from https://github.com/Anders-Holst/xled_plus/blob/master/xled_plus/shapes.py RunningText.place_text
    bounds = scene.get_scene_bounds()
    # Size is relative the total height of leds, convert to relative radius
    size = size1 * abs((bounds[1][1] - bounds[1][0]))
    # Speed is in letter heights per second, convert to length per step
    speed = 0.5
    currx = bounds[0][1] - 0.01  # Shifted slightly to the right
    endx = bounds[0][0]
    liney = -size / 1.7
    for ind, ch in enumerate(txt):
        color = (0, 0, 0) if ch == '0' and ind == 0 else ((10-ind) * 20, ind * 20, 255)
        sh = Letter(ch, (0, liney), 0, size, color)
        sh.lw = line_thickness
        sh.off[0] = -currx + (sh.extent[0] - sh.lw * 0.5) * size
        sh.off[1] = -liney
        sh.set_speed(-speed, 0.0)
        wdt = sh.extent[2] - sh.extent[0] + 2 * sh.lw
        #currx += 1.0395 * 0.2
        currx += 1.0569 * 0.2
        #currx += wdt * size
        scene.add_shape(sh)
    scene.nsteps = int(round((currx - endx) / speed + 0.5))
    scene.time = 1

scene = Scene(ctr=ctr)
ctr.adjust_layout_aspect(11)

for i in range(0, 10000):
    scene.shapes = []
    t = int(time.time())
    t = int(t) - 729414060
    t = t + 10 # due to leap seconds between 1993 and now not captured in unix time
    #t = int(t) - 729414060 + 604800 + (3600 * 18) # 1 week
    #t = int(1e9) - 5 + i
    t = str(t)
    #t = t + '.' + str(int(time.time() % 10))
    if len(t) == 9:
        t = '0' + t
    print(t)

    place_text(scene, t)
    scene.update(4)
    pattern = ctr.make_layout_pattern(scene.get_color, style="centered", index=True)
    cc.set_rt_frame_socket(ctr.to_movie(pattern),3)
    sleep(0.99)
