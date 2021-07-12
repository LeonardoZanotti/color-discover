# import the necessary packages
import numpy as np
import argparse
import cv2
from matplotlib import pyplot as plt

def main():
	# construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", help = "path to the image")
	args = vars(ap.parse_args())

	# load the image
	image = cv2.imread(args["image"], cv2.IMREAD_COLOR)
	if image is None:
		print('Use python3.7 color-discover-hsl.py --image path/to/image')
		return
	image_hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
	image_blur = cv2.medianBlur(image_hls, 15)
	image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# define the list of boundaries
	boundaries = [
		## HLS												# Average
		([ 20,  78, 205], [ 40, 178, 255], 'Yellow'),      	# [ 30 128 255]
		([ 23,  85, 141], [ 43, 185, 241], 'Light green'), 	# [ 33 135 191]
		([ 35,  58,  79], [ 55, 158, 179], 'Green'),       	# [ 45 108 129]
		([ 78,  27, 205], [ 98, 127, 255], 'Cyan'),        	# [ 88  77 255]
		([110,  77, 205], [130, 177, 255], 'Blue'),        	# [120 127 255]
		([123,  32, 202], [143, 132, 255], 'Dark blue'),   	# [133  82 252]
		([134,  38, 205], [154, 138, 255], 'Purple'),      	# [144  88 255]
		([158,  44, 156], [178, 144, 255], 'Magenta'),     	# [168  94 206]
		([  0,  77, 205], [ 10, 177, 255], 'Red'),         	# [  0 127 255]
		([  0,  79, 195], [ 18, 179, 255], 'Light red'),   	# [  8 129 245]
		([  7,  75, 205], [ 27, 175, 255], 'Orange'),      	# [ 17 125 255]
		([ 11,  75, 203], [ 31, 175, 255], 'Burnt yellow'),	# [ 21 125 253]
		([  0, 150,   0], [180, 255, 255], 'White'),       	# [  0 253   0]
		([ 95,  58,   0], [115, 158,  89], 'Gray'),        	# [105 108  39]
	] 
	
	imagesToShow = []

	# loop over the boundaries
	for (lower, upper, title) in boundaries:
		# create NumPy arrays from the boundaries
		lower = np.array(lower, dtype = "uint8")
		upper = np.array(upper, dtype = "uint8")
		# find the colors within the specified boundaries and apply
		# the mask
		mask = cv2.inRange(image_blur, lower, upper)
		output = cv2.bitwise_and(image_blur, image_blur, mask = mask)
		output_rgb = cv2.cvtColor(output, cv2.COLOR_HLS2RGB)

		## calculate the percentage
		totalPixels = output.size/3
		nonBlack = cv2.countNonZero(cv2.cvtColor(output, cv2.COLOR_BGR2GRAY))
		percent = round(nonBlack * 100 / totalPixels, 2)

		## append to array to show in the end
		imagesToShow.append([output_rgb, percent, title])

	# show the images
	for (output, percent, title) in imagesToShow:
		if (percent > 0.5):
			plt.subplot(121),plt.imshow(image_rgb),plt.title('Original')
			plt.xticks([]), plt.yticks([])
			plt.subplot(122),plt.imshow(output),plt.title(title + ' (' + str(percent) + '%)')
			plt.xticks([]), plt.yticks([])
			plt.show()

if __name__ == '__main__':
	main()