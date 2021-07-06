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
			singleCommands={},
			angleFunction=getEulerAnglesAzimuthElevation, startFrame=0)

shutil.rmtree('../__pycache__')