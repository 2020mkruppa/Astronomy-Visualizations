import sys
import shutil
sys.path.append("..")
from Producer import producePath
from Producer import getEulerAnglesAzimuthElevation
from Producer import fadeIn
from Producer import fadeOut

producePath(dataFileIn=open('pathData.txt', "r"), pathFileOut=open('outPath.wf', "w"),
			framesFileOut=open('makeFrames.cf', "w"), speedMultiplier=0.6, bezierTightness=1.2,
			numericalSteps=3500, timeOffset=0,
			singleCommands={**fadeIn(group='g2', start=3250, maxAlpha=0.9, frameStep=0.6),
							**fadeIn(group='g3', start=6650, maxAlpha=0.9, frameStep=0.6),
							**fadeOut(group='g3', start=7600, startAlpha=0.9, frameStep=0.6)},
			angleFunction=getEulerAnglesAzimuthElevation, startFrame=0, frameFolder="scene4Frames")

shutil.rmtree('../__pycache__')