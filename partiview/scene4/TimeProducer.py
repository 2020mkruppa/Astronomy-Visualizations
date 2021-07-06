import math
import sys
sys.path.append("..")
from Interpolator import getInterpolator

DATA_OUT = 'movingStars/movingStars.SPECK'
ORBIT_OUT = 'orbitPaths/orbits.SPECK'


def writePrimary(bright):
	if bright:
		f.write("0 0 0 0 2500 1\n")
	else:
		f.write("0 0 0 0 2500 2\n")

def writePlanet(pos, lum, texture):
	#for n in range(2):
	f.write("%.4f 0 %.4f 0 %.4f %d\n" % (pos[0], pos[1], lum, texture))


def getPosition(radius, time, period, offset):
	argument = ((6.28 / period) * time) - offset
	return [radius * math.cos(argument), radius * math.sin(argument)]

def inRange(i, ranges):
	for interval in ranges:
		if interval[0] <= i <= interval[1]:
			return True
	return False

radii   = [0.7]
periods = [1.1]
offsets = [0]


orbit = open(ORBIT_OUT, "w")
resolution = 150
for r in radii:
	orbit.write('mesh -c 0 -s wire {\n1 ' + str(resolution + 1) + '\n')
	for i in range(resolution + 1):
		pos = getPosition(r, i, resolution, 0)
		orbit.write("%.4f 0 %.4f\n" % (pos[0], pos[1]))
	orbit.write('}\n\n')



f = open(DATA_OUT, "w")
f.write('datavar  0  color\n')
f.write('datavar  1  lum\n')
f.write('datavar  2  texture\n')

f.write('texture  -O 3  silhouette.sgi\n')
f.write('texture  -O 4  peg51.sgi\n')
f.write('texture  -M 1  bright.sgi\n')
f.write('texture  -M 2  dark.sgi\n')

f.write('texturevar 2\n\n')

HIDDEN = [[1295, 1980]] #Hidden around the back
DARK = [[47, 58], [257, 268], [467, 478], [678, 688], [890, 898], [1101, 1107]]     #Silhouette

jupiter = getInterpolator(start_x=1450, end_x=1950, power=1, y_lists=[[0.5, -0.5]])
earth = getInterpolator(start_x=1500, end_x=2000, power=1, y_lists=[[0.5, -0.5]])

for i in range(4800):
	f.write('datatime ' + str(i) + '\n')
	t = 6.28 * (i / 1200)

	if inRange(i, DARK):
		writePlanet(getPosition(radii[0], t, periods[0], offsets[0]), 0.1, 3)
	elif not inRange(i, HIDDEN):
		writePlanet(getPosition(radii[0], t, periods[0], offsets[0]), 0.1, 4)

	writePrimary(not inRange(i, DARK))

	if 1450 < i < 2000:
		writePlanet([jupiter(i)[0], 0.05], 0.07, 3)
		writePlanet([earth(i)[0], 0.05], 0.002, 3)



