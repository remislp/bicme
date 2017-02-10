from math import sqrt, exp, log, pow, isnan, isinf
import random
import numpy as np

class RWMHProposal():
    """
    Random-walk Metropoli-Hastings proposal step.
    """
    
    def __init__(self, model, data, verbose=False):
        """
        Parameters
        ----------
        """
        
        self.model = model
        self.data = data
        
    def propose(self, theta, logLik0, ip, scale):
        
        proposal = theta.copy()
        proposal[ip] = exp(random.normalvariate(log(theta[ip]), scale[ip]))
        logLik = self.model(proposal, self.data)
        
        alpha = -float('inf')
        if not np.isinf(logLik):
            alpha = min(0, (logLik + np.sum(np.log(proposal)) - 
                           (logLik0 + np.sum(np.log(theta)))))
                           
        return alpha, proposal, logLik
        
    def propose_mixture(self, theta, logLik0, need_mixture, mass_matrix):
        """
        Propose a joint Metropolis-Hastings step for the parameters of a
        model based on proposing from a mixture distribution.
        """
        
        beta = 0.05
        k = len(theta)
        if need_mixture:
            L = np.linalg.cholesky((pow(2.38, 2) / k) * mass_matrix)
            mix1 = (1 - beta) * (theta + np.dot(L.T, np.random.normal(size=k)))
            mix2 = beta * (theta + (0.1 / sqrt(k)) * np.random.normal(size=k))
            proposal = mix1 + mix2
        else:
            proposal = theta + (0.1 / sqrt(k)) * np.random.normal(size=k)
                
        try:
            logLik = self.model(proposal, self.data)
        except:
            logLik = float('nan')
        
        alpha = -float('inf')
        if (not isinf(logLik)) and (not isnan(logLik)):
            alpha = min(0, logLik - logLik0)
                           
        return alpha, proposal, logLik
    
    def propose_mixture_cw(self, theta, logLik0, ip, need_mixture, mass_matrix):
        """
        Propose a joint Metropolis-Hastings step for the parameters of a
        model based on proposing from a mixture distribution.
        """
        
        beta = 0.05
        k = len(theta)
        if need_mixture:
            #L = np.linalg.cholesky((pow(2.38, 2) / k) * mass_matrix)
            mix1 = (1 - beta) * (theta[ip] + np.dot(mass_matrix, np.random.normal(size=k))[ip])
            mix2 = beta * (theta[ip] + (0.1 / sqrt(k)) * np.random.normal(size=1))
            proposal = mix1 + mix2
        else:
            proposal = theta[ip] + (0.1 / sqrt(k)) * np.random.normal(size=1)
                
        try:
            logLik = self.model(proposal, self.data)
        except:
            logLik = float('nan')
        
        alpha = -float('inf')
        if (not isinf(logLik)) and (not isnan(logLik)):
            alpha = min(0, logLik - logLik0)
                           
        return alpha, proposal, logLik