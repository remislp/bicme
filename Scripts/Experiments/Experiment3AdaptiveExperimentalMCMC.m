function Experiment3AdaptiveExperimentalMCMC(replicate)
fprintf('Pilot MCMC sampling on Real Data From Hatton 2003 Fig 11... \n')

fprintf('Loading data\n')
[pathstr,name,~] = fileparts(mfilename('fullpath'));
data = load(strcat(pathstr,'/../../Data/Experimental/AchRealData.mat'));
model = SevenState_10Param_AT();

%% sampling parameters
fprintf('Setting up MCMC parameters...\n')
SamplerParams.Samples=100000;
SamplerParams.Burnin=50000;
SamplerParams.AdjustmentLag=50; 
SamplerParams.NotifyEveryXSamples=1000;
SamplerParams.ScaleFactor=0.1;
SamplerParams.LowerAcceptanceLimit=0.1;
SamplerParams.UpperAcceptanceLimit=0.5;

load(strcat(pathstr,'/../../Data/Synthetic/SevenStateGuessesAndParams.mat'))

load(strcat(pathstr,'/../../Results/Experiment3PilotMWGExperimentalMCMC',num2str(replicate),'.mat'),'samples')

[maxPosterior, maxIndex] = max(samples.posteriors);

fprintf('Starting sampling at reasonable estimate of max posterior %.4f\n',maxPosterior(end))

startParams=samples.params(maxIndex(end),:);
clear samples;

proposalScheme = RwmhMixtureProposal(eye(model.k,model.k),0);

%% Set up the sampler
MCMCsampler = RosenthalAdaptiveSampler();

%% Sample!
fprintf('Performing MCMC sampling...\n')
rng_setting=rng(replicate);
samples=MCMCsampler.blockSample(SamplerParams,model,data,proposalScheme,startParams');

fprintf('Saving MCMC results...\n')
save(strcat(pathstr,'/../../Results/',name,num2str(replicate),'.mat'))