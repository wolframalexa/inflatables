# generates positions for circles and dots for the inflatable given some input parameters
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

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

# plot inflatable
plt.axis([0, 30, 0, 30])
plt.gca().set_aspect('equal', adjustable='box')

c = plt.Circle(circ, radius = rad)
plt.gca().add_artist(c)

plt.plot(dot1[0], dot1[1], 'ro')
plt.plot(dot2[0], dot2[1], 'ro')
plt.plot(dot3[0], dot3[1], 'ro')

# plots voronoi diagram
points = np.array([dot1, dot2, dot3, circ]) # TODO: incorporate circle into diagram
vor = Voronoi(points)
fig = voronoi_plot_2d(vor)
plt.show()

# function for rejection sampling


# perform rejection sampling


# 
