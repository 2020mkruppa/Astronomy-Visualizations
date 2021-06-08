import cv2

#In seconds
def getImage(img):
    height, width, layers = img.shape
    return img, (width, height)


def blocks(seed_name, messages):
    address = "frames.0000.png"
    img, size = getImage(cv2.imread(address))

    video_name = seed_name + str(60) + " fps.mp4"
    writer = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'DIVX'), 60, size)
    writer.write(img)

    maxFrame = 551
    frame_list = []
    for x in range(1, maxFrame + 1):
        frame_list.append("{:04d}".format(x))

    for x in range(len(frame_list)):
        if x % ((len(frame_list)) // messages) == 0 and x != 0:
            print("Image " + frame_list[x] + " out of " + str(len(frame_list)))
        address = "frames." + frame_list[x] + ".png"
        im = cv2.imread(address)
        try:
            img, size = getImage(im)
        except AttributeError:
            break
        writer.write(img)

    print()
    writer.release()

blocks("testing", 5)