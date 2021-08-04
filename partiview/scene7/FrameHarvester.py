import cv2
import sys
sys.path.append("..")

IN_MOVIE = "Baltimore.mp4"

def cropAndResizeImage(image):
	cropped = image[153:1469, 270:2610]
	return cv2.resize(cropped, (1920, 1080), interpolation=cv2.INTER_CUBIC)


def writeImage(frame, index):
	address = "../scene7Frames/frame." + "{:04d}".format(index) + ".png"
	cv2.imwrite(address, frame)  # save frame as JPEG file


cap = cv2.VideoCapture(IN_MOVIE)
frameNumber = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

for i in range(frameNumber):
	if i % (frameNumber // 40) == 0:
		print("Image " + str(i) + " out of " + str(frameNumber))
	img = cropAndResizeImage(cap.read()[1])
	writeImage(img, i)