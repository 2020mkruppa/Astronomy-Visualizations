import sys
import shutil
sys.path.append("..")
from Producer import producePath
from Producer import getEulerAnglesAzimuthElevation
from Producer import getEulerAnglesAxisAngle
from Producer import fadeIn
from Producer import fadeOut
from Interpolator import getInterpolator

def changeStarBrightness(startLum, endLum, startFrame, endFrame, group):
	commands = dict()
	interp = getInterpolator(start_x=startFrame, end_x=endFrame, power=1, y_lists=[[startLum, endLum]])
	for f in range(startFrame, endFrame + 1):
		commands[f] = 'eval ' + group + '\neval slum %.3f\n' % interp(f)[0]
		if f == startFrame:
			commands[startFrame] = 'eval ' + group + '\n' + commands[startFrame]
	return commands


def yearSeries(startYear, endYear, startFrame, endFrame, group):
	commands = dict()
	interp = getInterpolator(start_x=startFrame, end_x=endFrame, power=1, y_lists=[[startYear, endYear]])
	for f in range(startFrame, endFrame + 1):
		commands[f] = 'eval ' + group + '\neval only= year <%.5f\n' % interp(f)[0]
		if f == startFrame:
			commands[startFrame] = 'eval ' + group + '\neval on\n' + commands[startFrame]
	return commands

producePath(dataFileIn=open('pathData.txt', "r"), pathFileOut=open('outPath.wf', "w"),
			framesFileOut=open('makeFrames.cf', "w"), speedMultiplier=0.6, bezierTightness=1.2,
			numericalSteps=3500, timeOffset=0,
			singleCommands={**changeStarBrightness(startLum=5, endLum=0.5, startFrame=700, endFrame=800, group='g1'),
							**yearSeries(startYear=1995, endYear=2022, startFrame=800, endFrame=1500, group='g2')},
			angleFunction=getEulerAnglesAzimuthElevation, startFrame=0)

shutil.rmtree('../__pycache__')
'''
**fadeIn(group='g3', start=6650, maxAlpha=0.9, frameStep=0.6),
							**fadeOut(group='g3', start=7600, startAlpha=0.9, frameStep=0.6)'''