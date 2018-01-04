import numpy as np
import scipy.io as sio

from bicme.samplers import MWGSampler
from bicme.samplers import RosenthalAdaptiveSampler
from bicme.proposals import RWMHProposal
from bicme.tests.case_normal import CaseNormal

class TestRegressionMWGSamplerBlock:
    def setUp(self):
        mat1 = sio.loadmat('../BICME/Tests/Data/NormData.mat')
        data = np.array(mat1['data']).flatten()
        cn = CaseNormal(data)
        X0 = [2, 10]
        
        # Initialise Proposer
        proposer = RWMHProposal(cn.logPosterior, verbose=True)
        sampler = MWGSampler(samples_draw=10, notify_every=1, 
                         burnin_fraction=0.5, burnin_lag=5,
                         model=cn.logPosterior,  
                         proposal=proposer.propose_block,
                         verbose=True)  
        sampler.acceptance_limits = [0.3, 0.7]
        sampler.scale = 0.5
        np.random.seed(1)
        self.S = sampler.sample_block(X0)
        
    def tearDown(self):
        self.S = None

    def test_sample_number(self):
        assert self.S.N == 10
        
    def test_acceptances(self):
        np.testing.assert_array_equal(self.S.acceptances, np.array([ 0.,  1.,  0.,  0.,  0.,  1.,  0.,  0.,  1.,  1.]))
        
    def test_samples(self):
        np.testing.assert_allclose(self.S.samples, 
            [[  2.      ,   1.197827,   1.197827,   1.197827,   1.197827,
            0.969844,   0.969844,   0.969844,   0.191588,   0.829109],
            [ 10.      ,   9.551122,   9.551122,   9.551122,   9.551122,
            9.279555,   9.279555,   9.279555,  10.088997,  10.444314]],
            rtol=1e-05)
    
    def test_posteriors(self):
        np.testing.assert_allclose(self.S.posteriors, 
            [-1125.999436, -1121.863417, -1121.863417, -1121.863417,
            -1121.863417, -1121.695805, -1121.695805, -1121.695805,
            -1118.764857, -1121.048132],
            rtol=1e-05)


class TestRegressionMWGSamplerComponent:
    def setUp(self):
        mat1 = sio.loadmat('../BICME/Tests/Data/NormData.mat')
        data = np.array(mat1['data']).flatten()
        cn = CaseNormal(data)
        X0 = [2, 10]

        # Initialise Proposer
        proposer = RWMHProposal(cn.logPosterior, verbose=True)
        sampler = MWGSampler(samples_draw=5, notify_every=1, 
                         burnin_fraction=0.5, burnin_lag=3,
                         model=cn.logPosterior,  
                         proposal=proposer.propose_component,
                         verbose=True)  
        sampler.acceptance_limits = [0.3, 0.7]
        sampler.scale = 0.5
        np.random.seed(1)
        self.S = sampler.sample_component(X0)
        
    def test_sample_number(self):
        assert self.S.N == 5
    
    def test_acceptances(self):
        np.testing.assert_array_equal(self.S.acceptances, 
            np.array([[ 0.,  1.,  1.,  1.,  1.], [ 0.,  0.,  0.,  1.,  0.]]))
            
    def test_samples(self):
        np.testing.assert_allclose(self.S.samples, 
            [[  2.      ,   1.471828,  -0.89164 ,  -0.572601,   0.889507],
            [ 10.      ,  10.      ,  10.      ,   9.75063 ,   9.75063 ]],  
            rtol=1e-05)
             
    def test_posteriors(self):
        np.testing.assert_allclose(self.S.posteriors, 
            [[-1125.999436, -1122.833978, -1118.920605, -1118.470482,
            -1120.278702],
            [-1125.999436, -1122.833978, -1118.920605, -1118.339701,
            -1120.278702]],  
            rtol=1e-05)
  
    def tearDown(self):
        self.S = None


class TestRegressionRosenthalAdaptiveSamplerMixture:
    def setUp(self):
        mat1 = sio.loadmat('../BICME/Tests/Data/NormData.mat')
        data = np.array(mat1['data']).flatten()
        cn = CaseNormal(data)
        X0 = [1, 12]
        
        # Initialise Proposer
        proposer = RWMHProposal(cn.logPosterior, verbose=True)                      
        sampler = RosenthalAdaptiveSampler(samples_draw=10, 
                            notify_every=1, burnin_fraction=0.5, 
                            burnin_lag=5, model=cn.logPosterior,  
                            proposal=proposer.propose_block_mixture,
                            verbose=True)
                         
        sampler.acceptance_limits = [0.3, 0.7]
        sampler.scale = 0.01
        np.random.seed(2)
        self.S = sampler.sample_block(X0)

    def tearDown(self):
        self.S = None

    def test_sample_number(self):
        assert self.S.N == 10
        
    def test_acceptances(self):
        np.testing.assert_array_equal(self.S.acceptances, np.array([ 1.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]))
        
    def test_samples(self):
        np.testing.assert_allclose(self.S.samples, 
            [[  0.326148,  -2.539362,  -2.539362,  -2.539362,  -2.539362,
            -2.539362,  -2.539362,  -2.539362,  -2.539362,  -2.539362],
            [ 11.915842,  10.56568 ,  10.56568 ,  10.56568 ,  10.56568 ,
            10.56568 ,  10.56568 ,  10.56568 ,  10.56568 ,  10.56568 ]],
            rtol=1e-05)
    
    def test_posteriors(self):
        np.testing.assert_allclose(self.S.posteriors, 
            [-1128.819306, -1126.841037, -1126.841037, -1126.841037,
            -1126.841037, -1126.841037, -1126.841037, -1126.841037,
            -1126.841037, -1126.841037],
            rtol=1e-05)
        
        
