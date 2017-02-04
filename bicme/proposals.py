import math
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
        proposal[ip] = math.exp(random.normalvariate(math.log(theta[ip]), scale[ip]))
        logLik = self.model(proposal, self.data)
        
        alpha = -float('inf')
        if not np.isinf(logLik):
            alpha = min(0, (logLik + np.sum(np.log(proposal)) - 
                           (logLik0 + np.sum(np.log(theta)))))
                           
        return alpha, proposal, logLik
        
