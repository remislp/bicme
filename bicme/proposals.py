from math import sqrt, exp, log, pow
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
            #mass_matrix = np.identity(k) * scale
            L = np.linalg.cholesky(mass_matrix * pow(2.38, 2) / k)
            mix1 = (1 - beta) * (theta + np.dot(L.T, np.random.random(k)))
            mix2 = beta * (theta + (0.1 / sqrt(k)) * np.random.random(k))
            proposal = mix1 + mix2
        else:
            #proposal = theta + (0.1 / sqrt(k)) * np.random.random(k)
            proposal = np.exp(np.random.normal(np.log(theta), 0.1/k))
            print(proposal)
        
        logLik = self.model(proposal, self.data)
        
        alpha = -float('inf')
        if not np.isinf(logLik) and logLik is not np.isnan(logLik):
            alpha = min(0, logLik - logLik0)
                           
        return alpha, proposal, logLik