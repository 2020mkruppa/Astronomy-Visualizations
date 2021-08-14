import sys
import shutil
sys.path.append("..")
from Producer import producePath
from Producer import getEulerAnglesAzimuthElevation
from Producer import fadeIn


producePath(dataFileIn=open('pathData.txt', "r"), pathFileOut=open('outPath.wf', "w"),
			framesFileOut=open('makeFrames.cf', "w"), speedMultiplier=0.6, bezierTightness=1.2,
			numericalSteps=3500, timeOffset=0,
			singleCommands={**fadeIn(group='g2', start=2100, maxAlpha=0.9, frameStep=0.6)},
			angleFunction=getEulerAnglesAzimuthElevation, startFrame=0, framesFolder="scene4FramesRaw")

shutil.rmtree('../__pycache__')