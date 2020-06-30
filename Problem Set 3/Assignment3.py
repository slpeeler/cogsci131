import numpy as np 
import matplotlib.pyplot as plt
import math

#1a

def NorNum(sd):
	return np.random.normal(0, sd)

def randomAntPath(time):
	x = [0] * time
	y = [0] * time
	for i in range(1, time):
		xCh = NorNum(1)
		yCh = NorNum(1)
		y[i] = y[i - 1] + yCh
		x[i] = x[i - 1] + xCh
	return (x, y)

"""both = randomAntPath(3600)
x = both[0]
y = both[1]
plt.plot(x, y)
plt.title('Random Ant Path (time = 1 hour)')
plt.xlabel('horizontal travel')
plt.ylabel('vertical travel')
plt.show()"""


#1b

def distance(point1, point2):
	d = (point2[0] - point1[0]) ** 2
	d = d + ((point2[1] - point1[1]) ** 2)
	d = math.sqrt(d)
	return d

def antPathwithCheck(time, startPoint):
	x = [0] * time
	y = [0] * time
	x[0] = startPoint[0]
	y[0] = startPoint[1]
	for i in range(1, time):
		xCh = NorNum(1)
		yCh = NorNum(1)
		y[i] = y[i - 1] + yCh
		x[i] = x[i - 1] + xCh
		if (distance((x[i],y[i]), (0, 0))) <= 5:
			return 1
	return 0

def runSimulations(trials, time):
	successes = 0
	for i in range(0, trials):
		endpoint = randomAntPath(time)
		endpoint = (endpoint[0][time - 1], endpoint[1][time - 1])
		successes += antPathwithCheck(time, endpoint)
	return (successes / trials)

#print(runSimulations(10000, 3600)) # return ~0.142 probability


#1c

def closestDistance(time, startPoint):
	x = [0] * time
	y = [0] * time
	x[0] = startPoint[0]
	y[0] = startPoint[1]
	dist = distance((x[0], y[0]), (0, 0))
	for i in range(1, time):
		xCh = NorNum(1)
		yCh = NorNum(1)
		y[i] = y[i - 1] + yCh
		x[i] = x[i - 1] + xCh
		currDist = distance((x[i],y[i]), (0, 0))
		if (currDist < dist):
			dist = currDist
	return dist

def runDistSimulations(trials, time):
	total = 0
	for i in range(0, trials):
		endpoint = randomAntPath(time)
		endpoint = (endpoint[0][time - 1], endpoint[1][time - 1])
		total += closestDistance(time, endpoint)
	return (total / trials)

#print(runDistSimulations(10000, 3600)) # returns ~44.7 mm


#2

def walkAndRemember(sd, time):
	x = [0] * time
	y = [0] * time
	bigX = 0
	bigY = 0
	for i in range(1, time):
		xCh = NorNum(1)
		yCh = NorNum(1)
		y[i] = y[i - 1] + yCh
		x[i] = x[i - 1] + xCh
		bigX += (xCh + NorNum(sd))
		bigY += (yCh + NorNum(sd))
	return [bigX, bigY, (x[time - 1], y[time - 1])]

def runIntegSimulations(sd, time, trials):
	amountOff = 0
	for i in range(0, trials):
		walkData = walkAndRemember(sd, time)
		endpointX, endpointY = walkData[2][0], walkData[2][1]
		returnX, returnY = endpointX - walkData[0], endpointY - walkData[1]
		amountOff += distance((0, 0), (returnX, returnY))
	return (amountOff / trials)

"""x = [0.0001, 0.001, 0.01, 0.1, 1.0]
y = [runIntegSimulations(i, 3600, 10000) for i in x]
for i in range(0, len(x)):
	print("SD: ", x[i], " Dist from nest: ", y[i])
plt.title('Average Return Distance from \n Nest as a Function of SD')
plt.xlabel('standard deviation of Guassian noise (mm)')
plt.ylabel('ending distance away from nest (mm)')
plt.semilogx(x, y)
plt.show()"""

#3a

def outboundEnergy(sd):
	return math.exp(0.1/sd)

def inboundEnergy(xChange, yChange, endpoint):
	returnPoint = (endpoint[0] - xChange, endpoint[1] - yChange)
	dist = distance((0, 0), returnPoint)
	return dist ** 2

def runEnergySimulations(sd, time, trials):
	energy = 0
	for i in range(0, trials):
		energy += outboundEnergy(sd)
		walkData = walkAndRemember(sd, time)
		energy += inboundEnergy(walkData[0], walkData[1], walkData[2])
	return (energy / trials)

x = [0.01, 0.01, 0.1, 1.0]
y = [runEnergySimulations(i, 3600, 10000) for i in x]
for i in range(0, len(x)):
	print("SD: ", x[i], " Energy: ", y[i])
plt.title('Average Energy Expended during Path Integration \n as a Function of SD')
plt.xlabel('standard deviation of Guassian noise (mm)')
plt.ylabel('energy expended (energy units)')
plt.semilogx(x, y)
plt.show()
	



