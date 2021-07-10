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
		print('Use python3.7 color-discover-rgb.py --image path/to/image')
		return
	image_gau = cv2.GaussianBlur(image, (5, 5), 0)
	image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# define the list of boundaries
	boundaries = [
		## BGR												# Average
		([  0, 215, 215], [ 40, 255, 255], 'Yellow'),		# [  0, 255, 255] 
		([  5, 185, 167], [ 85, 255, 247], 'Light green'),	# [ 45, 225, 207]
		([ 13, 122,  66], [ 93, 202, 146], 'Green'),		# [ 53, 162, 106]
		([104, 114,   0], [184, 194,  40], 'Cyan'),			# [144, 154,   0]
		([214,   0,   0], [255,  40,  40], 'Blue'),			# [254,   0,   0]
		([124,   0,  29], [204,  41, 109], 'Dark blue'),	# [164,   1,  69]
		([137,   0,  99], [217,  40, 179], 'Purple'),		# [177,   0, 139]
		([ 37,   0, 130], [117,  58, 210], 'Magenta'),		# [ 77,  18, 170]
		([  0,   0, 214], [ 40,  40, 255], 'Red'),			# [  0,   0, 254] 
		([  0,  30, 210], [ 47, 110, 255], 'Light red'),	# [  7,  70, 250]
		([  0,  98, 210], [ 40, 178, 255], 'Orange'),		# [  0, 138, 250]
		([  0, 137, 208], [ 41, 217, 255], 'Burnt yellow'),	# [  1, 177, 248]
		([215, 215, 215], [255, 255, 255], 'White'), 		# [255, 255, 255] 
		([103,  86,  65], [145, 133, 128], 'Gray')			# [121, 110,  96]
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
		output_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)

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