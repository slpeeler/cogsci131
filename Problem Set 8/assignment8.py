import matplotlib.pyplot as plt
import numpy as np

#Hypotheses

H1 = [x for x in range(1, 101) if (x % 2 == 0)]
H2 = [x for x in range(1, 101) if (x % 2 != 0)]
H3 = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
H4 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
H5 = [x for x in range(1, 101) if (x % 5 == 0)]
H6 = [x for x in range(1, 101) if (x % 10 == 0)]
H7 = [x for x in range(1, 101)]

#list of all the hypotheses
allHyp = [H1, H2, H3, H4, H5, H6, H7]

#1
def SizePrincipleLikelihood(point, hyp):
	#the denominator
	total = len(hyp)
	#counting how many instances of the point (usually 1)
	count = [d for d in hyp if (d == point)]
	count = len(count)
	#likelihood ends up being the instances over the total
	return (count / total)

def GetAllLikelihoods(hypList):
	#calculating the likelihood for each point in each hypothesis
	for i in range(0, len(hypList)):
		#getting the correct hypothesis
		hyp = hypList[i]
		#create an ordered list with tuples, where item 1 is the point
		#and item 2 is the likelihood
		results = [(point, SizePrincipleLikelihood(point, hyp)) for point in hyp]
		#print out these results
		print("Likelihoods for H",i + 1, ":", results)
	return

GetAllLikelihoods(allHyp)


#2
def GetProportionsAndSum(hypList, knownData):
	#calculate the equal probability of each hypothesis
	hypProb = 1 / len(hypList)
	#where we will store our proportional P(H|D)'s
	propResults = []
	#if no known points, we will just keep equal probabilities
	if len(knownData) == 0:
		propResults = [hypProb] * len(hypList)
	else:
		#where we will store our actual calculations before proportional
		actualsResults = []
		#for each hypothesis, calculate the non-prop P(H|D)
		for hyp in hypList:
			actualResult = hypProb
			for data in knownData:
				actualResult *= SizePrincipleLikelihood(data, hyp)
			#add this value to our non-prop list
			actualsResults.append(actualResult)
		#sum up our non-prop calculations
		actualSum = sum(actualsResults)
		#find their proportional parts and store in propResults
		for result in actualsResults:
			propResults.append(result / actualSum)
	#with that, find P(n is accepted|D)
	nAccepted = []
	for n in range(1, 101):
		nSum = 0
		#perform the summation, calculate each part
		for i in range(0, len(hypList)):
			#factor is whether n is in the hypothesis
			factor = 1 if (n in hypList[i]) else 0
			#multiple factor with P(H|D) and add to the sum
			nSum += (factor * propResults[i])
		#nAccpted will contain the probabilities for all n 1-100
		nAccepted.append(nSum)
	x = np.arange(1, 101)
	y = nAccepted
	plt.xlabel('point n')
	plt.ylabel('probability n is in D')
	title = 'Posterior Predictive Probability with data' + str(knownData)
	plt.title(title)
	n = range(1, 101)
	plt.scatter(x, y)
	for i, txt in enumerate(n):
		plt.annotate(txt, (x[i], y[i]))
	plt.show()
	return

#knownData sets
kData = [[], [50], [53], [50, 53], [16], [10, 20], [2, 4, 8], [2, 4, 8, 10]]
for data in kData:
	GetProportionsAndSum(allHyp, data)

#3

def getRanges(start, end):
	#derive all possible ranges in a start and endpoint
	ranges = []
	for i in range(start, end):
		for j in range(i + 1, end + 1):
			ranges.append(range(i, j))
	return ranges

def GetProportionsAndSumRanges(hypList, ranges, knownData):
	#calculate the equal probability of each hypothesis
	hypProb = 1 / (len(hypList) + 1)
	rangeProb = hypProb / len(ranges)
	#where we will store our proportional P(H|D)'s
	propResults = []
	#if no known points, we will just keep equal probabilities
	if len(knownData) == 0:
		propResults = ([hypProb] * len(hypList)) + ([rangeProb] * len(ranges))
	else:
		#where we will store our actual calculations before proportional
		actualsResults = []
		#for each hypothesis and range, calculate the non-prop P(H|D)
		for hyp in hypList:
			actualResult = hypProb
			for data in knownData:
				actualResult *= SizePrincipleLikelihood(data, hyp)
			#add this value to our non-prop list
			actualsResults.append(actualResult)
		for rang in ranges:
			actualResult = rangeProb
			for data in knownData:
				actualResult *= SizePrincipleLikelihood(data, rang)
			#add this value to our non-prop list
			actualsResults.append(actualResult)
		#sum up our non-prop calculations
		actualSum = sum(actualsResults)
		#find their proportional parts and store in propResults
		for result in actualsResults:
			propResults.append(result / actualSum)
	#with that, find P(n is accepted|D)
	nAccepted = []
	for n in range(1, 101):
		nSum = 0
		#perform the summation, calculate each part (hypothesis and range)
		for i in range(0, len(hypList)):
			#factor is whether n is in the hypothesis
			factor = 1 if (n in hypList[i]) else 0
			#multiple factor with P(H|D) and add to the sum
			nSum += (factor * propResults[i])
		for i in range(0, len(ranges)):
			#factor is whether n is in the hypothesis
			factor = 1 if (n in ranges[i]) else 0
			#multiplie factor with P(H|D) and add to the sum
			nSum += (factor * propResults[i + len(hypList)])
		#nAccpted will contain the probabilities for all n 1-100
		nAccepted.append(nSum)
	x = np.arange(1, 101)
	y = nAccepted
	plt.xlabel('point n')
	plt.ylabel('probability n is in D')
	title = 'Posterior Predictive Probability with Ranges, with data' + str(knownData)
	plt.title(title)
	n = range(1, 101)
	plt.scatter(x, y)
	for i, txt in enumerate(n):
		plt.annotate(txt, (x[i], y[i]))
	plt.show()
	return

#knownData sets
kData = [[], [50], [53], [50, 53], [16], [10, 20], [2, 4, 8], [2, 4, 8, 10]]
r = getRanges(1, 100)
for data in kData:
	GetProportionsAndSumRanges(allHyp, r, data)




