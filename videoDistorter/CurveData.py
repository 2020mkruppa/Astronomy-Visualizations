import math

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


def inShape(x, y):
	if (y not in Y2XRight) or (y not in Y2XLeft) or (x not in X2Y):
		return False
	return X2Y[x] >= y >= bottom(x) and Y2XRight[y] >= x >= Y2XLeft[y]

def getXBaseNorm(norm):
	return Dx + norm * (1920 - Dx - Dx)


def generateLongitudeLookUpTable():
	print("Generating Longitude Lookup")
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
			if not inShape(x, y):
				continue
			longitudeMap[x][y].append([coords[0], coords[1], i / 2000.0])
	chooseBestCoordinateMap(longitudeMap)

def getYFromNorm(norm):
	return Ey + norm * (By - Ey)

def generateLatitudeLookUpTable():
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
			if not inShape(x, y):
				continue
			latitudeMap[x][y].append([coords[0], coords[1], i / 2000.0])
	chooseBestCoordinateMap(latitudeMap)

def chooseBestCoordinateMap(lookup):
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
			lookup[x][y] = value


#Coordinate maps for the top/side edge
X2Y = dict()
Y2XRight = dict()
Y2XLeft = dict()

#Normalized maps for final image mapping
longitudeMap = [[[] for y in range(1080)] for x in range(1920)]  #Access using [x][y]
latitudeMap = [[[] for yy in range(1080)] for xx in range(1920)]

generateEdgeLists()
generateLatitudeLookUpTable()
generateLongitudeLookUpTable()


print(longitudeMap[960][600])
print(longitudeMap[960][900])
