import cv2
import numpy as np
import CurveData as cd
import time

INPUT_IMAGE = "16x9Grid.png"

def warp(image):
	output = np.zeros((1080, 1920, 3), dtype=np.uint8)
	output[outputListY, outputListX] = image[inputListY, inputListX]
	return output


inputListX, inputListY, outputListX, outputListY = cd.getPointsMap(lookForPickle=False)
print("Received map")

inputImage = cv2.imread(INPUT_IMAGE)
start = time.time()
for i in range(1000):
	warp(inputImage)
end = time.time()
print(str(end - start))
cv2.imwrite("fast.png", warp(inputImage))
