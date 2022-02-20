# generates positions for circles and dots for the inflatable given some input parameters
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d


def points_in_circle_np(radius, x0=0, y0=0, ):
	# finds integer points on a given circle
	x_ = np.arange(x0 - radius - 1, x0 + radius + 1, dtype=int)
	y_ = np.arange(y0 - radius - 1, y0 + radius + 1, dtype=int)
	x, y = np.where((x_[:,np.newaxis] - x0)**2 + (y_ - y0)**2 <= radius**2)
	for x, y in zip(x_[x], y_[y]):
		yield x, y

numcircles = 1
numdots = 3
x = 30 # x dimension of inflatable [cm]
y = 30 # y dimension of inflatable [cm]


# parameters that should be machine-generated later, but for now, will be set
rad = 3 # circle radius
circ = (10, 10) # circle coordinates
dot1 = [5, 2]
dot2 = [20, 18]
dot3 = [15, 26]

circ_pts = list(points_in_circle_np(rad, x0=circ[0], y0 = circ[1]))

# plot inflatable
plt.axis([0, 30, 0, 30])
plt.gca().set_aspect('equal', adjustable='box')

c = plt.Circle(circ, radius = rad)
plt.gca().add_artist(c)

plt.plot(dot1[0], dot1[1], 'ro')
plt.plot(dot2[0], dot2[1], 'ro')
plt.plot(dot3[0], dot3[1], 'ro')

plt.plot(circ_pts)


# plots voronoi diagram
points = np.array([dot1, dot2, dot3]) # TODO: incorporate circle into diagram
points = np.concatenate((points, np.array(circ_pts))
vor = Voronoi(points)
fig = voronoi_plot_2d(vor)
plt.show()

# function for rejection sampling


# perform rejection sampling


# 
