DATA_SOURCE = 'stars.speck'
DATA_OUT = 'starsOut.speck'

MIN_RADIUS = 50

def shouldInclude(x, y, z):
	return x**2 + y**2 + z**2 > MIN_RADIUS**2



outfile = open(DATA_OUT, "w")
outfile.write('# MODIFIED TO OMIT STARS CLOSER THAN ' + str(MIN_RADIUS) + '\n\n')

infile = open(DATA_SOURCE, "r")
linesToCopy = 22 #Copy the lines at the top of the file
for line in infile.readlines():
	if linesToCopy > 0:
		linesToCopy -= 1
		outfile.write(line)
		continue

	parts = line.strip().split()
	if shouldInclude(float(parts[0]), float(parts[1]), float(parts[2])):
		outfile.write(line)

