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

def quick_display1(S, burnin, names):
    imax = np.where(S[-1] == S[-1].max())[0][0]
    Xmax = S[:, imax]
    count = 1
    r = len(S)
    fig = plt.figure(figsize = (10,20))
    for i in range(r):
        ax1 = fig.add_subplot(r, 2, count)
        ax1.plot(S[i])
        ax1.set_title(names[i])
        #ax1.set_xlabel('Iteration')
    
        count += 1
        ax2 = fig.add_subplot(r, 2, count)
        ax2.hist(S[i, burnin:], bins=20)
        ax2.axvline(x=Xmax[i], color='r')
        count += 1