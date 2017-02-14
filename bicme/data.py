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
    for i in range(len(c)):
        m.set_eff('c', c[i])
        l += lik[i](m.Q)
    return l * math.log(10)

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

    
    
    
