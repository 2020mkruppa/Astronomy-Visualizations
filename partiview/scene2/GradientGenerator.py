import math
#Formatter for https://colordesigner.io/gradient-generator
#Start color is 255 170 90, then 255 255 25, then 0 255 210

DATA_OUT = 'movingStars/colors.cmap'
DATA_IN = 'colorGradIn.txt'

def getOriginalFromNormalized(minimum, maximum, norm): #Norm is [0, 1], that returns a linear proportion between [min, max]
	return minimum + (norm * (maximum - minimum))

fileIn = open(DATA_IN, "r")
data = []
pos = 0
for line in fileIn.readlines():
	pos += 1
	if pos <= 20:
		r = getOriginalFromNormalized(0.76, 0.625, pos / 20)
		g = getOriginalFromNormalized(0.55, 0.625, pos / 20)
		b = getOriginalFromNormalized(0.50, 0.625, pos / 20)
		data.append("%.5f %.5f %.5f %.5f\n" % (r, g, b, 1.0))
	else:
		r = getOriginalFromNormalized(0.625, 0.54, (pos - 20) / 20)
		g = getOriginalFromNormalized(0.625, 0.66, (pos - 20) / 20)
		b = getOriginalFromNormalized(0.625, 0.99, (pos - 20) / 20)
		data.append("%.5f %.5f %.5f %.5f\n" % (r, g, b, 1.0))

		'''parts = line.strip()[4:].replace(" ", "").replace(")", "").split(",")
		r = int(parts[0]) / 255
		g = int(parts[1]) / 255
		b = int(parts[2]) / 255
		bias = 1.4 - (0.0006*(pos-20)*(pos-20))
		size = max(r + g + b - bias, 1)  #0.76 0.55 0.50
		print(size)
		rNorm = r / size
		gNorm = g / size
		bNorm = b / size
		#print("%.5f %.5f %.5f" % (rNorm + gNorm + bNorm, rNorm * gNorm * bNorm, rNorm**2 + gNorm**2 + bNorm**2))
		data.append("%.5f %.5f %.5f %.5f\n" % (rNorm, gNorm, bNorm, 1.0))'''

fileOut = open(DATA_OUT, "w")
fileOut.write(str(len(data)) + '\n')
for d in data:
	fileOut.write(d)
