import cv2
import os
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import sys
sys.path.append("..")
from Interpolator import getInterpolator

FADE_START = 590
YEAR_START = 660
YEAR_END = 4200
FADE_END = 4270

SEMI_24 = ImageFont.truetype("../fonts/Montserrat-SemiBold.ttf", 30)
SEMI_40 = ImageFont.truetype("../fonts/Montserrat-SemiBold.ttf", 50)

YEAR_INTERP = getInterpolator(start_x=YEAR_START, end_x=YEAR_END, power=1, y_lists=[[1995, 2021]])
WHITE = 255

def getFadeMultiplier(frameNum):
	if frameNum <= YEAR_START:
		return getInterpolator(start_x=FADE_START, end_x=YEAR_START, power=1, y_lists=[[0, 1]])(frameNum)[0]
	return getInterpolator(start_x=YEAR_END, end_x=FADE_END, power=1, y_lists=[[1, 0]])(frameNum)[0]

def addText(image, frameNum):
	if FADE_START <= frameNum <= FADE_END:
		black = Image.fromarray(image)
		draw = ImageDraw.Draw(black)

		fade = getFadeMultiplier(frameNum)
		year = int(YEAR_INTERP(frameNum)[0])
		fadeWhite = int(fade * WHITE)

		draw.text((22, 845), str(year), font=SEMI_40, anchor="lt", stroke_width=0, fill=(fadeWhite, fadeWhite, fadeWhite, 100))
		draw.text((55, 915), "Doppler Spectroscopy", font=SEMI_24, anchor="lt", stroke_width=0, fill=(fadeWhite, fadeWhite, fadeWhite, 100))
		draw.text((55, 965), "Transit", font=SEMI_24, anchor="lt", stroke_width=0, fill=(fadeWhite, fadeWhite, fadeWhite, 100))
		draw.text((55, 1015), "Other", font=SEMI_24, anchor="lt", stroke_width=0, fill=(fadeWhite, fadeWhite, fadeWhite, 100))
		texted = np.array(black)

		cv2.rectangle(texted, (25, 920), (40, 935), (0, 0, fadeWhite), -1)
		cv2.rectangle(texted, (25, 970), (40, 985), (fadeWhite, fadeWhite, 0), -1)
		cv2.rectangle(texted, (25, 1020), (40, 1035), (0, fadeWhite, fadeWhite), -1)

		return texted

	return image


def getNumberString(num):
	if num >= 10000:
		return str(num)
	return "{:04d}".format(num)


for i in range(FADE_START, FADE_END + 1):
	if i % ((FADE_END - FADE_START) // 20) == 0:
		print("Image " + str(i) + " out of " + str(FADE_END - FADE_START))
	address = "../scene5FramesRaw/frame." + getNumberString(i) + ".png"
	img = cv2.imread(address)
	img = addText(img, i)
	cv2.imwrite(address, img)  # save frame as JPEG file