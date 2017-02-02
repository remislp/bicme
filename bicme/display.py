import numpy as np
import pylab as plt

def quick_display(S, burnin=0, labels=None):
    """    
    """
    
    Lmax = S[-1].max()
    print ('Lmax=', Lmax)
    imax = np.where(S[-1] == S[-1].max())[0][0]
    print('pars=', S[:, imax])
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

