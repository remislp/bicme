import numpy as np
import scipy.stats

def norm_logPosterior(X, y):
    return norm_logLik(X, y) + norm_logPrior(X)

def norm_logLik(X, y):
    return np.sum(np.log(scipy.stats.norm.pdf(y, X[0], X[1]))) 
    
def norm_logPrior(X):
    mu_lims = [-20, 20]
    si_lims = [0, 100]
    mu_low, mu_range = mu_lims[0], mu_lims[1] - mu_lims[0]
    si_low, si_range = si_lims[0], si_lims[1] - si_lims[0]
    return (np.log(scipy.stats.uniform.pdf(X[0], mu_low, mu_range)) 
              + np.log(scipy.stats.uniform.pdf(X[1], si_low, si_range)))