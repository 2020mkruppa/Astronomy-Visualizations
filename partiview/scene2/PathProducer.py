import sys
import shutil
sys.path.append("..")
from Producer import producePath
from Producer import getEulerAnglesAzimuthElevation


producePath(dataFileIn=open('pathData.txt', "r"), pathFileOut=open('outPath.wf', "w"),
			framesFileOut=open('makeFrames.cf', "w"), speedMultiplier=1, bezierTightness=1.2,
			numericalSteps=3500, timeOffset=600,  singleCommands={600 : 'eval g2 on'},
			angleFunction=getEulerAnglesAzimuthElevation)

shutil.rmtree('../__pycache__')