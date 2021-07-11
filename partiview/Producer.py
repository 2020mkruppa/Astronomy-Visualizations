import math
#Values to be set by caller
SPEED_MULTIPLIER = 0       #Generally controls how fast the camera moves, specifically, multiplies globally into each iput speed
BEZIER_TIGHTNESS = 0     #Global multiplier into how sharp to make each bezier, too large or too small will make a cusp.
SUBDIVISIONS = 0        #Number of steps when numerically calculating arc length and other bezier calculations


CAM_HOME = [0, 0, -1]
CAM_INTERP_START = 0.1    #The camera panning interpolation will only interpolate between these 2 values, greater or smaller than them,
CAM_INTERP_END = 0.9      #it will be constant at either start or end

'''
Flight data is listed in rows. Format is [x y z] v [connection type]
[x y z] is a point to pass through with speed v, speed being step length until next output point. [connection type] is
whether to get to the next point in a straight line, or curve. One shouldn't have consecutive straights, or else there will be a 
sharp point in the path, and consecutive curves are not allowed since we need to know the tangent lines at the end points of each
curve to ensure a smooth path. One can always put in a very short straight to satisfy this. 

Velocity change is linear interpolation between endpoints. The graph of velocity against time/position
is continuous but not differentiable, but position against time is differentiable. Velocity cannot be 0, or else it will never move 
from a point, but it can be very small.
  
0 0 0  0.001  s   s
2 3 4  0.01   c   s
4 5 6  0.015  s   1 1 1
7 7 6  0.01   s   s

s indicates coming from previous point in a straight line, c is curve
The first and last path must be a straight (though again it can be short), so really the second to last connection type must be s
In the above example, we start at the origin nearly stationary, and move to (2, 3, 4) in a straight line, accelerating to 0.01 speed.
Then, we go to (4, 5, 6) in a curved path that is smooth, and accelerate to 0.015. Finally, we go to (7, 7, 6) and decelerate to 0.01.
The last connection type is always ignored

The last column is camera angles, s is straight ahead (roller coaster view), and specifying coordinates tells the camera to look there. 
Specifically, the camera symbol governs that path's camera. In the above example, camera is straight ahead from 0 0 0 to 2 3 4, and then 
smoothly pans so that at the end of the 2 3 4 to 4 5 6 segment, it is now looking at 1 1 1 (the point in space, not the vector direction).
From 4 5 6 to 7 7 6, it will pan back so that as we get to 7 7 6, we are looking straight ahead again.
'''


def readInPathData(file):
	data = []
	for line in file.readlines():
		parts = line.strip().split()
		if parts[4] != "s" and parts[4] != "c":
			raise Exception("Bad connection symbol")
		if float(parts[3]) == 0:
			raise Exception("Speed cannot be 0")
		if len(parts) == 6: #Look straight
			if parts[5] != "s":
				raise Exception("Bad straight symbol for camera")
			data.append([float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3]) * SPEED_MULTIPLIER, parts[4] == "s", True])
		elif len(parts) == 8: #Look at x y z
			data.append([float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3]) * SPEED_MULTIPLIER, parts[4] == "s", False,
						 float(parts[5]), float(parts[6]), float(parts[7])])
		else:
			raise Exception("Bad line length: " + str(len(parts)))
	return data

def createSections(inputData, outputData):
	for i in range(len(inputData) - 1):  #must make all straight sections first so we have tangent information
		if inputData[i][4]:
			createStraightSection(i, inputData, outputData)

	for i in range(len(inputData) - 1):
		if not inputData[i][4]:
			createCurvedSection(i, inputData, outputData)


def createStraightSection(i, inputData, outputData):
	segment = getStraight(inputData[i][0:3], inputData[i + 1][0:3])
	outputData[i] = returnTimeInformation(segment, i, inputData)


def createCurvedSection(i, inputData, outputData):
	previous = outputData[i - 1][-min(2, len(outputData[i - 1]) - 1)] #Second last data point for more accuracy, unless the list is too small
	beginTangentNormalized = normalize(vectorFromTo(previous, inputData[i][0:3]))

	future = outputData[i + 1][min(2, len(outputData[i + 1]) - 1)]
	endTangentNormalized = normalize(vectorFromTo(future, inputData[i + 1][0:3]))

	deflection = math.cos(getAngleBetween(beginTangentNormalized, endTangentNormalized))
	#Heuristic to control how far each control point is from the start/end point
	#It needs to be tangent to the incoming/outgoing path, but length will control how tight the turn is
	#Heuristic proportional to pure distance between start/end, the relative angle of the path, and a final global multiplier
	tangentScale = BEZIER_TIGHTNESS * distanceBetweenPoints(inputData[i][0:3], inputData[i + 1][0:3]) * getOriginalFromNormalized(0.3, 0.7, (deflection + 1) / 2)

	beginControlPoint = [a + (b * tangentScale) for a, b in zip(inputData[i][0:3], beginTangentNormalized)]
	endControlPoint = [a + (b * tangentScale) for a, b in zip(inputData[i + 1][0:3], endTangentNormalized)]

	bezier = getBezier(inputData[i][0:3], beginControlPoint, endControlPoint, inputData[i + 1][0:3])
	outputData[i] = returnTimeInformation(bezier, i, inputData)

def returnTimeInformation(path, i, inputData):
	pathLength = calculateLengthOfPath(path)
	intermediatePoints = [path(0)]
	distanceAlong = 0
	while distanceAlong < pathLength:    #Linear interpolation of speed based off of how far along the curve we are
		stride = getOriginalFromNormalized(inputData[i][3], inputData[i + 1][3], getNormFromOriginal(0, pathLength, distanceAlong))
		distanceAlong += stride
		percentAlongPath = distanceAlong / pathLength
		intermediatePoints.append(path(percentAlongPath))

	if distanceAlong > pathLength: #We might overshoot, so remove that point
		del intermediatePoints[-1] #There is still a chance we "undershot", and there is a small gap between the final end point
	return intermediatePoints      #and the next start point of the next curve, but it's a small problem and it won't be too visible

def getStraight(P0, P1):
	def function(percentAlongCurve):
		return [getOriginalFromNormalized(P0[0], P1[0], percentAlongCurve),
				getOriginalFromNormalized(P0[1], P1[1], percentAlongCurve),
				getOriginalFromNormalized(P0[2], P1[2], percentAlongCurve)]
	return function

def getBezier(P0, P1, P2, P3): #Unfortunately, moving as constant in time along a bezier does not mean constant stepping
	arcLengthToTime = {0 : 0} #so we have to map arc length to time to find the appropriate time given a length percent
	l = 0
	for i in range(0, SUBDIVISIONS):
		l += distanceBetweenPoints(bezierPoint(P0, P1, P2, P3, i / SUBDIVISIONS), bezierPoint(P0, P1, P2, P3, (i + 1) / SUBDIVISIONS))
		arcLengthToTime[l] = (i + 1) / SUBDIVISIONS
	normalized = []
	for key in arcLengthToTime:
		normalized.append([key / l, arcLengthToTime[key]]) #Normalize to total length

	def function(percentAlongCurve):
		return bezierPoint(P0, P1, P2, P3, binarySearchForClosestTime(normalized, 0, len(normalized) - 1, percentAlongCurve))
	return function


def binarySearchForClosestTime(normalized, start, end, target):
	mid = (start + end) // 2
	if normalized[mid][0] == target: #Hitting target is very unlikely for floating point comparison
		return normalized[mid][1]
	if start == end or end < start: #Shouldn't ever reach here
		raise Exception("Bad search")
	if abs(start - end) == 1: #Close enough to interpolate
		return getOriginalFromNormalized(normalized[start][1], normalized[end][1], 0.5)
	if normalized[mid][0] < target:
		return binarySearchForClosestTime(normalized, mid, end, target)
	return binarySearchForClosestTime(normalized, start, mid, target)


def bezierPoint(P0, P1, P2, P3, t):
	return [bezierComponentWise(P0[0], P1[0], P2[0], P3[0], t),
			bezierComponentWise(P0[1], P1[1], P2[1], P3[1], t),
			bezierComponentWise(P0[2], P1[2], P2[2], P3[2], t)]

def bezierComponentWise(p0, p1, p2, p3, t): #Cubic bezier
	return ((1 - t)**3 * p0) + (3 * p1 * t * (1 - t)**2) + (3 * t * t * p2 * (1 - t)) + p3 * t * t * t

def lengthOfVector(v):
	return distanceBetweenPoints(v, [0, 0, 0])

def normalize(v):
	return [comp / lengthOfVector(v) for comp in v]

def vectorFromTo(start, end):
	return [b - a for a, b in zip(start, end)]

def distanceBetweenPoints(P0, P1):
	return math.sqrt(sum([(a - b)**2 for a, b in zip(P0, P1)]))

#getOriginal(min, max, getNorm(min, max, value)) = value
def getOriginalFromNormalized(minimum, maximum, norm): #Norm is [0, 1], that returns a linear proportion between [min, max]
	return minimum + (norm * (maximum - minimum))

def getNormFromOriginal(minimum, maximum, value): #Returns normalized scale of location between min and max
	return (value - minimum) / (maximum - minimum)


def calculateLengthOfPath(b):
	l = 0
	for i in range(0, SUBDIVISIONS):
		l += distanceBetweenPoints(b(i / SUBDIVISIONS), b((i + 1) / SUBDIVISIONS))
	return l

def printPathToFile(flatPathData, f):
	for e in flatPathData:
		f.write("%.4f %.4f %.4f %.4f %.4f %.4f 60\n" % (e[0], e[1], e[2], e[3], e[4], e[5]))

def makeFramesFile(data, f, singleCommands, timeOffset, startFrame):
	f.write('eval snapset outFrames/frames%06d -n 0\n\n')
	for e in range(startFrame, len(data)):
		if e in singleCommands.keys():
			f.write(singleCommands[e] + '\n')

		f.write('eval frame ' + str(e) + '\n') #Flight path next frame
		if e >= timeOffset:
			f.write('eval step ' + str(e - timeOffset) + '\n')  #Time data next frame
		f.write('eval snapshot outFrames/frames\n')

def printPathToConsole(flatPathData): #Formated for Mathematica's ListPointPlot3D
	s = ""
	num = 0
	for position in flatPathData:
		s += "{%.4f, %.4f, %.4f}, " % (position[0], position[1], position[2])
		num += 1
		if num == 7:
			num = 0
			print(s)
			s = ""

def assessStride(flatPathData):
	for i in range(len(flatPathData) - 1):
		print("%.4f" % distanceBetweenPoints(flatPathData[i][0:2], flatPathData[i + 1][0:2]))


def calculatePathData(eulerFunction, file):
	inputData = readInPathData(file) #generally contains list [x, y, z, speed, straight (bool), camera straight ahead (bool), x, y, z]
	for i in range(len(inputData) - 1):                                                                                  #Optional camera coords
		if (not inputData[i][4]) and (not inputData[i + 1][4]):
			raise Exception("Consecutive curves")
	if not inputData[0][4]:
		raise Exception("First path not straight")
	if not inputData[-1][4]:
		raise Exception("Last path not straight")

	outputCurveData = [] #Each element corresponds to each connection and the element containts list of [x, y, x]
	for element in range(len(inputData) - 1):
		outputCurveData.append([]) #Create space for each path element

	createSections(inputData, outputCurveData)
	calculateCameraAngles(inputData, outputCurveData, eulerFunction)

	flatData = []
	for connection in outputCurveData:
		for position in connection:
			flatData.append(position)

	del flatData[-1] #Last point's angle is weird, don't need it
	return flatData

######################################### Below are methods for camera angle ##############################################
def dotProduct(a, b):
	return sum([a * b for a, b in zip(a, b)])

def getAngleBetween(u, v): #Returns in radians
	return math.acos(dotProduct(u, v) / (math.sqrt(dotProduct(u, u)) * math.sqrt(dotProduct(v, v))))

def getEulerAnglesAxisAngle(v): # vector to look at, this uses a straight rotation through axis-angle to get the rotation
	if lengthOfVector(v) == 0:
		raise Exception("Bad vector")
	axis = [CAM_HOME[1] * v[2] - CAM_HOME[2] * v[1],
			CAM_HOME[2] * v[0] - CAM_HOME[0] * v[2],
			CAM_HOME[0] * v[1] - CAM_HOME[1] * v[0]]  # Take CAM_HOME cross v, in this order for correct orientation
	if lengthOfVector(axis) == 0: #If |cross| = 0, then camera is parallel to CAM_HOME
		if dotProduct(v, CAM_HOME) > 0: #Same direction means 0 rotation at all
			return [0, 0, 0]
		return [0, 180, 0] #Exactly the opposite direction

	angle = getAngleBetween(CAM_HOME, v) # Angle in radians
	axis = normalize(axis)  #Axis must be normalized

	#Don't need to compute the whole rotation matrix, only neccesary entries
	R23 = (axis[1] * axis[2] * (1 - math.cos(angle))) - (axis[0] * math.sin(angle))
	R13 = (axis[0] * axis[2] * (1 - math.cos(angle))) + (axis[1] * math.sin(angle))
	R33 = math.cos(angle) + (axis[2] * axis[2] * (1 - math.cos(angle)))
	R21 = (axis[1] * axis[0] * (1 - math.cos(angle))) + (axis[2] * math.sin(angle))
	R22 = math.cos(angle) + (axis[1] * axis[1] * (1 - math.cos(angle)))
	#Conversion comes from the YXZ rotation matrix
	return [math.degrees(math.asin(-R23)), math.degrees(math.atan2(R13, R33)), math.degrees(math.atan2(R21, R22))]


def getEulerAnglesAzimuthElevation(v): # vector to look at, based purely on azimuth and elevation. This produces some interesting
	if lengthOfVector(v) == 0:                      #barrel-roll effects that are completely unintentional, but other times
		raise Exception("Bad vector")           #works much better than axis-angle
	v = normalize(v)

	azimuth = -math.atan2(v[0], -v[2]) #Need negative so to get the direction correct since rotation is CW
	elevation = math.asin(v[1])

	#Use intrinsic rotations to get elevation instead of rotation around x
	#totalRotation = Ry(azimuth) x Rx(elevation)

	#Don't need to compute the whole rotation matrix, only neccesary entries
	R23 = -math.sin(elevation)
	R13 = math.cos(elevation) * math.sin(azimuth)
	R33 = math.cos(elevation) * math.cos(azimuth)
	R21 = 0
	R22 = math.cos(elevation)
	#Conversion comes from the YXZ rotation matrix
	return [math.degrees(math.asin(-R23)), math.degrees(math.atan2(R13, R33)), math.degrees(math.atan2(R21, R22))]

def getInterpolatedCam(startCam, endCam):
	def function(t):
		if t > CAM_INTERP_END:
			return endCam
		if t < CAM_INTERP_START:
			return startCam
		return [polynomial_smoothing(CAM_INTERP_START, CAM_INTERP_END, startCam[i], endCam[i], t) for i in range(3)]
	return function

def polynomial_smoothing(start_t, end_t, start_y, end_y, t):
	t_diff = end_t - start_t
	y_diff = end_y - start_y
	if t <= (start_t + end_t) / 2:
		scale = 4 * y_diff / (t_diff**3)
		return (scale * ((t - start_t)**3)) + start_y
	else:
		scale = 4 * y_diff * -1 / ((-1 * t_diff)**3)
		return (scale * ((t - end_t) ** 3)) + end_y

def fadeIn(group, start, maxAlpha, frameStep):
	commands = dict()
	commands[start + int(frameStep)] = 'eval ' + group + '\neval on\neval alpha 0.01'
	for i in range(2, int(maxAlpha * 100) + 1):
		commands[start + int(frameStep * i)] = ('eval ' + group + '\neval on\neval alpha %.2f') % (i / 100)
	return commands

def fadeOut(group, start, startAlpha, frameStep):
	commands = dict()
	for i in range(int(startAlpha * 100), -1, -1):
		index = start + int(frameStep * (int(startAlpha * 100) - i))
		commands[index] = 'eval ' + group + '\neval alpha %.2f' % (i / 100)
	index = start + int(frameStep * int(startAlpha * 100))
	commands[index] = 'eval ' + group + '\neval alpha 0.00\neval off'
	return commands

def calculateCameraAngles(inputData, outputCurveData, eulerFunction):
	# s -> s is easy, just have it always along the tangent vector
	# s -> xyz, interpolate the initial vector direction and the ending vector direction
	# xyz -> s, same thing as above
	# xyz -> xyz, these coords can be the same or different
	for i in range(len(outputCurveData)):
		if inputData[i][5] and inputData[i + 1][5]:  # s -> s
			for posIndex in range(len(outputCurveData[i]) - 1):
				tangentNorm = vectorFromTo(outputCurveData[i][posIndex], outputCurveData[i][posIndex + 1])
				outputCurveData[i][posIndex].extend(eulerFunction(tangentNorm))
			if i != (len(outputCurveData) - 1):
				tangentNorm = vectorFromTo(outputCurveData[i][len(outputCurveData[i]) - 1], outputCurveData[i + 1][0])  # Connect to next segment
				outputCurveData[i][len(outputCurveData[i]) - 1].extend(eulerFunction(tangentNorm))
			else:
				outputCurveData[i][len(outputCurveData[i]) - 1].extend([0, 0, 0])  # Incorrect, but it'll be removed since it's the last frame

		elif inputData[i][6:] == inputData[i + 1][6:]:  # xyz ->xyz same coords
			for posIndex in range(len(outputCurveData[i])):
				camVector = vectorFromTo(outputCurveData[i][posIndex], inputData[i][6:])
				outputCurveData[i][posIndex].extend(eulerFunction(camVector))

		else:
			if inputData[i][5] and (not inputData[i + 1][5]):  # s -> xyz
				beginCamVector = vectorFromTo(outputCurveData[i][0], outputCurveData[i][1])
				endCamVector = vectorFromTo(outputCurveData[i][-1], inputData[i + 1][6:])
			elif (not inputData[i][5]) and (inputData[i + 1][5]):  # xyz -> s
				endCamVector = vectorFromTo(outputCurveData[i][-2], outputCurveData[i][-1])
				beginCamVector = vectorFromTo(outputCurveData[i][0], inputData[i][6:])
			else:  # xyz ->xyz different coords
				#endCamVector = vectorFromTo(outputCurveData[i][-1], inputData[i + 1][6:])
				#beginCamVector = vectorFromTo(outputCurveData[i][0], inputData[i][6:])
				interpolatedVector = getInterpolatedCam(inputData[i][6:], inputData[i + 1][6:])
				for posIndex in range(len(outputCurveData[i])):
					scaled = posIndex / len(outputCurveData[i])
					outputCurveData[i][posIndex].extend(eulerFunction(vectorFromTo(outputCurveData[i][posIndex], interpolatedVector(scaled))))
				continue

			interpolatedCam = getInterpolatedCam(normalize(beginCamVector), normalize(endCamVector))
			for posIndex in range(len(outputCurveData[i])):
				outputCurveData[i][posIndex].extend(eulerFunction(interpolatedCam(posIndex / len(outputCurveData[i]))))



def producePath(dataFileIn, pathFileOut, framesFileOut, speedMultiplier, bezierTightness, numericalSteps, timeOffset, singleCommands, angleFunction, startFrame):
	global SPEED_MULTIPLIER
	global BEZIER_TIGHTNESS
	global SUBDIVISIONS
	SPEED_MULTIPLIER = speedMultiplier
	BEZIER_TIGHTNESS = bezierTightness
	SUBDIVISIONS = numericalSteps

	finalPathData = calculatePathData(angleFunction, dataFileIn)
	printPathToConsole(finalPathData)
	#assessStride(finalPathData)
	printPathToFile(finalPathData,pathFileOut)
	makeFramesFile(finalPathData, framesFileOut, singleCommands, timeOffset, startFrame)
