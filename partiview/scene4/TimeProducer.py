import math
import sys
sys.path.append("..")
from Interpolator import getInterpolator

DATA_OUT = 'movingStars/movingStars.SPECK'
ORBIT_OUT = 'orbitPaths/orbits.SPECK'
MULTI_OUT = 'multiPlanetOrbits/orbits.SPECK'

def writePrimary(darkness): #Ranges from 0 to 3
	f.write("0.002 -0.001 0.0015 0 0.5 0\n") #Intentionally no texture, so it appears as opaque disc to provide backdrop
	f.write("0 0 0 0 100 %d\n" % (darkness + 5))

def writePlanet(pos, lum, texture):
	#for n in range(2):
	f.write("%.4f 0 %.4f 1 %.4f %d\n" % (pos[0], pos[1], lum, texture))


def getPosition(radius, time, period, offset):
	argument = ((6.28 / period) * time) - offset
	return [radius * math.cos(argument), radius * math.sin(argument)]

def getPositionExplicit(radius, arg):
	return [radius * math.cos(arg), radius * math.sin(arg)]

def inRange(i, ranges):
	for interval in ranges:
		if interval[0] <= i <= interval[1]:
			return True
	return False

def writeOrbit(file, r):
	resolution = 150
	file.write('mesh -c 0 -w 3 -s wire {\n1 ' + str(resolution + 1) + '\n')
	for i in range(resolution + 1):
		pos = getPosition(r, i, resolution, 0)
		file.write("%.4f 0 %.4f\n" % (pos[0], pos[1]))
	file.write('}\n\n')

radii   = [0.2, 0.25, 0.1]
periods = [1.1, 1.3, 0.5]
offsets = [0, 1, 1]


orbit = open(ORBIT_OUT, "w")

multi = open(MULTI_OUT, "w")
writeOrbit(multi, radii[1])
writeOrbit(multi, radii[2])


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
MAIN = [[49, 56], [259, 266], [469, 476], [679, 686], [889, 896], [1100, 1107], [1310, 1317], [1521, 1528],
		[1731, 1738], [1942, 1949], [2152, 2159], [2362, 2369], [2573, 2579], [2783, 2790], [2993, 3000],
		[3204, 3210], [6569, 6574], [6779, 6784], [6990, 6995], [7200, 7205], [7410, 7415], [7620, 7626],
		[7830, 7836], [8005, 8012], [8110, 8118], [8216, 8223], [8321, 8329]]     #Period 210 width 5

INNER = [[6727, 6734], [6822, 6829], [6918, 6925], [7013, 7020], [7108, 7115], [7203, 7210], [7298, 7305],
		 [7393, 7400], [7488, 7495], [7583, 7590]] #Period 95, width 7
OUTER = [[6810, 6814], [7058, 7062], [7307, 7311], [7555, 7560]] #Period 248, width 4

jupiter = getInterpolator(start_x=3600, end_x=4100, power=1, y_lists=[[0.1, -0.1]])
earth = getInterpolator(start_x=3650, end_x=4150, power=1, y_lists=[[0.1, -0.1]])

mainPlanet = getInterpolator(start_x=7900, end_x=8050, power=2, y_lists=[[radii[0], radii[0]/2], [0.005, 0.03], [6.28/210.19, 2*6.28/210.19], [1, 3]])
#																			orbital radius         planet lum         angle step           darkness score
angle = 0
for i in range(9400):
	f.write('datatime ' + str(i) + '\n')
	orbit.write('datatime ' + str(i) + '\n')
	t = 6.28 * (i / 1200)


	writePlanet(getPositionExplicit(mainPlanet(i)[0], angle), mainPlanet(i)[1], 1 if inRange(i, MAIN) else 2)
	angle += mainPlanet(i)[2]


	if 3600 < i < 4150:
		writePlanet([jupiter(i)[0], 0.03], 0.001, 1)
		writePlanet([earth(i)[0], 0.016], 0.00005, 1)

	if 7600 > i > 6650:
		writePlanet(getPosition(radii[1], t, periods[1], offsets[1]), 0.01, 1 if inRange(i, OUTER) else 3)
		writePlanet(getPosition(radii[2], t, periods[2], offsets[2]), 0.005, 1 if inRange(i, INNER) else 4)

	writeOrbit(orbit, mainPlanet(i)[0])
	darknessScore = 0
	for ranges in [MAIN, INNER, OUTER]:
		if inRange(i, ranges):
			darknessScore += 1
	if i >= 7900 and darknessScore > 0:
		darknessScore = int(mainPlanet(i)[3])
	writePrimary(darknessScore)
