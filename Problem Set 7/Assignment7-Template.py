import os
import numpy 
import matplotlib.pyplot as plt

# Functions that might be useful (please read the documentation)
# x.flatten() (take a N-dimensional numpy array and make it one-dimensional)
# numpy.random.choice -- choose from the list of images
# numpy.dot -- compute the dot product
# numpy.random.normal -- set up random initial weights

DIM = (28,28) #these are the dimensions of the image

def load_image_files(n, path="images/"):
    # helper file to help load the images
    # returns a list of numpy vectors
    images = []
    for f in os.listdir(os.path.join(path,str(n))): # read files in the path
        p = os.path.join(path,str(n),f)
        if os.path.isfile(p):
            i = numpy.loadtxt(p)
            assert i.shape == DIM # just check the dimensions here
            # i is loaded as a matrix, but we are going to flatten it into a single vector
            images.append(i.flatten())
    return images
            

# Load up these image files
#A = load_image_files(0)
#B = load_image_files(1)

#N = len(A[0]) # the total size
#assert N == DIM[0]*DIM[1] # just check our sizes to be sure

## Your code here:

#1
def Perceptron(d1, d2, big_list, weights):
    
    # we will keep track of how many the perceptron gets correct, and
    # also record our accuracy level every 25 images
    correct = 0
    accuracy_values = []


    for i in range(0, len(big_list)):
        
        # if our accuracy level has crossed 99%, break out
        if (i > 25) and (correct / i) > 0.99:
            stop = i
            break

        image = big_list[i]
        s = numpy.dot(image[0], weights) # dot the inputs with the weights
        compare = image[1]
        
        # y is the result of our step function
        y = 0
        if s < 0:
            y = 0
        else:
            y = 1
        
        # fix the weights depending on if y matches compare (the real digit)
        # add 1 to correct if it got it right
        if (y == 0) and (compare == 1):
            w = numpy.array(weights)
            x = numpy.array(image[0])
            weights = w + x
        elif (y == 1) and (compare == 0):
            w = numpy.array(weights)
            x = numpy.array(image[0])
            weights = w - x
        else:
            correct += 1

        # if we are on a 25th trial, record the accuracy level
        if (i != 0) and ((i + 1) % 25 == 0):
            accuracy_values.append(correct / i)

    # plot the accuracy level per 25 images
    x = numpy.arange(1, len(accuracy_values) + 1)
    x = [i * 25 for i in x]
    plt.xlabel("trial")
    plt.ylabel("accuracy")
    plt.title("accuracy with trials")
    plt.plot(x, accuracy_values)
    plt.show()
    return (weights, stop)

def runPerceptron(d1, d2):
    # get images for d1 and d2, and create lists of tuples that group each image
    # with the digit it is representing
    A = load_image_files(d1)
    A_list = [(x, d1) for x in A]
    B = load_image_files(d2)
    B_list = [(x, d2) for x in B]
    big_list = A_list + B_list

    # shuffle the list
    numpy.random.shuffle(big_list)

    # set up some random initial weights
    weights = numpy.random.normal(0,1,size=len(A[0]))
    
    return Perceptron(d1, d2, big_list, weights)
#3
#new_weights = runPerceptron(0, 1)[0]
#new_weights = numpy.reshape(new_weights, (28, 28))
#plt.matshow(new_weights)
#plt.show()

#4

def runPerceptronAdjust(d1, d2):

    # get images for d1 and d2, and create lists of tuples that group each image
    # with the digit it is representing
    A = load_image_files(d1)
    A_list = [(x, d1) for x in A]
    B = load_image_files(d2)
    B_list = [(x, d2) for x in B]
    big_list = A_list + B_list

    # shuffle the list
    numpy.random.shuffle(big_list)

    # set up some random initial weights
    weights = numpy.random.normal(0,1,size=len(A[0]))

    run = Perceptron(d1, d2, big_list, weights)
    # derive our adjusted weights and image index where we stopped our perceptron
    new_weights = run[0]
    index = run[1]
    trials = big_list[index : index + 1000]

    # creating some reference lists to help us change weights to 0
    weights_ref = []
    for i in range(0, len(new_weights)):
        weights_ref.append((abs(new_weights[i]), i))
    weights_ref = sorted(weights_ref, key = lambda x : x[0])[:780]

    # the y values for our plot
    accuracy_values = []

    for i in range(0, 78):
        
        # getting to values to set to 0 and removing them from reference
        weights_change = weights_ref[:10]
        weights_ref = weights_ref[10:]

        # changing the values in our actual weights
        for j in range(0, 10):
            change_index = weights_change[j][1]
            new_weights[change_index] = 0

        # test these weights over our 1000 new trials
        correct = 0
        for trial in trials:
            compare = trial[1]
            image = trial[0]
            dot = numpy.dot(image, new_weights)
            # y is the result of our step function
            y = 0
            if dot < 0:
                y = 0
            else:
                y = 1
            # see if our perceptron guessed correctly
            if (y == compare):
                correct += 1
        # record the accuracy
        accuracy_values.append(correct / 1000)

    x = numpy.arange(1, len(accuracy_values) + 1)
    x = [i * 10 for i in x]
    plt.xlabel("number of weights set to 0")
    plt.ylabel("accuracy")
    plt.title("accuracy as more weights are set to 0")
    plt.plot(x, accuracy_values)
    plt.show()

#runPerceptronAdjust(0, 1)

#5

def PerceptronAccuracy(d1, d2, big_list, weights):

    # like our previous perceptron, but it returns the accuracy after 2500 trials

    # we will keep track of how many the perceptron gets correct
    correct = 0

    for i in range(0, 2500):

        image = big_list[i]
        s = numpy.dot(image[0], weights) # dot the inputs with the weights
        compare = image[1]
        
        # y is the result of our step function
        y = 0
        if s < 0:
            y = 0
        else:
            y = 1
        
        # fix the weights depending on if y matches compare (the real digit)
        # add 1 to correct if it got it right
        if (y == 0) and (compare == d2):
            w = numpy.array(weights)
            x = numpy.array(image[0])
            weights = w + x
        elif (y == 1) and (compare == d1):
            w = numpy.array(weights)
            x = numpy.array(image[0])
            weights = w - x
        else:
            correct += 1

    return correct / 2500 # accuracy after 2500 training trials

def CompareAllDigs():

    # get images for all our digits, and create lists of tuples that group each image
    # with the digit it is representing
    all_images = {}
    for i in range(0, 10):
        images = load_image_files(i)
        all_images[i] = [(x, i) for x in images]
    
    # initalize our main matrix which will be 10x10
    big_matrix = []

    # find the accuracy between all pairs of digits
    for i in range(0, 10):
        i_compares = [] # the accuacies between our current i and all other digits
        for j in range(0, 10):
            if i == j:
                i_compares.append(1.0)
            else:
                # getting all our images
                big_list = all_images[i] + all_images[j]
                numpy.random.shuffle(big_list)
                weights = numpy.random.normal(0,1,size=len(big_list[0][0]))
                i_compares.append(PerceptronAccuracy(i, j, big_list, weights))
        # adding our list of 10 accuracies to our main matrix
        print(i, i_compares)
        big_matrix.append(i_compares)
    
    # showing the results
    plt.matshow(big_matrix)
    plt.show()

CompareAllDigs()






        









