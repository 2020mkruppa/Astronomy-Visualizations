import cv2
import numpy as np
import os
from PIL import ImageFont, ImageDraw, Image
from Interpolator import getInterpolator

MOVIE_NAME = 'exoplanets.mp4'
FADE_LENGTH = 60
FADE = getInterpolator(start_x=0, end_x=FADE_LENGTH, power=1, y_lists=[[1, 0]])
BLACK_RECT = np.zeros((1080, 1920, 3), dtype=np.uint8)
TIMES_NEW = ImageFont.truetype("timesNewRoman.ttf", 100)  #https://www.freebestfonts.com/times-new-roman-font

def showImage(img):
	while True:
		cv2.imshow('frame', img)
		if cv2.waitKey(0) & 0xFF == ord('q'):
			return

def getTitleScreen(color):
	black = Image.fromarray(BLACK_RECT)
	draw = ImageDraw.Draw(black)
	draw.text((960, 540), "E X O P L A N E T S", font=TIMES_NEW, anchor="ms", stroke_width=1, fill=(color, color, color, 100))
	texted = np.array(black)
	cv2.line(texted, (500, 565), (1420, 565), (color, color, color), 3)
	return texted

def titleScreen():
	for z in range(60):
		writer.write(BLACK_RECT)
	for z in range(30):
		writer.write(getTitleScreen(int(255 * z / 30)))
	for z in range(150):
		writer.write(getTitleScreen(255))
	for z in range(30):
		writer.write(getTitleScreen(int(255 * (1 - (z / 30)))))
	for z in range(60):
		writer.write(BLACK_RECT)

def pause():
	for z in range(60):
		writer.write(BLACK_RECT)

def overlayBlack(image, blackStength):
	return cv2.addWeighted(image, 1 - blackStength, BLACK_RECT, blackStength, 0)

def considerFade(image, inFlag, outFlag, index, totalFrames):
	if index < FADE_LENGTH and inFlag: #Fade in
		return overlayBlack(image, FADE(index)[0])
	if index >= totalFrames - FADE_LENGTH and outFlag:  # Fade out
		return overlayBlack(image, FADE(totalFrames - index)[0])
	return image

def resizeImage(image):
	return cv2.resize(image, (1920, 1080), interpolation=cv2.INTER_CUBIC)

def folderFrames(folder, fadeIn, fadeOut, resize):
	frameNum = len(os.listdir(folder))
	print(folder + ": " + str(frameNum))

	for i in range(frameNum):
		if i % (frameNum // 20) == 0:
			print("Image " + str(i) + " out of " + str(frameNum))
		address = folder + "/frame." + "{:04d}".format(i) + ".png"
		img = cv2.imread(address)
		if resize:
			img = resizeImage(img)
		writer.write(considerFade(img, fadeIn, fadeOut, i, frameNum))



writer = cv2.VideoWriter(MOVIE_NAME, cv2.VideoWriter_fourcc(*'DIVX'), 60, (1920, 1080))
#############################################
titleScreen()
pause()
folderFrames(folder='scene0Frames', fadeIn=True, fadeOut=False, resize=False)
folderFrames(folder='scene1Frames', fadeIn=False, fadeOut=True, resize=True)
pause()
############################################
writer.release()