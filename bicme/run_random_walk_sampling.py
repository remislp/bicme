from math import pow
from scipy.special import gammaln
import numpy as np
import pylab as plt

def popln(n1, r, b, T):
    
    """
    Calculate blowfly population size at each time moment. 

    Parameters
    ----------
    n1 : integer
        Initial population size.
    r : float
        r ~ 1
    b : float
        b ~ 1/n
    T : integer
        Time (t = 1,2,...T)
    
    Returns
    -------
    n : vector of floats
        Population size at generation t.
    """
    n = np.zeros(T)
    n[0] = n1
    for i in range(1, T):
        n[i] = r * n[i-1] / (1 + pow((b * n[i-1]), 4))
    return n
	
def LogLkd(vec, y):
    """
    Calculate logarithm of probability to count y flies given that there were
    in fact n.
    
    Parameters
    ----------
    n1 : integer
        Initial population size.
    r : float
        r ~ 1
    b : float
        b ~ 1/n
    y : vector
        Observed size of generations.
    
    Returns
    -------
    llik : float
        Log likelihood.
    """
    n1, r, b = vec[0], vec[1], vec[2]
    T = len(y)
    n = popln(n1, r, b, T)
    llik = np.sum(y * np.log(n) - n - gammaln(y + 1))
    return llik

def proposal_func(theta):
    # MCMC proposed jump in parameters
    scale = np.array([10, 0.1, 0.0001])
    return theta + scale * (2 * np.random.rand(len(theta)) - 1)

def display_results(S, burnin=0, labels=None):
    """
    
    """
    r = len(S)
    count = 1
    for i in range(r):
        plt.subplot(r, 2, count)
        plt.plot(S[i])
        count += 1
        #plt.ylabel('n1')
        plt.subplot(r, 2, count)
        plt.hist(S[i, burnin:])
        count += 1
    plt.show()

# Data.
y = np.array([1225, 825, 4752, 774, 3547, 1549])

# X0- initial guesses (starting parameters)
X0 = np.array([y[0], 2, 0.0005])


# Sampler parameters
N, M = 100000, 1000
from samplers import Sampler
rw_sampler = Sampler(samples_draw=N, notify_every=M, 
                     model=LogLkd, data=y, proposal=proposal_func, 
                     verbose=True)
S, X, last_func_val = rw_sampler.sample(X0)
display_results(S, burnin=10000)


