from math import cos
from math import sin
from math import acos
from math import radians as rad

MESH_OUT = 'multiPlanetOrbits/orbits.SPECK'

TILE_ANGLE = 23.45
RADIUS = 100
TILE_SECTORS = 8
def toXYZ(latitude, longitude):
	return [RADIUS * cos(rad(latitude)) * cos(rad(longitude)),
			RADIUS * cos(rad(latitude)) * sin(rad(longitude)),
			RADIUS * sin(rad(latitude))]


def addPanel(P1, P2, P3, P4):
	meshes.write("mesh -c 0 -s solid {\n2 2\n")
	meshes.write("%.5f %.5f %.5f\n" % (P1[0], P1[1], P1[2]))
	meshes.write("%.5f %.5f %.5f\n" % (P2[0], P2[1], P2[2]))
	meshes.write("%.5f %.5f %.5f\n" % (P3[0], P3[1], P3[2]))
	meshes.write("%.5f %.5f %.5f\n" % (P4[0], P4[1], P4[2]))
	meshes.write("}\n")

def addEdge(points):
	for i in range(5):
		meshes.write("mesh -c 0 -s line {\n1 %d\n" % (len(points)))
		for x, y, z in points:
			meshes.write("%.5f %.5f %.5f\n" % (x, y, z))
		meshes.write("}\n")


def rotateY(point, angleDegrees):
	angle = rad(angleDegrees)
	return [cos(angle) * point[0] + sin(angle) * point[2],
			point[1],
			-sin(angle) * point[0] + cos(angle) * point[2]]

def rotateZ(point, angleDegrees):
	angle = rad(angleDegrees)
	return [cos(angle) * point[0] - sin(angle) * point[1],
			sin(angle) * point[0] + cos(angle) * point[1],
			point[2],]

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
	edgeList = [[], [], [], []] #top, bottom, right, left
	for latNum in range(TILE_SECTORS):
		lat = lowerLat + (latNum * TILE_ANGLE / TILE_SECTORS)
		nextLat = lowerLat + ((latNum + 1) * TILE_ANGLE / TILE_SECTORS)
		for longNum in range(TILE_SECTORS):
			long = -rightLong + (longNum * (2 * rightLong) / TILE_SECTORS)
			nextLong = -rightLong + ((longNum + 1) * (2 * rightLong) / TILE_SECTORS)
			sectors.append([toXYZ(lat, long), toXYZ(nextLat, long), toXYZ(lat, nextLong), toXYZ(nextLat, nextLong)])

			if latNum == 0:
				edgeList[1].append(toXYZ(lat, long))
			if latNum == TILE_SECTORS - 1:
				edgeList[0].append(toXYZ(nextLat, long))
			if longNum == 0:
				edgeList[3].append(toXYZ(lat, long))
			if longNum == TILE_SECTORS - 1:
				edgeList[2].append(toXYZ(lat, nextLong))

	edgeList[1].append(toXYZ(lowerLat, rightLong))
	edgeList[0].append(toXYZ(upperLat, rightLong))
	edgeList[3].append(toXYZ(upperLat, -rightLong))
	edgeList[2].append(toXYZ(upperLat, rightLong))

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


VERTICAL_ROTATIONS = [18, 42, 66, 90, -18, -42, -66, -90]
HORIZONTAL_ROTATIONS = []
for long_num in range(13):
	HORIZONTAL_ROTATIONS.append(long_num * (360 / 13))



meshes = open(MESH_OUT, "w")
miniTiles, edges = computeMasterTile()


for horiz in HORIZONTAL_ROTATIONS:
	for vert in VERTICAL_ROTATIONS:
		rotatedTiles = rotateListOfPoints(rotateY, vert, miniTiles)
		rotatedEdges = rotateListOfPoints(rotateY, vert, edges)
		rotatedTiles2 = rotateListOfPoints(rotateZ, horiz, rotatedTiles)
		rotatedEdges2 = rotateListOfPoints(rotateZ, horiz, rotatedEdges)

		for a, b, c, d in rotatedTiles2:
			addPanel(a, b, c, d)
		for edge in rotatedEdges2:
			addEdge(edge)
