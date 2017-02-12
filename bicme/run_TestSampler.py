import math
import numpy as np
import scipy.io as sio
import scipy.stats

from samplers import MWGSampler
from proposals import RWMHProposal
from display import quick_display

def norm_logPosterior(X, y):
    return norm_logLik(X, y) + norm_logPrior(X)

def norm_logLik(X, y):
    return -0.5 * (len(y) * math.log(2 * math.pi * math.pow(X[1], 2)) +
            (1 / math.pow(X[1], 2)) * np.sum(np.power(y - X[0], 2)))
    #return np.sum(np.log(scipy.stats.norm.pdf(y, X[0], X[1]))) 
    


def norm_logPrior(X):
    mu_lims = [-20, 20]
    si_lims = [0, 100]
    return (np.log(scipy.stats.uniform.pdf(X[0], mu_lims[0], mu_lims[1])) 
              + np.log(scipy.stats.uniform.pdf(X[1], si_lims[0], si_lims[1])))

def test_normal_case_MWG(data):
    
    X0 = [2, 10]
    # Initialise Proposer
    proposer = RWMHProposal(norm_logPosterior, data, verbose=True)

    # Initialise Sampler
    sampler = MWGSampler(samples_draw=100000, notify_every=1000, 
                         burnin_fraction=0.5, burnin_lag=50,
                         model=norm_logPosterior, data=data, 
                         proposal=proposer.propose_component,
                         verbose=True)                         
    # Sample
    S = sampler.sample_component(X0)

    #print('acceptances= ', sampler.acceptances)
    #print('proposals= ', sampler.all_proposals)
    #print('samples= ', sampler.all_samples)

    quick_display(S, burnin=5000)

mat1 = sio.loadmat('../Tests/Data/NormData.mat')
#for key, value in mat1.items() :
#    print (key)
data = np.array(mat1['data']).flatten()
#print('data: ', data)

X0 = [1.3509862348087593, 11.1811660419655325]
print('X0= ', X0)
print('logLik= ', norm_logPosterior(X0, data))
X1 = [-0.1950727276889210, 10.4227127446818404]
print('X1= ', X1)
print('logLik= ', norm_logPosterior(X1, data))


#data = np.array([-1.97794885e+01, 1.04568872e+01, 5.14080369e+00, -1.21177720e+00])

#test_normal_case_MWG(data)