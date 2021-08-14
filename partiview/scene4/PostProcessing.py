import cv2
import sys
sys.path.append("..")
from Interpolator import getInterpolator

FADE_START = 2790
FULL_START = 2840
FULL_END = 3550
FADE_END = 3600

def getFadeMultiplier(frameNum):
	if frameNum <= FULL_START:
		return getInterpolator(start_x=FADE_START, end_x=FULL_START, power=1, y_lists=[[0, 1]])(frameNum)[0]
	return getInterpolator(start_x=FULL_END, end_x=FADE_END, power=1, y_lists=[[1, 0]])(frameNum)[0]

def overlayBlack(base, black, blackStength):
	return cv2.addWeighted(base, 1 - blackStength, black, blackStength, 0)

def addCircles(image, frameNum):
	if FADE_START <= frameNum <= FADE_END:
		fade = getFadeMultiplier(frameNum)
		circled = image.copy()

		cv2.circle(circled, (920, 545), 25, (0, 0, 0), -1, cv2.LINE_AA)
		#cv2.circle(circled, (1033, 545), 2.5, (0, 0, 0), -1, cv2.LINE_AA)
		cv2.circle(circled, (2066, 1090), 5, (0, 0, 0), -1, cv2.LINE_AA, 1)
		return overlayBlack(image, circled, fade)

	return image


def getNumberString(num):
	if num >= 10000:
		return str(num)
	return "{:04d}".format(num)


for i in range(FADE_START, FADE_END + 1):
	if i % ((FADE_END - FADE_START) // 20) == 0:
		print("Image " + str(i) + " out of " + str(FADE_END - FADE_START))
	address = "../scene4FramesRaw/frame." + getNumberString(i) + ".png"
	img = cv2.imread(address)
	img = addCircles(img, i)
	cv2.imwrite(address, img)