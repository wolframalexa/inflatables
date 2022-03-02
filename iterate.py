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
	interlim = 1.5 # distance from element to element [in]

	if points is None:
		pass
	else:
		for point in points:
		# element is not too close to edge
			# print(point)
			if (point[0] > 12 - edgelim) or (point[0] < edgelim) or (point[1] > 12 - edgelim) or (point[1] < edgelim):
				out = False
#				print("Too close to edge")
				break

			# element is not too close to other elements
			surround = [point[0], point[1], interlim]
			counter = 0 # use counter rather than t/f bc the point should be within its own circle (when point = point2)

			for point2 in points:
				if incircle(point2, surround):
					counter += 1

				if counter > 1:
					out = False
#					print("Too close to others")
					break

			for circle in circles:
				if incircle(point, circle):
					out = False
#					print("Point in circle")
					break

	for circle in circles:
		# element is not too close to edge
		x = circle[0]
		y = circle[1]
		rad = circle[2]
		extremes = np.array([[x + rad, y], [x - rad, y], [y + rad, x], [y - rad, x]])

		for i in extremes:
			if (i[0] > 12 - edgelim) or (i[0] < edgelim):
#				print("Circle too close to edge")
				out = False
				break

		# element is not too close to other elements
		surround = [x, y, rad + interlim]
		counter = 0 # use counter rather than t/f bc the point should be within its own circle (when point = point2)

		for point2 in points:
			if incircle(point2, surround):
				counter += 1
			if counter > 1:
#				print("circle too close to others")
				out = False
				break

		counter = 0 # use counter rather than t/f bc circle should intersect itself
		for circle2 in circles: # check that circles do not intersect
			dist = ((circle[0]-circle2[0])**2 + (circle[1]-circle2[1])**2)**0.5
			if dist <= circle[2] + circle2[2] + interlim:
				counter += 1
			if counter > 1:
#				print(circle, circle2)
#				print("Circles intersect")
				out = False
				break

	return(out)

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
	center1 = [np.random.uniform(1, 11), np.random.uniform(1, 11)]
	center2 = [np.random.uniform(1, 11), np.random.uniform(1, 11)]
	center3 = [np.random.uniform(1, 11), np.random.uniform(1, 11)]
	return multivariate_normal.pdf(pos, center1, [[1, 0], [0, 1]]) + multivariate_normal.pdf(pos, center2, [[1, 0], [0, 1]]) + multivariate_normal.pdf(pos, center3, [[1, 0], [0, 1]])

# Large gaussian encompassing the entire mixture
def getqx(pos):
	return multivariate_normal([6, 6], [[12, 0], [0, 12]]).pdf(pos)


iterations = 1000
numcircles = 3
numdots = 12

circles = np.zeros((numcircles, 3))
dots = np.zeros((numdots, 2))

pro_circles = np.zeros((numcircles, 3)) # proposed circles and dots
pro_dots = np.zeros((numdots, 2))

count = 0
tracker = 1
# place circles first
while (count < numcircles) and (tracker < iterations): # time out if over some max # of iterations
	# generate circle
	rad = np.random.uniform(1,2) # random circle radius
	x = np.random.uniform(3,9)
	y = np.random.uniform(3,9)

	curr = np.array([x, y, rad])
	pro_circles = circles
	pro_circles[count, :] = curr


	itergraph(pro_circles, pro_dots)
	plt.savefig('image/img' + str(tracker) + '.png')
	tracker += 1

	# meets configuration? if yes - then accept
	if followsRules(pro_circles[:count+1, :], []):
			circles[count, :] = curr
			count += 1

# generate dots
count = 0
x, y = np.mgrid[0:12:.01, 0:12:.01]
pos = np.dstack((x, y))

while (count < numdots) and (tracker < iterations):
	k = np.amax(np.divide(getpx(pos), getqx(pos)))
	samples = np.zeros([1, 2])

	test = np.zeros([1,2])
	test = np.random.multivariate_normal([6, 6], [[12, 0], [0, 12]])
	u = np.random.uniform(0, (k*getqx(test)))
	pro_dots = dots

	if u <= getpx(test):
		pro_dots[count, :] = test

		itergraph(circles, pro_dots)
		plt.savefig('image/img' + str(tracker) + '.png')
		tracker += 1

		# check if follows rules
		if followsRules(circles, pro_dots[:count+1, :]):
			dots[count, :] = test
			count += 1
		# else, pro_dots[count,:] is replaced at the following loop so no need to handle

print("Dots:", dots)
print("Circles:", circles)
