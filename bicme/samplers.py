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
        print('Sampler initialised...')
    
    def sample(self, theta):
        """
        theta - starting values for the parameters
        """

        S = np.zeros((len(theta) + 1, self.N))
        ll0 = self.model(theta, *self.data)
        local_theta = theta.copy()
        
        for i in range(self.N):
            # Generate candidate state
            p = self.proposal(local_theta)
             # accept / reject new state
            if p.all() > 0:
                try:
                    llp = self.model(p, *self.data)
                except:
                    llp = inf
                alpha = min(1, np.exp(llp-ll0))
                if random.random() < alpha:
                    local_theta, ll0 = p, llp
                    
            # every M print job progress in percentage
            if self.verbose and i % self.M == 0:
                if self.verbose: print (100 * (self.M + i) / float(self.N), '%')
            # store sample
            S[ : , i] = np.append(np.exp(local_theta), ll0)
        return S

class MWGSampler(Sampler):
    """
    Multiplicative Metropolis_within_Gibbs sampler with scaling during burn-in.
    """
    def __init__(self, samples_draw=100000, notify_every=100,
                 model=None, data=None, proposal=None, verbose=False):
        Sampler.__init__(self, samples_draw, notify_every,
                         model, data, proposal, verbose)
                         
    def cw_sample(self):
        """
        Samples parameters one by one to improwe mixing.
        """
        pass