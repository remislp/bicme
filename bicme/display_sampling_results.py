import numpy as np
import pylab as plt

def display_results(S, burnin=0, labels=None):
    """    
    """
    
    Lmax = S[-1].max()
    imax = np.where(S[-1] == S[-1].max())[0][0]
    count = 1
    r = len(S)
    for i in range(r):
        plt.subplot(r, 2, count)
        plt.plot(S[i])
        count += 1
        #plt.ylabel('n1')
        plt.subplot(r, 2, count)
        plt.hist(S[i, burnin:], bins=20)
        plt.axvline(x=S[i, imax], color='r')
        count += 1
    plt.show()

S = np.loadtxt('AChR_MCMC.csv', delimiter=',')
display_results(S, burnin=5000)


