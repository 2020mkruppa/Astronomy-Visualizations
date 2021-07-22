import math
import random
DATA_SOURCE = 'data.csv'
DATA_OUT = 'exoplanets.speck'

''' Columns to select:

# COLUMN pl_name:        Planet Name
# COLUMN discoverymethod: Discovery Method
# COLUMN disc_year:      Discovery Year
# COLUMN disc_pubdate:   Discovery Publication Date
# COLUMN disc_facility:  Discovery Facility
# COLUMN st_mass:        Stellar Mass [Solar mass]
# COLUMN glat:           Galactic Latitude [deg]
# COLUMN glon:           Galactic Longitude [deg]
# COLUMN sy_dist:        Distance [pc]
'''

def printSortedDict(d):
	for key, value in sorted(d.items(), key=lambda item: item[1], reverse=True):
		print(str(key) + ": " + str(value))
	print()

def getDetectionCode(s):
	if s == "Radial Velocity":
		return 0
	if s == "Transit":
		return 1
	if s == "Imaging":
		return 2
	if s == "Microlensing":
		return 3
	return 4

def getTelescopeCode(s):
	if s == "K2":
		return 0
	if s == "Kepler":
		return 1
	if s == "Transiting Exoplanet Survey Satellite (TESS)":
		return 2
	return 3

def getPosition(latDegrees, longDegrees, r):
	lat = math.radians(latDegrees)
	long = math.radians(longDegrees)
	return r * math.cos(lat) * math.cos(long), r * math.cos(lat) * math.sin(long), r * math.sin(lat)

outfile = open(DATA_OUT, "w")
outfile.write("#Data pulled from NASA Exoplanet Archive\n\n")
outfile.write("datavar 0 year\n")
outfile.write("datavar 1 method\n")
outfile.write("datavar 2 telescope\n")
outfile.write("datavar 3 texture\n")
outfile.write("texture 1 -M halo.pbm\n")
outfile.write("texturevar 3\n\n")

nameSet = set() #Prevent duplicates

methodSet = dict()
telescopeSet = dict()

badDataPoints = 0
infile = open(DATA_SOURCE, "r")

skipTitles = True
for line in infile.readlines():
	if line[0] == "#":  #Skip header commments
		continue
	if skipTitles:
		skipTitles = False #Skip header titles
		continue

	parts = line.strip().split(",")

	try:
		name = parts[0]
		detectionCode = getDetectionCode(parts[1])
		year = int(parts[2]) + random.random()
		telescopeCode = getTelescopeCode(parts[4])
		x, y, z = getPosition(float(parts[6]), float(parts[7]), float(parts[8]))
	except:
		badDataPoints += 1
		continue

	if name not in nameSet:
		nameSet.add(name)
		for i in range(2):
			outfile.write("%.5f %.5f %.5f %.5f %d %d 1\n" % (x, y, z, year, detectionCode, telescopeCode))

		if parts[1] in methodSet.keys():
			methodSet[parts[1]] += 1
		else:
			methodSet[parts[1]] = 1

		if parts[4] in telescopeSet.keys():
			telescopeSet[parts[4]] += 1
		else:
			telescopeSet[parts[4]] = 1

print("Missing Data Points: " + str(badDataPoints) +"\n")

printSortedDict(methodSet)
printSortedDict(telescopeSet)