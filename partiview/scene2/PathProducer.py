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

producePath(dataFileIn=open('pathData.txt', "r"), pathFileOut=open('outPath.wf', "w"),
			framesFileOut=open('makeFrames.cf', "w"), speedMultiplier=0.46, bezierTightness=1.2,
			numericalSteps=3500, timeOffset=0,
			singleCommands=mergeDict([fadeIn(group='g2', start=3700, maxAlpha=0.99, frameStep=2),

							fadeOut(group='g2', start=8600, startAlpha=0.99, frameStep=1.5),

							fadeOut(group='g3', start=9720, startAlpha=0.99, frameStep=0.6),
							fadeIn(group='g3', start=9850, maxAlpha=0.99, frameStep=0.6),
							fadeIn(group='g2', start=9850, maxAlpha=0.99, frameStep=0.6),
							fadeOut(group='g3', start=10090, startAlpha=0.99, frameStep=0.6),
							fadeIn(group='g3', start=10180, maxAlpha=0.99, frameStep=0.6)
							]),
			angleFunction=getEulerAnglesAzimuthElevation, startFrame=0, framesFolder="scene2FramesRaw")

shutil.rmtree('../__pycache__')