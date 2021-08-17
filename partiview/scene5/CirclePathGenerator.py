import math
import sys
sys.path.append("..")
from Interpolator import getInterpolator

THETA_START = math.pi / 4
THETA_END = 7 * math.pi / 4

p1 = getInterpolator(start_x=THETA_START, end_x=THETA_END, power=1, y_lists=[[52, 39], [15, 12.5], [0.32, 0.22]]) #radius, y coord, vel

def getData(theta):
	return p1(theta)

angle = THETA_START
straight = True
while angle < THETA_END:
	r, y, vel = getData(angle)
	print("%.4f %.4f %.4f \t\t %.4f %s 0 0 0" % (r * math.sin(angle), y, r * math.cos(angle), vel, "s" if straight else "c"))
	straight = not straight
	angle += 0.04

'''

0 15 45              0.3  c 0 0 0
0 10 -37           0.3  s 0 0 0
-15 10 -30           0.2  c 0 0 0
-25 0 30           0.1  s 0 0 0
-20 0  60           0.03  s 0 0 0
'''