import sys
import shutil
sys.path.append("..")
from Producer import producePath
from Producer import getEulerAnglesAzimuthElevation
from Producer import fadeIn
from Producer import fadeOut

producePath(dataFileIn=open('pathData.txt', "r"), pathFileOut=open('outPath.wf', "w"),
			framesFileOut=open('makeFrames.cf', "w"), speedMultiplier=0.46, bezierTightness=1.2,
			numericalSteps=3500, timeOffset=0,
			singleCommands={**fadeIn(group='g2', start=4042, maxAlpha=0.65, frameStep=3),
							**fadeOut(group='g2', start=8866, startAlpha=0.65, frameStep=3),
							**fadeOut(group='g3', start=9909, startAlpha=0.99, frameStep=0.6),
							**fadeIn(group='g3', start=10013, maxAlpha=0.99, frameStep=0.6),
							**fadeIn(group='g2', start=10091, maxAlpha=0.99, frameStep=1.2),
							**fadeOut(group='g3', start=10613, startAlpha=0.99, frameStep=0.6),
							**fadeIn(group='g3', start=10887, maxAlpha=0.99, frameStep=0.6)
							},
			angleFunction=getEulerAnglesAzimuthElevation, startFrame=0, framesFolder="scene2FramesRaw")

shutil.rmtree('../__pycache__')