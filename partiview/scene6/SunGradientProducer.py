import sys
sys.path.append("..")
from Interpolator import getInterpolator

colors = open('movingStarsSolar/colors.cmap', "w")
gradNum = 40
colors.write("%d\n" % (gradNum + 3))
colors.write("1.0 0.8 0.5 1.0\n0.8 0.95 0.93 1.0\n0.16 0.64 1.0 1.0\n")

COLOR = getInterpolator(start_x=0, end_x=gradNum, power=1, y_lists=[[1, 1], [1, 0.55], [0.5, 0.2]])

for i in range(gradNum):
	col = COLOR(i)
	colors.write("%.3f %.3f %.3f 1.0\n" % (col[0], col[1], col[2]))
