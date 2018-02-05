#!/usr/bin/python

import math
import time
import numpy as np
import scipy.stats
import scipy.io as sio
from scipy.optimize import minimize

from bicme.samplers import MWGSampler
from bicme.samplers import RosenthalAdaptiveSampler
from bicme.proposals import RWMHProposal

try:
    from HJCFIT.likelihood import Log10Likelihood
except:
    print("bicme: Warning: HJCFIT module is missing")

def calculate_autocorrelation(X):
    """ """
    X = X - np.mean(X)
    acf = np.correlate(X, X, mode='full')
    return acf[int(acf.size/2) : ] / acf[int(acf.size / 2)]

def calculate_KDE(X):
    """Calculate kernel-density estimate using Gaussian kernel. """
    x = np.linspace(np.amin(X), np.amax(X), len(X))
    d = scipy.stats.gaussian_kde(X)
    d.covariance_factor = lambda : 0.25
    d._compute_covariance()
    return x, d(x)

def load_bursts_from_matfile(fmat):
    """Load bursts from Matlab .mat file."""
    mat = sio.loadmat(fmat)
    conc = [item for sublist in mat['concs'] for item in sublist]
    tr = [item for sublist in mat['tres'] for item in sublist]
    tc = [item for sublist in mat['tcrit'] for item in sublist]
    chs = [item for sublist in mat['useChs'] for item in sublist]
    for i in range(len(chs)):
        if chs[i] < 1:
            tc[i] *= -1
    mb = mat['bursts'].tolist()[0]
    bursts = []
    for i in range(len(mb)):
        rec = []
        rb = mb[i][0]
        for arr in rb:
            rec.append(arr[0].tolist())
        bursts.append(rec)
    return bursts, conc, tr, tc

def sample_MWG(log_posterior, theta, N=100000, sample_comp=True):
    """
    Run Metropolis_within_Gibbs (MWG) sampling component- or block-wise.
    """
    proposer = RWMHProposal(log_posterior, verbose=True)
    if sample_comp:
        print('Sampling componentwise...')
        proposal=proposer.propose_component_log
    else:
        print('Sampling block...')
        proposal=proposer.propose_block_log
    sampler = MWGSampler(samples_draw=N, notify_every=int(N/100), 
                             burnin_fraction=0.5, burnin_lag=50,
                             model=log_posterior, #data=args, 
                             proposal=proposal, 
                             verbose=True) 
    print ("\nInitial posterior = {0:.6f}".format(log_posterior(theta)))
    start = time.clock()
    if sample_comp:
        chain = sampler.sample_component(theta)
    else:
        chain = sampler.sample_block(theta)
    print ('\nCPU time in MWG sampler =', time.clock() - start)
    return chain

def sample_RA(log_posterior, theta, N=100000):
    """
    Run Rosenthal adaptive sampling with mixture proposal.
    """
    proposer = RWMHProposal(log_posterior, verbose=True)
    sampler = RosenthalAdaptiveSampler(samples_draw=N, notify_every=int(N/100), 
                         burnin_fraction=0.5, burnin_lag=50,
                         model=log_posterior, #data=args, 
                         proposal=proposer.propose_block_mixture,
                         verbose=True)
    print ("\nInitial posterior = {0:.6f}".format(log_posterior(theta)))
    start = time.clock()
    chain = sampler.sample_block(theta)
    print ('\nCPU time in Rosenthal sampler =', time.clock() - start)
    return chain


class CaseHJCFIT(object):
    """
    HJCFIT model.  Provide log poterior function for MCMC sampling.
    """
    def __init__(self, bursts, conc, tres, tcrit, mec):
        """
        Parameters
        ----------
        bursts : list of list of floats
            List of bursts.
        conc : list of floats
            Concentrations for each record.
        tres : list of floats
            Imposed temporal resolution.
        tcrit : list of floats
            Critical time interval to separate bursts.
        mec : object
            DCPYPS mechanism.
        """
        self.bursts, self.c, self.tr, self.tc = bursts, conc, tres, tcrit
        self.mec = mec
        self.kwargs = {'nmax': 2, 'xtol': 1e-12, 'rtol': 1e-12, 'itermax': 100,
            'lower_bound': -1e6, 'upper_bound': 0}
        self.lik = self.HJCFITLogLik()
        self.logSpace = False

    def logPosterior(self, X):
        return -self.logLik(X) + self.logPrior(X)

    def logLik(self, X):
        """Calculate total log likelihood."""
        if self.logSpace:
            self.mec.theta_unsqueeze(np.exp(X))
        else:
            self.mec.theta_unsqueeze(X)
        l = 0.0
        try:
            for i in range(len(self.c)):
                self.mec.set_eff('c', self.c[i])
                l -= self.lik[i](self.mec.Q)
            return l * math.log(10)
        except:
            return float('inf')

    def logPrior(self, X):
        """ """
        lp = 0.0
        for rate in self.mec.Rates:
            if not rate.fixed and not rate.is_constrained and not rate.mr:
                lp += math.log(scipy.stats.uniform.pdf(rate.unit_rate(), 
                      rate.limits[0][0], rate.limits[0][1]))
        return lp
    
    def HJCFITLogLik(self):
        likelihood = []
        for i in range(len(self.bursts)):
            likelihood.append(Log10Likelihood(self.bursts[i], self.mec.kA,
                self.tr[i], self.tc[i], **self.kwargs))
        return likelihood
    
    def run_MLL_fit(self, initial_guess=None):
        """
        Run HJCFIT: maximum log likelihood fit.
        Parameters:"""
    
        if initial_guess is not None:
            theta = initial_guess
        else: 
            theta = self.mec.theta()
        self.logSpace = True
        print("\nRunning MLL fit; Starting likelihood (DCprogs)= {0:.6f}".
                format(self.logLik(np.log(theta))))
        start = time.clock()
        success = False
        while not success:
            result = minimize(self.logLik, np.log(theta), 
                method='Nelder-Mead', #callback=printiter,
                options={'xtol':1e-5, 'ftol':1e-5, 
                'maxiter': 30000, 'maxfev': 150000, 'disp': True})
            success = result.success
            self.mec.theta_unsqueeze(np.exp(result.x))
        print ('CPU time in simplex=', time.clock() - start)
        print ("\nDCPROGS Fitting finished: %4d/%02d/%02d %02d:%02d:%02d"
                %time.localtime()[0:6])
        print ("\n Final rate constants:", self.mec)

