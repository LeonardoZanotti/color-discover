# import the necessary packages
import numpy as np
import argparse
import cv2
from matplotlib import pyplot as plt

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())

# load the image
image = cv2.imread(args["image"], cv2.IMREAD_COLOR)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# define the list of boundaries
boundaries = [
	([17, 15, 100], [50, 56, 200], 'Red'),
	([86, 31, 4], [220, 88, 50], 'Blue'),
	([25, 146, 190], [62, 174, 250], 'Yellow'),
	([103, 86, 65], [145, 133, 128], 'Gray')
]

imagesToShow = []

# loop over the boundaries
for (lower, upper, title) in boundaries:
	# create NumPy arrays from the boundaries
	lower = np.array(lower, dtype = "uint8")
	upper = np.array(upper, dtype = "uint8")
	# find the colors within the specified boundaries and apply
	# the mask
	mask = cv2.inRange(image, lower, upper)
	output = cv2.bitwise_and(image, image, mask = mask)
	output_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)

	## calculate the percentage
	summed = np.sum(output, axis=2)
	totalPixels = output.size
	nonBlack = np.count_nonzero(summed)
	percent = str(round(nonBlack * 100 / totalPixels, 2))

	## append to array to show in the end
	imagesToShow.append([output_rgb, percent, title])

# show the images
for (output, percent, title) in imagesToShow:
	plt.subplot(121),plt.imshow(image_rgb),plt.title('Original')
	plt.xticks([]), plt.yticks([])
	plt.subplot(122),plt.imshow(output),plt.title(title + ' (' + percent + '%)')
	plt.xticks([]), plt.yticks([])
	plt.show()