import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import math
from scipy.stats import multivariate_normal
from scipy.stats import uniform


def followsRules(circles, points):
	out = True
	# format of circles: [[x, y, rad], ]
	# format of points: [[x, y], ]

	edgelim = 1 # distance to edge [in]
	interlim = 2 # distance from element to element
	for point in points:

		# element is not too close to edge

		if (point[0] > 12 - edgelim) or (point[0] < edgelim) or (point[1] > 12 - edgelim) or (point[1] < edgelim):
			out = False
			break

		# element is not too close to other elements

		surround = [point[0], point[1], interlim]
		counter = 0 # use counter rather than t/f bc the point should be within its own circle (when point = point2)

		for point2 in points:
			if incircle(point2, surround):
				counter += 1

			if counter > 1:
				out = False
				break

	for circle in circles:
		# element is not too close to edge
		x = circle[0]
		y = circle[1]
		rad = circle[2]
		extremes = np.array([[x + rad, y], [x - rad, y], [y + rad, x], [y - rad, x]])

		for i in extremes:
			if (i[0] > 12 - edgelim) or (i[0] < edgelim):
				out = False
				break

		# element is not too close to other elements
		surround = [x, y, rad + interlim]
		counter = 0 # use counter rather than t/f bc the point should be within its own circle (when point = point2)
		for point2 in points:
			if incircle(point2, surround):
				counter += 1
			if counter > 1:
				out = False
				break
	return(out)

#TODO: does not currently check circle-to-circle
#TODO: circle radius currently not being checked

def dist(a, b):
	# a & b are points in numpy arrays
	return(np.sqrt(np.sum(np.square(a - b))))

def incircle(point, circle):
	x = circle[0]
	y = circle[1]
	rad = circle[2]

	if (point[0] > x - rad) and (point[0] < x + rad) and (point[1] > y - rad) and (point[1] < y + rad):
		return True
	else:
		return False

# Mixture distribution (aka u can make the means and covariance matrix anything that you want)
def getpx(pos):
    return multivariate_normal.pdf(pos, [5, 5], [[1, 0], [0, 1]]) + multivariate_normal.pdf(pos, [8, 8], [[1, 0], [0, 1]]) + multivariate_normal.pdf(pos, [2, 9], [[1, 0], [0, 1]])

# Large gaussian encompassing the entire mixture
def getqx(pos):
    return multivariate_normal([6, 6], [[12, 0], [0, 12]]).pdf(pos)


iterations = 10
numcircles = 1
numdots = 2

circles = np.zeros((numcircles, 3))
dots = np.zeros((numdots, 2))

pro_circles = np.zeros((numcircles, 3)) # proposed circles and dots
pro_dots = np.zeros((numdots, 2))

# TODO: logic currently doesn't allow for re-use of points - needs to be fixed (eg if a circle is accepted at step 1, it should remain accepted all the way to step 10)

for i in range(0, iterations):
	# generate circle
	rad = np.random.uniform(1,3) # random circle radius
	x = np.random.uniform(1,11)
	y = np.random.uniform(1,11)

	pro_circles[0] = [x, y, rad]

	# meets configuration? if yes - then accept
	if followsRules(pro_circles, []):
		circles = pro_circles

	# generate dots
	x, y = np.mgrid[0:12:.01, 0:12:.01]
	pos = np.dstack((x, y))

	k = np.amax(np.divide(getpx(pos), getqx(pos)))
	samples = np.zeros([numdots + numcircles, 2])
	i = 0

	while i < numdots:
	    test = np.zeros([1,2])
	    test = np.random.multivariate_normal([6, 6], [[12, 0], [0, 12]])
	    u = np.random.uniform(0, (k*getqx(test)))

	    if u <= getpx(test):
	        samples[i, :] = test
	        i+=1

	# check if follows rules
	if followsRules(pro_circles, samples):
		points = samples

	# plot the image as it is
	plt.axis([0, 12, 0, 12])

	for circle in circles:
		c = plt.Circle((circle[0], circle[1]), radius = circle[2])
		plt.gca().add_artist(c)
	plt.scatter(points[:,0], points[:,1])
	plt.show()

	path = "../plots/" + str(i) + ".jpg"
	plt.savefig(path)
