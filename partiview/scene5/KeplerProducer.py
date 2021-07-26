from math import cos
from math import sin
from math import pow
from math import acos
from math import floor
from math import ceil
from math import radians as rad
import sys
sys.path.append("..")
from Interpolator import getInterpolator


MESH_OUT = 'keplerSphere/keplerSphere.speck'
STATIC_OUT = 'keplerSphereStatic/keplerSphereStatic.speck'

TILE_ANGLE = 2.34
TILE_SEP = TILE_ANGLE * 272 / 230 #Seperation
RADIUS = 20
TILE_SECTORS = 5
START_TIME = 5150
END_TIME = 5500
STARTING_EXPONENT = 1
TILE_ANIM_LENGTH = 70
OUTLINE_INTERP = getInterpolator(start_x=0, end_x=1, power=2, y_lists=[[0, 4]])
TILE_FADE_INTERP = getInterpolator(start_x=0, end_x=1, power=1, y_lists=[[0, 20]])

def toXYZ(latitude, longitude):
	return [RADIUS * cos(rad(latitude)) * cos(rad(longitude)),
			RADIUS * cos(rad(latitude)) * sin(rad(longitude)),
			RADIUS * sin(rad(latitude))]


def addPanel(P1, P2, P3, P4, fadeNum, file):
	file.write("mesh -c %d -s solid {\n2 2\n" % fadeNum)
	file.write("%.5f %.5f %.5f\n" % (P1[0], P1[1], P1[2]))
	file.write("%.5f %.5f %.5f\n" % (P2[0], P2[1], P2[2]))
	file.write("%.5f %.5f %.5f\n" % (P3[0], P3[1], P3[2]))
	file.write("%.5f %.5f %.5f\n" % (P4[0], P4[1], P4[2]))
	file.write("}\n")

def addEdge(points, file):
	for i in range(5):
		file.write("mesh -c 20 -s line {\n1 %d\n" % (len(points)))
		for x, y, z in points:
			file.write("%.5f %.5f %.5f\n" % (x, y, z))
		file.write("}\n")


def rotateY(point, angleDegrees):
	angle = rad(angleDegrees)
	return [cos(angle) * point[0] + sin(angle) * point[2],
			point[1],
			-sin(angle) * point[0] + cos(angle) * point[2]]

def rotateZ(point, angleDegrees):
	angle = rad(angleDegrees)
	return [cos(angle) * point[0] - sin(angle) * point[1],
			sin(angle) * point[0] + cos(angle) * point[1],
			point[2]]

def rotateX(point, angleDegrees):
	angle = rad(angleDegrees)
	return [point[0],
			cos(angle) * point[1] - sin(angle) * point[2],
			sin(angle) * point[1] + cos(angle) * point[2]]

def sphericalDist(lat1, long1, lat2, long2):
	deltaLong = rad(long2 - long1)
	return RADIUS * acos((sin(rad(lat1) * sin(rad(lat2))) + (cos(rad(lat1)) * cos(rad(lat2)) * cos(deltaLong))))

def computeMasterTile():
	lowerLat = -TILE_ANGLE / 2
	upperLat = TILE_ANGLE / 2

	distance = sphericalDist(lowerLat, 0, upperLat, 0)
	def masterWidth(long):
		return sphericalDist(upperLat, -long, upperLat, long) - distance
	rightLong = binarySearchForClosest(masterWidth, TILE_ANGLE * 0.3, TILE_ANGLE * 0.7)

	sectors = []
	edgeList = [[], [], [], []] #top, right, bottom, left
	for latNum in range(TILE_SECTORS):
		lat = lowerLat + (latNum * TILE_ANGLE / TILE_SECTORS)
		nextLat = lowerLat + ((latNum + 1) * TILE_ANGLE / TILE_SECTORS)
		for longNum in range(TILE_SECTORS):
			long = -rightLong + (longNum * (2 * rightLong) / TILE_SECTORS)
			nextLong = -rightLong + ((longNum + 1) * (2 * rightLong) / TILE_SECTORS)
			sectors.append([toXYZ(lat, long), toXYZ(nextLat, long), toXYZ(lat, nextLong), toXYZ(nextLat, nextLong)])

			if latNum == 0:
				edgeList[2].append(toXYZ(lat, long))
			if latNum == TILE_SECTORS - 1:
				edgeList[0].append(toXYZ(nextLat, long))
			if longNum == 0:
				edgeList[3].append(toXYZ(lat, long))
			if longNum == TILE_SECTORS - 1:
				edgeList[1].append(toXYZ(lat, nextLong))

	edgeList[2].append(toXYZ(lowerLat, rightLong))
	edgeList[0].append(toXYZ(upperLat, rightLong))
	edgeList[3].append(toXYZ(upperLat, -rightLong))
	edgeList[1].append(toXYZ(upperLat, rightLong))

	edgeList[1].reverse()
	edgeList[2].reverse()

	return sectors, edgeList

def binarySearchForClosest(errorFunction, start, end):
	mid = (start + end) / 2
	error = errorFunction(mid)
	if abs(error) < 0.0001:  # Hitting target is very unlikely for floating point comparison
		return mid
	if start == end or end < start:  # Shouldn't ever reach here
		return mid
	if error > 0:
		return binarySearchForClosest(errorFunction, start, mid)
	return binarySearchForClosest(errorFunction, mid, end)


def rotateListOfPoints(direction, angle, points):
	rotated = []
	for subList in points:
		subRotated = []
		for p in subList:
			subRotated.append(direction(p, angle))
		rotated.append(subRotated)
	return rotated

def getStartingInverse(end_y, y):
	return pow(y * ((END_TIME - START_TIME)**STARTING_EXPONENT) / end_y, 1 / STARTING_EXPONENT) + START_TIME


def drawNormedSector(tiles, edges, norm, file):
	fade_num = TILE_FADE_INTERP(norm)[0]
	for a, b, c, d in tiles:
		addPanel(a, b, c, d, fade_num, file)

	drawingProgress = OUTLINE_INTERP(norm)[0]
	if drawingProgress <= 1:
		addEdge(interperolateEdge(edges[0], drawingProgress), file)
	elif drawingProgress <= 2:
		addEdge(edges[0], file)
		addEdge(interperolateEdge(edges[1], drawingProgress - 1), file)
	elif drawingProgress <= 3:
		addEdge(edges[0], file)
		addEdge(edges[1], file)
		addEdge(interperolateEdge(edges[2], drawingProgress - 2), file)
	else:
		addEdge(edges[0], file)
		addEdge(edges[1], file)
		addEdge(edges[2], file)
		addEdge(interperolateEdge(edges[3], drawingProgress - 3), file)

def interperolateEdge(edge, norm):
	index = (len(edge) - 1) * norm
	floorIndex = floor(index)
	ceilingIndex = ceil(index)
	croppedEdge = []
	for i in range(floorIndex + 1):
		croppedEdge.append(edge[i])
	croppedEdge.append(linInterp(edge[floorIndex], edge[ceilingIndex], index - floorIndex))
	return croppedEdge


def linInterp(start, end, norm):
	return [((b - a) * norm) + a for a, b in zip(start, end)]


ROTATIONS = [[-2 * TILE_SEP, [-TILE_SEP, 0, TILE_SEP]],
			 [-TILE_SEP, [-2 * TILE_SEP, -TILE_SEP, 0, TILE_SEP, 2 * TILE_SEP]],
			 [0, [-2 * TILE_SEP, -TILE_SEP, 0, TILE_SEP, 2 * TILE_SEP]],
			 [TILE_SEP, [-2 * TILE_SEP, -TILE_SEP, 0, TILE_SEP, 2 * TILE_SEP]],
			 [2 * TILE_SEP, [-TILE_SEP, 0, TILE_SEP]]]



meshes = open(MESH_OUT, "w")
static = open(STATIC_OUT, "w")
miniTiles, edges = computeMasterTile()

completedPanels = []

tileNumber = 0
for horizontal, verts in ROTATIONS:
	for vertical in verts:
		rotatedTiles = rotateListOfPoints(rotateY, vertical, miniTiles)
		rotatedEdges = rotateListOfPoints(rotateY, vertical, edges)
		rotatedTiles = rotateListOfPoints(rotateZ, horizontal, rotatedTiles)
		rotatedEdges = rotateListOfPoints(rotateZ, horizontal, rotatedEdges)

		#Now to rotate to correct fov
		rotatedTiles = rotateListOfPoints(rotateX, -32.5, rotatedTiles)
		rotatedEdges = rotateListOfPoints(rotateX, -32.5, rotatedEdges)
		rotatedTiles = rotateListOfPoints(rotateY, -13.41, rotatedTiles)
		rotatedEdges = rotateListOfPoints(rotateY, -13.41, rotatedEdges)
		rotatedTiles = rotateListOfPoints(rotateZ, 76.34, rotatedTiles)
		rotatedEdges = rotateListOfPoints(rotateZ, 76.34, rotatedEdges)


		completedPanels.append([rotatedTiles, rotatedEdges, getStartingInverse(21, tileNumber)])
		tileNumber += 1

for t in range(START_TIME, END_TIME + TILE_ANIM_LENGTH + 1):
	if t % 20 == 0:
		print(t)
	meshes.write('datatime ' + str(t) + '\n')

	for tiles, edges, start in completedPanels:
		if t < start:
			continue
		timeNorm = min((t - start) / TILE_ANIM_LENGTH, 1)
		drawNormedSector(tiles, edges, timeNorm, meshes)

#STATIC WRITING
for tiles, edges, start in completedPanels:
	drawNormedSector(tiles, edges, 1, static)