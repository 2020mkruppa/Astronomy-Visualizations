DATA_SOURCE = 'stars.speck'
DATA_OUT = 'starsOut.speck'

HOLES = [(10, [0, 0 ,0])] #List of (radius, [origin])

#COPY_SHIFT = [320, 0, 0] #None if no shift
COPY_SHIFT = None

def shouldInclude(x, y, z):
	for radius, origin in HOLES:
		if (x - origin[0])**2 + (y - origin[1])**2 + (z - origin[2])**2 < radius**2:
			return False

	if 40 < z < 150 and (x**2 + y**2 < 2000):
		return False
	if -40 < y < 150 and (x**2 + z**2 < 2800):
		return False
	return True

outfile = open(DATA_OUT, "w")
outfile.write('# MODIFIED TO OMIT STARS\n\n')
if COPY_SHIFT is not None:
	outfile.write('# MODIFIED TO COPY STARS TO ' + str(COPY_SHIFT) + '\n\n')

infile = open(DATA_SOURCE, "r")
linesToCopy = 22 #Copy the lines at the top of the file
skipNum = 0
for line in infile.readlines():
	if linesToCopy > 0:
		linesToCopy -= 1
		outfile.write(line)
		continue

	parts = line.strip().split()
	if shouldInclude(float(parts[0]), float(parts[1]), float(parts[2])):
		outfile.write(line)

	skipNum = (skipNum + 1) % 3
	if COPY_SHIFT is not None and skipNum == 0:
		newX = float(parts[0]) + COPY_SHIFT[0]
		newY = float(parts[1]) + COPY_SHIFT[1]
		newZ = float(parts[2]) + COPY_SHIFT[2]
		if shouldInclude(newX, newY, newZ):
			parts[0] = str(newX)
			parts[1] = str(newY)
			parts[2] = str(newZ)
			outfile.write(" ".join(parts) + "\n")