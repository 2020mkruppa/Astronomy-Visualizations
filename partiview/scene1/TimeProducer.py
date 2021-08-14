import math
import sys
sys.path.append("..")
from OrbitDrawer import drawOrbitXZ

DATA_OUT = 'movingStars/movingStars.SPECK'
ORBIT_OUT = 'orbitPaths/orbits.SPECK'
omega = 1.2       #Generally controls how fast the points move, specifically, multiplies globally into each input speed

def writePoint(pos, color, lum, texture): #Motion along x-z plane
	for n in range(2):
		f.write("%.4f 0 %.4f %d %d %d 9 9 9 9 9 9\n" % (pos[0], pos[1], color, lum, texture))

def writeTexture(pos, lum, texture):
	if texture == 11 or texture == 12:
		f.write("%.4f 0 %.4f 0 %.4f %d 1 0 0 0 -0.5 0.866\n" % (pos[0], pos[1], lum, texture))
	else:
		f.write("%.4f 0 %.4f 0 %.4f %d 9 9 9 9 9 9\n" % (pos[0], pos[1], lum, texture))

def getPosition(radius, time, period, offset):
	argument = ((math.pi * 2 / period) * time) + offset
	return [radius * math.cos(argument), radius * math.sin(argument)]

radii   = [0.39, 0.72, 1.00, 1.52, 5.20, 9.54, 19.2, 30.1] #Real life
periods = [0.24, 0.62, 1.00, 1.88, 11.8, 29.5, 84.0, 165]  #Real life
offsets = [2.6, 2.6, 0, 0.55, 1.335, 2.94, 2, 0]


orbit = open(ORBIT_OUT, "w")
resolution = 15
for r in radii:
	drawOrbitXZ(r, orbit)

f = open(DATA_OUT, "w")
f.write('datavar  0  color\n')
f.write('datavar  1  lum\n')
f.write('datavar  2  texture\n')

f.write('texture  -M 1  halo.pbm\n')
f.write('texture  -O 3  mars.sgi\n')
f.write('texture  -O 4  jupiter.sgi\n')
f.write('texture  -M 5  weakHalo.sgi\n')
f.write('texture  -O 6  mercury.sgi\n')
f.write('texture  -O 7  venus.sgi\n')
f.write('texture  -M 11  rings1.sgi\n')
f.write('texture  -O 8  saturn.sgi\n')
f.write('texture  -M 12  rings2.sgi\n')
f.write('texture  -O 9  uranus.sgi\n')
f.write('texture  -O 10  neptune.sgi\n')

f.write('texture  -O 2  earthFinal.sgi\n')   #Last to be front-most
f.write('texturevar 2\n\n')

for i in range(4800):
	f.write('datatime ' + str(i) + '\n')
	t = math.pi * 2 * (i / 1200) * omega

	writePoint([0, 0], 0, 160, 1) #Sun
	writeTexture(getPosition(radii[0], t, periods[0], offsets[0]), 0.7, 6) #Mercury
	writeTexture(getPosition(radii[1], t, periods[1], offsets[1]), 1, 7) #Venus
	writeTexture(getPosition(radii[2], t, periods[2], offsets[2]), 2, 2) #Earth
	writeTexture(getPosition(radii[3], t, periods[3], offsets[3]), 2, 3) #Mars
	writeTexture(getPosition(radii[4], t, periods[4], offsets[4]), 25, 4) #Jupiter

	writeTexture(getPosition(radii[5], t, periods[5], offsets[5]), 44, 11)  # Saturn
	writeTexture(getPosition(radii[5], t, periods[5], offsets[5]), 30, 8)  # Saturn
	writeTexture(getPosition(radii[5], t, periods[5], offsets[5]), 44, 12)  # Saturn

	writeTexture(getPosition(radii[6], t, periods[6], offsets[6]), 30, 9)  #Uranus
	writeTexture(getPosition(radii[7], t, periods[7], offsets[7]), 30, 10)  #Neptune


