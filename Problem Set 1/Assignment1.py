import matplotlib.pyplot as plt
import numpy as np

#1
x = np.arange(0., 5., 0.0001)
y = np.sin(2 ** x)
plt.xlabel('x')
plt.ylabel('sin(2^x)')
plt.plot(x, y)
plt.show()

#2
x = np.arange(0., 5., 0.0001)
y = np.sin(2 ** x)
p = np.sin(2 ** (x + 0.1))
s = y/p
plt.xlabel('x')
plt.ylabel('sin(2^x)/sin(2^(x + 0.1))')
plt.ylim(-20, 20)
plt.plot(x, s)
plt.show()

#3a
def f(x):
	return (1/(x + 1))

def summation(x):
	if x == 1:
		return f(1)
	else:
		return f(x) + summation(x - 1)

#3b
x = np.arange(1, 100, 0.001)
y = [summation(i) for i in x.astype(int)]
plt.xlabel('x')
plt.ylabel('summation')
plt.plot(x, y)
plt.show()

#4
samples = np.random.normal(0, 1, 10000)
data = np.sin(samples)
plt.hist(data, bins = 20)
plt.xlabel('x')
plt.ylabel('sin(x)')
plt.show()

#5
samples = np.random.uniform(0, 1.5, 10000)
data = np.exp(samples)
plt.hist(data, bins = 20)
plt.xlabel('x')
plt.ylabel('exp(x)')
plt.show()

#6a
samples = np.random.normal(0, 1, 1000)
samples = np.sort(samples)
data = [(samples[x] - samples[x - 1]) for x in range(1, len(samples))]
plt.hist(data, bins = 15)
plt.xlabel('x')
plt.ylabel('difference')
plt.show()

#6b
x = np.arange(1, 1000, 1)
plt.plot(x, data)
plt.xlabel('position')
plt.ylabel('difference')
plt.show()


