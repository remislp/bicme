import math
import numpy as np
import scipy.io as sio
import scipy.stats

from samplers import MWGSampler
from samplers import RosenthalAdaptiveSampler
from proposals import RWMHProposal
from display import quick_display

def norm_logPosterior(X, y):
    return norm_logLik(X, y) + norm_logPrior(X)

def norm_logLik(X, y):
    #return -0.5 * (len(y) * math.log(2 * math.pi * math.pow(X[1], 2)) +
    #        (1 / math.pow(X[1], 2)) * np.sum(np.power(y - X[0], 2)))
    return np.sum(np.log(scipy.stats.norm.pdf(y, X[0], X[1]))) 
    
def norm_logPrior(X):
    mu_lims = [-20, 20]
    si_lims = [0, 100]
    return (np.log(scipy.stats.uniform.pdf(X[0], mu_lims[0], 40)) 
              + np.log(scipy.stats.uniform.pdf(X[1], si_lims[0], si_lims[1])))

def test_normal_case_MWG(data):
    X0 = [2, 10]
    # Initialise Proposer
    proposer = RWMHProposal(norm_logPosterior, data, verbose=True)
    # Initialise Sampler
    sampler = MWGSampler(samples_draw=10, notify_every=1, 
                         burnin_fraction=0.5, burnin_lag=5,
                         model=norm_logPosterior, data=data, 
                         proposal=proposer.propose_block,
                         verbose=True)  
    sampler.acceptance_limits = [0.3, 0.7]
    sampler.scale = 0.5
    # Sample
    S = sampler.sample_block(X0)
    print('acceptances= ', sampler.acceptances)
    print('proposals= ', sampler.proposals)
    print('samples= ', sampler.samples)
    #quick_display(S, burnin=5)
    
def test_normal_case_RosenthalAdaptive(data):
    # Initialise Proposer
    proposer = RWMHProposal(norm_logPosterior, data, verbose=True)
    # Initialise Sampler
    sampler = RosenthalAdaptiveSampler(samples_draw=100000, notify_every=100, 
                         burnin_fraction=0.5, burnin_lag=50,
                         model=norm_logPosterior, data=data, 
                         proposal=proposer.propose_block_mixture,
                         verbose=True)                         
    # Sample
    X0 = [2, 10]
    S = sampler.sample_block(X0)
    quick_display(S, burnin=5000)

mat1 = sio.loadmat('../Tests/Data/NormData.mat')
data = np.array(mat1['data']).flatten()
np.random.seed(1)
test_normal_case_MWG(data)
#test_normal_case_RosenthalAdaptive(data)
