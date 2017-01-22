import random
import numpy as np

class Sampler(object):
    """
    Random-walk sampling algorithm with fixed jump size. 
    """
    
    def __init__(self, samples_draw=100000, notify_every=100,
                 model=None, data=None, proposal=None, verbose=False):
        """
        Parameters
        ----------
        samples_draw : int
            A total number of samples to draw.
        notify_every : int
            If verbose, display intermediate information every n'th sample.
        model : obj
            Container for the model specifications and likelihood.
        data : 
            The data required to evaluate the model likelihood.
        proposal : obj
            Proposal object contains function to use as a proposal.
        

        Returns
        -------
        samples - a structure containing the samples, acceptances etc.
        """
        self.N = samples_draw
        self.M = notify_every
        self.model = model
        self.data = data
        self.proposal = proposal
        self.verbose = verbose
    
    def sample(self, theta):
        """
        theta - starting values for the parameters
        """

        # store every M'th sample in S
        #S = np.zeros((len(theta) + 1, 1 + self.N / self.M))
        # store every sample
        S = np.zeros((len(theta) + 1, self.N))
        ll0 = self.model(theta, self.data)
        #S[:,0] = np.append(theta, ll0)
        local_theta = theta.copy()
        
        for i in range(self.N):
            # Generate candidate state
            p = self.proposal(local_theta)
            #p = local_theta + a * (2 * np.random.rand(len(local_theta)) - 1)
            # accept / reject new state
            if p.all() > 0:
                llp = self.model(p, self.data)
                alpha = min(1, np.exp(llp-ll0))
                if random.random() < alpha:
                    local_theta, ll0 = p, llp

            # every M print job progress in percentage
            if self.verbose and i % self.M == 0:
                if self.verbose: print (100 * (self.M + i) / float(self.N), '%')
            
            # store sample
            S[ : , i] = np.append(local_theta, ll0)
        return S, local_theta, ll0

