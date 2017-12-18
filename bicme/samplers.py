from math import log
from random import random
import numpy as np

class Sampler(object):
    """
    Random-walk sampling algorithm with fixed jump size. 
    """
    
    def __init__(self, samples_draw=100000, notify_every=100,
                 burnin_fraction=0.5, burnin_lag=50,
                 model=None, data=None, proposal=None, verbose=False):
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
        self.data = data
        self.proposal = proposal
        self.verbose = verbose
        self.acceptance_limits = [0.1, 0.5]
        self.scale = 0.1
        self.scale_factors = []
        self.proposals = []
        self.samples = []
        self.acceptances = np.zeros(self.N)
        print('Sampler initialised...')
        
    def do_print(self, i):
        if i % self.M == 0 and self.verbose:
            print (100 * i / float(self.N), '%')

    def sample(self, theta):
        """
        theta - starting values for the parameters
        """
        S = np.zeros((len(theta) + 1, self.N))
        ll0 = self.model(theta, self.data)
        local_theta = theta.copy()
        for i in range(self.N):
            # Generate candidate state
            p = self.proposal(local_theta)
             # accept / reject new state
            if p.all() > 0:
                try:
                    llp = self.model(p, self.data)
                except:
                    llp = float('inf')
                alpha = min(1, np.exp(llp-ll0))
                if random() < alpha:
                    local_theta, ll0 = p, llp
            S[ : , i] = np.append(local_theta, ll0)
            self.do_print(i+1)
        return S
    
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
                 model=None, data=None, proposal=None, verbose=False):
        Sampler.__init__(self, samples_draw, notify_every, 
                 burnin_fraction, burnin_lag,
                 model, data, proposal, verbose)
                 
    def sample_block(self, theta):
        self.k = len(theta)
        scale_factor = 1
        L0 = self.model(theta, self.data)
        theta0 = theta.copy()
        for i in range(self.N):
            # Get proposal
            alpha, theta_p, Lp = self.proposal(theta0, L0, scale_factor, None)
            self.proposals.append(theta_p)
            # Check alpha
            if alpha == 0 or alpha > log(random()):
                self.acceptances[i] = 1
                theta0, L0 = theta_p, Lp
            self.samples.append(np.append(theta0, L0))
            self.scale_factors.append(scale_factor)
            #if (i+1) % self.lag == 0:
            if ((i+1) % self.lag == 0) and (i < self.B):
                acceptance_proportion = (np.sum(
                    self.acceptances[i - self.lag + 1 : i + 1]) / self.lag)
                scale_factor = self.tune_scale(scale_factor, acceptance_proportion, i)
            self.do_print(i+1)
        return np.array(self.samples).T
        
    def sample_component(self, theta):
        """
        Samples parameters one by one to improwe mixing.
        """
        self.k = len(theta)
        self.acceptances = np.zeros((self.k, self.N))
        self.proposals = np.zeros((self.k, self.N))
        self.samples = np.zeros((self.k, self.N))
        self.posteriors = np.zeros((self.k, self.N))
        scale_factor = np.ones(self.k)
        L0 = self.model(theta, self.data)
        theta0 = theta.copy()
        # Sampling loop
        for i in range(self.N):
            # Sample parameter one at a time
            for j in range(self.k):
                self.posteriors[j, i] = L0
                self.samples[j, i] = theta0[j]
                alpha, theta_p, Lp = self.proposal(theta0, L0, scale_factor, j)
                self.proposals[j, i] = theta_p[j] #.append(theta_p)
                if alpha == 0 or alpha > log(random()):
                    self.acceptances[j , i] = 1
                    theta0, L0 = theta_p, Lp
                    self.samples[j, i] = theta_p[j]
                    self.posteriors[j, i] = Lp
                    
                #self.samples.append(np.append(theta0, L0))
                # Tune sampler step
                self.scale_factors.append(scale_factor)
                if ((i+1) % self.lag == 0) and (i < self.B):
                    acceptance_proportion = (np.sum(
                        self.acceptances[j, i - self.lag + 1 : i + 1]) / (self.lag))
                    scale_factor[j] = self.tune_scale(scale_factor[j], acceptance_proportion, i)
            #self.samples.append(np.append(theta0, L0))
            self.do_print(i+1)  
        return self.samples, self.posteriors, self.proposals

    
class RosenthalAdaptiveSampler(Sampler):
    """
    Algorithm taken from Rosenthal 2006 technical report.
    """
    def __init__(self, samples_draw=10000, notify_every=100,
                 burnin_fraction=0.5, burnin_lag=50,
                 model=None, data=None, proposal=None, verbose=False):
        Sampler.__init__(self, samples_draw, notify_every, 
                 burnin_fraction, burnin_lag,
                 model, data, proposal, verbose)
                
    def sample_block(self, theta):
        """
        Samples parameters one by one to improwe mixing.
        """         
        self.k = len(theta)
        start_adaption = 2 * self.k
        need_mixture = False
        mass_matrix = np.identity(self.k)
        scale_factor = 1
        L0 = self.model(theta, self.data)
        theta0 = theta.copy()
        
        #self.posteriors = []
        self.proposals = np.zeros((self.N, self.k))
        self.samples = np.zeros((self.N, self.k))
        self.posteriors = np.zeros((1, self.N))
        
        #mass_matrix = np.identity(self.k) * scale_factor
        
        # Sampling loop
        for i in range(self.N):
            # Update covariance matrix
            if i+1 >= start_adaption:
                need_mixture = True
                mass_matrix = np.cov(np.array(self.samples)[ : i-1, : ].T) * scale_factor
            else:
                mass_matrix = np.identity(self.k) * scale_factor
            # Get proposal
            alpha, theta_p, Lp = self.proposal(theta0, L0, mass_matrix, need_mixture)
            self.proposals[i] = theta_p
            # Check alpha
            if alpha == 0 or alpha > log(random()):
                self.acceptances[i] = 1
                theta0, L0 = theta_p, Lp
            self.samples[i] = theta0
            self.posteriors[:, i] = L0
            self.scale_factors.append(scale_factor)
            if ((i+1) % self.lag == 0) and (i < self.B):
                acceptance_proportion = (np.sum(
                    self.acceptances[i - self.lag + 1 : i + 1]) / self.lag)
                scale_factor = self.tune_scale(scale_factor, acceptance_proportion, i)
            self.do_print(i+1)
        return self.samples.T, self.posteriors, self.proposals.T