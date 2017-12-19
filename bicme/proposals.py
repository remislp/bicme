from math import sqrt, exp, log, pow, isnan, isinf
import random
import numpy as np

class RWMHProposal():
    """
    Random-walk Metropoli-Hastings proposal step.
    """
    
    def __init__(self, model, verbose=False):
        """
        Parameters
        ----------
        """
        self.model = model
        
    def __get_alpha(self, proposal, logLik0):
        try:
            logLik = self.model(proposal) #, self.data)
        except:
            logLik = float('nan')
        alpha = -float('inf')
        if (not isinf(logLik)) and (not isnan(logLik)):
            alpha = min(0, logLik - logLik0)
        return alpha, proposal, logLik
    
    def __get_alpha_logpars(self, proposal, theta, logLik0):
        try:
            logLik = self.model(proposal) #, self.data)
        except:
            logLik = float('nan')
        alpha = -float('inf')
        if (not isinf(logLik)) and (not isnan(logLik)):
            alpha = min(0, (logLik + np.sum(np.log(proposal)) - 
                           (logLik0 + np.sum(np.log(theta)))))
        return alpha, proposal, logLik
    
    def propose_block(self, theta, logLik0, scale, ip=None):
        L = np.linalg.cholesky(np.identity(len(theta)) * scale)
        proposal = theta.copy() +  np.dot(L.T, np.random.normal(size=len(theta)))
        return self.__get_alpha(proposal, logLik0)
    
    def propose_block_log(self, theta, logLik0, scale, ip=None):
        L = np.linalg.cholesky(np.identity(len(theta)) * scale)
        proposal = np.log(theta.copy()) +  np.dot(L.T, np.random.normal(size=len(theta)))
        return self.__get_alpha_logpars(np.exp(proposal), theta, logLik0)
    
    def propose_component(self, theta, logLik0,  scale, ip):
        proposal = theta.copy()
        proposal[ip] = random.normalvariate(theta[ip], scale[ip])
        return self.__get_alpha(proposal, logLik0)
        
    def propose_component_log(self, theta, logLik0, scale, ip):
        proposal = theta.copy()
        proposal[ip] = exp(random.normalvariate(log(theta[ip]), scale[ip]))
        return self.__get_alpha_logpars(proposal, theta, logLik0)
        
    def propose_block_mixture(self, theta, logLik0, mass_matrix, ip=None, need_mixture=True):
        """
        Propose a joint Metropolis-Hastings step for the parameters of a
        model based on proposing from a mixture distribution.
        """
        beta = 0.05
        k = len(theta)
        if need_mixture:
            L = np.linalg.cholesky((pow(2.38, 2) / k) * mass_matrix)
            proposal = (1 - beta) * (theta + np.dot(L.T, np.random.normal(size=k)))
            proposal += beta * (theta + (0.1 / sqrt(k)) * np.random.normal(size=k))
        else:
            proposal = theta + (0.1 / sqrt(k)) * np.random.normal(size=k)                
        return self.__get_alpha(proposal, logLik0)
                           