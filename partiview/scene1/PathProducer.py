import sys
import shutil
sys.path.append("..")
from Producer import producePath
from Producer import getEulerAnglesAzimuthElevation
from Producer import fadeIn

producePath(dataFileIn=open('pathData.txt', "r"), pathFileOut=open('outPath.wf', "w"),
			framesFileOut=open('makeFrames.cf', "w"), speedMultiplier=0.95, bezierTightness=1.2,
			numericalSteps=3500, timeOffset=2000,  singleCommands={**fadeIn(group='g2', start=2000, maxAlpha=0.99, frameStep=0.8)},
			angleFunction=getEulerAnglesAzimuthElevation, startFrame=0, framesFolder="scene1FramesRaw")


shutil.rmtree('../__pycache__')
