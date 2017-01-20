
class MH(object):
    """
    Metropolis-Hastings sampling algorithm. Class contains two methods with 
    which to perform MCMC sampling. Sampling is either performed jointly 
    (block_sample), or componentwise (component_sample).
    """
    
    def __init__(self, samplerParams=None, model=None, data=None, 
                 proposal=None, startParams=None):
        """
        Parameters
        ----------
        samplerParams - a stucture of sampling parameters
        model - contains the model specification and likelihood
        data - the data required to evaluate the model likelihood
        proposal - Proposal object contains function to use as a proposal,
        startParams - starting values for the parameters

        Returns
        -------
        samples - a structure containing the samples, acceptances etc.
        """
        pass
    
    def block_sample(self):
        pass
    
    def component_sample(self):
        pass
    
    