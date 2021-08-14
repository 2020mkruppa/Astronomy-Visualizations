import sys
sys.path.append("..")
from Interpolator import getInterpolator

DATA_OUT = 'constellation/data.speck'
HORSE_OUT = 'horse/data.speck'
LINES_OUT = 'constellationLines/data.speck'
#x, y, brightness multiplier
RAW = [(64, 177, 0.8), (597, 125, 0.7), (497, -315, 1), (37, -239, 0.8),
		 (-115, -303, 0.65), (-348, -400, 0.4),
		 (-60, -122, 0.55), (-85, -88, 0.35), (-377, -147, 0.4), (-540, -165, 0.5),
		 (-116, 325, 0.4), (-215, 381, 0.2), (-371, 473, 0.3), (-577, 344, 0.9)]

CONNECTIONS = [[1, 2], [2, 3], [3, 0], [0, 1], [0, 10], [10, 11], [11, 12], [12, 13], [3, 4], [4, 5],
			   [3, 6], [6, 7], [7, 8], [8, 9]]

SCALE = 0.075
STARS = []

for tup in RAW:
	STARS.append((tup[0] * SCALE, tup[1] * SCALE, tup[2]))

def writeStar(pos, color, lum): #Motion along x-z plane
	for n in range(2):
		const.write("%.4f %.4f 0 %d %d 1\n" % (pos[0], pos[1], color, pos[2] * lum))

def writeHorse(pos, lum):
	horse.write("%.4f %.4f 0 0 %d 1\n" % (pos[0], pos[1], lum))

def linInterp(start, end, norm):
	return [((b - a) * norm) + a for a, b in zip(start, end)]

def writeLines(norm):
	if norm == 0:
		return
	for line in CONNECTIONS:
		start = STARS[line[0]][:2]
		end = linInterp(start, STARS[line[1]][:2], norm)
		writeMesh(start, end)

def writeMesh(start, end):
	lines.write('mesh -c 1 -w 4 -s wire {\n1 2\n')
	lines.write("%.4f %.4f 0\n" % (start[0], start[1]))
	lines.write("%.4f %.4f 0\n}\n" % (end[0], end[1]))


lines = open(LINES_OUT, "w")
lines.write('datavar  0  color\n')

horse = open(HORSE_OUT, "w")
horse.write('datavar  0  color\n')
horse.write('datavar  1  lum\n')
horse.write('datavar  2  texture\n')
horse.write('texture  -M 1  pegHorse.sgi\n')
horse.write('texturevar 2\n\n')


const = open(DATA_OUT, "w")
const.write('datavar  0  color\n')
const.write('datavar  1  lum\n')
const.write('datavar  2  texture\n')
const.write('texture  -M 1  halo.pbm\n')
const.write('texturevar 2\n\n')

luminosityUp = getInterpolator(start_x=1180, end_x=1220, power=1, y_lists=[[500, 14000]])
luminosityDown = getInterpolator(start_x=1650, end_x=1740, power=1, y_lists=[[14000, 500]])
drawingProgress = getInterpolator(start_x=1290, end_x=1400, power=2, y_lists=[[0, 1]])

for i in range(9000):
	const.write('datatime ' + str(i) + '\n')
	horse.write('datatime ' + str(i) + '\n')
	lines.write('datatime ' + str(i) + '\n')

	lum = luminosityUp(i)[0]
	if i >= 1220:
		lum = luminosityDown(i)[0]

	for tup in STARS:
		writeStar(tup, 0, lum)
	writeHorse((5.5, 11.6), 2800000)
	writeLines(drawingProgress(i)[0])