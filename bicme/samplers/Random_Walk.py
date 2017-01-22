import random
import numpy as np

class RW_sampler(object):
    """
    Random-walk sampling algorithm with fixed jump size. 
    """
    
    def __init__(self, samplerParams=None, model=None, data=None, 
                 proposal=None, startParams=None):
        """
        Parameters
        ----------
        samplerParams - a stucture of sampling parameters
        model - contains the model specification and likelihood
        data - the data required to evaluate the model likelihood
        proposal - Proposal object contains function to use as a proposal,
        startParams - starting values for the parameters

        Returns
        -------
        samples - a structure containing the samples, acceptances etc.
        """
        pass
    
    def sample(self, y, theta, func, a, N=1000000, M=1000, verbose=False):
        """
        """

        # store every M'th sample in S
        S = np.zeros((len(theta)+1, 1+N/M))
        ll0 = func(theta, y)
        S[:,0] = np.append(theta, ll0)

        for i in range(N):
            # Generate candidate state
            p = theta + a * (2 * np.random.rand(len(theta)) - 1)
            # accept / reject new state
            if p.all() > 0:
                llp = func(p, y)
                alpha = min(1, np.exp(llp-ll0))
                if random.random() < alpha:
                    theta, ll0 = p, llp

            # every M updates draw a sample and print current values
            if i % M == 0:
                if verbose: print (100 * (M+i) / float(N), '%')
                S[ : , 1+i/M] = np.append(theta, ll0)
        return S