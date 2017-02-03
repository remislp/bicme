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
                if random.random() < alpha:
                    local_theta, ll0 = p, llp
                    
            # every M print job progress in percentage
            if self.verbose and i % self.M == 0:
                if self.verbose: print (100 * (self.M + i) / float(self.N), '%')
            # store sample
            #S[ : , i] = np.append(np.exp(local_theta), ll0)
            S[ : , i] = np.append(local_theta, ll0)
        return S

class MWGSampler(Sampler):
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
        
    def __prepare_sampling_containers(self):
        self.scale_factors = np.ones(self.N)
        self.all_samples = np.zeros((self.N, self.k))
        self.all_proposals = np.zeros((self.N, self.k))
        self.acceptances = np.zeros(self.N)
        self.posteriors = np.zeros(self.N)
                         
    def sample_block_wise(self, theta):
        """
        Samples parameters one by one to improwe mixing.
        """
        
        self.k = len(theta)
        self.__prepare_sampling_containers()
        scale_factor = 1
        L0 = self.model(theta, self.data)
        theta0 = theta.copy()
        
        # Sampling loop
        for i in range(self.N):
            # Get proposal
            alpha, theta_p, L_p = self.proposal(self.model, self.data,
                                                theta0, L0, scale_factor)
            self.proposals[i] = theta_p
            
            # Check acceptance
            if alpha == 0 or alpha > random.random():
                self.acceptances[i] = 1
                self.posteriors[i] = L_p
                L0 = L_p
                self.all_samples[i] = theta_p
                theta0 = theta_p
            else:
                self.all_samples[i] = theta0
                self.posteriors[i] = L0
            
            # Tune sampler step
            self.scale_factors[i] = scale_factor
            if i < self.B and i >= self.lag:
                if i % self.lag == 0:
                    acceptance_proportion = (np.sum(
                        self.acceptances[(i-self.lag) : ]) / self.lag)
                    if acceptance_proportion < self.acceptance_limits[0]:
                        scale_factor *= 1 - self.scale
                        print("Acceptance: {0:d}; Scale factor decreased to",
                            format(acceptance_proportion) +
                            " {0:.3f} at iteration {1:d}".
                            format(scale_factor, i))
                    elif acceptance_proportion > self.acceptance_limits[1]:
                        scale_factor *= 1 + self.scale
                        print("Acceptance: {0:d}; Scale factor increased to",
                            format(acceptance_proportion) +
                            " {0:.3f} at iteration {1:d}".
                            format(scale_factor, i))
            
            if i % self.N == 0 and self.verbose:
                print ("{0:.3f}%: ".format(100 * (self.M + i) / float(self.N)))

            