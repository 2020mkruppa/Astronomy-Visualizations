DATA_SOURCE = 'stars.speck'
DATA_OUT = 'starsDim.speck'

MAX_LUM = 100


def shouldInclude(b):
	return b < MAX_LUM

outfile = open(DATA_OUT, "w")
outfile.write('# MODIFIED TO OMIT STARS TOO BRIGHT\n\n')

infile = open(DATA_SOURCE, "r")
linesToCopy = 22 #Copy the lines at the top of the file
for line in infile.readlines():
	if linesToCopy > 0:
		linesToCopy -= 1
		outfile.write(line)
		continue

	parts = line.strip().split()
	if shouldInclude(float(parts[4])):
		outfile.write(line)
