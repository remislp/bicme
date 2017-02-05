from math import log
from random import random
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
        #ll0 = self.model(theta, *self.data)
        ll0 = self.model(theta, self.data)
        local_theta = theta.copy()
        
        for i in range(self.N):
            # Generate candidate state
            p = self.proposal(local_theta)
             # accept / reject new state
            if p.all() > 0:
                try:
                    #llp = self.model(p, *self.data)
                    llp = self.model(p, self.data)
                except:
                    llp = float('inf')
                alpha = min(1, np.exp(llp-ll0))
                if random() < alpha:
                    local_theta, ll0 = p, llp
                    
            # every M print job progress in percentage
            if self.verbose and i % self.M == 0:
                if self.verbose: print (100 * (self.M + i) / float(self.N), '%')
            # store sample
            #S[ : , i] = np.append(np.exp(local_theta), ll0)
            S[ : , i] = np.append(local_theta, ll0)
        return S

class MWGSampler(object):
    """
    Multiplicative Metropolis_within_Gibbs sampler with scaling during burn-in.
    """
    def __init__(self, samples_draw=10000, notify_every=100, 
                 burnin_fraction=0.5, burnin_lag=50,
                 model=None, data=None, proposal=None, verbose=False):

        # Sampler parameters
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
        print('Sampler initialised...')
        
    def sample(self, theta):
        """
        Samples parameters one by one to improwe mixing.
        """
        
        self.k = len(theta)
        self.scale_factors = np.ones((self.N * self.k, self.k))
        self.all_samples = np.zeros((self.N * self.k, self.k+1))
        self.all_proposals = np.zeros((self.N * self.k, self.k))
        self.acceptances = np.zeros(self.N * self.k)
        
        scale_factor = np.ones(self.k)
        L0 = self.model(theta, self.data)
        theta0 = theta.copy()
        
        # Sampling loop
        for i in range(self.N):
            # Sample parameter one at a time
            for j in range(self.k):
                alpha, theta_p, Lp = self.proposal(theta0, L0, j, scale_factor)
                self.all_proposals[i] = theta_p
                
                if alpha == 0 or alpha > log(random()):
                    self.acceptances[i * self.k + j] = 1
                    self.all_samples[i * self.k + j] = np.append(theta_p, Lp)
                    theta0, L0 = theta_p, Lp
                else:
                    self.all_samples[i * self.k + j] = np.append(theta0, L0)

                # Tune sampler step
                self.scale_factors[i * self.k + j] = scale_factor
                if i < self.B and i >= self.lag:
                    if i % self.lag == 0:
                        acceptance_proportion = (np.sum(
                            self.acceptances[((i*self.k)-self.lag-1) : ]) / self.lag)
                        if acceptance_proportion < self.acceptance_limits[0]:
                            scale_factor[j] *= 1 - self.scale
                            #print("Acceptance: {0:.9f}; Scale factor decreased to".
                            #    format(acceptance_proportion) +
                            #    " {0:.9f} at iteration {1:d}".
                            #    format(scale_factor[j], i))
                        elif acceptance_proportion > self.acceptance_limits[1]:
                            scale_factor[j] *= 1 + self.scale
                            #print("Acceptance: {0:.9f}; Scale factor increased to".
                            #    format(acceptance_proportion) +
                            #    " {0:.9f} at iteration {1:d}".
                            #    format(scale_factor[j], i))
            
            if i % self.M == 0 and self.verbose:
                   print (100 * (self.M + i) / float(self.N), '%')
        
        return self.all_samples.T
    
    
class RosenthalAdaptiveSampler(object):
    """
    Algorithm taken from Rosenthal 2006 technical report.
    """
    def __init__(self, samples_draw=10000, notify_every=100, 
                 burnin_fraction=0.5, burnin_lag=50,
                 model=None, data=None, proposal=None, verbose=False):

        # Sampler parameters
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
        print('Sampler initialised...')
        
    def sample(self, theta):
        """
        Samples parameters one by one to improwe mixing.
        """
        
        
        self.k = len(theta)
        self.scale_factors = np.ones((self.N, self.k))
        self.all_samples = np.zeros((self.N, self.k+1))
        self.all_proposals = np.zeros((self.N, self.k))
        self.acceptances = np.zeros(self.N)
        
        start_adaption = 100
        need_mixture = False
        covariance_matrix = np.identity(self.k)
        mass_matrix = covariance_matrix.copy()
        scale_factor = 1
        
        L0 = self.model(theta, self.data)
        theta0 = theta.copy()
        
        # Sampling loop
        for i in range(self.N):
            #print(i)
        
            # Update covariance matrix
            if i == start_adaption:
                need_mixture = True
            elif i > start_adaption:
                try:
                    temp = covariance_matrix * scale_factor
                    L = np.linalg.cholesky(temp)
                    mass_matrix = covariance_matrix * scale_factor
                    #print('cov=', covariance_matrix)
                    #print('mas=', mass_matrix)
                except:
                    #print('Warning: mass matrix not positive definite')
                    mass_matrix = np.identity(self.k) * scale_factor
            else:
                covariance_matrix = np.identity(self.k)
                mass_matrix = covariance_matrix * scale_factor
                
            # Get proposal
            alpha, theta_p, Lp = self.proposal(theta0, L0, need_mixture, mass_matrix)
            self.all_proposals[i] = theta_p
                
            # Check alpha
            if alpha == 0 or alpha > log(random()):
                self.acceptances[i] = 1
                self.all_samples[i] = np.append(theta_p, Lp)
                theta0, L0 = theta_p, Lp
            else:
                self.all_samples[i] = np.append(theta0, L0)
                
            # Estimate the covariance matrix using previous samples
            if i > start_adaption:
                covariance_matrix = np.cov(self.all_samples[i-100 : i, : -1].T)
                
            # Tune sampler step
            self.scale_factors[i] = scale_factor
            if i < self.B and i >= self.lag:
                if i % self.lag == 0:
                    acceptance_proportion = (np.sum(
                        self.acceptances[(i-self.lag-1) : ]) / self.lag)
                    if acceptance_proportion < self.acceptance_limits[0]:
                        scale_factor *= 1 - self.scale
                        #print("Acceptance: {0:.9f}; Scale factor decreased to".
                        #    format(acceptance_proportion) +
                        #    " {0:.9f} at iteration {1:d}".
                        #    format(scale_factor, i))
                    elif acceptance_proportion > self.acceptance_limits[1]:
                        scale_factor *= 1 + self.scale
                        #print("Acceptance: {0:.9f}; Scale factor increased to".
                        #    format(acceptance_proportion) +
                        #    " {0:.9f} at iteration {1:d}".
                        #    format(scale_factor, i))
            
            if i % self.M == 0 and self.verbose:
                   print (100 * (self.M + i) / float(self.N), '%')
                   
        return self.all_samples.T