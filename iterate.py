import numpy as np

# Generates inflatables by iteration through some rules

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
