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
			singleCommands={**fadeIn(group='g2', start=3100, maxAlpha=0.65, frameStep=3),
							**fadeOut(group='g2', start=6800, startAlpha=0.65, frameStep=3),
							**fadeOut(group='g3', start=7600, startAlpha=0.99, frameStep=0.6),
							**fadeIn(group='g3', start=7680, maxAlpha=0.99, frameStep=0.6),
							**fadeIn(group='g2', start=7740, maxAlpha=0.99, frameStep=1.2),
							**fadeOut(group='g3', start=8140, startAlpha=0.99, frameStep=0.6),
							**fadeIn(group='g3', start=8350, maxAlpha=0.99, frameStep=0.6)
							},
			angleFunction=getEulerAnglesAzimuthElevation, startFrame=0, framesFolder="scene2Frames")

shutil.rmtree('../__pycache__')