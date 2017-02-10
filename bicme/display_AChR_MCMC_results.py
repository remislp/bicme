import numpy as np
#from display import quick_display

S1 = np.loadtxt('AChR_MCMC_multiplicative_100k.csv', delimiter=',')
print(S1.shape)
S = S1[: , 5::6]
#quick_display(S, burnin=5000)

from display import DisplayResults

par_names = ['beta1', 'beta2', 'alpha1', 'alpha2', 'k(-1)', 'k(+2)', 'logLik']

display = DisplayResults(S, burnin=50000, names=par_names)
#display.normalised = True
#display.show_labels = False

display.corner()

#display.chains()
#display.distributions()
#display.autocorrelations()
#display.correlations(3, 1)
