import matplotlib.pyplot as plt
import numpy as np
import random as ran

#1a


def rascola(x, start, a):
	b = 0.1
	counter = 0
	while (counter < x):
		start = (start + (a * b * (1 - start)))
		counter += 1
	return start



x = np.arange(0, 20, 1)
y1 = [rascola(i, 0.05, 0.5) for i in x.astype(int)]
y2 = [rascola(i, 0.5, 0.5) for i in x.astype(int)]
plt.xlabel('time')
plt.ylabel('light association')
plt.title('Rescorla-Wagner model of \n starting associations of 0.5 and 0.05')
plt.plot(x, y1, color = 'red', label = '0.05 starting association')
plt.plot(x, y2, color = 'blue',label = '0.5 starting association')
plt.legend()
plt.show()


#1b

def findTrial(goal, start, a):

	#finds the number of trials for the association to reach goal

	trial = 0
	t = 0
	while (t < goal):
		trial += 1
		t = rascola(trial, start, a)
	return trial

print("trial: ", findTrial(0.8, 0.05, 0.5)) #returns 31


#1c

def findSalience(goal, start, time):
	s = 0.0
	r = rascola(time, start, s)
	while (r < goal):
		s += 0.00001
		r = rascola(time, start, s)
	return s

print ("salience: ", findSalience(0.8, 0.0, 13)) #returns 1.1644699999991612

x = np.arange(0, 15, 1)
y = [rascola(i, 0, findSalience(0.8, 0.0, 13)) for i in x.astype(int)]
plt.xlabel('time')
plt.ylabel('buzzer association')
plt.title('Rescorla-Wagner model of \n association 0 -> 0.8 after 13 trials')
plt.plot(x, y)
plt.show()

#2

def doubleRascola(trial, start1, start2, a):

	#returns association for item 1, taking into account item 2
	#switch parameters start1 and start2 for association of item 2

	b = 0.1
	counter = 0
	while (counter < trial):
		start1 = start1 + (a * b * (1 - (start1 + start2)))
		start2 = start2 + (a * b * (1 - (start1 + start2)))
		counter += 1
	return start1

x = np.arange(0, 20, 1)
y1 = [doubleRascola(i, 0, 0.8, 0.2) for i in x.astype(int)]
y2 = [doubleRascola(i, 0.8, 0, 0.5) for i in x.astype(int)]
plt.xlabel('time')
plt.ylabel('bell association')
plt.title('Rescorla-Wagner model of just the bell association')
plt.plot(x, y1)
plt.show()
plt.xlabel('time')
plt.ylabel('association')
plt.title('Rescorla-Wagner model of both \n the bell and light association')
plt.plot(x, y1, color = 'blue', label = 'bell association')
plt.plot(x, y2, color = 'red', label = 'light association')
plt.legend()
plt.show()


#3a


x = np.arange(0, 100)
y1 = [0] * 100
for i in range(1, 100):
	if (i % 2 == 0):
		y1[i] = y1[i - 1] - (0.2 * 0.1 * (y1[i - 1]))
	else:
		y1[i] = y1[i - 1] + (0.2 * 0.1 * (1 - y1[i - 1]))
	
plt.xlabel('time')
plt.ylabel('bell association')
plt.title('Rescorla-Wagner model of an \n alternating bell stimulus')
plt.plot(x, y1, label = 'alternating trials')
y2 = [rascola(i, 0, 0.2) for i in x.astype(int)]
plt.plot(x, y2, label = 'only learning trials')
plt.legend()
plt.show()

# The first graph is of the alternating trials; the second is the graph
# if we just gave food and rang the bell each trial. The first graph
# shows the association after 20 trials is only 0.2, whereas the 
# second graph shows the association is 0.3. This makes sense, as one
# can imagine that doing repeated trials with both stimuli without
# interruption or change is going to reinforce the assocation, whereas
# having the trials that don't present food are going to somewhat weaken
# the association. Also, the first graph takes a more linear journey to 
# full association than the second graph, which gets closer to 1 sooner
# and has to start tapering off sooner.


#3b

def genDecision(prob):

	# will return 1 with probability (prob), and 0 with 
	# probability (1 - prob)

	return np.random.choice(2, 1, p = [1 - prob, prob])

x = np.arange(0, 100)

def probPlot(p):
	y = [0] * 100
	for i in range(1, 100):
		decision = genDecision(p)
		if (decision == 1):
			y[i] = y[i - 1] + (0.2 * 0.1 * (1 - y[i - 1]))
		else:
			y[i] = y[i - 1] - (0.2 * 0.1 * (y[i - 1]))
	return y
	
plt.xlabel('time')
plt.ylabel('bell association')
plt.title('Rescorla-Wagner model of association \n with a bell presented with \n various probabilities')
plt.plot(x, probPlot(0.5), color = 'blue', label = '0.5 probability')
plt.plot(x, probPlot(0.3), color = 'red', label = '0.3 probability')
plt.plot(x, probPlot(0.7), color = 'green', label = '0.7 probability')
plt.plot(x, probPlot(0.1), color = 'purple', label = '0.1 probability')
plt.plot(x, probPlot(0.9), color = 'orange', label = '0.9 probability')
plt.plot(x, probPlot(1), color = 'black', label = '1.0 probability')
plt.plot(x, probPlot(0), color = 'gray', label = '0.0 probability')
plt.legend()
plt.show()


