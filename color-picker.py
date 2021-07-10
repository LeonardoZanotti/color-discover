import cv2
import numpy as np
import sys

image = None   # global ;(
pixel = (20,60,80) # some stupid default

# mouse callback function for hsl
def pick_color_hsl(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        image_hsl = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
        pixel = image_hsl[y, x]

        # you might want to adjust the ranges(+-10, etc):
        pixel1 = 180 if pixel[0] + 5 > 180 else pixel[0] + 5
        pixel2 = 255 if pixel[1] + 10 > 255 else pixel[1] + 10
        pixel3 = 255 if pixel[2] + 10 > 255 else pixel[2] + 10
        pixel4 = 0 if pixel[0] - 5 < 0 else pixel[0] - 5
        pixel5 = 0 if pixel[1] - 10 < 0 else pixel[1] - 10
        pixel6 = 0 if pixel[2] - 10 < 0 else pixel[2] - 10
        upper = '[' + str(pixel1) + ', ' + str(pixel2) + ', ' + str(pixel3) + ']'
        lower = '[' + str(pixel4) + ', ' + str(pixel5) + ', ' + str(pixel6) + ']'
        print(lower, pixel, upper)

        upperNp =  np.array([pixel1, pixel2, pixel3])
        lowerNp =  np.array([pixel4, pixel5, pixel6])

        image_mask = cv2.inRange(image_hsl, lowerNp, upperNp)
        cv2.imshow("mask", image_mask)

# mouse callback function for bgr
def pick_color_bgr(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = image[y, x]

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

        upperNp =  np.array([pixel1, pixel2, pixel3])
        lowerNp =  np.array([pixel4, pixel5, pixel6])

        image_mask = cv2.inRange(image, lowerNp, upperNp)
        cv2.imshow("mask", image_mask)

def main():
    global image, pixel # so we can use it in mouse callback

    image = cv2.imread(sys.argv[1])  # pick.py my.png
    if image is None:
        print ("Use python3.7 color-pycker.py path/to/image")
        return

    if (image.shape[1] > 1000 or image.shape[0] > 1000):
        image = cv2.resize(image, (0,0), fx=0.5, fy=0.5)

    cv2.imshow("bgr", image)
    ## set mouse click for bgr
    cv2.namedWindow('bgr')

    if (len(sys.argv) > 2):
        color_style = sys.argv[2]

    if ('color_style' in locals() and color_style == 'hsl'):
        cv2.setMouseCallback('bgr', pick_color_hsl)
    else:
        cv2.setMouseCallback('bgr', pick_color_bgr)

    cv2.waitKey(50000)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()