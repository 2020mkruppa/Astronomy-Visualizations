import math


COLOR_IN = 'movingStars/colors.cmap'
DATA_OUT = 'movingStars/movingStars.SPECK'
ORBIT_OUT = 'orbitPaths/orbits.SPECK'
omega = 0.8       #Generally controls how fast the points move, specifically, multiplies globally into each input speed

def findRGBSize():
	colors = open(COLOR_IN, "r")
	discardFirst = True
	intensities = []
	for line in colors.readlines():
		if discardFirst:
			discardFirst = False
			continue
		parts = line.split(" ")
		intensities.append(float(parts[0])**2 + float(parts[1])**2 + float(parts[2])**2)
	return intensities

def writePoint(pos, color, lum, texture): #Motion along x-z plane
	#for n in range(2):
	f.write("%.4f 0 %.4f %d %d %d\n" % (pos[0], pos[1], color, 120, 2))
	f.write("%.4f 0 %.4f %d %d %d\n" % (pos[0], pos[1], color, 120, 2))

	#f.write("%.4f 0 %.4f %d %d %d\n" % (pos[0], pos[1], 40, 60, 1))
	#f.write("%.4f 0 %.4f %d %d %d\n" % (pos[0], pos[1], 40, 60, 1))


def writeTexture(pos, color, lum, texture):
	f.write("%.4f 0 %.4f %d %d %d\n" % (pos[0], pos[1], color, lum, texture))
	f.write("%.4f 0 %.4f %d %d %d\n" % (pos[0], pos[1], color, lum, texture))

def getPosition(radius, time, period, offset):
	argument = ((6.28 / period) * time) - offset
	return [radius * math.cos(argument), radius * math.sin(argument)]





radii   = [0.39, 0.72, 1.00, 1.52, 5.20, 9.54, 19.2, 30.1] #Real life
periods = [0.24, 0.62, 1.00, 1.88, 11.8, 29.5, 84.0, 165]  #Real life
offsets = [5.91, 2.6, 3.14 * 1.5, 4.5, 4.84, 6.19, 4.63, 2.11] #randomly generated except earth


orbit = open(ORBIT_OUT, "w")
resolution = 150
for r in radii:
	orbit.write('mesh -c 0 -s wire {\n1 ' + str(resolution + 2) + '\n')
	for i in range(resolution + 2):
		pos = getPosition(r, i, resolution, 0)
		orbit.write("%.4f 0 %.4f\n" % (pos[0], pos[1]))
	orbit.write('}\n\n')


sizes = findRGBSize()

f = open(DATA_OUT, "w")
f.write('datavar  0  color\n')
f.write('datavar  1  lum\n')
f.write('datavar  2  texture\n')

f.write('texture  -M 1  haloCenter.sgi\n')
f.write('texture  -M 2  haloAround.sgi\n')
f.write('texturevar 2\n\n')

for i in range(4800):
	f.write('datatime ' + str(i) + '\n')
	t = 6.28 * (i / 1200) * omega

	writePoint([0, 0], int(20 * math.sin(6.28 * (i / 60)) + 20), 160, 1) #Sun
	#writePoint(getPosition(radii[0], t, periods[0], offsets[0]), 1, 15, 5) #Mercury
	#writePoint(getPosition(radii[1], t, periods[1], offsets[1]), 2, 35, 5) #Venus
	#writeTexture([0.4, 0.4], int(20 * math.sin(6.28 * (i / 60)) + 20), 2, 1) #Earth



