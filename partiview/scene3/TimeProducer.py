import math

DATA_OUT = 'movingStars/movingStars.SPECK'
ORBIT_OUT = 'orbitPaths/orbits.SPECK'
omega = 0.8       #Generally controls how fast the points move, specifically, multiplies globally into each input speed


def writeColorChanger(pos, color, lum): #Motion along x-z plane
	for n in range(2):
		f.write("%.4f %.4f 0 %d %d 2\n" % (pos[0], pos[1], color, lum))

def writePeg51(pos, lum):
	for n in range(2):
		f.write("%.4f %.4f 0 0 %.2f 4\n" % (pos[0], pos[1], lum))


def writeDarkPlanet(pos, lum):
	for n in range(2):
		f.write("%.4f 0 %.4f 0 %.4f 1\n" % (pos[0], pos[1], lum))

def writeStar(pos, color, lum):
	for n in range(2):
		f.write("%.4f 0 %.4f %d %d 3\n" % (pos[0], pos[1], color, lum))

def getPosition(radius, time, period, offset):
	argument = ((6.28 / period) * time) - offset
	return [radius * math.cos(argument), radius * math.sin(argument)]

def canShow(i):
	for interval in HIDDEN:
		if interval[0] <= i <= interval[1]:
			return False
	return True

radii   = [0.15, 1]
periods = [1, 1]
offsets = [0, 3.14]


orbit = open(ORBIT_OUT, "w")
resolution = 150
for r in radii:
	orbit.write('mesh -c 0 -s wire {\n1 ' + str(resolution + 1) + '\n')
	for i in range(resolution + 1):
		pos = getPosition(r, i, resolution, 0)
		orbit.write("%.4f %.4f 0\n" % (pos[0], pos[1]))
	orbit.write('}\n\n')


f = open(DATA_OUT, "w")
f.write('datavar  0  color\n')
f.write('datavar  1  lum\n')
f.write('datavar  2  texture\n')

f.write('texture  -O 1  darkPlanet.sgi\n')
f.write('texture  -M 2  colorChanger.sgi\n')
f.write('texture  -M 3  halo.pbm\n')
f.write('texture  -O 4  peg51.sgi\n')
f.write('texturevar 2\n\n')

START_COLOR_CHANGE = 2300
END_COLOR_CHANGE = 2800

HIDDEN = [[2802, 2813], [3041, 3052], [3280, 3291]] #Inclusive

for i in range(4800):
	f.write('datatime ' + str(i) + '\n')
	t = 6.28 * (i / 1200) * omega

	writeStar([150.5, 0], 42, 500)
	writeDarkPlanet([151, 0], 0.02)

	amplitude = 20 * (min(END_COLOR_CHANGE, max(START_COLOR_CHANGE, i)) - START_COLOR_CHANGE) / (END_COLOR_CHANGE - START_COLOR_CHANGE)

	writeColorChanger(getPosition(radii[0], t, periods[0], offsets[0]), int(-amplitude * math.cos(6.28 * (t / periods[0])) + 19), 2500)

	if canShow(i):
		writePeg51(getPosition(radii[1], t, periods[1], offsets[1]), 0.1)



