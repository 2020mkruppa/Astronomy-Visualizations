import sys
import shutil
sys.path.append("..")
from Producer import producePath
from Producer import getEulerAnglesAzimuthElevation
from Producer import fadeIn
from Producer import fadeOut
from Interpolator import getInterpolator

def mergeDict(dics):
	output = dict()
	for partial in dics:
		for key in partial:
			if key in output.keys():
				output[key] = output[key] + "\n" + partial[key]
			else:
				output[key] = partial[key]
	return output


def changeStarBrightness(startLum, endLum, startFrame, endFrame, group):
	commands = dict()
	interp = getInterpolator(start_x=startFrame, end_x=endFrame, power=1, y_lists=[[startLum, endLum]])
	for f in range(startFrame, endFrame + 1):
		commands[f] = 'eval ' + group + ' slum %.3f' % interp(f)[0]
	return commands


def yearSeries(startYear, endYear, startFrame, endFrame):
	commands = dict()
	interp = getInterpolator(start_x=startFrame, end_x=endFrame, power=1, y_lists=[[startYear, endYear]])
	for f in range(startFrame, endFrame + 1):
		command = 'eval g2 on\neval g3 on\neval g4 on\neval g5 on\n' if f == startFrame else ""
		command += 'eval g2 only= year <%.5f\n' % interp(f)[0]
		command += 'eval g3 only= year <%.5f\n' % interp(f)[0]
		command += 'eval g4 only= year <%.5f\n' % interp(f)[0]
		command += 'eval g5 only= year <%.5f\n' % interp(f)[0]
		commands[f] = command
	return commands

def flip(frame, group, parity):
	return {frame: 'eval ' + group + '\neval ' + parity + '\n'}

def polygons(frame, group, parity):
	return {frame: 'eval ' + group + '\neval polygons ' + parity + '\n'}


def fadeOutPartly(group, start, startAlpha, endAlpha, frameStep):
	commands = dict()
	for i in range(int(startAlpha * 100), int(endAlpha * 100) -1, -1):
		index = start + int(frameStep * (int(startAlpha * 100) - i))
		commands[index] = 'eval ' + group + '\neval alpha %.2f' % (i / 100)
	return commands

FIRST_HIGHLIGHT_START = 4200
FIRST_HIGHLIGHT_END = 4270
FIRST_HIGHLIGHT_SELECT = 4340

SECOND_FADE_START = 6660
SECOND_FADE_END = 6730

THIRD_FADE_START = 6970
THIRD_FADE_END = 7060
THIRD_FADE_SELECT = 7150

producePath(dataFileIn=open('pathData.txt', "r"), pathFileOut=open('outPath.wf', "w"),
			framesFileOut=open('makeFrames.cf', "w"), speedMultiplier=0.6, bezierTightness=1.2,
			numericalSteps=3500, timeOffset=0,
			singleCommands=mergeDict([changeStarBrightness(startLum=5, endLum=0.6, startFrame=500, endFrame=600, group='g1'),
			yearSeries(startYear=1995, endYear=2022, startFrame=600, endFrame=2700),

			changeStarBrightness(startLum=1, endLum=15, startFrame=FIRST_HIGHLIGHT_START, endFrame=FIRST_HIGHLIGHT_END, group='g2'),
			changeStarBrightness(startLum=1, endLum=0.02, startFrame=FIRST_HIGHLIGHT_START, endFrame=FIRST_HIGHLIGHT_END, group='g3'),
			changeStarBrightness(startLum=1, endLum=0.02, startFrame=FIRST_HIGHLIGHT_START, endFrame=FIRST_HIGHLIGHT_END, group='g4'),
			changeStarBrightness(startLum=1, endLum=0.02, startFrame=FIRST_HIGHLIGHT_START, endFrame=FIRST_HIGHLIGHT_END, group='g5'),
			changeStarBrightness(startLum=15, endLum=1, startFrame=FIRST_HIGHLIGHT_END, endFrame=FIRST_HIGHLIGHT_SELECT, group='g2'),
			polygons(frame=FIRST_HIGHLIGHT_END, group='g3', parity='off'),
			polygons(frame=FIRST_HIGHLIGHT_END, group='g4', parity='off'),
			polygons(frame=FIRST_HIGHLIGHT_END, group='g5', parity='off'),
			polygons(frame=4500, group='g2', parity='off'),


			fadeIn(group='g7', start=5050, maxAlpha=0.15, frameStep=2),

			flip(frame=5571, group='g8', parity='off'),
			flip(frame=5571, group='g9', parity='on'),


			fadeOut(group='g9', start=6600, startAlpha=0.15, frameStep=2),
			changeStarBrightness(startLum=1, endLum=0.02, startFrame=SECOND_FADE_START, endFrame=SECOND_FADE_END, group='g2'),


			polygons(frame=THIRD_FADE_START, group='g3', parity='on'),
			changeStarBrightness(startLum=0.02, endLum=1.8, startFrame=THIRD_FADE_START, endFrame=THIRD_FADE_END, group='g3'),
			changeStarBrightness(startLum=1.8, endLum=0.02, startFrame=THIRD_FADE_END, endFrame=THIRD_FADE_SELECT, group='g3'),
			polygons(frame=THIRD_FADE_SELECT, group='g3', parity='off'),

		    flip(frame=8551, group='g6', parity='off'),
		    flip(frame=8551, group='g10', parity='on'),

			fadeOutPartly(group='g10', start=9300, startAlpha=0.15, endAlpha=0.05, frameStep=4),

									  ]),

			angleFunction=getEulerAnglesAzimuthElevation, startFrame=0)

shutil.rmtree('../__pycache__')