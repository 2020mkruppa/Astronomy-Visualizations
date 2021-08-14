import math
import sys
sys.path.append("..")
from Interpolator import getInterpolator
from OrbitDrawer import drawOrbitXZ

DATA_OUT = 'movingStars/movingStars.SPECK'
ORBIT_OUT = 'orbitPaths/orbits.SPECK'

def writePrimary(darkness): #Ranges from 0 to 3
	f.write("0.002 -0.001 0.0015 0 0.5 0\n") #Intentionally no texture, so it appears as opaque disc to provide backdrop
	f.write("0 0 0 0 100 %d\n" % (darkness + 5))

def writePlanet(pos, lum, texture):
	#for n in range(2):
	f.write("%.4f 0 %.4f 1 %.4f %d\n" % (pos[0], pos[1], lum, texture))


def getPosition(radius, time, period, offset):
	argument = ((math.pi * 2 / period) * time) - offset
	return [radius * math.cos(argument), radius * math.sin(argument)]

def getPositionExplicit(radius, arg):
	return [radius * math.cos(arg), radius * math.sin(arg)]

def inRange(i, ranges):
	for interval in ranges:
		if interval[0] <= i <= interval[1]:
			return True
	return False

def writeOrbit(file, r):
	drawOrbitXZ(r, file)

radii   = [0.2, 0.25, 0.1]
periods = [1.1, 1.3, 0.5]
offsets = [0, 1, 1]


orbit = open(ORBIT_OUT, "w")


f = open(DATA_OUT, "w")
f.write('datavar  0  color\n')
f.write('datavar  1  lum\n')
f.write('datavar  2  texture\n')

f.write('texture  -O 1  silhouette.sgi\n')
f.write('texture  -O 2  peg51.sgi\n')
f.write('texture  -O 3  mercury.sgi\n')
f.write('texture  -O 4  venus.sgi\n')

f.write('texture  -M 5  dark0.sgi\n')
f.write('texture  -M 6  dark1.sgi\n')
f.write('texture  -M 7  dark2.sgi\n')
f.write('texture  -M 8  dark3.sgi\n')

f.write('texturevar 2\n\n')
#Period 210
MAIN = [[49, 56], [259, 266], [469, 477], [679, 687], [889, 897], [1100, 1108], [1310, 1318], [1521, 1529],
		[1731, 1739], [1942, 1949], [2153, 2158],

		[4888, 4891], [5098, 5102], [5308, 5312],
		[6359, 6364], [6568, 6575], [6778, 6785], [6989, 6996], [7198, 7206],

		[7395, 7402], [7505, 7513], [7610, 7618], [7715, 7723], [7820, 7829], [7926, 7934]]     #Period 210 width 5

mainPlanet = getInterpolator(start_x=7320, end_x=7470, power=2, y_lists=[[radii[0], radii[0]/2], [0.005, 0.03], [6.28/210.19, 2*6.28/210.19], [1, 3]])
#																			orbital radius         planet lum         angle step           darkness score
angle = 0
for i in range(8400):
	f.write('datatime ' + str(i) + '\n')
	orbit.write('datatime ' + str(i) + '\n')
	t = math.pi * 2 * (i / 1200)


	writePlanet(getPositionExplicit(mainPlanet(i)[0], angle), mainPlanet(i)[1], 1 if inRange(i, MAIN) else 2)
	angle += mainPlanet(i)[2]

	writeOrbit(orbit, mainPlanet(i)[0])
	darknessScore = 1 if inRange(i, MAIN) else 0
	if i >= 7320 and darknessScore > 0:
		darknessScore = int(mainPlanet(i)[3])
	writePrimary(darknessScore)
