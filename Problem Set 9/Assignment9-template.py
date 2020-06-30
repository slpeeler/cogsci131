
# Template for Assignment 9
import numpy as np
from math import log, sqrt
import matplotlib.pyplot as plt
import scipy.stats

import pandas as pd
df = pd.read_csv('Assignment9-data.csv')
n1 = df['n1'].values
n2 = df['n2'].values
a = df['correct'].values

def log_likelihood(n1, n2, a, W):
    # this function takes a numpy array for n1, n2, and the accuracy (0/1), whether they answerd correctly
    # as well as W (the hypothesis)
    # and returns the *log* likelihood of the responses, log P(accuracy | n1, n2, W)
    
    assert(len(n1) == len(n2) == len(a))

    p = 1.0-scipy.stats.norm.cdf(0, loc=np.abs(n1-n2), scale=W*np.sqrt(n1**2 + n2**2)) # the probability of answering correctly
    return np.sum(np.where(a, np.log(p), np.log(1.0-p)))

#3
def log_prior(W):
	# computes the log prior with a given W: e^(-W)
	if W < 0:
		return 0
	else:
		return np.log(np.exp(-W))

def log_posterior(prior, likelihood):
	# calculates the log posterior given a prior and a likelihood
	return prior + likelihood

#4
def Metropolis(n):
	# implmentation of the Metropolis algorithm that runs 
	# over the first n samples
	
	# generate W and its posterior, and initialize the
	# arrays we will use to store values over samples
	w = np.random.uniform()
	values_array = [w]
	w_pos = log_posterior(log_prior(w), log_likelihood(n1, n2, a, w))
	posterior_array = [w_pos]

	for i in range(0, n - 1):
		# generate W prime and its posterior
		noise = np.random.normal(0, 0.1)
		wP = w + noise
		wP_pos = log_posterior(log_prior(wP), log_likelihood(n1, n2, a, wP))
		w_pos = posterior_array[i]

		# perform the division between the two posteriors
		# comparison = P(W’|D)/P(W|D)
		comparison = np.exp(wP_pos - w_pos)

		# if W prime is better, accept it as new W
		if comparison > 1:
			w = wP
		# if W prime not better, accept it with probability
		else:
			w = np.random.choice([w, wP], 1, p = [1 - comparison, comparison])[0]

		# append this run's values to our values and posteriors arrays
		values_array.append(w)
		if w == wP:
			posterior_array.append(wP_pos)
		else:
			posterior_array.append(w_pos)

	return (values_array, posterior_array)

#4(a)
results = Metropolis(300)
samples = np.arange(300)
posteriors = results[1]
plt.xlabel('sample number')
plt.ylabel('posterior of W')
plt.title('Posterior of W over 300 Samples')
plt.plot(samples, posteriors)
plt.show()
#4(b)
values = results[0]
plt.xlabel('sample number')
plt.ylabel('value of W')
plt.title('Values of W over 300 Samples')
plt.plot(samples, values)
plt.show()
#4(c)
results = Metropolis(11000)
samples = np.arange(10000)
values = results[0][1000:]
plt.xlabel('value of W')
plt.ylabel('frequency')
plt.title('Values of W over 10,000 Samples (after 1000 sample burn)')
plt.hist(values, 20)
plt.show()

#5
count = 0
for value in values:
	if (value >= 0.6) and (value <= 0.65):
		count += 1
count = count / 10000
probability = "The probability that W is in the interval 0.6 and 0.65 is " + str(count)
print(probability)

def Metropolis_Prior(n):
	# implmentation of the Metropolis algorithm that runs 
	# over the first n samples
	
	# generate W and its prior, and initialize the
	# arrays we will use to store values over samples
	w = np.random.uniform()
	values_array = [w]
	w_pos = log_prior(w)
	posterior_array = [w_pos]

	for i in range(0, n - 1):
		# generate W prime and its prior
		noise = np.random.normal(0, 0.1)
		wP = w + noise
		wP_pos = log_prior(wP)
		w_pos = posterior_array[i]

		# perform the division between the two posteriors
		# comparison = P(W’|D)/P(W|D)
		comparison = np.exp(wP_pos - w_pos)

		# if W prime is better, accept it as new W
		if comparison > 1:
			w = wP
		# if W prime not better, accept it with probability
		else:
			w = np.random.choice([w, wP], 1, p = [1 - comparison, comparison])[0]

		# append this run's values to our values and posteriors arrays
		values_array.append(w)
		if w == wP:
			posterior_array.append(wP_pos)
		else:
			posterior_array.append(w_pos)

	return (values_array, posterior_array)

results1 = Metropolis(11000)
results2 = Metropolis_Prior(11000)
values1 = results1[0][1000:]
values2 = results2[0][1000:]
plt.xlabel('value of W')
plt.ylabel('frequency')
plt.title('Values of W over 10,000 Samples (after 1000 sample burn)')
plt.hist([values1, values2], 20, color = ['red', 'blue'], label = ['posterior samples', 'prior samples'])
plt.legend()
plt.show()



