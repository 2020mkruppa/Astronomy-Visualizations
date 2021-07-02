import math

DATA_OUT = 'movingStars/movingStars.SPECK'
ORBIT_OUT = 'orbitPaths/orbits.SPECK'

def writeColorChanger(pos, color, lum): #Motion along x-z plane
	for n in range(2):
		f.write("%.4f %.4f 0 %d %d 2\n" % (pos[0], pos[1], color, lum))

def writeDarkPlanet(pos, lum):
	for n in range(2):
		f.write("%.4f 0 %.4f 0 %.4f 1\n" % (pos[0], pos[1], lum))

def writeStar(pos, color, lum):
	for n in range(2):
		f.write("%.4f 0 %.4f %d %d 3\n" % (pos[0], pos[1], color, lum))

def writeOrbitStar(pos, color, lum):
	for n in range(2):
		f.write("%.4f %.4f 0 %d %d 3\n" % (pos[0], pos[1], color, lum))

def writeRadius(r):
	resolution = 100
	orbit.write('mesh -c 0 -s wire {\n1 ' + str(resolution + 1) + '\n')
	for i in range(resolution + 1):
		pos = getPosition(r, ((6.28 / resolution) * i))
		orbit.write("%.4f %.4f 0\n" % (pos[0], pos[1]))
	orbit.write('}\n')


def getPosition(radius, argument):
	return [radius * math.cos(argument), radius * math.sin(argument)]


def polynomial_smoothing(start_t, end_t, start_y, end_y, t, power):
	t_diff = end_t - start_t
	y_diff = end_y - start_y
	if t <= (start_t + end_t) / 2.0:
		scale = (2**(power - 1)) * y_diff / (t_diff**power)
		return (scale * ((t - start_t)**power)) + start_y
	else:
		scale = (2 ** (power - 1)) * y_diff * -1 / ((-1 * t_diff) ** power)
		return (scale * ((t - end_t) ** power)) + end_y

def getChangingMass(t):
	if t < START_SIZE:
		return MID_MASS
	if t > END_SIZE:
		return MIN_MASS
	if t <= MIDDLE_SIZE:
		return polynomial_smoothing(start_t=START_SIZE, end_t=MIDDLE_SIZE, start_y=MID_MASS, end_y=MAX_MASS, t=t, power=2)
	return polynomial_smoothing(start_t=MIDDLE_SIZE, end_t=END_SIZE, start_y=MAX_MASS, end_y=MIN_MASS, t=t, power=2)

def getChangingRadius(m):
	return CONSTANT_MASS * CONSTANT_RADIUS / m

def getChangingPeriod(m1, m2, r1, r2):
	return 400 * math.sqrt(((r1 + r2)**3) / (m1 + m2))


orbit = open(ORBIT_OUT, "w")
f = open(DATA_OUT, "w")
f.write('datavar  0  color\n')
f.write('datavar  1  lum\n')
f.write('datavar  2  texture\n')

f.write('texture  -O 1  darkPlanet.sgi\n')
f.write('texture  -M 2  colorChanger.sgi\n')
f.write('texture  -M 3  halo.pbm\n')
f.write('texturevar 2\n\n')

START_SIZE = 2000
MIDDLE_SIZE = 2300
END_SIZE = 2700

CONSTANT_MASS = 10
CONSTANT_RADIUS = 0.05

MID_MASS = 3
MAX_MASS = 10
MIN_MASS = 1

timestep = 0.08
angle = 0
for i in range(4000):
	f.write('datatime ' + str(i) + '\n')
	orbit.write('datatime ' + str(i) + '\n')

	writeStar([150.5, 0], 40, 500)
	writeDarkPlanet([151, 0], 0.02)

	m1 = getChangingMass(i)
	r1 = getChangingRadius(m1)
	T = getChangingPeriod(m1, CONSTANT_MASS, r1, CONSTANT_RADIUS)
	deltaAngle = 6.28 * timestep / T
	angle += deltaAngle



	#amplitude = 20 * (min(END_COLOR_CHANGE, max(START_COLOR_CHANGE, i)) - START_COLOR_CHANGE) / (END_COLOR_CHANGE - START_COLOR_CHANGE)
	if i > 1500:
		writeOrbitStar(getPosition(CONSTANT_RADIUS, angle), 40, 35)
		writeOrbitStar(getPosition(r1, angle + 3.14), 41, 35 * (m1 / CONSTANT_MASS)**2)
		writeRadius(CONSTANT_RADIUS)
		writeRadius(r1)
	#writeColorChanger(getPosition(radii[0], t, periods[0], offsets[0]), int(-amplitude * math.cos(6.28 * (t / periods[0])) + 19), 2500)

	#if canShow(i):
	#	writePeg51(getPosition(radii[1], t, periods[1], offsets[1]), 0.1)



