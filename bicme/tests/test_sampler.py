import numpy as np

#from bicme.samplers.Metropolis_Hastings import MH
from bicme.samplers import Sampler
from case_fly import LogLkd, proposal_fly

def test_Sampler_initiation():
    sampler = Sampler()
    assert sampler.N == 100000
    assert sampler.M == 100
    assert sampler.model is None
    sampler1 = Sampler(samples_draw=333, notify_every=23)
    assert sampler1.N == 333
    assert sampler1.M == 23

def test_fly_case():
    # Data.
    y = np.array([1225, 825, 4752, 774, 3547, 1549])
    # X0- initial guesses (starting parameters)
    X0 = np.array([y[0], 2, 0.0005])
    # Sampler parameters
    N, M = 10000, 1000
    # Initialise Sampler
    rw_sampler = Sampler(samples_draw=N, notify_every=M, model=LogLkd,
                         data=y, proposal=proposal_fly, verbose=True)
    # Sample
    S = rw_sampler.sample(X0)

    assert -S[-1].max() > 755.0 and -S[-1].max() < 765.0
    imax = np.where(S[-1] == S[-1].max())[0][0]
    assert S[0, imax] > 490 and S[0, imax] < 500
    assert S[1, imax] > 3 and S[1, imax] < 3.5
    assert S[2, imax] > 0.0004 and S[2, imax] < 0.0005
    
    
    