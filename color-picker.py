import cv2
import numpy as np
import sys

image_bgr = None   # global ;(
pixel = (20,60,80) # some stupid default

# mouse callback function
def pick_color(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = image_bgr[y, x]

        # you might want to adjust the ranges(+-10, etc):
        pixel1 = 255 if pixel[0] + 40 > 255 else pixel[0] + 40
        pixel2 = 255 if pixel[1] + 40 > 255 else pixel[1] + 40
        pixel3 = 255 if pixel[2] + 40 > 255 else pixel[2] + 40
        pixel4 = 0 if pixel[0] - 40 < 0 else pixel[0] - 40
        pixel5 = 0 if pixel[1] - 40 < 0 else pixel[1] - 40
        pixel6 = 0 if pixel[2] - 40 < 0 else pixel[2] - 40
        upper = '[' + str(pixel1) + ', ' + str(pixel2) + ', ' + str(pixel3) + ']'
        lower = '[' + str(pixel4) + ', ' + str(pixel5) + ', ' + str(pixel6) + ']'
        print(lower, pixel, upper)

        upperNp =  np.array([pixel[0] + 10, pixel[1] + 10, pixel[2] + 40])
        lowerNp =  np.array([pixel[0] - 10, pixel[1] - 10, pixel[2] - 40])

        image_mask = cv2.inRange(image_bgr, lowerNp, upperNp)
        cv2.imshow("mask", image_mask)

def main():
    global image_bgr, pixel # so we can use it in mouse callback

    image_bgr = cv2.imread(sys.argv[1])  # pick.py my.png
    if image_bgr is None:
        print ("Use python3.7 color-pycker.py path/to/image")
        return
    cv2.imshow("bgr", image_bgr)

    ## set mouse click
    cv2.namedWindow('bgr')
    cv2.setMouseCallback('bgr', pick_color)

    cv2.waitKey(50000)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()