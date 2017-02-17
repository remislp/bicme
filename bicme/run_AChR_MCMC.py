import time
import numpy as np

from data import HJCFIT_LogLik
from data import CH82_simulated_1patch
from display import DisplayResults
   
ACh_data = CH82_simulated_1patch()
par_names = ['beta1', 'beta2', 'alpha1', 'alpha2', 'k(-1)', 'k(+2)', 'logLik']
theta = [10, 10000, 1000, 100, 1100, 1e+8]
lik = HJCFIT_LogLik(theta, ACh_data)
print ("\nInitial likelihood = {0:.6f}".format(lik))

def run_MWG(samples=10000):
    from samplers import MWGSampler
    from proposals import RWMHProposal 
    proposer = RWMHProposal(HJCFIT_LogLik, ACh_data, verbose=True)
    # Initialise Sampler
    sampler = MWGSampler(samples_draw=samples, notify_every=int(samples/10), 
                         burnin_fraction=0.5, burnin_lag=50,
                         model=HJCFIT_LogLik, data=ACh_data, 
                         proposal=proposer.propose_component_log,
                         verbose=True)                         
    start = time.clock()
    S = sampler.sample_component(theta)
    t = time.clock() - start
    print ('\nCPU time in MWG sampler =', t)
    return S

def run_adaptive(samples=10000):
    from samplers import RosenthalAdaptiveSampler
    from proposals import RWMHProposal

    S1 = run_MWG(1000)
    imax = np.where(S1[-1] == S1[-1].max())[0][0]
    X = S1[:-1, imax]

    proposer = RWMHProposal(HJCFIT_LogLik, ACh_data, verbose=True)
    sampler = RosenthalAdaptiveSampler(samples_draw=samples, 
                        notify_every=int(samples/10), 
                        burnin_fraction=0.5, burnin_lag=50,
                        model=HJCFIT_LogLik, data=ACh_data, 
                        proposal=proposer.propose_block_mixture,
                        verbose=True)                         
    start = time.clock()
    S = sampler.sample_block(X)
    t = time.clock() - start
    print ('\nCPU time in adaptive sampler =', t)
    return S

    
S = run_MWG(10000)
#S = run_adaptive(10000)

#np.savetxt('AChR_MCMC_MWG.csv', S, delimiter=',')
#S = np.loadtxt('AChR_MCMC_MWG.csv', delimiter=',')

Lmax = S[-1].max()
print('Lmax = ', Lmax)
imax = np.where(S[-1] == S[-1].max())[0][0]
print('imax = ', imax)
print('pars=', S[:, imax])

end_lik = HJCFIT_LogLik(S[:, imax], ACh_data)
print ("\nEnd likelihood = {0:.6f}".format(end_lik))

display = DisplayResults(S, burnin=int(len(S[-1])/2), names=par_names)
#display.normalised = True
#display.show_labels = False
display.chains()
#display.distributions()
#display.corner()
#display.autocorrelations()
#display.correlations(3, 1)

