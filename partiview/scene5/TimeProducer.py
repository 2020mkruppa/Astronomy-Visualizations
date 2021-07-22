import math
import sys
sys.path.append("..")
from Interpolator import getInterpolator

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
	file.write('mesh -c 0 -s wire {\n1 ' + str(resolution + 1) + '\n')
	for i in range(resolution + 1):
		pos = getPosition(r, i, resolution, 0)
		file.write("%.4f 0 %.4f\n" % (pos[0], pos[1]))
	file.write('}\n\n')

radii   = [0.2, 0.25, 0.1]
periods = [1.1, 1.3, 0.5]
offsets = [0, 1, 1]


multi = open(MULTI_OUT, "w")
writeOrbit(multi, radii[1])
writeOrbit(multi, radii[2])


#Period 210

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
