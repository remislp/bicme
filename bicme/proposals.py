import numpy as np


class RWMHProposal():
    """
    Random-walk Metropoli-Hastings proposal step.
    """
    
    def __init__(self, k, is_comp_wise=False, verbose=False):
        """
        Parameters
        ----------
        k : int
            Number of parameters.
        is_comp_wise : bool
            True if proposal is componentwise; false- joint proposal for all 
            parameters. 
        """
        
        self.mass_matrix = np.identity(k)
        self.is_cw = is_comp_wise
