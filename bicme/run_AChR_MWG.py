import time
import math
#from scipy.special import gammaln
import numpy as np

from dcpyps.samples import samples
from dcpyps import dataset, mechanism
   
def dcprogslik(x, data):
    lik, m, c = data
    m.theta_unsqueeze(x)
    l = 0
    for i in range(len(c)):
        m.set_eff('c', c[i])
        l += lik[i](m.Q)
    return l * math.log(10)

def proposal_func(theta):
    #propose_theta = np.random.normal(theta, 0.001)
    #print('propose_theta = ', propose_theta)
    #return np.exp(propose_theta)
    return np.random.normal(theta, 0.01)


# Data.
fname = "CH82.scn" # binary SCN file containing simulated idealised single-channel open/shut intervals
tr = 1e-4 # temporal resolution to be imposed to the record
tc = 4e-3 # critical time interval to cut the record into bursts
conc = 100e-9 # agonist concentration 
# Initaialise SCRecord instance.
rec = dataset.SCRecord([fname], conc, tres=tr, tcrit=tc)
rec.printout()

# Model.
mec = samples.CH82()
mec.printout()
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


# Initial guesses (starting parameters)
#Propose initial guesses different from recorded ones 
#initial_guesses = [100, 3000, 10000, 100, 1000, 1000, 1e+7, 5e+7, 6e+7, 10]
initial_guesses = mec.unit_rates()
mec.set_rateconstants(initial_guesses)
mec.update_constrains()
mec.printout()
theta = mec.theta()
theta = [10, 10000, 1000, 100, 1100, 1e+8]
print ('\n\ntheta=', theta)

# Import HJCFIT likelihood function
from HJCFIT.likelihood import Log10Likelihood
# Get bursts from the record
bursts = rec.bursts.intervals()
# Initiate likelihood function with bursts, number of open states,
# temporal resolution and critical time interval
likelihood = Log10Likelihood(bursts, mec.kA, tr, tc)
lik = dcprogslik(theta, ([likelihood], mec, [conc]))
print ("\nInitial likelihood = {0:.6f}".format(lik))

# Sampler parameters
N, M = 100000, 1000
from samplers import MWGSampler
from proposals import RWMHProposal 
#sampler = MWGSampler(samples_draw=N, notify_every=M, 
#                     model=dcprogslik, data=([likelihood], mec, [conc]),
#                     proposal=proposal_func, verbose=True)
                     
                     
proposer = RWMHProposal(dcprogslik, ([likelihood], mec, [conc]), verbose=True)
    
# Initialise Sampler
sampler = MWGSampler(samples_draw=N, notify_every=M, 
                     burnin_fraction=0.5, burnin_lag=50,
                     model=dcprogslik, data=([likelihood], mec, [conc]), proposal=proposer.propose,
                     verbose=True)                         

start = time.clock()
S = sampler.sample(theta)
t = time.clock() - start
print ('\nCPU time in sampler =', t)

np.savetxt('AChR_MCMC_MWG.csv', S, delimiter=',')

Lmax = S[-1].max()
print('Lmax = ', Lmax)
imax = np.where(S[-1] == S[-1].max())[0][0]
print('imax = ', imax)

X = S[:-1, imax]
mec.theta_unsqueeze(X)
mec.printout()





