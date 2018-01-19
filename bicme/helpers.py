#!/usr/bin/python

import math
import numpy as np
import scipy.stats
import scipy.io as sio

try:
    from HJCFIT.likelihood import Log10Likelihood
except:
    raise ImportError("HJCFIT module is missing")

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

    def logPosterior(self, X):
        return self.logLik(X) + self.logPrior(X)

    def logLik(self, X):
        """Calculate total log likelihood."""
        self.mec.theta_unsqueeze(X)
        l = 0
        try:
            for i in range(len(self.c)):
                self.mec.set_eff('c', self.c[i])
                l += self.lik[i](self.mec.Q)
            return l * math.log(10)
        except:
            return -float('inf')

    def logPrior(self, X):
        """ """
        lp = 0.0
        for rate in self.mec.Rates:
            if not rate.fixed and not rate.is_constrained and not rate.mr:
                lp += math.log(scipy.stats.uniform.pdf(rate.unit_rate(), 
                      rate.limits[0][0], rate.limits[0][1]))
        return lp

    def MLL_logLik(self, X):
        self.mec.theta_unsqueeze(np.exp(X))
        l = 0.0
        for i in range(len(self.conc)):
            self.mec.set_eff('c', self.conc[i])
            l += -self.lik[i](self.mec.Q) * math.log(10)
        return l
    
    def HJCFITLogLik(self):
        likelihood = []
        for i in range(len(self.bursts)):
            likelihood.append(Log10Likelihood(self.bursts[i], self.mec.kA,
                self.tr[i], self.tc[i], **self.kwargs))
        return likelihood
