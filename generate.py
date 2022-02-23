# generates positions for circles and dots for the inflatable given some input parameters
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np
import math
from scipy.stats import multivariate_normal
from scipy.stats import uniform

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

#Mixture distribution (aka u can make the means and covariance matrix anything that you want)
def getpx(pos):
    return multivariate_normal.pdf(pos, [5, 5], [[1, 0], [0, 1]]) + multivariate_normal.pdf(pos, [8, 8], [[1, 0], [0, 1]]) + multivariate_normal.pdf(pos, [2, 9], [[1, 0], [0, 1]])
 
#Large gaussian encompassing the entire mixture
def getqx(pos):
    return multivariate_normal([6, 6], [[12, 0], [0, 12]]).pdf(pos)

numcircles = 1
numdots = 3

x, y = np.mgrid[0:12:.01, 0:12:.01]
pos = np.dstack((x, y))

k = np.amax(np.divide(getpx(pos), getqx(pos)))
samples = np.zeros([numdots + numcircles, 2])
i = 0

while i < numdots + numcircles:
    test = np.zeros([1,2])
    test = np.random.multivariate_normal([6, 6], [[12, 0], [0, 12]])
    u = np.random.uniform(0, (k*getqx(test)))
   
    if u <= getpx(test):
        samples[i, :] = test # center of circle is the last "sample"
        i+=1


# parameters that should be machine-generated later, but for now, will be set
rad = np.random.uniform(1,3) # circle radius
x0 = samples[-1,0]
y0 = samples[-1,1]
circ_pts = np.array(circle_to_hexagon(rad, x0, y0))

# plots voronoi diagram
points = np.concatenate((samples, circ_pts))
vor = Voronoi(points)


fig = voronoi_plot_2d(vor)
ax2 = fig.add_subplot(111)
plt.axis([0, 12, 0, 12])
ax2.contourf(x, y, getpx(pos))
plt.axis([0, 12, 0, 12])
plt.gca().set_aspect('equal', adjustable='box')
ax2.scatter(samples[:, 0], samples[:, 1], s=20, color = 'black')

# plot circle
ax3 = fig.add_subplot()
circle = plt.Circle((x0, y0), rad, fill = False)
ax3.add_artist(circle)
ax3.set_aspect(1)
