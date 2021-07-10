import cv2
import numpy as np
import sys

image_bgr = None   # global ;(
pixel = (20,60,80) # some stupid default

# mouse callback function
def pick_color(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = image_bgr[y, x]

        #you might want to adjust the ranges(+-10, etc):
        upper =  np.array([pixel[0] + 10, pixel[1] + 10, pixel[2] + 40])
        lower =  np.array([pixel[0] - 10, pixel[1] - 10, pixel[2] - 40])
        print(lower, pixel, upper)

        image_mask = cv2.inRange(image_bgr, lower, upper)
        cv2.imshow("mask", image_mask)

def main():
    global image_bgr, pixel # so we can use it in mouse callback

    image_src = cv2.imread(sys.argv[1])  # pick.py my.png
    if image_src is None:
        print ("Use python3.7 color-pycker.py path/to/image")
        return
    cv2.imshow("bgr", image_src)

    ## set mouse click
    cv2.namedWindow('bgr')
    cv2.setMouseCallback('bgr', pick_color)

    # now click into the hsv img , and look at values:
    image_bgr = cv2.cvtColor(image_src, cv2.COLOR_BGR2RGB)
    cv2.imshow("rgb", image_bgr)

    cv2.waitKey(50000)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()