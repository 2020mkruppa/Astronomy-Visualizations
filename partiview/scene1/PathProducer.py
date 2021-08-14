import sys
import shutil
sys.path.append("..")
from Producer import producePath
from Producer import getEulerAnglesAzimuthElevation
from Producer import fadeIn

producePath(dataFileIn=open('pathData.txt', "r"), pathFileOut=open('outPath.wf', "w"),
			framesFileOut=open('makeFrames.cf', "w"), speedMultiplier=0.95, bezierTightness=0.7,
			numericalSteps=3500, timeOffset=2500,  singleCommands={**fadeIn(group='g2', start=2550, maxAlpha=0.9, frameStep=1.2)},
			angleFunction=getEulerAnglesAzimuthElevation, startFrame=0, framesFolder="scene1FramesRaw")


shutil.rmtree('../__pycache__')
