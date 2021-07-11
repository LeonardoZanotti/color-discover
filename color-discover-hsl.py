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
	image_gau = cv2.medianBlur(image_hls, 15)
	image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# define the list of boundaries
	boundaries = [
		## HLS												# Average
		([ 25,  88, 215], [ 35, 168, 255], 'Yellow'),       # [ 30 128 255]
		([ 28,  95, 151], [ 38, 175, 231], 'Light green'),  # [ 33 135 191]
		([ 40,  68,  89], [ 50, 148, 169], 'Green'),        # [ 45 108 129]
		([ 83,  37, 215], [ 93, 117, 255], 'Cyan'),         # [ 88  77 255]
		([115,  87, 215], [125, 167, 255], 'Blue'),         # [120 127 255]
		([128,  42, 212], [138, 122, 255], 'Dark blue'),    # [133  82 252]
		([139,  48, 215], [149, 128, 255], 'Purple'),       # [144  88 255]
		([163,  54, 166], [173, 134, 246], 'Magenta'),      # [168  94 206]
		([  0,  87, 215], [  5, 167, 255], 'Red'),          # [  0 127 255]
		([  3,  89, 205], [ 13, 169, 255], 'Light red'),    # [  8 129 245]
		([ 12,  85, 215], [ 22, 165, 255], 'Orange'),       # [ 17 125 255]
		([ 16,  85, 213], [ 26, 165, 255], 'Burnt yellow'), # [ 21 125 253]
		([  0, 212,   0], [  5, 255,  40], 'White'),        # [  0 252   0]
		([ 99,  70,   0], [109, 150,  77], 'Gray'),         # [104 110  37]
	] 
	
	imagesToShow = []

	# loop over the boundaries
	for (lower, upper, title) in boundaries:
		# create NumPy arrays from the boundaries
		lower = np.array(lower, dtype = "uint8")
		upper = np.array(upper, dtype = "uint8")
		# find the colors within the specified boundaries and apply
		# the mask
		mask = cv2.inRange(image_gau, lower, upper)
		output = cv2.bitwise_and(image_gau, image_gau, mask = mask)
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