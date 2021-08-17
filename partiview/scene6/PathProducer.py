import sys
import shutil
sys.path.append("..")
from Producer import producePath
from Producer import getEulerAnglesAzimuthElevation
from Producer import fadeIn
from Producer import fadeOut

def mergeDict(dics):
	output = dict()
	for partial in dics:
		for key in partial:
			if key in output.keys():
				output[key] = output[key] + "\n" + partial[key]
			else:
				output[key] = partial[key]
	return output

def flip(frame, group, parity):
	return {frame: 'eval ' + group + '\neval ' + parity + '\n'}

producePath(dataFileIn=open('pathData.txt', "r"), pathFileOut=open('outPath.wf', "w"),
			framesFileOut=open('makeFrames.cf', "w"), speedMultiplier=0.95, bezierTightness=1.2,
			numericalSteps=3500, timeOffset=0,  singleCommands=mergeDict([
									fadeIn(group='g7', start=1650, maxAlpha=0.65, frameStep=1),
									fadeIn(group='g5', start=3990, maxAlpha=0.99, frameStep=0.7),
									fadeIn(group='g6', start=3990, maxAlpha=0.99, frameStep=0.7),

								    flip(frame=5370, group='g7', parity='off'),
								    flip(frame=5370, group='g2', parity='on'),
								    flip(frame=5520, group='g2', parity='off'),
								    flip(frame=5520, group='g8', parity='on'),

									fadeOut(group='g3', start=5340, startAlpha=0.99, frameStep=0.7),
																		  ]),
			angleFunction=getEulerAnglesAzimuthElevation, startFrame=0, framesFolder="scene6FramesRaw")


shutil.rmtree('../__pycache__')
