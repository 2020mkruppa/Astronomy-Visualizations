import math

DATA_OUT = 'movingStars/movingStars.SPECK'
ORBIT_OUT = 'orbitPaths/orbits.SPECK'
omega = 0.8       #Generally controls how fast the points move, specifically, multiplies globally into each input speed

def writePoint(pos, color, lum, texture): #Motion along x-z plane
	for n in range(2):
		f.write("%.4f 0 %.4f %d %d %d\n" % (pos[0], pos[1], color, lum, texture))

def writeTexture(pos, lum, texture):
	f.write("%.4f 0 %.4f 0 %d %d\n" % (pos[0], pos[1], lum, texture))

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

f = open(DATA_OUT, "w")
f.write('datavar  0  color\n')
f.write('datavar  1  lum\n')
f.write('datavar  2  texture\n')

f.write('texture  -M 1  halo.pbm\n')
f.write('texture  -O 3  mars.sgi\n')
f.write('texture  -O 4  jupiter.sgi\n')
f.write('texture  -M 5  weakHalo.sgi\n')
f.write('texture  -O 2  earth.sgi\n')   #Last to be front-most
f.write('texturevar 2\n\n')

for i in range(4800):
	f.write('datatime ' + str(i) + '\n')
	t = 6.28 * (i / 1200) * omega

	writePoint([0, 0], 0, 160, 1) #Sun
	writePoint(getPosition(radii[0], t, periods[0], offsets[0]), 1, 15, 5) #Mercury
	writePoint(getPosition(radii[1], t, periods[1], offsets[1]), 2, 35, 5) #Venus
	writeTexture(getPosition(radii[2], t, periods[2], offsets[2]), 2, 2) #Earth
	writeTexture(getPosition(radii[3], t, periods[3], offsets[3]), 2, 3) #Mars
	writeTexture(getPosition(radii[4], t, periods[4], offsets[4]), 20, 4) #Jupiter
	writePoint(getPosition(radii[5], t, periods[5], offsets[5]), 3, 160, 5) #Saturn
	writePoint(getPosition(radii[6], t, periods[6], offsets[6]), 4, 160, 5) #Uranus
	writePoint(getPosition(radii[7], t, periods[7], offsets[7]), 5, 160, 5) #Neptune


