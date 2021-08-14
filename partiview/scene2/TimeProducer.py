import math
import sys
sys.path.append("..")
from Interpolator import getInterpolator
from OrbitDrawer import drawOrbitXZ
from OrbitDrawer import drawOrbitXY

DATA_OUT = 'movingStars/movingStars.SPECK'
ORBIT_OUT = 'orbitPaths/orbits.SPECK'


def writeDarkPlanet(pos, lum):
	for n in range(2):
		f.write("%.4f 0 %.4f 0 %.4f 1\n" % (pos[0], pos[1], lum))

def writeStar(pos, color, lum):
	for n in range(2):
		f.write("%.4f 0 %.4f %d %d 3\n" % (pos[0], pos[1], color, lum))

def writeOrbitStar(pos, color, lum):
	for n in range(2):
		f.write("%.4f %.4f 0 %d %d 2\n" % (pos[0], pos[1], color, lum))

def writeLinearStar(pos, color, lum):
	for n in range(2):
		f.write("%.4f %.4f %.4f %d %d 2\n" % (pos[0], pos[1], pos[2], color, lum))

def writeSun(pos):
	for n in range(2):
		f.write("%.4f 0 %.4f %d %d 3\n" % (pos[0], pos[1], 40, 400))

def writeSunOrbit(r):
	drawOrbitXZ(r, orbit)

def writeRadius(r):
	drawOrbitXY(r, orbit)


def getPosition(radius, argument):
	return [radius * math.cos(argument), radius * math.sin(argument)]


orbit = open(ORBIT_OUT, "w")
f = open(DATA_OUT, "w")
f.write('datavar  0  color\n')
f.write('datavar  1  lum\n')
f.write('datavar  2  texture\n')

f.write('texture  -O 1  darkPlanet.sgi\n')
f.write('texture  -M 2  colorChanger.sgi\n')
f.write('texture  -M 3  halo.pbm\n')
f.write('texturevar 2\n\n')

#																				  S1 Lum   S2 Lum     S1 Radius    S2 Radius    Period
sizeInterpolator = getInterpolator(start_x=4050, end_x=5000, power=2, y_lists=[[30, 15], [30, 800], [0.05, 0.45], [0.05, 0.05], [5.5, 17]])
colorAmplitude = getInterpolator(start_x=7850, end_x=8050, power=1, y_lists=[[0, 20], [0, 20]]) #S1, S2

linearStar = getInterpolator(start_x=5710, end_x=8210, power=1, y_lists=[[-8, 8], [4.35, -4.00], [-7.5, 8.5]])
linearColor = getInterpolator(start_x=6945, end_x=7030, power=1, y_lists=[[39, 0]])

orbitRadius = getInterpolator(start_x=10100, end_x=10200, power=3, y_lists=[[0.8, 0.006]])

timestep = 0.08
angle = 0
for i in range(11600):
	f.write('datatime ' + str(i) + '\n')
	orbit.write('datatime ' + str(i) + '\n')

	writeStar([250.5, 0], 40, 500)
	writeDarkPlanet([251, 0], 0.02)

	data = sizeInterpolator(i)

	deltaAngle = math.pi * 2 * timestep / data[4]
	angle += deltaAngle

	colors = colorAmplitude(i)
	if 2000 < i < 9800:
		writeRadius(data[2])
		writeRadius(data[3])
		writeOrbitStar(getPosition(data[2], angle), int(-colors[0] * math.cos(angle) + 19), data[0]) #S1
		writeOrbitStar(getPosition(data[3], angle + 3.14), int(colors[1] * math.cos(angle) + 19), data[1]) #S2

		writeLinearStar(linearStar(i), linearColor(i)[0], 10) #Linear doppler shift star

	if 9850 < i:
		writeSunOrbit(orbitRadius(i)[0])
		writeSun(getPosition(orbitRadius(i)[0], angle))




