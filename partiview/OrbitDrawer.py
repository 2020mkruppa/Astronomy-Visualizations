import math
def drawOrbitXZ(r, file):
	resolution = 150
	file.write('mesh -c 0 -w 3 -s wire {\n1 ' + str(resolution + 1) + '\n')
	for i in range(resolution + 1):
		pos = getPosition(r, i, resolution)
		file.write("%.4f 0 %.4f\n" % (pos[0], pos[1]))
	file.write('}\n')

def drawOrbitXY(r, file):
	resolution = 150
	file.write('mesh -c 0 -w 3 -s wire {\n1 ' + str(resolution + 1) + '\n')
	for i in range(resolution + 1):
		pos = getPosition(r, i, resolution)
		file.write("%.4f %.4f 0\n" % (pos[0], pos[1]))
	file.write('}\n')

def getPosition(radius, time, period):
	argument = ((math.pi * 2 / period) * time)
	return [radius * math.cos(argument), radius * math.sin(argument)]