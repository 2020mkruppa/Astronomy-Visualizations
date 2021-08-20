import math
import pickle
import os.path
import numpy as np

#THESE ARE BOTTOM LEFT_INDEXED COORDINATES, FROM DESMOS
#Keep .0 to ensure floating point calculations

By = 908.0
Dx = 318.0
Dy = 237.0
Ey = 411.0
y1 = 31.0

bottomSMSquared = pow(Dx - 960, 2) / (1 - pow((Dy - y1) / (Ey - y1), 2))

def bottom(x):
	return y1 + (Ey - y1) * math.sqrt(1 - (pow(x - 960, 2) / bottomSMSquared))

def ellipseSlope(x):
	return -(Ey - y1) * (x - 960) / math.sqrt(bottomSMSquared**2 - (bottomSMSquared * ((x-960)**2)))

def normalSlope(x):
	return -1.0 / ellipseSlope(x)

def normalPoints(xBase, yOffset):
	if xBase == 960:
		return [xBase, yOffset + bottom(xBase)]
	return [(yOffset / normalSlope(xBase)) + xBase,
			yOffset + bottom(xBase)]

def bottomLongitudeControl(x):
	return normalPoints(x, 245)


def topLongitudeControl(x):
	return [((x - 960) / 1.37) + 960,
			By - 80 + 0.00022*((x - 960)**2)]


def longitudeLine(xBase, t):
	bottomC = bottomLongitudeControl(xBase)
	topC = topLongitudeControl(xBase)
	return [((1-t)**3)*xBase + 3*t*((1-t)**2)*bottomC[0] + 3*(1-t)*t*t*topC[0] + (t**3)*960,
			((1-t)**3)*bottom(xBase) + 3*t*((1-t)**2)*bottomC[1] + 3*(1-t)*t*t*topC[1] + (t**3)*By]


def getYnorm(y):
	return (y - Ey) / (By - Ey)


def topBias(x, norm):
	return By + (0.009*(norm**3) + 0.0008)*((x - 960)**2)

def latitudeLine(yBase, x):
	norm = getYnorm(yBase)
	return [x, bottom(x)*(1 - norm) + topBias(x, norm)*norm]


def generateEdgeLists():
	# Coordinate maps for the top/side edge
	X2Y = dict()
	Y2XRight = dict()
	Y2XLeft = dict()
	for i in range(0, 2001):
		tNorm = i / 2000.0
		coords = longitudeLine(Dx, tNorm)
		x = int(coords[0])
		y = int(coords[1])
		X2Y[x] = y
		Y2XLeft[y] = x
	for i in range(0, 2000):
		tNorm = i / 2000.0
		coords = longitudeLine(1920 - Dx, tNorm)
		x = int(coords[0])
		y = int(coords[1])
		X2Y[x] = y
		Y2XRight[y] = x
	return X2Y, Y2XLeft, Y2XRight

def inShape(x, y, X2Y, Y2XLeft, Y2XRight):
	if (y not in Y2XRight) or (y not in Y2XLeft) or (x not in X2Y):
		return False
	return X2Y[x] >= y >= bottom(x) and Y2XRight[y] >= x >= Y2XLeft[y]

def getXBaseNorm(norm):
	return Dx + norm * (1920 - Dx - Dx)


def generateLongitudeLookUpTable(X2Y, Y2XLeft, Y2XRight):
	print("Generating Longitude Lookup")
	longitudeMap = [[[] for y in range(1080)] for x in range(1920)] #Access using [x][y]
	for i in range(0, 2001):
		if i % 100 == 0:
			print(i)
		xBase = getXBaseNorm(i / 2000.0)
		for up in range(0, 2001):
			tNorm = up / 2000.0
			try:
				coords = longitudeLine(xBase, tNorm)
			except ValueError:
				continue
			x = int(coords[0])
			y = int(coords[1])
			if not inShape(x, y, X2Y, Y2XLeft, Y2XRight):
				continue
			longitudeMap[x][y].append([coords[0], coords[1], i / 2000.0])
	return chooseBestCoordinateMap(longitudeMap)


def getYFromNorm(norm):
	return Ey + norm * (By - Ey)

def generateLatitudeLookUpTable(X2Y, Y2XLeft, Y2XRight):
	latitudeMap = [[[] for y in range(1080)] for x in range(1920)]
	print("Generating Latitude Lookup")
	for i in range(0, 2001):
		if i % 100 == 0:
			print(i)
		yBase = getYFromNorm(i / 2000.0)
		for x in range(0, 1920):
			try:
				coords = latitudeLine(yBase, x)
			except ValueError:
				continue
			x = int(coords[0])
			y = int(coords[1])
			if not inShape(x, y, X2Y, Y2XLeft, Y2XRight):
				continue
			latitudeMap[x][y].append([coords[0], coords[1], i / 2000.0])
	return chooseBestCoordinateMap(latitudeMap)


def chooseBestCoordinateMap(lookup):
	selectedMap = [[[] for y in range(1080)] for x in range(1920)]
	for x in range(len(lookup)):
		for y in range(len(lookup[0])):
			choices = lookup[x][y]
			bestDistance = 1000
			value = 0.0
			for choice in choices: #Works for any number of choices, 0 through n
				distance = (choice[0] - x)**2 + (choice[1] - y)**2
				if distance < bestDistance:
					bestDistance = distance
					value = choice[2]
			selectedMap[x][y] = value
	return selectedMap


def getWarpedCoordinates(x, y, longitudeMap, latitudeMap):
	return [min(1919, int(longitudeMap[x][y] * 1920)), min(1079, int(latitudeMap[x][y] * 1080))]


def getPointsMap(lookForPickle):
	pickleName = "mappingData.pkl"
	if lookForPickle and os.path.isfile(pickleName):
		with open(pickleName, "rb") as infile:
			maps = pickle.load(infile)
			return np.array(maps[0]), np.array(maps[1]), np.array(maps[2]), np.array(maps[3])

	X2Y, Y2XLeft, Y2XRight = generateEdgeLists()
	latitudeLookup = generateLatitudeLookUpTable(X2Y, Y2XLeft, Y2XRight)
	longitudeLookup = generateLongitudeLookUpTable(X2Y, Y2XLeft, Y2XRight)

	inputListY = []
	inputListX = []
	outputListY = []
	outputListX = []

	for x in range(1920):
		for y in range(1080):
			if inShape(x, y, X2Y, Y2XLeft, Y2XRight):
				outCoords = getWarpedCoordinates(x, y, longitudeLookup, latitudeLookup)
				outputListY.append(1079 - y)
				outputListX.append(x)
				inputListY.append(1079 - outCoords[1])
				inputListX.append(outCoords[0])


	with open(pickleName, "wb") as outfile:
		pickle.dump([inputListX, inputListY, outputListX, outputListY], outfile)

	return np.array(inputListX), np.array(inputListY), np.array(outputListX), np.array(outputListY)