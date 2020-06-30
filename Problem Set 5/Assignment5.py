import numpy as np 
import matplotlib.pyplot as plt
import math
import csv

### BEGIN: CSV DATA EXTRACTION ###

# first, we derive a list of just the sport names
# we end up with this list stored in a global variable 'sports'
with open('Assignment5-similarities.csv', mode = 'r') as csv_file:
	reader = csv.reader(csv_file)
	sports = next(reader)

# we initialise our dictionary that will hold our
# psychological distance values as a global variable
psiDict = {}

# then we derive the values from the list and place them in the dictionary
with open('Assignment5-similarities.csv', mode = 'r') as csv_file:
	
	# creatng a dictionary with the sport index as the key (0 thru 20)
	# and the distances to the other sports as a list as the values (in order)
	
	reader = csv.DictReader(csv_file)
	elem1 = 0
	for row in reader:
		rowDict = row
		valuesList = rowDict.values()
		
		# we calculate our psychological distance to be the value from 
		# the csv table subtraced from 1 (so that a higher similarity)
		# gives a lower psychological distance)
		valuesList = [(1 - float(x)) for x in valuesList]
		psiDict[elem1] = valuesList
		elem1 += 1

# we initialise our dictionary that will hold our
# similarity values as a global variable
similarityDict = {}

with open('Assignment5-similarities.csv', mode = 'r') as csv_file:
	
	# creatng a dictionary with the sport index as the key (0 thru 20)
	# and the similarities to the other sports as a list as the values (in order)
	
	reader = csv.DictReader(csv_file)
	elem1 = 0
	for row in reader:
		rowDict = row
		valuesList = rowDict.values()
		valuesList = [float(x) for x in valuesList]
		similarityDict[elem1] = valuesList
		elem1 += 1

### END: CSV DATA EXTRACTION ###

### BEGIN: HELPER FUNCTIONS ###

def genPositions(num):
	# use 21 for num to get random starting coordinates 
	# for all 21 sports
	
	positionMatrix = []
	for i in range(0, num):
		a = np.random.uniform()
		b = np.random.uniform()
		positionMatrix.append((a, b))
	return positionMatrix

def dist(p1, p2):
	d = ((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2)
	d = math.sqrt(d)
	return d

def oneStress(p1, p2, in1, in2):
	# calculate the stress of two points

	# we first calculate the physical distance between
	# the coordinates using the distance formula
	d = dist(p1, p2)

	# then we derive the psychological distance that we 
	# extracted from the csv file earlier
	sim = psiDict[in1][in2]

	return (sim - d) ** 2

def stress(positions):
	# calculate the stress of all points
	
	s = 0
	for i in range(0, len(positions)):
		for j in range(i + 1, len(positions)):
			pos1, pos2 = positions[i], positions[j]
			s += oneStress(pos1, pos2, i, j)
	return s

def gradient(positions):
	gradient = []
	
	# calculate the gradient of a plane of coordinates
	# p is the index of our coordinate (0 through 20)
	p = 0
	for point in positions:
		
		# first we calculate gradX, the gradient of the current
		# coordinate's x component
		i = positions[:]
		i[p] = (i[p][0] + 0.001, i[p][1])
		s1 = stress(i)
		i[p]= (i[p][0] - 0.001, i[p][1])
		s2 = stress(i)
		gradX = (s1 - s2) / (2 * 0.001)

		# then we calculate gradY, the gradient of the current 
		# coordinate's y component
		i = positions[:]
		i[p]= (i[p][0], i[p][1] + 0.001)
		s1 = stress(i)
		i[p]= (i[p][0], i[p][1] - 0.001)
		s2 = stress(i)
		gradY = (s1 - s2) / (2 * 0.001)

		gradient.append((gradX, gradY))
		p += 1
	
	# at the end, gradient hold a list of our gradients in order
	# i.e. (gradX1, gradY1, gradX2, gradY2, ...)
	return gradient

def adjustCoor(positions, gradient):
	
	# adjust our coordinates based on the values we got from the gradient
	for i in range(0, len(positions)):
		
		# checking whether to move x up or down
		if gradient[i][0] < 0:
			positions[i] = (positions[i][0] + (-0.01 * gradient[i][0]), positions[i][1])
		elif gradient[i][0] > 0:
			positions[i] = (positions[i][0] - (0.01 * gradient[i][0]), positions[i][1])
		
		# checking whether to move y up or down
		if gradient[i][1] < 0:
			positions[i] = (positions[i][0], positions[i][1] + (-0.01 * gradient[i][1]))
		elif gradient[i][1] > 0:
			positions[i] = (positions[i][0], positions[i][1] - (0.01 * gradient[i][1]))
	return positions

def displayPlot(positions):
	
	# calculates the stress of our coordinates
	#  and creates a scatterplot of our coordinates
	print("Stress:", stress(positions))
	x = []
	y = []
	for i in range(0, len(positions)):
		x.append(positions[i][0])
		y.append(positions[i][1])
	plt.xlabel('horizontal similarity')
	plt.ylabel('vertical similarity')
	plt.title('Sports Organized by Similarity using MDS')
	plt.scatter(x, y)
	for i, sport in enumerate(sports):
		plt.annotate(sport, (x[i], y[i]))
	plt.show()

### END: HELPER FUNCTIONS

### BEGIN: MDS EXECUTION ###

def executeMDS(i):
	
	# our main execution function that pulls everything together
	# start by generating random coordinates for our sports
	p = genPositions(21)
	
	# display the orig. stress and scatterplot before MDS
	displayPlot(p)
	
	# for i iterations, we will calculate the gradient and
	# adjust our coordinates accordingly
	for k in range(0, i):
		g = gradient(p)
		p = adjustCoor(p, g)
	
	# display our ending stress and scatterplot after MDS
	displayPlot(p)
	return p

#executeMDS(1000)

def executeMDSStress(i):

	# initialize an array to hold the stress values over time
	stresses = []
	
	# for i iterations, we will calculate the gradient and
	# adjust our coordinates accordingly, then calculate stress
	# and add it to our stresses array
	p = executeMDS(i)
	s = stress(p)
	stresses.append(s)
	
	# we now have the data to plot our stress values over time
	x = np.arange(0, i + 1)
	y = stresses
	plt.xlabel('MDS iteration')
	plt.ylabel('stress')
	plt.title('Stress of Sport Similarity Coordinates over \n Iterations of MDS')
	plt.plot(x, y)
	plt.show()

#executeMDSStress(1000)

def makeSubplots(t, i):

	# this function will plot t subplots, each one representing a fresh trial
	# of our MDS algorithm (t must be divisble by 2)

	fig, sub = plt.subplots(t // 2, 2)

	# j will be our row index
	for j in range(0, t // 2):
		# k will be our column index
		for k in range(0, 2):
			
			# we generate a new vector of positions and run MDS
			p = executeMDS(i)

			# we create the plot for this trial 
			x = []
			y = []
			for i in range(0, len(p)):
				x.append(p[i][0])
				y.append(p[i][1])
			sub[j][k].scatter(x, y)
			for i, sport in enumerate(sports):
				sub[j][k].annotate(sport, (x[i], y[i]))
	
	# once finished with all trials, we show all trials together
	plt.show()

#makeSubplots(10, 1000)


def findBestTrial(t, i):
	
	# this function will run our MDS algorithm t times and use the
	# ending stress of each trial to determine which trial produced the
	# best graph

	# first we iniialize our variable that will help us keep track
	# of the best graph
	p = genPositions(21)
	best = stress(p)
	bestIndex = 0
	bestPositions = p

	# then we run our algorithm t times
	for k in range(1, t + 1):
		p = executeMDS(i)
		s = stress(p)
		
		# for each trial, we have to see if the trial's result is 
		# better than our previous best result
		if (s < best):
			best = s
			bestIndex = k
			bestPositions = p

	print("Our best trial was trial", bestIndex)
	displayPlot(bestPositions)

#findBestTrial(10, 1000)

def plotMDSvsPsi(i):

	# this function will plot the psi distances against the distances
	# we calculate with MDS

	p = executeMDS(i)
	MDSDist = []
	for j in range(0, len(p)):
		for k in range(j + 1, len(p)):
			d = dist(p[j], p[k])
			MDSDist.append(d)

	psiDist = []
	count = 1
	for key in psiDict:
		curr = psiDict[key]
		psiDist += curr[count:]
		count += 1

	print(MDSDist)
	print(psiDist)

	plt.xlabel('MDSDist')
	plt.ylabel('psiDist')
	plt.title('MDSDist vs psiDist')
	plt.scatter(MDSDist, psiDist)
	plt.show()

plotMDSvsPsi(1000)

### END: MDS EXECUTION ###



