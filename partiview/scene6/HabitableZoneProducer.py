from math import cos
from math import sin
from math import radians as rad
import sys
sys.path.append("..")
from Interpolator import getInterpolator

ZONE_OUT = 'habitableZoneMoving/habitableZoneMoving.speck'
INNER_OUT = 'habitableZoneInner/habitableZoneInner.speck'
OUTER_OUT = 'habitableZoneOuter/habitableZoneOuter.speck'

RADIUS = getInterpolator(start_x=5370, end_x=5520, power=2, y_lists=[[8, 0.25], [3.2, 0.13]]) #Outer, Inner
GRAD_INSET = 0.15
GRAD_LENGTH = 0.4
COLOR_NUM = 40

def addBoundary(r, file):
	length = 4
	stroke = 6
	for reps in range(6):
		for i in range(int(360 / (2 * length))):
			file.write('mesh -c 82 -w 3 -s wire {\n1 ' + str(stroke) + '\n')
			for a in range(stroke):
				arg = rad(2 * i * length + a)
				file.write("%.4f 0 %.4f\n" % (r * cos(arg), r * sin(arg)))
			file.write('}\n')

def addGradientRegion(rInner, rOuter, file):
	length = 3
	for i in range(0, 360, length):
		arg1 = rad(i)
		arg2 = rad(i + length)

		gradInset = (rOuter - rInner) * GRAD_INSET
		addPanel(rInner + gradInset, arg1, rOuter - gradInset, arg2, 40, file)

		gradLength = (rOuter - rInner) * GRAD_LENGTH
		deltaRadius = gradLength / COLOR_NUM
		for radNum in range(COLOR_NUM):
			outer = rInner + gradInset - (radNum * deltaRadius)
			inner = rInner + gradInset - ((radNum + 1) * deltaRadius)
			addPanel(inner, arg1, outer, arg2, COLOR_NUM - 1 - radNum, file)

		for radNum in range(COLOR_NUM):
			inner = rOuter - gradInset + (radNum * deltaRadius)
			outer = rOuter - gradInset + ((radNum + 1) * deltaRadius)
			addPanel(inner, arg1, outer, arg2, radNum + COLOR_NUM, file)

def addPanel(r1, arg1, r2, arg2, color, file):
	file.write("mesh -c %d -s solid {\n2 2\n" % color)
	file.write("%.5f 0 %.5f\n" % (r1 * cos(arg1), r1 * sin(arg1)))
	file.write("%.5f 0 %.5f\n" % (r2 * cos(arg1), r2 * sin(arg1)))
	file.write("%.5f 0 %.5f\n" % (r1 * cos(arg2), r1 * sin(arg2)))
	file.write("%.5f 0 %.5f\n" % (r2 * cos(arg2), r2 * sin(arg2)))
	file.write("}\n")


zone = open(ZONE_OUT, "w")
for t in range(5370, 5520):
	if t % 20 == 0:
		print(t)
	zone.write('datatime ' + str(t) + '\n')

	inner = RADIUS(t)[1]
	outer = RADIUS(t)[0]
	addBoundary(inner, zone)
	addBoundary(outer, zone)
	addGradientRegion(inner, outer, zone)

inner = open(INNER_OUT, "w")
radiusInner = RADIUS(100000)[1]
radiusOuter = RADIUS(100000)[0]
addBoundary(radiusInner, inner)
addBoundary(radiusOuter, inner)
addGradientRegion(radiusInner, radiusOuter, inner)

outer = open(OUTER_OUT, "w")
radiusInner = RADIUS(0)[1]
radiusOuter = RADIUS(0)[0]
addBoundary(radiusInner, outer)
addBoundary(radiusOuter, outer)
addGradientRegion(radiusInner, radiusOuter, outer)