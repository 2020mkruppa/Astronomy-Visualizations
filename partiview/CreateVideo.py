import cv2
from Interpolator import getInterpolator

FPS = 60
MAX_FRAME_NUM = 4698
MOVIE_NAME = 'scene6v2'

ADD_YEAR_TEXT = False
FADE_START = 530
YEAR_START = 600
YEAR_END = 2700
FADE_END = 2770

YEAR_INTERP = getInterpolator(start_x=YEAR_START, end_x=YEAR_END, power=1, y_lists=[[1995, 2021]])
WHITE = 255
def getFadeMultiplier(frameNum):
	if frameNum <= YEAR_START:
		return getInterpolator(start_x=FADE_START, end_x=YEAR_START, power=1, y_lists=[[0, 1]])(frameNum)[0]
	return getInterpolator(start_x=YEAR_END, end_x=FADE_END, power=1, y_lists=[[1, 0]])(frameNum)[0]


def addText(image, frameNum):
	if FADE_START <= frameNum <= FADE_END:
		fade = getFadeMultiplier(frameNum)

		year = int(YEAR_INTERP(frameNum)[0])
		fadeWhite = fade * WHITE

		cv2.putText(image, str(year), (15, 870), cv2.FONT_HERSHEY_DUPLEX, 1.5, (fadeWhite, fadeWhite, fadeWhite), 2)
		cv2.rectangle(image, (25, 920), (40, 935), (0, 0, fadeWhite), -1)
		cv2.putText(image, "Doppler Spectroscopy", (55, 935), cv2.FONT_HERSHEY_DUPLEX, 1, (fadeWhite, fadeWhite, fadeWhite), 2)

		cv2.rectangle(image, (25, 970), (40, 985), (fadeWhite, fadeWhite, 0), -1)
		cv2.putText(image, "Transit", (55, 985), cv2.FONT_HERSHEY_DUPLEX, 1, (fadeWhite, fadeWhite, fadeWhite), 2)

		cv2.rectangle(image, (25, 1020), (40, 1035), (0, fadeWhite, fadeWhite), -1)
		cv2.putText(image, "Other", (55, 1035), cv2.FONT_HERSHEY_DUPLEX, 1, (fadeWhite, fadeWhite, fadeWhite), 2)

	return image

def getImage(img):
	height, width, layers = img.shape
	return img, (width, height)


def processFrame(frame):
	blurred = cv2.GaussianBlur(frame, [3, 3], 0)
	#fin = cv2.resize(blurred, [19, 10])
	return blurred



address = "outFrames/frames.0000.png"
img, size = getImage(cv2.imread(address))

video_name = MOVIE_NAME +".mp4"
writer = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'DIVX'), FPS, size)
writer.write(img)

frame_list = []
for x in range(1, MAX_FRAME_NUM + 1):
	frame_list.append("{:04d}".format(x))

for x in range(len(frame_list)):
	if x % ((len(frame_list)) // 20) == 0 and x != 0:
		print("Image " + frame_list[x] + " out of " + str(len(frame_list)))
	address = "outFrames/frames." + frame_list[x] + ".png"
	im = cv2.imread(address)
	try:
		img, size = getImage(im)
	except AttributeError:
		break

	if ADD_YEAR_TEXT:
		img = addText(img, x)
	writer.write(img)

writer.release()

