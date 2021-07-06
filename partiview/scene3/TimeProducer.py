import math
import sys
sys.path.append("..")
from Interpolator import getInterpolator

DATA_OUT = 'movingStars/movingStars.SPECK'
ORBIT_OUT = 'orbitPaths/orbits.SPECK'
EARTH_ORBIT_OUT = 'earthOrbit/orbits.SPECK'
omega = 1.2       #Generally controls how fast the points move, specifically, multiplies globally into each input speed


def writeColorChanger(pos, color, lum): #Motion along x-z plane
	for n in range(2):
		f.write("%.4f 0 %.4f %d %d 2\n" % (pos[0], pos[1], color, lum))

def writePeg51(pos, lum):
	for n in range(2):
		f.write("%.4f 0 %.4f 0 %.2f 4\n" % (pos[0], pos[1], lum))


def getPosition(radius, time, period, offset):
	argument = ((6.28 / period) * time) - offset
	return [radius * math.cos(argument), radius * math.sin(argument)]

def canShow(i):
	for interval in HIDDEN:
		if interval[0] <= i <= interval[1]:
			return False
	return True

radii   = [0.05, 1.05]
periods = [1, 1]
offsets = [0, 3.14]


orbit = open(ORBIT_OUT, "w")
resolution = 150
for r in radii:
	orbit.write('mesh -c 0 -s wire {\n1 ' + str(resolution + 1) + '\n')
	for i in range(resolution + 1):
		pos = getPosition(r, i, resolution, 0)
		orbit.write("%.4f 0 %.4f\n" % (pos[0], pos[1]))
	orbit.write('}\n\n')

earth = open(EARTH_ORBIT_OUT, "w")
resolution = 150
earth.write('mesh -c 0 -s wire {\n1 ' + str(resolution + 1) + '\n')
for i in range(resolution + 1):
	pos = getPosition(19, i, resolution, 0)
	earth.write("%.4f 0 %.4f\n" % (pos[0], pos[1]))
earth.write('}\n\n')


f = open(DATA_OUT, "w")
f.write('datavar  0  color\n')
f.write('datavar  1  lum\n')
f.write('datavar  2  texture\n')

f.write('texture  -O 1  darkPlanet.sgi\n')
f.write('texture  -M 2  colorChanger.sgi\n')
f.write('texture  -M 3  halo.pbm\n')
f.write('texture  -O 4  peg51.sgi\n')
f.write('texturevar 2\n\n')

colorAmplitude = getInterpolator(start_x=1000, end_x=1500, power=1, y_lists=[[20, 0]])
orbitRadius = getInterpolator(start_x=400, end_x=500, power=1, y_lists=[[0, radii[0]]])

HIDDEN = [[0, 1001], [2802, 2813]] #Inclusive

for i in range(4800):
	f.write('datatime ' + str(i) + '\n')
	t = 6.28 * (i / 1200) * omega

	writeColorChanger(getPosition(orbitRadius(i)[0], t, periods[0], offsets[0]), int(colorAmplitude(i)[0] * math.cos(6.28 * (t / periods[0])) + 19), 2500)

	if canShow(i):
		writePeg51(getPosition(radii[1], t, periods[1], offsets[1]), 0.1)



