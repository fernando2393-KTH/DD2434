import pylab as pb
import numpy as np
import scipy as sp
import math
import scipy.optimize as opt
import matplotlib.pyplot as plt

# This function returns the likelihood
def likelihood(W):

    W_l = np.reshape(W, (10,2))
    C = calculateC(W_l, sigma)

    result = np.trace(np.dot(np.linalg.inv(C), S))
    result = math.log(np.linalg.det(C)) + result
    result = Y.shape[1] * math.log(2*math.pi) +  result

    return (Y.shape[0]/2) * result

# This function returns the C necessary for the derivative
def calculateC(W, sigma):
    return np.dot(W,np.transpose(W)) + sigma * np.identity(len(W))

# This function returns the S necessary for the derivative
def calculateS(Y):

    S = np.zeros(shape=(len(Y[1]), len(Y[1])))
    mean = np.mean(Y, axis=0)

    for i in range(Y.shape[0]):
        S = S + np.dot((Y[i] - mean), np.transpose(Y[i] - mean))

    return S/(Y.shape[0])

# This function calculates the derivative
def calculateDerivative(W):

    W_d = np.reshape(W, (10,2))
    C_der = calculateC(W_d, sigma)

    result = np.dot(np.dot(np.dot(np.linalg.inv(C_der), S), np.linalg.inv(C_der)), W_d)
    result = np.subtract(result,np.dot(np.linalg.inv(C_der), W_d))
    result = Y.shape[0] * result

    return result.reshape(-1)

# This function generates the non-linear distribution
def genNonLinear(x):

    result = np.zeros(shape=(len(x),2))

    for i in range(x.shape[0]):
        result[i] = [math.sin(x[i]) - x[i] * math.cos(x[i]), math.cos(x[i]) + x[i] * math.sin(x[i])]
    
    return result

# This function generates the linear distribution
def genLinear(val, A):
    return np.dot(val,np.transpose(A))

# This function generates the A matrix
def genA():
    A = np.zeros(shape=(10,2))
    
    for i in range(10):
        for j in range(2):
            A[i][j] = np.random.normal(0, 1)

    return A

x = np.arange(0,4*math.pi,(4*math.pi)/100)
A = genA()

val = genNonLinear(x)
val = np.transpose(val)
plt.plot(val[0],val[1], 'o')

val = np.transpose(val)
Y = genLinear(val, A)

W = np.random.rand(10,2)
sigma = 1
S = calculateS(Y)

opt_w = opt.fmin_cg(likelihood, W, fprime=calculateDerivative)

opt_w = opt_w.reshape(10,2)

M = calculateC(opt_w, sigma)
finalres = np.dot(np.linalg.inv(M), opt_w)

finalmean = np.subtract(Y,np.mean(Y, axis=0))
finalres = np.dot(np.transpose(finalres), np.transpose(finalmean))

plt.plot(finalres[0], finalres[1], 'o')
plt.show()

