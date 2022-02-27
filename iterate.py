import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.stats import multivariate_normal
from scipy.stats import uniform

def followsRules(circles, points):
	out = True
	# format of circles: [[x, y, rad], ]
	# format of points: [[x, y], ]

	edgelim = 1 # distance to edge [in]
	interlim = 1 # distance from element to element [in]

	if points is None:
		pass
	else:
		for point in points:
		# element is not too close to edge
			print(point)
			if (point[0] > 12 - edgelim) or (point[0] < edgelim) or (point[1] > 12 - edgelim) or (point[1] < edgelim):
				out = False
				print("Too close to edge")
				break

			# element is not too close to other elements
			surround = [point[0], point[1], interlim]
			counter = 0 # use counter rather than t/f bc the point should be within its own circle (when point = point2)

			for point2 in points:
				if incircle(point2, surround):
					counter += 1

				if counter > 1:
					out = False
					print("Too close to others")
					break

	for circle in circles:
		# element is not too close to edge
		x = circle[0]
		y = circle[1]
		rad = circle[2]
		extremes = np.array([[x + rad, y], [x - rad, y], [y + rad, x], [y - rad, x]])

		for i in extremes:
			if (i[0] > 12 - edgelim) or (i[0] < edgelim):
				print("Circle too close to edge")
				out = False
				break

		# element is not too close to other elements
		surround = [x, y, rad + interlim]
		counter = 0 # use counter rather than t/f bc the point should be within its own circle (when point = point2)
		for point2 in points:
			if incircle(point2, surround):
				counter += 1
			if counter > 1:
				print("circle too close to others")
				out = False
				break
	return(out)

#TODO: does not currently check circle-to-circle
#TODO: circle radius currently not being checked


def itergraph(circles, points):
	# graphs circles and points as they currently are
	# initialize plot
	fig = plt.figure()
	plt.axis([0, 12, 0, 12])
	plt.gca().set_aspect('equal', adjustable='box')

	# plot circles
	for circle in circles:
		c = plt.Circle((circle[0], circle[1]), circle[2], fill=False)
		fig.gca().add_artist(c)

	#print("Points:", points)
	plt.scatter(points[:,0], points[:,1], s=20, color='black')

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
    return multivariate_normal.pdf(pos, [3, 2], [[1, 0], [0, 1]]) + multivariate_normal.pdf(pos, [9, 9], [[1, 0], [0, 1]]) + multivariate_normal.pdf(pos, [9, 1], [[1, 0], [0, 1]]) + multivariate_normal.pdf(pos, [1, 9], [[1, 0], [0, 1]]) + multivariate_normal.pdf(pos, [5, 5], [[1, 0], [0, 1]])

# Large gaussian encompassing the entire mixture
def getqx(pos):
    return multivariate_normal([6, 6], [[12, 0], [0, 12]]).pdf(pos)


iterations = 20
numcircles = 1
numdots = 7

circles = np.zeros((numcircles, 3))
dots = np.zeros((numdots, 2))

pro_circles = np.zeros((numcircles, 3)) # proposed circles and dots
# print("Proposed circles initialized:", pro_circles)
pro_dots = np.zeros((numdots, 2))
# print("Proposed Dots Initialized:", pro_dots)

i = 1
count = 0
tracker = 1
# place circles first
while (count < numcircles): # time out if over some max # of iterations
	i += 1
#	print("Number of nonzero:", np.count_nonzero(circles))

	# generate circle
	rad = np.random.uniform(1,2) # random circle radius
	x = np.random.uniform(1,11)
	y = np.random.uniform(1,11)

	curr = np.array([x, y, rad])
#	print("Current:", curr)
#	print("Proposed circles:", pro_circles)
	print(count)
#	print("Proposed circles:", pro_circles)
	pro_circles[count, :] = curr


	itergraph(pro_circles, pro_dots)
	plt.savefig('images/img' + str(tracker) + '.png')
	tracker += 1

	# meets configuration? if yes - then accept
	if followsRules(pro_circles, []):
		circles[count, :] = curr
		count += 1
		print("Circles:", circles)



# generate dots
count = 0
x, y = np.mgrid[0:12:.01, 0:12:.01]
pos = np.dstack((x, y))

while (count < numdots):
#	print("Nonzero dots:", np.count_nonzero(dots))
	i += 1

	k = np.amax(np.divide(getpx(pos), getqx(pos)))
	samples = np.zeros([1, 2])

	test = np.zeros([1,2])
	test = np.random.multivariate_normal([6, 6], [[12, 0], [0, 12]])
	u = np.random.uniform(0, (k*getqx(test)))
	pro_dots = dots

	if u <= getpx(test):
		pro_dots[count, :] = test
		print("Proposed dots:", pro_dots)

		itergraph(circles, pro_dots)
		plt.savefig('images/img' + str(tracker) + '.png')
		tracker += 1

		# check if follows rules
		if followsRules(circles, pro_dots[:count+1, :]):
			dots[count, :] = test
			count += 1
			print("Dots:", dots)
		# else, pro_dots[count,:] is replaced at the following loop so no need to handle
