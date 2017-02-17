import sys
import time
import math
import numpy as np

from dcpyps import dcio
from dcpyps import dataset
from HJCFIT.likelihood import Log10Likelihood

from data import HJCFIT_LogLik
from data import flip_constrain_dala
from display import DisplayResults

# LOAD FLIP MECHANISM USED in Burzomato et al 2004
mecfn = 'F:/MCMC/datasets/Dalanine/M1.mec'
version, meclist, max_mecnum = dcio.mec_get_list(mecfn)
mec = dcio.mec_load(mecfn, meclist[1][0])
rates = [2520.72656, 132.55000, 1406.42651, 18731.98242, 566.22235, 20994.61133, 9.55771e+006,
          17867.06055, 1.04155e+007, 999938.00000, 4.77886e+006, 26800.59180, 12456.89160,
          14022.08691, 2425.19238, 32008.14258, 8554.56738, 130096.73438, 5703.04492, 260193.46875,
          2851.52246, 390290.21875]
mec.set_rateconstants(rates)
mec = flip_constrain_dala(mec)
#mec.printout()
theta = mec.theta()
#print('\nNumber of free parameters = ', len(np.log(mec.theta())))

# LOAD DATA
scnfiles = [["F:/MCMC/datasets/Dalanine/E.SCN"], 
            ["F:/MCMC/datasets/Dalanine/F.SCN"],
            ["F:/MCMC/datasets/Dalanine/A.SCN"], 
            ["F:/MCMC/datasets/Dalanine/IA.SCN"],
            ["F:/MCMC/datasets/Dalanine/LA.SCN"], 
            ["F:/MCMC/datasets/Dalanine/HA.SCN"],
            ["F:/MCMC/datasets/Dalanine/Y.SCN"], 
            ["F:/MCMC/datasets/Dalanine/T.SCN"],
            ["F:/MCMC/datasets/Dalanine/U.SCN"]]
tr = [0.000030, 0.000030, 0.000030, 0.000030, 0.000030, 0.000030, 0.000030, 0.000030, 0.000030]
tc = [0.0006, 0.0005, 0.0006, -0.08, -0.08, -0.06, -0.003, -0.003, -0.003]
conc = [100e-6, 100e-6, 100e-6, 2000e-6, 2000e-6, 2000e-6, 10000e-6, 10000e-6, 10000e-6]

# Initaialise SCRecord instance.
recs = []
bursts = []
for i in range(len(scnfiles)):
    rec = dataset.SCRecord(scnfiles[i], conc[i], tr[i], tc[i])
    recs.append(rec)
    bursts.append(rec.bursts.intervals())    
    #rec.printout()

# Import HJCFIT likelihood function
kwargs = {'nmax': 2, 'xtol': 1e-12, 'rtol': 1e-12, 'itermax': 100,
    'lower_bound': -1e6, 'upper_bound': 0}
likelihood = []
for i in range(len(recs)):
    likelihood.append(Log10Likelihood(bursts[i], mec.kA,
        recs[i].tres, recs[i].tcrit, **kwargs))
Dala_data = (likelihood, mec, conc)
lik = HJCFIT_LogLik(np.log(mec.theta()), Dala_data)
print ("\nInitial likelihood = {0:.6f}".format(lik))

from samplers import MWGSampler
from proposals import RWMHProposal 
proposer = RWMHProposal(HJCFIT_LogLik, Dala_data, verbose=True)
# Initialise Sampler
sampler = MWGSampler(samples_draw=1000, notify_every=int(10), 
                     burnin_fraction=0.5, burnin_lag=50,
                     model=HJCFIT_LogLik, data=Dala_data, 
                     proposal=proposer.propose_component_log,
                     verbose=True)                         
start = time.clock()
S = sampler.sample_component(theta)
t = time.clock() - start
print ('\nCPU time in MWG sampler =', t)

np.savetxt('F:/MCMC/datasets/Dalanine/GlyR_Dala_megaset_MCMC_MWG.csv', S, delimiter=',')
#S = np.loadtxt('AChR_MCMC_MWG.csv', delimiter=',')

Lmax = S[-1].max()
print('Lmax = ', Lmax)
imax = np.where(S[-1] == S[-1].max())[0][0]
print('imax = ', imax)
print('pars=', S[:, imax])

par_names = ['alpha1', 'beta1', 'alpha2', 'beta2', 'alpha3', 'beta3',
             '2kf(-2)', 'gamma1', 'kf(+3)', 'gamma2', 'delta2', 'delta3', 
             'k(+3)', 'k(-1)', 'logLik']

display = DisplayResults(S, burnin=int(len(S[-1])/2), names=par_names)
#display.normalised = True
#display.show_labels = False
display.chains()
display.distributions()
display.corner()
#display.autocorrelations()
#display.correlations(3, 1)
