import numpy as np

from samplers import MWGSampler, RosenthalAdaptiveSampler
from proposals import RWMHProposal
from tests.case_fly import LogLkd
from display import quick_display

y = np.array([1225, 825, 4752, 774, 3547, 1549])
# X0- initial guesses (starting parameters)
X0 = np.array([y[0], 2, 0.0005])
# Sampler parameters
N, M = 10000, 1000


def test_proposal():
    # Initialise Proposer
    proposer = RWMHProposal(LogLkd, y, len(X0), verbose=True)
                         
    L0 = LogLkd(X0, y)
    factor = np.ones(3)
    # Propose
    alpha, X, L = proposer.propose(X0, L0, factor)
    return alpha, X, L

def test_fly_case_MWG():
    # Initialise Proposer
    proposer = RWMHProposal(LogLkd, y, verbose=True)
    
    # Initialise Sampler
    sampler = MWGSampler(samples_draw=N, notify_every=M, 
                         burnin_fraction=0.5, burnin_lag=50,
                         model=LogLkd, data=y, proposal=proposer.propose,
                         verbose=True)                         
    # Sample
    S = sampler.sample(X0)
    return S

def test_fly_case_RosenthalAdaptive():
    # Initialise Proposer
    proposer = RWMHProposal(LogLkd, y, verbose=True)
    
    # Initialise Sampler
    sampler = RosenthalAdaptiveSampler(samples_draw=N, notify_every=M, 
                         burnin_fraction=0.5, burnin_lag=50,
                         model=LogLkd, data=y, proposal=proposer.propose_mixture,
                         verbose=True)                         
    # Sample
    S = sampler.sample(X0)
    return S


print('X0= ', X0)
#for i in range(100):
#    alpha, X, L = test_proposal()
#    print('alpha= ', alpha, '; logLik= ', L)
#    print('proposal= ', X)

#S = test_fly_case_MWG()
S = test_fly_case_RosenthalAdaptive()
quick_display(S, burnin=N/2)