import numpy as np
import pylab as plt

class DisplayResults(object):
    """
    Display MCMC results. 
    """
    
    def __init__(self, samples, burnin=0, names=None):
        """
        Parameters
        ----------
        samples : array like
            All samples containing parameters and posterior function value.
        burnin : int
            Number of samples in burn-in phase.
        labels : list of strings
            Parameters' names.
        """
        
        self.S = samples
        self.M = len(self.S[0, : -1]) # number of samples
        self.k = len(self.S) # numer of parameters
        self.burnin = burnin
        self.names = names
        self.imax = np.where(self.S[-1] == self.S[-1].max())[0][0]
        self.Xmax = self.S[:, self.imax]
        self.Snorm = self.S / self.S.max(axis=0)
        
        self.normalised = False
        self.show_labels = True
        self.binsnum = 20
        
    def chains(self, ind=None):
        """ Display the parameters in a chain."""
        self.__general_figure(self.__chain, ind)
        
    def distributions(self, ind=None):
        self.__general_figure(self.__distribution, ind)
                              
    def autocorrelations(self, ind=None):
        self.__general_figure(self.__autocorrelation, ind)
                              
    def correlations(self, ind, jnd):
        fig = plt.figure(figsize = (4,3))
        ax = fig.add_subplot(1, 1, 1)
        self.__correlation(ax, ind, jnd)
        plt.show()
        
    def corner(self):
        self.show_labels = False
        fig = plt.figure(figsize = (10,10))
        for i in range(self.k):
            for j in range(i+1):
                if j == i:
                    ax = fig.add_subplot(self.k, self.k, self.k*i+j+1)
                    self.__distribution(ax, j)
                    ax.tick_params(labelbottom='off')
                    ax.tick_params(labelleft='off')
                    if j == 0:
                        ax.set_ylabel(self.names[i])
                    if i == self.k-1:
                        ax.set_xlabel(self.names[j])
                else:
                    ax = fig.add_subplot(self.k, self.k, self.k*i+j+1)
                    self.__correlation(ax, j, i)
                    ax.tick_params(labelbottom='off')
                    ax.tick_params(labelleft='off')
                    if j == 0:
                        ax.set_ylabel(self.names[i])
                    if i == self.k-1:
                        ax.set_xlabel(self.names[j])
            
        plt.show()
                    
            
    def __general_figure(self, plot_type, ind):
        """  Displays a selected parameter indicated by ind or, if ind=None,
        displays chains of all parameters and the posterior function value.
        """
        fig = plt.figure(figsize = (8,10))
        if ind is None:
            for i in range(self.k):
                ax = fig.add_subplot(self.k, 1, i+1)
                plot_type(ax, i)
        else:
            ax = fig.add_subplot(1, 1, 1)
            plot_type(ax, ind)
        plt.show()
        
    def __distribution(self, ax, ind):
        if self.normalised:
            ax.hist(self.S[ind, self.burnin:] / self.Xmax[ind], bins=self.binsnum)
            ax.axvline(x=1, color='r')
        else:
            ax.hist(self.S[ind, self.burnin:], bins=self.binsnum)
            ax.axvline(x=self.Xmax[ind], color='r')
        if self.show_labels:
            ax.set_xlabel(self.names[ind])
            #ax.set_ylabel()
        
    def __chain(self, ax, ind):
        if self.normalised:
            ax.plot(self.S[ind] / self.Xmax[ind])
            ax.axhline(y=1, color='r')
        else:
            ax.plot(self.S[ind])
            ax.axhline(y=self.Xmax[ind], color='r')
        if self.show_labels:
            ax.set_xlabel('Step number')
            ax.set_ylabel(self.names[ind])
            
    def __calculate_autocorrelation(self, X):
        X = X - np.mean(X)
        acf = np.correlate(X, X, mode='full')
        return acf[int(acf.size/2) : ] / acf[int(acf.size / 2)]
            
    def __autocorrelation(self, ax, ind):
        ax.plot(self.__calculate_autocorrelation(self.S[ind, self.burnin:]))
        ax.set_ylim(-1, 1)
        ax.axhline(y=0, color='k')
        #ax.set_xlim(0, 400)
        if self.show_labels:
            ax.set_xlabel('Lag')
            ax.set_ylabel('Autocorrelation')
        ax.set_title(self.names[ind])
    
    def __correlation(self, ax, ind, jnd):
        ax.plot(self.S[ind, self.burnin:], self.S[jnd, self.burnin:], '.')
        ax.axvline(x=self.Xmax[ind], color='r')
        ax.axhline(y=self.Xmax[jnd], color='r')
        if self.show_labels:
            ax.set_xlabel(self.names[ind])
            ax.set_ylabel(self.names[jnd])


def quick_display(S, burnin=0, labels=None):
    """    
    """
    
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