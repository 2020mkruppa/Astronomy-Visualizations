import math
import sys
sys.path.append("..")
from Interpolator import getInterpolator

MOVING_SOLAR = 'movingStarsSolar/movingStars.speck'
ORBIT_SOLAR = 'orbitPathsSolar/orbits.speck'
MOVING_TRAPPIST = 'movingStarsTrappist/movingStars.speck'
ORBIT_TRAPPIST = 'orbitPathsTrappist/orbits.speck'

TELESCOPE = 'telescope/telescope.speck'
omega = 0.25       #Generally controls how fast the points move, specifically, multiplies globally into each input speed

def writePoint(pos, color, lum, texture, file, backdrop): #Motion along x-z plane
	for n in range(4):
		file.write("%.4f 0 %.4f %d %.4f %d\n" % (pos[0], pos[1], color, lum, texture))
	#if backdrop:
		#file.write("0.002 -0.001 0.0015 0 %.4f 0\n" % (lum / 200))  # Intentionally no texture, so it appears as opaque disc to provide backdrop

def writeTexture(pos, lum, texture, file):
	file.write("%.4f 0 %.4f 0 %.4f %d\n" % (pos[0], pos[1], lum, texture))

def getPosition(radius, time, period, offset):
	argument = ((6.28 / period) * time) + offset
	return [radius * math.cos(argument), radius * math.sin(argument)]

def writeOrbit(file, r):
	resolution = 150
	file.write('mesh -c 0 -w 3 -s wire {\n1 ' + str(resolution + 1) + '\n')
	for i in range(resolution + 1):
		pos = getPosition(r, i, resolution, 0)
		file.write("%.4f 0 %.4f\n" % (pos[0], pos[1]))
	file.write('}\n\n')

radii   = [[0.39 * 5, 0.72 * 5, 1.00 * 5, 1.52 * 5, 5.20 * 5, 9.54 * 5, 19.2 * 5, 30.1 * 5],
		   [0.011 * 5, 0.016 * 5, 0.022 * 5, 0.029 * 5, 0.038 * 5, 0.047 * 5, 0.062 * 5]]
periods = [[0.24, 0.62, 1.00, 1.88, 11.8, 29.5, 84.0, 165],
		   [0.0041 * 10, 0.0066 * 10, 0.011 * 10, 0.0167 * 10, 0.025 * 10, 0.0338 * 10, 0.051 * 10]]
offsets = [[2.6, 2.6, 0, 0.55, 1.335, 3, 2, 0], [2.6, 2.6, 0, 0.55, 1.335, 3, 2]]


orbitSolar = open(ORBIT_SOLAR, "w")
orbitTrap = open(ORBIT_TRAPPIST, "w")
movingSolar = open(MOVING_SOLAR, "w")
movingTrap = open(MOVING_TRAPPIST, "w")
telescope = open(TELESCOPE, "w")

for r in radii[0]:
	writeOrbit(orbitSolar, r)
for r in radii[1]:
	writeOrbit(orbitTrap, r)


movingSolar.write('datavar  0  color\n')
movingSolar.write('datavar  1  lum\n')
movingSolar.write('datavar  2  texture\n')

movingSolar.write('texture  -M 1  halo.pbm\n')
movingSolar.write('texture  -O 3  mars.sgi\n')
movingSolar.write('texture  -O 4  jupiter.sgi\n')
movingSolar.write('texture  -M 5  weakHalo.sgi\n')
movingSolar.write('texture  -O 6  mercury.sgi\n')
movingSolar.write('texture  -O 7  venus.sgi\n')
movingSolar.write('texture  -O 2  earth.sgi\n')   #Last to be front-most
movingSolar.write('texturevar 2\n\n')


movingTrap.write('datavar  0  color\n')
movingTrap.write('datavar  1  lum\n')
movingTrap.write('datavar  2  texture\n')

movingTrap.write('texture  -O 1  planet1.sgi\n')
movingTrap.write('texture  -O 2  planet2.sgi\n')
movingTrap.write('texture  -O 3  planet3.sgi\n')
movingTrap.write('texture  -O 4  planet4.sgi\n')
movingTrap.write('texture  -O 5  planet5.sgi\n')
movingTrap.write('texturevar 2\n\n')

SUN = getInterpolator(start_x=3100, end_x=3200, power=2, y_lists=[[800, 2], [3, 42]])

for i in range(6000):
	movingSolar.write('datatime ' + str(i) + '\n')
	movingTrap.write('datatime ' + str(i) + '\n')
	t = 6.28 * (i / 1200) * omega

	writePoint([0, 0], int(SUN(i)[1]), SUN(i)[0] /4, 1, movingSolar, True) #Sun

	if i < 3300:
		writeTexture(getPosition(radii[0][0], t, periods[0][0], offsets[0][0]), 1.6, 6, movingSolar) #Mercury
		writeTexture(getPosition(radii[0][1], t, periods[0][1], offsets[0][1]), 1.8, 7, movingSolar) #Venus
		writeTexture(getPosition(radii[0][2], t, periods[0][2], offsets[0][2]), 2.2, 2, movingSolar) #Earth
		writeTexture(getPosition(radii[0][3], t, periods[0][3], offsets[0][3]), 3.0, 3, movingSolar) #Mars
		writeTexture(getPosition(radii[0][4], t, periods[0][4], offsets[0][4]), 60, 4, movingSolar) #Jupiter
		writePoint(getPosition(radii[0][5], t, periods[0][5], offsets[0][5]), 0, 350, 5, movingSolar, False) #Saturn
		writePoint(getPosition(radii[0][6], t, periods[0][6], offsets[0][6]), 1, 350, 5, movingSolar, False) #Uranus
		writePoint(getPosition(radii[0][7], t, periods[0][7], offsets[0][7]), 2, 350, 5, movingSolar, False) #Neptune

	writeTexture(getPosition(radii[1][0], t, periods[1][0], offsets[1][0]), 0.015, 1, movingTrap)
	writeTexture(getPosition(radii[1][1], t, periods[1][1], offsets[1][1]), 0.015, 2, movingTrap)
	writeTexture(getPosition(radii[1][2], t, periods[1][2], offsets[1][2]), 0.015, 3, movingTrap)
	writeTexture(getPosition(radii[1][3], t, periods[1][3], offsets[1][3]), 0.015, 4, movingTrap)
	writeTexture(getPosition(radii[1][4], t, periods[1][4], offsets[1][4]), 0.015, 5, movingTrap)
	writeTexture(getPosition(radii[1][5], t, periods[1][5], offsets[1][5]), 0.015, 2, movingTrap)
	writeTexture(getPosition(radii[1][6], t, periods[1][6], offsets[1][6]), 0.015, 4, movingTrap)


telescope.write('datavar  0  color\n')
telescope.write('datavar  1  lum\n')
telescope.write('datavar  2  texture\n')
telescope.write('texture  -M 1  telescopeFront.sgi\n')
telescope.write('texturevar 2\n\n')
telescope.write('0 1 0 0 60 1')
