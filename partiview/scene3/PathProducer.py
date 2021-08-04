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
			framesFileOut=open('makeFrames.cf', "w"), speedMultiplier=0.6, bezierTightness=1.2,
			numericalSteps=3500, timeOffset=0,
			singleCommands=mergeDict([
							fadeIn(group='g6', start=1250, maxAlpha=0.9, frameStep=0.6),
							fadeOut(group='g6', start=1400, startAlpha=0.9, frameStep=0.6),
							fadeOut(group='g7', start=1400, startAlpha=1.0, frameStep=0.6),
							fadeOut(group='g5', start=3000, startAlpha=1.0, frameStep=0.6),


							fadeIn(group='g2', start=3100, maxAlpha=0.65, frameStep=3),
							fadeIn(group='g3', start=5300, maxAlpha=0.7, frameStep=2)]),
			angleFunction=getEulerAnglesAzimuthElevation, startFrame=0, frameFolder="scene3Frames")

shutil.rmtree('../__pycache__')