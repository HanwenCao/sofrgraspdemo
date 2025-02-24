#! /usr/bin/python3.8

#from skimage.measure import structural_similarity as ssim
from skimage.metrics import structural_similarity as ssim
#https://scikit-image.org/docs/stable/api/skimage.metrics.html#skimage.metrics.structural_similarity

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import time
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages') # in order to import cv2 under python3
import cv2
sys.path.append('/opt/ros/kinetic/lib/python2.7/dist-packages')

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def compare_images(imageA, imageB, title):
	# compute the mean squared error and structural similarity
	# index for the images
	t0 = time.time()
	m = mse(imageA, imageB)
	s = ssim(imageA, imageB) #SSIM value can vary between -1 and 1, where 1 indicates perfect similarity.
	print('Done. (%.3fs)' % (time.time() - t0))
	# setup the figure
	fig = plt.figure(title)
	plt.suptitle("MSE: %.2f, SSIM: %.2f" % (m, s))
	# show first image
	ax = fig.add_subplot(1, 2, 1)
	plt.imshow(imageA, cmap = plt.cm.gray)
	plt.axis("off")
	# show the second image
	ax = fig.add_subplot(1, 2, 2)
	plt.imshow(imageB, cmap = plt.cm.gray)
	plt.axis("off")
	# show the images
	plt.show()
	fig.savefig('diff.jpg')


# load the images -- the original, the original + contrast,
# and the original + photoshop
original = cv2.imread("./images2/0.jpg")
contrast = cv2.imread("./images2/1.jpg")
shopped = cv2.imread("./images2/00.jpg")
# convert the images to grayscale
original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
contrast = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
shopped = cv2.cvtColor(shopped, cv2.COLOR_BGR2GRAY)

# initialize the figure
fig = plt.figure("Images")
images = ("Original", original), ("Contrast", contrast), ("Photoshopped", shopped)
# loop over the images
for (i, (name, image)) in enumerate(images):
	# show the image
	ax = fig.add_subplot(1, 3, i + 1)
	ax.set_title(name)
	plt.imshow(image, cmap = plt.cm.gray)
	plt.axis("off")
# show the figure
plt.show()
fig.savefig('all.jpg')
# compare the images
#compare_images(original, original, "Original vs. Original")
compare_images(original, contrast, "Original vs. Contrast")
#compare_images(original, shopped, "Original vs. Photoshopped")


