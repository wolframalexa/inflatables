import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.stats as stats
from scipy.stats import multivariate_normal
from scipy.stats import uniform

def followsRules(circles, points):
	out = True
	# format of circles: [[x, y, rad], ]
	# format of points: [[x, y], ]

	edgelim = 0.75 # distance to edge [in]
	interlim = 1.5 # distance from element to element [in]

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
				if incircle(point, circle):
					out = False
					print("Point in circle")
					break

				dist = (((point[0] - circle[0])**2) + ((point[1] - circle[1])**2))**(1/2) - circle[2]
				if dist < interlim:
					out = False
					print("Point too close to circle")
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

# Mixture distribution


# Large gaussian encompassing the entire mixture
def getqx(pos):
	return multivariate_normal([6, 6], [[12, 0], [0, 12]]).pdf(pos)
 


x, y = np.mgrid[0:12:.01, 0:12:.01]
pos = np.dstack((x, y))

iterations = 200
numcircles = 3
numdots = 10

circles = np.zeros((numcircles, 3))
dots = np.zeros((numdots, 2))

pro_circles = np.zeros((numcircles, 3)) # proposed circles and dots
pro_dots = np.zeros((numdots, 2))

count = 0
tracker = 1
# place circles first
while (count < numcircles) and (tracker < iterations): # time out if over some max # of iterations
	#print(tracker)
	# generate circle
	rad = 2.25/2
	x = np.random.uniform(3,9)
	y = np.random.uniform(3,9)

	curr = np.array([x, y, rad])
	pro_circles = circles
	pro_circles[count, :] = curr


	#itergraph(pro_circles, pro_dots)
	#plt.savefig('antirejection/img' + str(tracker) + '.png')
	tracker += 1

	# meets configuration? if yes - then accept
	if followsRules(pro_circles[:count+1, :], []):
			circles[count, :] = curr
			count += 1


#Plot initialization
fig_2, ax_2 = plt.subplots(2, 3, figsize=(14,12))

#Plotting function
def plot_2_d(i,j, mu, cov, iteration):
    #Get proper color for each data point and plot it
    #Plot estimated distribution
    xy = np.mgrid[1:11:0.01, 1:11:0.01]
    x = xy[0]
    y = xy[1]
    xy = np.dstack((x,y))
    #for i in range(0, len(mu)):
      
    classes = np.zeros([len(mu), 1000, 1000])
    
    for h in range(0, len(mu)):
      classes[h, :, :] = stats.multivariate_normal.pdf(xy, mu[h,:], cov[h, :, :])
      if h < 3:
        ax_2[i,j].contour(x, y, classes[h, :, :], levels = 3, zorder = 3, colors = 'red')
      else:
        ax_2[i,j].contour(x, y, classes[h, :, :], levels = 3, zorder = 3)

    ax_2[i,j].set_title(f'L = {iteration} iterations')

#EM steps
def em_2_d(mu, cov, pi, data):
    #Equation 9.23
    gam = np.zeros([len(mu), 500])
    for i in range(0, len(mu)):
      gam[i, :] = pi[0, i]*stats.multivariate_normal.pdf(data, mu[i], 2*cov[i, :, :])
    

    gam_sum = np.sum(gam, axis = 0)
    for i in range(0, len(mu)):
      gam[i, :] = np.atleast_2d(gam[i, :]/gam_sum)

    
    #Equation 9.24
    for i in range(3, len(mu)):
      mu[i, :] = 1/np.sum(gam[i, :]) * (np.mat(gam[i, :]) * np.mat(data))
    

    #Equation 9.25
    for i in range(3, len(mu)):
      cov[i, :, :] = (gam[i, :]*(data-mu[i, :]).T @ (data-mu[i, :]))/np.sum(gam[i, :])


    #Equation 9.26
    for i in range(3, len(mu)):
      pi[0, i] = np.sum(gam[i, :])/500

    return mu, cov, pi,



#Mission control
def part_2(mu2_new, cov2_new, pi2_new, full_data):
    for i in range(21):
        if i==0: plot_2_d(0,0, mu2_new, cov2_new, i)
        if i==1: plot_2_d(0,1, mu2_new, cov2_new, i)
        if i==2: plot_2_d(0,2, mu2_new, cov2_new,  i)
        if i==5: plot_2_d(1,0, mu2_new, cov2_new,  i) 
        if i==10: plot_2_d(1,1, mu2_new, cov2_new,  i)
        if i==20: plot_2_d(1,2, mu2_new, cov2_new,  i)
        mu2_new, cov2_new, pi2_new  = em_2_d(mu2_new, cov2_new, pi2_new, full_data)

    return mu2_new, cov2_new

def EMlogic(circle):
  #Process data from txt file
  N = 500
  full_data = np.zeros([N, 2])

  full_data[:, 0] = np.random.uniform(size = N,low = 1,high = 11)
  full_data[:, 1] = np.random.uniform(size = N,low = 1,high = 11)

  #Initial Guesses
  mu2_init = np.concatenate((circle, np.array([[2, 2], [10,10], [2, 10], [10, 2], [2, 6], [6, 2], [10, 6], [6, 10]]))) #Each row is it's own guess
  cov2_init = np.array([[[.75,0], [0,.75]], [[.75,0], [0,.75]], [[.75,0], [0,.75]], [[.75,0], [0,.75]], [[.75,0], [0,.75]],[[.75,0], [0,.75]], [[.75,0], [0,.75]],[[.75,0], [0,.75]], [[.75,0], [0,.75]],[[.75,0], [0,.75]], [[.75,0], [0,.75]]])
  pi2_init = np.full([1, len(mu2_init)], .5)        

  mu2_new = np.copy(mu2_init)
  cov2_new = np.copy(cov2_init)
  pi2_new = np.copy(pi2_init)

  return part_2(mu2_new, cov2_new, pi2_new, full_data)

meann, covv = EMlogic(circles[:, :2])
print(meann)
print(meann.shape)
print(covv)
print(covv.shape)

def getpx(test):
	pxx = 0
	for i in range(3, len(meann)):
		pxx += multivariate_normal.pdf(test, meann[i, :], covv[i, :, :])
		
	return pxx

count = 0

# generate dots
while (count < numdots) and (tracker < iterations):
	#print(tracker)
	k = np.amax(np.divide(getpx(pos), getqx(pos)))
	print(k)
	samples = np.zeros([1, 2])

	test = np.zeros([1,2])
	test = np.random.uniform(1, 11, [1, 2])
 
	u = np.random.uniform(0, (k*getqx(test)))
	pro_dots = dots

	if u <= getpx(test):
		print("accepted")
		pro_dots[count, :] = test

		#itergraph(circles, pro_dots)
		#plt.savefig('antirejection/img' + str(tracker) + '.png')
		tracker += 1

		# check if follows rules
		if followsRules(circles, pro_dots[:count+1, :]):
			dots[count, :] = test
			count += 1
			#success
		# else, pro_dots[count,:] is replaced at the following loop so no need to handle


itergraph(circles, pro_dots)
print("Dots:", dots)
print("Circles:", circles[:, :2])