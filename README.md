# bicme - Bayesian Analysis of Ion-channels with Missed Events

This is code used in our recent paper **"Bayesian Statistical Inference in Ion-Channel Models with Exact Missed Event Correction"** that appeared in *Biophysical Journal in 2016* (doi: 10.1016/j.bpj.2016.04.053), available [here](http://www.cell.com/biophysj/fulltext/S0006-3495(16)30450-7)

# Prequisites

1. A C++11 compiler installed - required for steps 2 and 4
2. Install the DCPROGS c++ library - this is a reimplementation of the Colquhoun & Hawkes likelihood calculation originally written in Fortran. The library is available [here](https://github.com/DCPROGS/HJCFIT) with required documentation and installation wiki.
3. Matlab 2014b installed.
4. An ability to compile mex functions using the command line. Scripts are provided for Mac OSX (10.11) and Linux but may need some caressing to compile the mex functions so that they can be called in matlab

# Installation and Testing steps

## Command line steps
1. Check out the bicme repo at [github](https://github.com/miepstei/bicme)
2. Compile the mex functions from the command line. There is a shell script in `C/compile_mex.sh` which can serve as a template for compilation. This step compiles the mex files which wrap around calls to the C++ library so they can be called from MATLAB.

## MATLAB steps
3. Within MATLAB, add the base of the repo to the MATLAB path from the directory tree (right-click -> "add to path")
4. Run the Unit tests. There are tests in the `Tests/` directory that test models, likelihood calculations and data parsing.
To run the tests:
	`cd Tests`
	`tests = matlab.unittest.TestSuite.fromFolder('.')`
	`run(tests)`

# To run the examples from the paper...

There is a single main script called `RunAllExperiments` which should be on the MATLAB path. This will take a long time to complete.
Instead, each set of experiments can be run individually. This requires setting a `replicateNo` that seeds the RND.

1. The synthetic experiments (Figures 3, 4 and 5) can be run as follows:
	`synthetic = 2; replicateNo = 10; RunExperiment(synthetic, replicateNo); GenerateFigures(synthetic, replicateNo) `
	
2. The experiments on the real data (Figures 6, 7, 8) can be run as follows:
	`real = 3; replicateNo = 10; RunExperiment(real, replicateNo); GenerateFigures(synthetic, replicateNo)`
	
3. The comparison experiment (Figure10) can be plotted as follows. This performs just the HJCFit likelihood calculation against prior derived results from Siekmann et al. 2012
	`comparison = 4; replicateNo = 10; RunExperiment(comparison, replicateNo); GenerateFigures(comparison, replicateNo)`
	
All the plotted eps output is produced in `Results/Figures/Paper`
	
# third party acknowledgements

## I have vectorised a version of John D'Errico's `Hessian` calculation available on [Mathworks](http://uk.mathworks.com/matlabcentral/fileexchange/13490-adaptive-robust-numerical-differentiation/content/DERIVESTsuite/hessian.m) to calculate the Hessian numerically using finite differences.
## I have modified plotting functions described in this presentation[http://www.gatsby.ucl.ac.uk/~turner/TeaTalks/matlabFigs/matlabFig.pdf] in order to produce reasonable MATLAB figures.



 

