#from bicme.samplers.Metropolis_Hastings import MH
from bicme.samplers import Sampler

sampler = Sampler()
assert sampler.N == 100000
assert sampler.M == 100
assert sampler.model is None

