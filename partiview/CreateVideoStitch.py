import cv2
import numpy as np
import os
from PIL import ImageFont, ImageDraw, Image
from Interpolator import getInterpolator

MOVIE_NAME = 'testing.mp4'
FADE_LENGTH = 60
FADE = getInterpolator(start_x=0, end_x=FADE_LENGTH, power=1, y_lists=[[1, 0]])
BLACK_RECT = np.zeros((1080, 1920, 3), dtype=np.uint8)
BOLD_95 = ImageFont.truetype("fonts/Montserrat-Bold.ttf", 95)  #google fonts
SEMI_35 = ImageFont.truetype("fonts/Montserrat-SemiBold.ttf", 35)
SEMI_30 = ImageFont.truetype("fonts/Montserrat-SemiBold.ttf", 30)
SEMI_24 = ImageFont.truetype("fonts/Montserrat-SemiBold.ttf", 24)


def showImage(img):
	while True:
		cv2.imshow('frame', img)
		if cv2.waitKey(0) & 0xFF == ord('q'):
			return

def getTitleScreen(color):
	black = Image.fromarray(BLACK_RECT)
	draw = ImageDraw.Draw(black)
	draw.text((960, 540), "E X O P L A N E T S", font=BOLD_95, anchor="ms", stroke_width=1, fill=(color, color, color, 100))
	texted = np.array(black)
	cv2.line(texted, (500, 565), (1420, 565), (color, color, color), 3)
	return texted

def titleScreen():
	pause()
	for z in range(40):
		writer.write(getTitleScreen(int(255 * z / 30)))
	for z in range(150):
		writer.write(getTitleScreen(255))
	for z in range(40):
		writer.write(getTitleScreen(int(255 * (1 - (z / 30)))))
	pause()

def pause():
	for z in range(60):
		writer.write(BLACK_RECT)

def getCreditScreen2(color):
	black = Image.fromarray(BLACK_RECT)
	draw = ImageDraw.Draw(black)
	draw.text((960, 380), "Support from", font=SEMI_30, anchor="ms", stroke_width=0, fill=(color, color, color, 100))
	draw.text((960, 440), "Partiview", font=SEMI_24, anchor="ms", stroke_width=0, fill=(color, color, color, 100))
	draw.text((960, 500), "American Museum of Natural History", font=SEMI_24, anchor="ms", stroke_width=0, fill=(color, color, color, 100))
	draw.text((960, 560), "NASA Exoplanet Archive", font=SEMI_24, anchor="ms", stroke_width=0, fill=(color, color, color, 100))
	draw.text((960, 620), "Google Earth Studio", font=SEMI_24, anchor="ms", stroke_width=0, fill=(color, color, color, 100))
	draw.text((960, 680), "National Science Foundation", font=SEMI_24, anchor="ms", stroke_width=0, fill=(color, color, color, 100))

	texted = np.array(black)
	cv2.line(texted, (850, 395), (1070, 395), (color, color, color), 1)
	return texted

def getCreditScreen1(color):
	black = Image.fromarray(BLACK_RECT)
	draw = ImageDraw.Draw(black)
	draw.text((960, 450), "Advised by", font=SEMI_30, anchor="ms", stroke_width=0, fill=(color, color, color, 100))
	draw.text((960, 520), "Jacob Hamer", font=SEMI_30, anchor="ms", stroke_width=0, fill=(color, color, color, 100))
	draw.text((960, 580), "Dr. Kevin Schlaufman", font=SEMI_30, anchor="ms", stroke_width=0, fill=(color, color, color, 100))
	texted = np.array(black)
	cv2.line(texted, (870, 465), (1050, 465), (color, color, color), 1)
	return texted

def getCreditScreen0(color):
	black = Image.fromarray(BLACK_RECT)
	draw = ImageDraw.Draw(black)
	draw.text((960, 540), "Created by Michael Kruppa", font=SEMI_35, anchor="ms", stroke_width=0, fill=(color, color, color, 100))
	texted = np.array(black)
	return texted

def creditScreen():
	pause()
	for screen in [getCreditScreen0, getCreditScreen1, getCreditScreen2]:
		for z in range(60):
			writer.write(screen(int(255 * z / 30)))
		for z in range(150):
			writer.write(screen(255))
		for z in range(60):
			writer.write(screen(int(255 * (1 - (z / 30)))))
		pause()


def overlayBlack(image, blackStength):
	return cv2.addWeighted(image, 1 - blackStength, BLACK_RECT, blackStength, 0)

def considerFade(image, inFlag, outFlag, index, totalFrames):
	if index < FADE_LENGTH and inFlag: #Fade in
		return overlayBlack(image, FADE(index)[0])
	if index >= totalFrames - FADE_LENGTH and outFlag:  # Fade out
		return overlayBlack(image, FADE(totalFrames - index)[0])
	return image

def getNumberString(num):
	if num >= 10000:
		return str(num)
	return "{:04d}".format(num)


def folderFrames(folder, fadeIn, fadeOut):
	frameNum = len(os.listdir(folder))
	print(folder + ": " + str(frameNum))

	for i in range(frameNum):
		if i % (frameNum // 20) == 0:
			print("Image " + str(i) + " out of " + str(frameNum))
		address = folder + "/frame." + getNumberString(i) + ".png"
		img = cv2.imread(address)
		writer.write(considerFade(img, fadeIn, fadeOut, i, frameNum))



writer = cv2.VideoWriter(MOVIE_NAME, cv2.VideoWriter_fourcc(*'DIVX'), 60, (1920, 1080))
#############################################
'''titleScreen()
pause()
folderFrames(folder='scene0Frames', fadeIn=True, fadeOut=False)
folderFrames(folder='scene1FramesRaw', fadeIn=False, fadeOut=True)
folderFrames(folder='scene2FramesRaw', fadeIn=True, fadeOut=True)
pause()
folderFrames(folder='scene3FramesRaw', fadeIn=True, fadeOut=True)
pause()
folderFrames(folder='scene4FramesRaw', fadeIn=True, fadeOut=True)
pause()
folderFrames(folder='scene5FramesRaw', fadeIn=True, fadeOut=True)
pause()
folderFrames(folder='scene6FramesRaw', fadeIn=True, fadeOut=True)
pause()
folderFrames(folder='scene7Frames', fadeIn=True, fadeOut=True)
pause()'''
creditScreen()
############################################
writer.release()
#showImage(getCreditScreen0(255))
#showImage(getCreditScreen1(255))
#showImage(getCreditScreen2(255))