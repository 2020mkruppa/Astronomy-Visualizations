COLOR_OUT = 'multiPlanetOrbits/colors.cmap'
colors = open(COLOR_OUT, "w")
gradNum = 20
colors.write(str(gradNum) + "\n")
for i in range(gradNum):
	v = (1 / (gradNum - 1)) * i
	colors.write("%.3f %.3f %.3f 1.0\n" % (v, v, v))