import sys
import shutil
sys.path.append("..")
from Producer import producePath
from Producer import getEulerAnglesAzimuthElevation


producePath(dataFileIn=open('pathData.txt', "r"), pathFileOut=open('outPath.wf', "w"),
			framesFileOut=open('makeFrames.cf', "w"), speedMultiplier=0.95, bezierTightness=1.2,
			numericalSteps=3500, timeOffset=2300,  singleCommands={2300 : 'eval g2', 2308: 'eval on\neval alpha 0.03',
								   2316: 'eval alpha 0.06', 2324: 'eval alpha 0.09', 2332: 'eval alpha 0.12', 2340: 'eval alpha 0.15',
								   2348: 'eval alpha 0.18', 2356: 'eval alpha 0.21', 2364: 'eval alpha 0.24', 2372: 'eval alpha 0.27',
								   2380: 'eval alpha 0.30', 2388: 'eval alpha 0.33', 2396: 'eval alpha 0.36', 2404: 'eval alpha 0.39',
								   2412: 'eval alpha 0.42', 2420: 'eval alpha 0.45', 2428: 'eval alpha 0.48', 2436: 'eval alpha 0.51',
								   2444: 'eval alpha 0.54', 2452: 'eval alpha 0.57', 2460: 'eval alpha 0.60', 2468: 'eval alpha 0.63',
								   2476: 'eval alpha 0.66'},
			angleFunction=getEulerAnglesAzimuthElevation)

shutil.rmtree('../__pycache__')
