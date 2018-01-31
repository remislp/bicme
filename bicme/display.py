#!/usr/bin/python

import numpy as np
import pylab as plt

import bicme.helpers

class DisplayResults(object):
    """
    Display MCMC results. 
    """
    
    def __init__(self, chain, burnin=0, names=None):
        """
        Parameters
        ----------
        chain : Chain type instance
            Object containing all MCMC samples, proposals, posteriors, etc.
        burnin : int
            Number of samples in burn-in phase.
        names : list of strings
            Parameters' names.
        """
        
        self.S = chain
        #self.M = len(self.S[0, : -1]) # number of samples
        #self.k = len(self.S) # numer of parameters
        self.burnin = burnin
        self.names = names
        #self.imax = np.where(self.S.posteriors == self.S.posteriors.max())[0][0]
        #self.Xmax = self.S.samples[:, self.imax]
        self.Snorm = self.S.samples / self.S.samples.max(axis=0)
        
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
        fig = plt.figure(figsize = (self.S.k*2,self.S.k*2))
        for i in range(self.S.k):
            for j in range(i+1):
                if j == i:
                    ax = fig.add_subplot(self.S.k, self.S.k, self.S.k*i+j+1)
                    self.__distribution(ax, j)
                    ax.tick_params(labelbottom='off')
                    ax.tick_params(labelleft='off')
                    if j == 0:
                        ax.set_ylabel(self.names[i])
                    if i == self.S.k-1:
                        ax.set_xlabel(self.names[j])
                else:
                    ax = fig.add_subplot(self.S.k, self.S.k, self.S.k*i+j+1)
                    self.__correlation(ax, j, i)
                    ax.tick_params(labelbottom='off')
                    ax.tick_params(labelleft='off')
                    if j == 0:
                        ax.set_ylabel(self.names[i])
                    if i == self.S.k-1:
                        ax.set_xlabel(self.names[j])
        plt.show()
                    
            
    def __general_figure(self, plot_type, ind):
        """  Displays a selected parameter indicated by ind or, if ind=None,
        displays chains of all parameters and the posterior function value.
        """
        fig = plt.figure(figsize = (6,self.S.k*3))
        if ind is None:
            for i in range(self.S.k):
                ax = fig.add_subplot(self.S.k, 1, i+1)
                plot_type(ax, i)
        else:
            ax = fig.add_subplot(1, 1, 1)
            plot_type(ax, ind)
        plt.show()
        
    def __distribution(self, ax, ind):
        if self.normalised:
            ax.hist(self.S.samples[ind, self.burnin:] / self.S.MEP_samples[ind], bins=self.binsnum)
            ax.axvline(x=1, color='r')
        else:
            ax.hist(self.S.samples[ind, self.burnin:], bins=self.binsnum)
            ax.axvline(x=self.S.MEP_samples[ind], color='r')
        if self.show_labels:
            ax.set_xlabel(self.names[ind])
            #ax.set_ylabel()
        
    def __chain(self, ax, ind):
        if self.normalised:
            ax.plot(self.S.samples[ind] / self.S.MEP_samples[ind])
            ax.axhline(y=1, color='r')
        else:
            ax.plot(self.S.samples[ind])
            ax.axhline(y=self.S.MEP_samples[ind], color='r')
        if self.show_labels:
            ax.set_xlabel('Step number')
            ax.set_ylabel(self.names[ind])
            
    def __autocorrelation(self, ax, ind, xlims=(0,100)):
        ax.plot(bicme.helpers.calculate_autocorrelation(self.S.samples[ind, self.burnin:]))
        ax.set_ylim(-1, 1)
        ax.axhline(y=0, color='k')
        ax.set_xlim(xlims)
        if self.show_labels:
            ax.set_xlabel('Lag')
            ax.set_ylabel('Autocorrelation')
        ax.set_title(self.names[ind])
    
    def __correlation(self, ax, ind, jnd):
        ax.plot(self.S.proposals[ind, self.burnin:], self.S.samples[jnd, self.burnin:], 'b.')
        ax.plot(self.S.samples[ind, self.burnin:], self.S.samples[jnd, self.burnin:], 'r.')
        ax.axvline(x=self.S.MEP_samples[ind], color='r')
        ax.axhline(y=self.S.MEP_samples[jnd], color='r')
        if self.show_labels:
            ax.set_xlabel(self.names[ind])
            ax.set_ylabel(self.names[jnd])


def quick_display(S, burnin=0):
    """    
    """
    imax = S.MEP_index
    fig = plt.figure(figsize = (8,S.k*3))
    for i in range(S.k):
        ax1 = fig.add_subplot(S.k, 2, 2*i+1)
        ax1.plot(S.samples[i])
        #ax1.set_title(names[i])
        ax1.set_xlabel('Iteration')
        ax2 = fig.add_subplot(S.k, 2, 2*i+2)
        ax2.hist(S.samples[i, burnin:], bins=20)
        ax2.axvline(x=S.samples[i, imax], color='r')
    plt.show()
