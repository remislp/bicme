import numpy as np
import scipy.stats

class CaseNormal(object):
    """
    Normal distribution case.
    """
    
    def __init__(self, data, lims=[[-20, 20], [0, 100]]):
        """
        Parameters
        ----------
        data : ndarray
            The data required to evaluate the model likelihood.
        mu_lims, si_lims : list of lists
            Parameter limits. In normal case: limits for average and standard deviation.
        
        """
        self.data = data
        self.mu_low = lims[0][0]
        self.mu_range = lims[0][1] - lims[0][0]
        self.si_low = lims[1][0]
        self.si_range = lims[1][1] - lims[1][0]

    def logPosterior(self, X):
        """            
        """
        return self.logLik(X) + self.logPrior(X)

    def logLik(self, X):
        return np.sum(np.log(scipy.stats.norm.pdf(self.data, X[0], X[1]))) 
    
    def logPrior(self, X):
        return (np.log(scipy.stats.uniform.pdf(X[0], self.mu_low, self.mu_range)) 
            + np.log(scipy.stats.uniform.pdf(X[1], self.si_low, self.si_range)))
              