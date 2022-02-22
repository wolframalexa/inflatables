# generates positions for circles and dots for the inflatable given some input parameters
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np
import math

def circle_to_hexagon(r, x, y):
	a = 0.5*r
	b = math.sqrt(3)/2 * r
	pts = [[x - r, y],
		[x - a, y + b],
		[x + a, y + b],
		[x + r, y],
		[x + a, y - b],
		[x - a, y - b]]
	return(pts)

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

circ_pts = circle_to_hexagon(rad, circ[0], circ[1])
print(circ_pts)

# # plot inflatable
# plt.axis([0, 30, 0, 30])

# c = plt.Circle(circ, radius = rad)
# plt.gca().add_artist(c)

# plt.plot(dot1[0], dot1[1], 'ro')
# plt.plot(dot2[0], dot2[1], 'ro')
# plt.plot(dot3[0], dot3[1], 'ro')

# plt.plot(circ_pts)


# plots voronoi diagram
points = np.array([dot1, dot2, dot3]) # TODO: incorporate circle into diagram
points = np.concatenate((points, np.array(circ_pts)))
vor = Voronoi(points)
fig = voronoi_plot_2d(vor)
plt.axis([0, 30, 0, 30])
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
