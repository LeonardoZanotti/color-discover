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
        standard255 = 50
        standard180 = 10

        pixel1 = 180 if pixel[0] + standard180 > 180 else pixel[0] + standard180
        pixel2 = 255 if pixel[1] + standard255 > 255 else pixel[1] + standard255
        pixel3 = 255 if pixel[2] + standard255 > 255 else pixel[2] + standard255
        pixel4 = 0 if pixel[0] - standard180 < 0 else pixel[0] - standard180
        pixel5 = 0 if pixel[1] - standard255 < 0 else pixel[1] - standard255
        pixel6 = 0 if pixel[2] - standard255 < 0 else pixel[2] - standard255
        upper = np.array([pixel1, pixel2, pixel3])
        lower = np.array([pixel4, pixel5, pixel6])
        print(lower, pixel, upper)

        image_mask = cv2.inRange(image_hsl, lower, upper)
        cv2.imshow("mask", image_mask)

# mouse callback function for bgr
def pick_color_bgr(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = image[y, x]
        standard255 = 40

        # you might want to adjust the ranges(+-10, etc):
        pixel1 = 255 if pixel[0] + standard255 > 255 else pixel[0] + standard255
        pixel2 = 255 if pixel[1] + standard255 > 255 else pixel[1] + standard255
        pixel3 = 255 if pixel[2] + standard255 > 255 else pixel[2] + standard255
        pixel4 = 0 if pixel[0] - standard255 < 0 else pixel[0] - standard255
        pixel5 = 0 if pixel[1] - standard255 < 0 else pixel[1] - standard255
        pixel6 = 0 if pixel[2] - standard255 < 0 else pixel[2] - standard255
        upper = np.array([pixel1, pixel2, pixel3])
        lower = np.array([pixel4, pixel5, pixel6])
        print(lower, pixel, upper)

        image_mask = cv2.inRange(image, lower, upper)
        cv2.imshow("mask", image_mask)

def main():
    global image, pixel # so we can use it in mouse callback

    image = cv2.imread(sys.argv[1])  # pick.py my.png
    if image is None:
        print ("Use python3.7 color-pycker.py path/to/image <color style>")
        return

    if (image.shape[1] > 1000 or image.shape[0] > 1000):
        image = cv2.resize(image, (0,0), fx=0.5, fy=0.5)

    cv2.imshow("bgr", image)
    ## set mouse click for bgr
    cv2.namedWindow('bgr')

    if (len(sys.argv) > 2):
        color_style = sys.argv[2]

    if ('color_style' in locals() and color_style == 'hsl'):
        print('HLS MASK')
        cv2.setMouseCallback('bgr', pick_color_hsl)
    elif ('color_style' in locals() and color_style == 'bgr'):
        print('BGR MASK')
        cv2.setMouseCallback('bgr', pick_color_bgr)
    else:
        print ("Use python3.7 color-pycker.py path/to/image <color style>")
        return
    cv2.waitKey(50000)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()