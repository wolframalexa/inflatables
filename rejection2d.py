import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
from scipy.stats import uniform


x, y = np.mgrid[0:12:.01, 0:12:.01]
pos = np.dstack((x, y))

#Mixture distribution (aka u can make the means and covariance matrix anything that you want)
def getpx(pos):
    return multivariate_normal.pdf(pos, [5, 5], [[1, 0], [0, 1]]) + multivariate_normal.pdf(pos, [8, 8], [[1, 0], [0, 1]]) + multivariate_normal.pdf(pos, [2, 9], [[1, 0], [0, 1]])
 
#Large gaussian encompassing the entire mixture
def getqx(pos):
    return multivariate_normal([6, 6], [[12, 0], [0, 12]]).pdf(pos)

#Just to see the mixture heatmap
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.contourf(x, y, getpx(pos))


k = np.amax(np.divide(getpx(pos), getqx(pos)))
samples = np.zeros([5, 2]) #Currently 5 samples (can change this with the loop condition to make more)
i = 0

while i < 5: #5 samples
    test = np.zeros([1,2])
    test = np.random.multivariate_normal([6, 6], [[12, 0], [0, 12]])
    u = np.random.uniform(0, (k*getqx(test)))
   
    if u <= getpx(test):
        samples[i, :] = test
        i+=1

#See the samples (5x2 with each row being a coordinate of the sample)
ax2.scatter(samples[:, 0], samples[:, 1], s=20, color = 'black')
print(samples)


