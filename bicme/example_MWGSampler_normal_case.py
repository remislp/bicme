import numpy as np
import scipy.io as sio

from samplers import MWGSampler
from proposals import RWMHProposal
from display import quick_display

from tests.case_normal import norm_logPosterior

mat1 = sio.loadmat('../Tests/Data/NormData.mat')
data = np.array(mat1['data']).flatten()

X0 = [2, 10]
# Initialise Proposer
proposer = RWMHProposal(norm_logPosterior, data, verbose=True)
# Initialise Sampler
sampler = MWGSampler(samples_draw=10000, notify_every=100, 
                     burnin_fraction=0.5, burnin_lag=50,
                     model=norm_logPosterior, data=data, 
                     proposal=proposer.propose_block,
                     verbose=True)  
sampler.acceptance_limits = [0.3, 0.7]
sampler.scale = 0.5
# Sample
np.random.seed(1)
S = sampler.sample_block(X0)
print('acceptances= ', sampler.acceptances)
#print('proposals= ', sampler.proposals)
print('samples= ', sampler.samples)
print('max posterior = ', max(S[-1,:]))
quick_display(S, burnin=5000)
    



