import math

SUB_DIRECTORY = 'radialVelocity'
DATA_SOURCE = '../' + SUB_DIRECTORY + '/timeData.txt'
DATA_OUT = '../' + SUB_DIRECTORY + '/movingStars/movingStars.SPECK'

SPEED_MULTIPLIER = 3       #Generally controls how fast the camera moves, specifically, multiplies globally into each iput speed
SUBDIVISIONS = 1500        #Number of steps when numerically calculating arc length and other bezier calculations


def readInPathData():
	file = open(DATA_SOURCE, "r")
	data = []
	for line in file.readlines():
		parts = line.strip().split()
		if parts[4] != "s" and parts[4] != "c":
			raise Exception("Bad connection symbol")
		if float(parts[3]) == 0:
			raise Exception("Speed cannot be 0")
		if len(parts) == 6: #Look straight
			if parts[5] != "s":
				raise Exception("Bad straight synbol for camera")
			data.append([float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3]) * SPEED_MULTIPLIER, parts[4] == "s", True])
		elif len(parts) == 8: #Look at x y z
			data.append([float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3]) * SPEED_MULTIPLIER, parts[4] == "s", False,
						 float(parts[5]), float(parts[6]), float(parts[7])])
		else:
			raise Exception("Bad line length: " + str(len(parts)))
	return data

f = open(DATA_OUT, "w")
f.write('datavar  0  color\n')
f.write('datavar  1  lum\n')
f.write('datavar  2  texture\n')
f.write('texture  1  -M halo.pbm\n')
f.write('texturevar 2\n\n')
for i in range(1200):
	x = 1 + math.cos(6.28 * (i / 1200))
	y = 1 + math.sin(6.28 * (i / 1200))
	f.write('datatime ' + str(i) + '\n')
	f.write("%.4f %.4f %.4f 0.8 10 1\n" % (x, y, 1))
	f.write("%.4f %.4f %.4f 0.8 10 1\n" % (x, y, 1))
