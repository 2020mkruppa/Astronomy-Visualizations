#Formatter for https://colordesigner.io/gradient-generator
DATA_OUT = 'movingStars/colors.cmap'
def getOriginalFromNormalized(minimum, maximum, norm): #Norm is [0, 1], that returns a linear proportion between [min, max]
	return minimum + (norm * (maximum - minimum))

data = []
for pos in range(40):
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

fileOut = open(DATA_OUT, "w")
fileOut.write(str(len(data) + 2) + '\n')
for d in data:
	fileOut.write(d)
fileOut.write("1.0 1.0 0.5 1.0\n")
fileOut.write("1.0 1.0 1.0 1.0")
