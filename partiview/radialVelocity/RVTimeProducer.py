import math

DATA_OUT = 'movingStars/movingStars.SPECK'
omega = 4       #Generally controls how fast the camera moves, specifically, multiplies globally into each iput speed

def writeStar(xPos, yPos, lum):
	for n in range(2):
		f.write("%.4f %.4f %.4f 0 %.1f 1\n" % (xPos, yPos, 0, lum))

def writePlanet(xPos, yPos):
	f.write("%.4f %.4f %.4f 1 40 2\n" % (xPos, yPos, 0))
	#f.write("%.4f %.4f %.4f 1 40 2\n" % (xPos, yPos, 0))

f = open(DATA_OUT, "w")
f.write('datavar  0  color\n')
f.write('datavar  1  lum\n')
f.write('datavar  2  texture\n')
f.write('texture  -M 1  halo.pbm\n')
f.write('texture -O 2  earth.sgi\n')
f.write('texturevar 2\n\n')
for i in range(1200):
	f.write('datatime ' + str(i) + '\n')
	theta = 6.28 * (i / 1200)
	writeStar(0.07 * math.cos(omega * theta), 0.07 * math.sin(omega * theta), 20 + 15 * math.sin(3 * omega * theta))
	writePlanet(0.4 * math.cos((omega * theta) - math.pi), 0.4 * math.sin((omega * theta) - math.pi))

