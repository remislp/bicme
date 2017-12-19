import numpy as np
import scipy.io as sio


from bicme.samplers import MWGSampler
#from bicme.samplers import RosenthalAdaptiveSampler
from bicme.proposals import RWMHProposal
from bicme.tests.case_normal import CaseNormal

class TestMWGSampler:
    def setUp(self):
        mat1 = sio.loadmat('../BICME/Tests/Data/NormData.mat')
        data = np.array(mat1['data']).flatten()
        self.cn = CaseNormal(data)
        self.X0 = [2, 10]
        
    def tearDown(self):
        pass

    def test_normal_block(self):
        # Initialise Proposer
        proposer = RWMHProposal(self.cn.logPosterior, verbose=True)
        sampler = MWGSampler(samples_draw=10, notify_every=1, 
                         burnin_fraction=0.5, burnin_lag=5,
                         model=self.cn.logPosterior,  
                         proposal=proposer.propose_block,
                         verbose=True)  
        sampler.acceptance_limits = [0.3, 0.7]
        sampler.scale = 0.5
        #np.random.seed(1)
        S = sampler.sample_block(self.X0)
        assert sampler.N == 10
        print('acceptances= ', sampler.acceptances)
#        np.testing.assert_array_equal(sampler.acceptances, np.array([ 0.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,  1.]))
#        np.testing.assert_allclose(sampler.samples, 
#            [np.array([    2.        ,    10.        , -1125.99943572]), 
#             np.array([    2.        ,    10.        , -1125.99943572]), 
#             np.array([    2.        ,    10.        , -1125.99943572]), 
#             np.array([    2.        ,    10.        , -1125.99943572]), 
#             np.array([    2.        ,    10.        , -1125.99943572]), 
#             np.array([    2.        ,    10.        , -1125.99943572]), 
#             np.array([    1.77201661,     9.72843256, -1124.74956645]), 
#             np.array([    1.77201661,     9.72843256, -1124.74956645]), 
#             np.array([    1.77201661,     9.72843256, -1124.74956645]), 
#             np.array([    1.80186624,    10.14054515, -1124.77280787])],  
#             rtol=1e-07)

    def test_normal_component(self):
        # Initialise Proposer
        proposer = RWMHProposal(self.cn.logPosterior, verbose=True)
        sampler = MWGSampler(samples_draw=5, notify_every=1, 
                         burnin_fraction=0.5, burnin_lag=3,
                         model=self.cn.logPosterior,  
                         proposal=proposer.propose_component,
                         verbose=True)  
        sampler.acceptance_limits = [0.3, 0.7]
        sampler.scale = 0.5
        #np.random.seed(1)
        S = sampler.sample_component(self.X0)
        assert sampler.N == 5
        print('acceptances= ', sampler.acceptances)
#        np.testing.assert_array_equal(sampler.acceptances, 
#            np.array([[ 0.,  0.,  0.,  1.,  1.], [ 0.,  0.,  1.,  0.,  1.]]))
        print('samples= ', sampler.samples)
#        np.testing.assert_allclose(sampler.samples, 
#            [np.array([    2.        ,    10.        , -1125.99943572]), 
#             np.array([    2.        ,    10.        , -1125.99943572]), 
#             np.array([    2.        ,     9.8623926 , -1126.09264797]), 
#             np.array([    1.78865897,     9.8623926 , -1124.68717786]), 
#             np.array([    1.69108142,    10.13314303, -1124.11683614])],  
#             rtol=1e-07)
  


