import cv2
import sys
import math
sys.path.append("..")
from Interpolator import getInterpolator

IN_STARS = "stars.png"
IN_MOVIE = "Scene0.mp4"

BLACK = [50, 20, 5] #Threshold of black
LAST_EASY_FRAME = 893
DIAGONAL = getInterpolator(start_x=0, end_x=1, power=1, y_lists=[[0, 960], [0, 540]]) #Absolute x and absolute y
ATTRIBUTION_FADE = getInterpolator(start_x=1020, end_x=1080, power=1, y_lists=[[1, 0]])

def isBlack(norm, image):
	x, y = diagonalMap(norm)
	return image.item(y, x, 2) <= BLACK[0] and image.item(y, x, 1) <= BLACK[1] and image.item(y, x, 0) <= BLACK[2]

def isWhite(x, y, image):
	return image.item(y, x, 2) >= 140 and image.item(y, x, 1) >= 140 and image.item(y, x, 0) >= 140

def diagonalMap(norm):
	return int(DIAGONAL(norm)[0]), int(DIAGONAL(norm)[1])

def findBorder(image):
	norm = 0
	while isBlack(norm, image):
		norm += 0.08
	return binarySearchForBorder(norm - 0.08, norm, image)

def binarySearchForBorder(start, end, image):
	mid = (start + end) / 2
	if abs(start - end) <= 0.001 or end < start:
		return mid
	if isBlack(mid, image):
		return binarySearchForBorder(mid, end, image)
	return binarySearchForBorder(start, mid, image)

def copyImage(image, excludedRadius, index):
	for x in range(1920):
		for y in range(1080):
			if x > 1625 and y > 980 and isWhite(x, y, image):
				fade = ATTRIBUTION_FADE(index)[0]
				image.itemset((y, x, 0), fade * image.item(y, x, 0))
				image.itemset((y, x, 1), fade * image.item(y, x, 1))
				image.itemset((y, x, 2), fade * image.item(y, x, 2))
				continue
			if math.sqrt((x - 960)**2 + (y - 540)**2) < excludedRadius:
				continue
			image.itemset((y, x, 0), stars.item(y, x, 0))
			image.itemset((y, x, 1), stars.item(y, x, 1))
			image.itemset((y, x, 2), stars.item(y, x, 2))


def process(image, index):
	if index <= LAST_EASY_FRAME: #No sky shown
		return image
	borderX, borderY = diagonalMap(findBorder(image))
	copyImage(image, math.sqrt((borderX - 960)**2 + (borderY - 540)**2), index)
	return image


def cropAndResizeImage(image):
	cropped = image[153:1469, 270:2610]
	return cv2.resize(cropped, (1920, 1080), interpolation=cv2.INTER_CUBIC)


def writeImage(frame, index):
	image = process(frame, index)
	address = "../scene0Frames/frame." + "{:04d}".format(index) + ".png"
	cv2.imwrite(address, image)  # save frame as JPEG file


stars = cv2.imread(IN_STARS)
cap = cv2.VideoCapture(IN_MOVIE)
frameNumber = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


for i in range(frameNumber):
	if i % (frameNumber // 40) == 0:
		print("Image " + str(i) + " out of " + str(frameNumber))
	img = cropAndResizeImage(cap.read()[1])
	writeImage(img, i)