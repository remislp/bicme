import time
import math
#from scipy.special import gammaln
import numpy as np

from dcpyps.samples import samples
from dcpyps import dataset, mechanism
from HJCFIT.likelihood import Log10Likelihood

def HJCFIT_LogLik(x, data):
    lik, m, c = data
    m.theta_unsqueeze(x)
    l = 0
    try:
        for i in range(len(c)):
            m.set_eff('c', c[i])
            l += lik[i](m.Q)
        return l * math.log(10)
    except:
        return -float('inf')
    

def flip_constrain_dala(mec):
    # PREPARE RATE CONSTANTS.
    # Fixed rates.
    #fixed = np.array([False, False, False, False, False, False, False, True,
    #    False, False, False, False, False, False])
    for i in range(len(mec.Rates)):
        mec.Rates[i].fixed = False
    # Constrained rates.
    mec.Rates[21].is_constrained = True
    mec.Rates[21].constrain_func = mechanism.constrain_rate_multiple
    mec.Rates[21].constrain_args = [17, 3]
    mec.Rates[19].is_constrained = True
    mec.Rates[19].constrain_func = mechanism.constrain_rate_multiple
    mec.Rates[19].constrain_args = [17, 2]
    mec.Rates[16].is_constrained = True
    mec.Rates[16].constrain_func = mechanism.constrain_rate_multiple
    mec.Rates[16].constrain_args = [20, 3]
    mec.Rates[18].is_constrained = True
    mec.Rates[18].constrain_func = mechanism.constrain_rate_multiple
    mec.Rates[18].constrain_args = [20, 2]
    mec.Rates[11].is_constrained = True
    mec.Rates[11].constrain_func = mechanism.constrain_rate_multiple
    mec.Rates[11].constrain_args = [7, 1.5]
    mec.Rates[6].is_constrained = True
    mec.Rates[6].constrain_func = mechanism.constrain_rate_multiple
    mec.Rates[6].constrain_args = [10, 2]
    mec.update_constrains()
    # Rates constrained by microscopic reversibility
    mec.set_mr(True, 9, 1)
    mec.set_mr(True, 14, 0)
    # Update constrains
    mec.update_constrains()
    return mec

def CH82_simulated_1patch():
    
    # Data.
    fname = "CH82.scn" # binary SCN file containing simulated idealised single-channel open/shut intervals
    tr = 1e-4 # temporal resolution to be imposed to the record
    tc = 4e-3 # critical time interval to cut the record into bursts
    conc = 100e-9 # agonist concentration 
    # Initaialise SCRecord instance.
    rec = dataset.SCRecord([fname], conc, tres=tr, tcrit=tc)
    # Get bursts from the record
    bursts = rec.bursts.intervals()

    # Model.
    mec = samples.CH82()
    # PREPARE RATE CONSTANTS.
    # Fixed rates
    mec.Rates[7].fixed = True
    # Constrained rates
    mec.Rates[5].is_constrained = True
    mec.Rates[5].constrain_func = mechanism.constrain_rate_multiple
    mec.Rates[5].constrain_args = [4, 2]
    mec.Rates[6].is_constrained = True
    mec.Rates[6].constrain_func = mechanism.constrain_rate_multiple
    mec.Rates[6].constrain_args = [8, 2]
    # Rates constrained by microscopic reversibility
    mec.set_mr(True, 9, 0)
    # Update rates
    mec.update_constrains()
    
    likelihood = Log10Likelihood(bursts, mec.kA, tr, tc)
    
    return ([likelihood], mec, [conc])

    
    
    
