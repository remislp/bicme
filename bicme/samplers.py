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
        if (i + 1) % self.M == 0 and self.verbose:
            print (100 * (i + 1) / float(self.N), '%')

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
            self.do_print(i)
        return S
    
    def tune_scale(self, scale_factor, acceptance_proportion, i):
        if i < self.B and i >= self.lag:
            if i % self.lag == 0:
                if acceptance_proportion < self.acceptance_limits[0]:
                    scale_factor *= 1 - self.scale
                    print("Acceptance: {0:.9f}; Scale factor decreased to".
                        format(acceptance_proportion) +
                        " {0:.9f} at iteration {1:d}".
                        format(scale_factor, i))
                elif acceptance_proportion > self.acceptance_limits[1]:
                    scale_factor *= 1 + self.scale
                    print("Acceptance: {0:.9f}; Scale factor increased to".
                        format(acceptance_proportion) +
                        " {0:.9f} at iteration {1:d}".
                        format(scale_factor, i))
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
            if i % self.lag == 0:
                acceptance_proportion = (np.sum(
                    self.acceptances[(i-self.lag-1) : ]) / self.lag)
            scale_factor = self.tune_scale(scale_factor, acceptance_proportion, i)
            self.do_print(i)
        return np.array(self.samples).T
        
    def sample_component(self, theta):
        """
        Samples parameters one by one to improwe mixing.
        """
        self.k = len(theta)
        self.acceptances = np.zeros(self.N * self.k)
        scale_factor = np.ones(self.k)
        L0 = self.model(theta, self.data)
        theta0 = theta.copy()
        # Sampling loop
        for i in range(self.N):
            # Sample parameter one at a time
            for j in range(self.k):
                alpha, theta_p, Lp = self.proposal(theta0, L0, scale_factor, j)
                self.proposals.append(theta_p)
                if alpha == 0 or alpha > log(random()):
                    self.acceptances[i * self.k + j] = 1
                    theta0, L0 = theta_p, Lp
                self.samples.append(np.append(theta0, L0))
                # Tune sampler step
                self.scale_factors.append(scale_factor)
                if i % self.lag == 0:
                    acceptance_proportion = (np.sum(
                        self.acceptances[((i*self.k)-self.lag-1) : ]) / self.lag)
                scale_factor[j] = self.tune_scale(scale_factor[j], acceptance_proportion, i)
            self.do_print(i)  
        return np.array(self.samples).T

    
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
        
    def sample_component(self, theta):
        """
        Samples parameters one by one to improwe mixing.
        """
        self.k = len(theta)
        self.required_samples = np.zeros((self.N, self.k+1))
        self.acceptances = np.zeros(self.N * self.k)
        start_adaption = 2 * self.k
        need_mixture = False
        covariance_matrix = np.identity(self.k)
        mass_matrix = covariance_matrix.copy()
        mass_matrix_L = covariance_matrix.copy()
        scale_factor = np.ones(self.k)
        L0 = self.model(theta, self.data)
        theta0 = theta.copy()
        # Sampling loop
        for i in range(self.N):
            # Update covariance matrix
            if i > start_adaption:
                need_mixture = True
                mass_matrix = covariance_matrix * scale_factor
                L = np.linalg.cholesky((pow(2.38, 2) / self.k) * mass_matrix)
                mass_matrix_L = L.T
            else:
                mass_matrix = np.identity(self.k) * scale_factor
            # Sample parameter one at a time
            for j in range(self.k):
                # Get proposal
                alpha, theta_p, Lp = self.proposal(theta0, L0, mass_matrix_L, j, need_mixture)
                self.proposals.append(theta_p)
                # Check alpha
                if alpha == 0 or alpha > log(random()):
                    self.acceptances[i * self.k + j] = 1
                    theta0, L0 = theta_p, Lp
                self.samples.append(np.append(theta0, L0))
                # Tune sampler step
                self.scale_factors.append(scale_factor)
                if i % self.lag == 0:
                    acceptance_proportion = (np.sum(
                        self.acceptances[((i*self.k)-self.lag-1) : ]) / self.lag)
                scale_factor[j] = self.tune_scale(scale_factor[j], acceptance_proportion, i)
            self.required_samples[i] = np.append(theta0, L0)
            # Estimate the covariance matrix using previous samples
            if i > start_adaption:
                covariance_matrix = np.cov(self.required_samples[ : i, : -1].T)
            self.do_print(i) 
        return np.array(self.samples).T
        
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
        # Sampling loop
        for i in range(self.N):
            # Update covariance matrix
            if i > start_adaption:
                need_mixture = True
                mass_matrix = np.cov(np.array(self.samples)[ : i-1, : -1].T) * scale_factor
            else:
                mass_matrix = np.identity(self.k) * scale_factor
            # Get proposal
            alpha, theta_p, Lp = self.proposal(theta0, L0, mass_matrix, None, need_mixture)
            self.proposals.append(theta_p)
            # Check alpha
            if alpha == 0 or alpha > log(random()):
                self.acceptances[i] = 1
                theta0, L0 = theta_p, Lp
            self.samples.append(np.append(theta0, L0))
            self.scale_factors.append(scale_factor)
            if i % self.lag == 0:
                acceptance_proportion = (np.sum(
                    self.acceptances[(i-self.lag-1) : ]) / self.lag)
            scale_factor = self.tune_scale(scale_factor, acceptance_proportion, i)
            self.do_print(i)
        return np.array(self.samples).T