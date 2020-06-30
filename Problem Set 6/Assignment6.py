import numpy as np 
import matplotlib.pyplot as plt

def genRegions(n):

	# generate n regions and store them as tuples in a list

	regions = []
	for i in range(0, n):
		low = np.random.uniform(-11, 11)
		high = np.random.uniform(-11, 11)
		if (low < high):
			regions.append((low, high))
		else:
			regions.append((high, low))
	return regions

regions = genRegions(10000)

# PROBLEM 1

def contains(region, point):
	
	# check if region contains points

	if (point <= region[1]) and (point >= region[0]):
		return True
	return False

# PROBLEM 2

def findProb(point, regions):

	# finds the probability a region in regions contains point
	# if it contains 0 as well

	weight = 1 / len(regions)

	# find P(x = 0 & x = 1)
	num = 0
	den = 0
	for region in regions:
		height = 1 / (region[1] - region[0])
		if (contains(region, 0)):
			den += weight * height 
			if contains(region, point):
				num += weight * height
	p1 = num / den

	# find P(x = 0)
	num = 0
	den = 0
	for region in regions:
		height = 1 / (region[1] - region[0])
		if (contains(region, 0)):
			num += weight * height
			den += weight * height
	p2 = num / den

	return (p1 / p2)


print("The probability of getting x=1 for regions containing x=0 is:", findProb(1, regions))

# PROBLEM 3

def findProbOverRange(rStart, rEnd, regions):

	# plots the probability for each point in [rStart, rEnd) that it 
	# is in a region in regions given that region contains 0

	probabilities = []

	for p in range(rStart, rEnd):
		probabilities.append(findProb(p, regions))

	return probabilities

y = findProbOverRange(0, 11, regions)
x = np.arange(0, 11)
plt.xlabel("chosen point")
plt.ylabel("probability point is sampled")
plt.title("Probability each point is sampled, given the region contains 0")
plt.plot(x, y)
plt.show()

# PROBLEM 5

y = findProbOverRange(-5, 6, regions)
x = np.arange(-5, 6)
plt.xlabel("chosen point")
plt.ylabel("probability point is sampled")
plt.title("Probability each point is sampled (on a logarithmic scale), \n given the region contains 0")
plt.semilogy(x, y)
plt.show()

y = findProbOverRange(-10, 11, regions)
x = np.arange(-10, 11)
plt.xlabel("chosen point")
plt.ylabel("probability point is sampled")
plt.title("Probability each point is sampled (on a logarithmic scale), \n given the region contains 0")
plt.semilogy(x, y)
plt.show()

# PROBLEM 6
r = int(np.random.uniform(0, 9990))

y = findProbOverRange(0, 11, regions[r : r + 10])
x = np.arange(0, 11)
plt.xlabel("chosen point")
plt.ylabel("probability point is sampled")
plt.title("Probability each point is sampled (out of 10 regions), \n given the region contains 0")
plt.plot(x, y)
plt.show()

r = int(np.random.uniform(0, 9900))

y = findProbOverRange(0, 11, regions[r : r + 100])
x = np.arange(0, 11)
plt.xlabel("chosen point")
plt.ylabel("probability point is sampled")
plt.title("Probability each point is sampled (out of 100 regions), \n given the region contains 0")
plt.plot(x, y)
plt.show()

r = int(np.random.uniform(0, 9000))

y = findProbOverRange(0, 11, regions[r : r + 1000])
x = np.arange(0, 11)
plt.xlabel("chosen point")
plt.ylabel("probability point is sampled")
plt.title("Probability each point is sampled (out of 1000 regions), \n given the region contains 0")
plt.plot(x, y)
plt.show()





