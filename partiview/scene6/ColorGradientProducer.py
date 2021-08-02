import sys
sys.path.append("..")
from Interpolator import getInterpolator

def write(s):
	colors1.write(s)
	colors2.write(s)
	colors3.write(s)

COLOR1 = 'habitableZoneMoving/colors.cmap'
COLOR2 = 'habitableZoneInner/colors.cmap'
COLOR3 = 'habitableZoneOuter/colors.cmap'


colors1 = open(COLOR1, "w")
colors2 = open(COLOR2, "w")
colors3 = open(COLOR3, "w")

gradNum = 40
write("83\n")

FADE_OUT = getInterpolator(start_x=22, end_x=40, power=1, y_lists=[[1, 0]])
FADE_IN = getInterpolator(start_x=0, end_x=18, power=1, y_lists=[[0, 1]])
GREEN_MULTIPLIER = 0.4
for i in range(gradNum):#Red to green
	fade = FADE_IN(i)[0]
	v = (1 / (gradNum - 1)) * i
	write("%.3f %.3f %.3f 1.0\n" % ((1 - v) * fade, v * fade * GREEN_MULTIPLIER, 0))

for i in range(gradNum):#Green to blue
	fade = FADE_OUT(i)[0]
	v = (1 / (gradNum - 1)) * i
	write("%.3f %.3f %.3f 1.0\n" % (0, (1 - v) * fade * GREEN_MULTIPLIER, v * fade))

write("0.0 %.3f 0.0 1.0\n" % GREEN_MULTIPLIER)
write("1.0 1.0 1.0 1.0\n")
write("1.0 1.0 0.0 1.0\n")