import cv2

FPS = 60
MAX_FRAME_NUM = 3072
MOVIE_NAME = 'scene2v1'

#In seconds
def getImage(img):
	height, width, layers = img.shape
	return img, (width, height)


address = "outFrames/frames.0000.png"
img, size = getImage(cv2.imread(address))

video_name = MOVIE_NAME +".mp4"
writer = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'DIVX'), FPS, size)
writer.write(img)

frame_list = []
for x in range(1, MAX_FRAME_NUM + 1):
	frame_list.append("{:04d}".format(x))

for x in range(len(frame_list)):
	if x % ((len(frame_list)) // 10) == 0 and x != 0:
		print("Image " + frame_list[x] + " out of " + str(len(frame_list)))
	address = "outFrames/frames." + frame_list[x] + ".png"
	im = cv2.imread(address)
	try:
		img, size = getImage(im)
	except AttributeError:
		break
	writer.write(img)

writer.release()

