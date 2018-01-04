from math import log
import numpy as np


class Chain(object):
    """Data structure to save MCMC sampling result."""
    def __init__(self, k, N, sample_type='block'):
        self.k = k
        self.N = N
        self.stype = sample_type
        self.proposals = np.zeros((k, N))
        self.samples = np.zeros((k, N))
        if self.stype == 'block':
            self.acceptances = np.zeros(N)
            self.posteriors = np.zeros(N)
            self.scale_factors = np.zeros(N)
        elif self.stype == 'component':
            self.acceptances = np.zeros((k, N))
            self.posteriors = np.zeros((k, N))
            self.scale_factors = np.zeros((k, N))
            
    def insert_sample_block(self, i, thetaP, theta0, L0, scale, acceptance):
        self.proposals[:, i] = thetaP
        self.scale_factors[i] = scale
        self.samples[:, i] = theta0
        self.posteriors[i] = L0
        self.acceptances[i] = acceptance

    def insert_sample_component(self, i, j, 
                                thetaP, theta0, L0, scale, acceptance):
        self.proposals[j, i] = thetaP
        self.scale_factors[j, i] = scale
        self.samples[j, i] = theta0
        self.posteriors[j, i] = L0
        self.acceptances[j, i] = acceptance
        
    def _set_MEP_index(self):
        self._MEP_index = self._get_MEP_index()
    def _get_MEP_index(self):
        return np.where(self.posteriors == self.posteriors.max())[-1][0]
    MEP_index = property(_get_MEP_index, _set_MEP_index)
    
    def _set_MEP(self):
        self._MEP = self._get_MEP()
    def _get_MEP(self):
        """
        Maximal estimated posterior.
        """
        if self.stype == 'component':
            return self.posteriors[-1, self.MEP_index]
        elif self.stype == 'block':
            return self.posteriors[self.MEP_index]
    MEP = property(_get_MEP, _set_MEP)

    def _set_MEP_samples(self):
        self._MEP_samples = self._get_MEP_samples()
    def _get_MEP_samples(self):
        return self.samples[ : , self.MEP_index]
    MEP_samples = property(_get_MEP_samples, _set_MEP_samples)


class Sampler(object):
    """
    Random-walk sampling algorithm with fixed jump size. 
    """
    
    def __init__(self, samples_draw=100000, notify_every=100,
                 burnin_fraction=0.5, burnin_lag=50,
                 model=None, proposal=None, verbose=False):
        """
        Parameters
        ----------
        samples_draw : int
            A total number of samples to draw.
        notify_every : int
            If verbose, display intermediate information every n'th sample.
        burnin_fraction : float
        burnin_lag : int
        model : obj
            Container for the model specifications and likelihood.
        data : 
            The data required to evaluate the model likelihood.
        proposal : function
            Function to propose parameters.
        
        Returns
        -------
        samples - a structure containing the samples, acceptances etc.
        """
        self.N = samples_draw
        self.M = notify_every
        self.B = int(samples_draw * burnin_fraction)
        self.lag = burnin_lag
        self.model = model
        self.proposal = proposal
        self.verbose = verbose
        self.acceptance_limits = [0.1, 0.5]
        self.scale = 0.1
        print('Sampler initialised...')
        
    def do_print(self, i):
        if i % self.M == 0 and self.verbose:
            print (100 * i / float(self.N), '%')
            
    def sample(self, theta):
        """
        theta - starting values for the parameters
        """
        chain = Chain(len(theta), self.N)
        L0 = self.model(theta) #, self.data)
        theta0 = theta.copy()
        for i in range(self.N):
            is_accepted = 0
            # Generate candidate state
            thetaP = self.proposal(theta0)
             # accept / reject new state
            if thetaP.all() > 0:
                try:
                    Lp = self.model(thetaP) #, self.data)
                except:
                    Lp = float('inf')
                alpha = min(1, np.exp(Lp-L0))
                if np.random.rand() < alpha:
                    theta0, L0 = thetaP, Lp
                    is_accepted = 1
            
            chain.insert_sample(i, thetaP, theta0, L0, 1, is_accepted)
            self.do_print(i+1)
        return chain
    
    def tune_scale(self, scale_factor, acceptance_proportion, i):
        message = 'not changed'
        if acceptance_proportion < self.acceptance_limits[0]:
            scale_factor *= 1 - self.scale
            message = 'decreased'
        elif acceptance_proportion > self.acceptance_limits[1]:
            scale_factor *= 1 + self.scale
            message = 'increased'
        print("Iteration {0:d}; Acceptance: {1:.6f}; Scale factor {2:.6f}: {3}".
                format(i+1, acceptance_proportion, scale_factor, message))
        return scale_factor

class MWGSampler(Sampler):
    """
    Multiplicative Metropolis_within_Gibbs sampler with scaling during burn-in.
    """
    def __init__(self, samples_draw=10000, notify_every=100,
                 burnin_fraction=0.5, burnin_lag=50,
                 model=None, proposal=None, verbose=False):
        Sampler.__init__(self, samples_draw, notify_every, 
                 burnin_fraction, burnin_lag,
                 model, proposal, verbose)
                 
    def sample_block(self, theta):
        self.k = len(theta)
        chain = Chain(self.k, self.N, 'block')
        scale_factor = 1
        L0 = self.model(theta)
        theta0 = theta.copy()
        for i in range(self.N):
            is_accepted = 0
            # Get proposal and check alpha
            alpha, thetaP, Lp = self.proposal(theta0, L0, scale_factor, None)
            if alpha == 0 or alpha > log(np.random.rand()):
                is_accepted = 1
                theta0, L0 = thetaP, Lp
            chain.insert_sample_block(i, 
                thetaP, theta0, L0, scale_factor, is_accepted)
            # Tune sampler step
            if ((i+1) % self.lag == 0) and (i < self.B):
                acceptance_proportion = (np.sum(
                    chain.acceptances[i - self.lag + 1 : i + 1]) / self.lag)
                scale_factor = self.tune_scale(scale_factor, acceptance_proportion, i)
            self.do_print(i+1)
        return chain
        
    def sample_component(self, theta):
        """
        Samples parameters one by one to improwe mixing.
        """
        self.k = len(theta)
        chain = Chain(self.k, self.N, 'component')
        scale_factor = np.ones(self.k)
        L0 = self.model(theta)
        theta0 = theta.copy()
        # Sampling loop
        for i in range(self.N):
            # Sample parameter one at a time
            for j in range(self.k):
                is_accepted = 0
                alpha, thetaP, Lp = self.proposal(theta0, L0, scale_factor, j)
                if alpha == 0 or alpha > log(np.random.rand()):
                    is_accepted = 1
                    theta0, L0 = thetaP, Lp
                chain.insert_sample_component(i, j, 
                    thetaP[j], theta0[j], L0, scale_factor[j], is_accepted)
                # Tune sampler step
                if ((i+1) % self.lag == 0) and (i < self.B):
                    acceptance_proportion = (np.sum(
                        chain.acceptances[j, i - self.lag + 1 : i + 1]) / (self.lag))
                    scale_factor[j] = self.tune_scale(scale_factor[j], acceptance_proportion, i)
            self.do_print(i+1)  
        return chain

    
class RosenthalAdaptiveSampler(Sampler):
    """
    Algorithm taken from Rosenthal 2006 technical report.
    """
    def __init__(self, samples_draw=10000, notify_every=100,
                 burnin_fraction=0.5, burnin_lag=50,
                 model=None, proposal=None, verbose=False):
        Sampler.__init__(self, samples_draw, notify_every, 
                 burnin_fraction, burnin_lag,
                 model, proposal, verbose)
                
    def sample_block(self, theta):
        """
        Samples parameters one by one to improwe mixing.
        """         
        self.k = len(theta)
        chain = Chain(self.k, self.N, 'block')
        start_adaption = 2 * self.k
        need_mixture = False
        mass_matrix = np.identity(self.k)
        scale_factor = 1
        L0 = self.model(theta) #, self.data)
        theta0 = theta.copy()
               
        #mass_matrix = np.identity(self.k) * scale_factor
        
        # Sampling loop
        for i in range(self.N):
            is_accepted = 0
            # Update covariance matrix
            if i+1 >= start_adaption:
                need_mixture = True
                mass_matrix = np.cov(np.array(chain.samples[ : i, : ])) * scale_factor
            else:
                mass_matrix = np.identity(self.k) * scale_factor
            # Get proposal
            alpha, thetaP, Lp = self.proposal(theta0, L0, mass_matrix, need_mixture)
            # Check alpha
            if alpha == 0 or alpha > log(np.random.rand()):
                is_accepted = 1
                theta0, L0 = thetaP, Lp
            chain.insert_sample_block(i, 
                thetaP, theta0, L0, scale_factor, is_accepted)
            
            if ((i+1) % self.lag == 0) and (i < self.B):
                acceptance_proportion = (np.sum(
                    chain.acceptances[i - self.lag + 1 : i + 1]) / self.lag)
                scale_factor = self.tune_scale(scale_factor, acceptance_proportion, i)
            self.do_print(i+1)
        return chain