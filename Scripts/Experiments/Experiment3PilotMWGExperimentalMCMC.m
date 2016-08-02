function Experiment3PilotMWGExperimentalMCMC(replicate)

    fprintf('Pilot MCMC sampling on Real Data From Hatton 2003 Fig 11... \n')

    fprintf('Loading data\n')
    [pathstr,name,~] = fileparts(mfilename('fullpath'));
    data = load(strcat(pathstr,'/../../Data/Experimental/AchRealData.mat'));
    model = SevenState_10Param_AT();

    %% sampling parameters
    fprintf('Setting up MCMC parameters...\n')
    SamplerParams.Samples=10000;
    SamplerParams.Burnin=5000;
    SamplerParams.AdjustmentLag=50; 
    SamplerParams.NotifyEveryXSamples=1000;
    SamplerParams.ScaleFactor=0.1;
    SamplerParams.LowerAcceptanceLimit=0.1;
    SamplerParams.UpperAcceptanceLimit=0.5;

    load(strcat(pathstr,'/../../Data/Synthetic/SevenStateGuessesAndParams.mat'))

    startParams=guess2(ten_param_keys);

    proposalScheme = LogRwmhProposal(eye(model.k,model.k),1);

    %% Set up the sampler
    MCMCsampler = Sampler();

    %% Sample!
    fprintf('Performing MCMC sampling...\n')
    rng_setting=rng(replicate);
    samples=MCMCsampler.cwSample(SamplerParams,model,data,proposalScheme,startParams');

    fprintf('Saving MCMC results...\n')
    save(strcat(pathstr,'/../../Results/',name,num2str(replicate),'.mat'))
end