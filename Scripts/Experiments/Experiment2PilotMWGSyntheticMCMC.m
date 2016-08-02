
function Experiment2PilotMWGSyntheticMCMC(replicate)

    fprintf('Running the Pilot MCMC scheme on synthetically generated data... \n')
    [pathstr,name,~] = fileparts(mfilename('fullpath'));
    %% sampling parameters
    fprintf('Setting up MCMC sampling... \n')
    model = SevenState_10Param_AT();

    SamplerParams.Samples=10000;
    SamplerParams.Burnin=5000;
    SamplerParams.AdjustmentLag=50; 
    SamplerParams.NotifyEveryXSamples=1000;
    SamplerParams.ScaleFactor=0.1;
    SamplerParams.LowerAcceptanceLimit=0.1;
    SamplerParams.UpperAcceptanceLimit=0.5;

    data = load(strcat(pathstr,'/../../Data/Synthetic/Ach', num2str(replicate), '.mat'));

    %start params
    load([pathstr , '/../../Data/Synthetic/SevenStateGuessesAndParams.mat'])
    startParams=guess2(ten_param_keys);

    proposalScheme = LogRwmhProposal(eye(model.k,model.k),1);

    %% Set up the sampler
    MCMCsampler = Sampler();

    %% Sample!
    fprintf('Running up MCMC sampling... \n')
    samples=MCMCsampler.cwSample(SamplerParams,model,data,proposalScheme,startParams');
    fprintf('Saving results... \n')
    save(strcat(pathstr,'/../../Results/',name,num2str(replicate),'.mat'))
end

