function Experiment4AdaptiveSyntheticMCMC(replicate)
    

    [pathstr,name,~] = fileparts(mfilename('fullpath'));
    %load data generated in pilot experiment
    data = load(strcat(pathstr,'/../../Data/Synthetic/Ach', num2str(replicate), '.mat'));
    model = SevenState_13Param_QET();

    %% sampling parameters
    SamplerParams.Samples=100000;
    SamplerParams.Burnin=50000;
    SamplerParams.AdjustmentLag=50; 
    SamplerParams.NotifyEveryXSamples=1000;
    SamplerParams.ScaleFactor=0.1;
    SamplerParams.LowerAcceptanceLimit=0.1;
    SamplerParams.UpperAcceptanceLimit=0.5;

    load(strcat(pathstr,'/../../Data/Synthetic/SevenStateGuessesAndParams.mat'))
    load(strcat(pathstr,'/../../Results/Experiment4PilotMWGSyntheticMCMC',num2str(replicate),'.mat'),'samples')

    [maxPosterior, maxIndex] = max(samples.posteriors);

    fprintf('Starting sampling at reasonable estimate of max posterior %.4f\n',maxPosterior(end))

    startParams=samples.params(maxIndex(end),:)';

    clear samples;

    proposalScheme = RwmhMixtureProposal(eye(model.k,model.k),0);

    %% Set up the sampler
    MCMCsampler = RosenthalAdaptiveSampler();

    %% Sample!
    sprintf('MCMC sampling... \n')
    samples=MCMCsampler.blockSample(SamplerParams,model,data,proposalScheme,startParams);
    
    fprintf('Saving results... \n')
    save(strcat(pathstr,'/../../Results/',name,num2str(replicate),'.mat'))

end