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

def drawOrbit(eccentricity):
	resolution = 150
	baseRadius = radii[1] * 19
	earth.write('mesh -c 0 -s wire {\n1 ' + str(resolution + 1) + '\n')
	for i in range(resolution + 1):
		arg = (6.28 * i / resolution)
		r = baseRadius * (1 - eccentricity**2) / (1 - eccentricity * math.cos(arg))
		earth.write("%.4f 0 %.4f\n" % (r * math.cos(arg - (3.14 / 2)), r * math.sin(arg - (3.14 / 2))))
	earth.write('}\n\n')

def drawSmallOrbit(r):
	resolution = 150
	orbit.write('mesh -c 0 -s wire {\n1 ' + str(resolution + 1) + '\n')
	for i in range(resolution + 1):
		pos = getPosition(r, i, resolution, 0)
		orbit.write("%.4f 0 %.4f\n" % (pos[0], pos[1]))
	orbit.write('}\n\n')


radii   = [0.05, 2]
periods = [1, 1]
offsets = [0, 3.14]


orbit = open(ORBIT_OUT, "w")
earth = open(EARTH_ORBIT_OUT, "w")

f = open(DATA_OUT, "w")
f.write('datavar  0  color\n')
f.write('datavar  1  lum\n')
f.write('datavar  2  texture\n')

f.write('texture  -O 1  darkPlanet.sgi\n')
f.write('texture  -M 2  colorChanger.sgi\n')
f.write('texture  -M 3  halo.pbm\n')
f.write('texture  -O 4  peg51.sgi\n')
f.write('texturevar 2\n\n')

colorAmplitude1 = getInterpolator(start_x=3150, end_x=4300, power=1, y_lists=[[20, 5]])
colorAmplitude2 = getInterpolator(start_x=4750, end_x=6000, power=1, y_lists=[[5, 20]])
colorAmplitude3 = getInterpolator(start_x=6000, end_x=7000, power=1, y_lists=[[20, 0]])

orbitRadius = getInterpolator(start_x=1150, end_x=1250, power=1, y_lists=[[0, radii[0]]])
pegOrbitRadius = getInterpolator(start_x=8100, end_x=8200, power=2, y_lists=[[radii[1], 10]])

orbitColorOffset = getInterpolator(start_x=3200, end_x=4100, power=2, y_lists=[[0, -3.14 / 2]])

eccentricityUp = getInterpolator(start_x=6900, end_x=7000, power=2, y_lists=[[0, 0.7]])
eccentricityDown = getInterpolator(start_x=7050, end_x=7150, power=2, y_lists=[[0.7, 0]])


HIDDEN = [[0, 3071], [3220, 3231], [3379, 3388]] #Inclusive

for i in range(9000):
	f.write('datatime ' + str(i) + '\n')
	earth.write('datatime ' + str(i) + '\n')
	orbit.write('datatime ' + str(i) + '\n')

	t = 6.28 * (i / 1200) * omega

	if i > 3050:
		drawSmallOrbit(pegOrbitRadius(i)[0])

	arg = (6.28 * (t / periods[0])) - orbitColorOffset(i)[0]
	amp = colorAmplitude1(i)[0]
	if i > 4750:
		amp = colorAmplitude2(i)[0]
	if i > 6000:
		amp = colorAmplitude3(i)[0]

	writeColorChanger(getPosition(orbitRadius(i)[0], t, periods[0], offsets[0]), int(amp * math.cos(arg) + 19), 9000)

	if canShow(i):
		writePeg51(getPosition(radii[1], t, periods[1], offsets[1]), 0.24)

	if i >= 4970:
		e = eccentricityUp(i)[0]
		if i > 7050:
			e = eccentricityDown(i)[0]
		drawOrbit(e)

