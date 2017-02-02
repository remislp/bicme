import numpy as np
from display import quick_display

S = np.loadtxt('AChR_MCMC.csv', delimiter=',')
quick_display(S, burnin=5000)


