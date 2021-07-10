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
if image is None:
	print('Use python3.7 color-discover-hsl.py --image path/to/image')
image_hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
image_gau = cv2.GaussianBlur(image_hls, (5, 5), 0)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# define the list of boundaries
boundaries = [
	## HLS												# Average
	([25, 118, 245], [35, 138, 255], 'Yellow'), 		# [30, 128, 255]
	([28, 125, 181], [38, 145, 201], 'Light green'), 	# [33, 135, 191]
	([40, 98, 119], [50, 118, 139], 'Green'), 			# [45, 108, 129] 
	([83, 67, 245], [93, 87, 255], 'Cyan'), 			# [88, 77, 255]
	([115, 117, 245], [125, 137, 255], 'Blue'), 		# [120, 127, 255]
	([128, 72, 242], [138, 92, 255], 'Darl blue'), 		# [133, 82, 252]
	([139, 78, 245], [149, 98, 255], 'Purple'), 		# [144, 88, 255]
	([163, 84, 196], [173, 104, 216], 'Magenta'), 		# [168, 94, 206]
	([0, 117, 245], [5, 137, 255], 'Red'), 				# [0, 127, 255]
	([3, 119, 235], [13, 139, 255], 'Light red'), 		# [8, 129, 245] 
	([12, 115, 245], [22, 135, 255], 'Orange'), 		# [17, 125, 255]
	([16, 115, 243], [26, 135, 255], 'Burnt yellow'),	# [21, 125, 253]
	([0, 245, 0], [5, 255, 10], 'White'), 				# [0, 255,   0]
	([100, 100, 33], [110, 120, 53], 'Gray')			# [105, 110,  43]
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