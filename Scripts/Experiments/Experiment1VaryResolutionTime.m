%% Script to compare the Siekmann likelihood with missed events with the same data
function Experiment1VaryResolutionTime(replicate,data_tres)

    fprintf('Performing experiment as per Siekmann 2012...\n')
    rng_setting=rng(replicate);    
    fprintf('Using random number generator %s with seed %s...\n', rng_setting.Type, num2str(rng_setting.Seed))
    fprintf('Generating data with resolution %.4f ms...\n',data_tres)

    %% Data Generation - perfect resolution
    [pathstr,name,~] = fileparts(mfilename('fullpath'));
    intervals = 18000; %about 100,000 data points as per Siekmann 2012
    model = FourState_6Param_S();
    generativeParams=[3.5; 0.1; 7; 0.4; 0.05; 0.5]; 

    concs = 1; %agonist concentration is irrelevent
    tres = 0.05; %sampling time
    %data_tres = 0.025; %resolution time of the data
    tcrit = 9999; %treat as one long interval
    filenames = generateData(model,concs,intervals,generativeParams);

    %parse these data files
    bursts=cell(1,length(concs));
    for i=1:length(concs)
        [~,intervaldata]=DataController.read_scn_file(filenames{i});
        intervaldata.intervals=intervaldata.intervals/1000; %intervals are factored up by 1,000 relative to time scale

        resolvedData= RecordingManipulator.imposeResolution(intervaldata,data_tres);
        rawbursts = RecordingManipulator.getBursts(resolvedData,tcrit(i));
        stripped_bursts = [rawbursts.withinburst];
        bursts{i} = {stripped_bursts.intervals};
    end

    data.bursts = bursts;
    data.concs = concs;
    data.tres = tres; %in msec
    data.tcrit = tcrit; %treat all data as one 'burst' interval
    data.data_tres = data_tres;

    %% Perform the Siekmann analysis
    % MCMC Sampling
    fprintf('Setting up MCMC parameters...\n')
    %%sampler params here
    SamplerParams.Samples=30000;
    SamplerParams.Burnin=15000;
    SamplerParams.AdjustmentLag=50; 
    SamplerParams.NotifyEveryXSamples=1000;
    SamplerParams.ScaleFactor=0.1;
    SamplerParams.LowerAcceptanceLimit=0.1;
    SamplerParams.UpperAcceptanceLimit=0.5;

    % Set up the sampler
    MCMCsampler = Sampler();

    %proposal defined
    delta = 0.05;
    proposalScheme = SiekmannProposal(delta);
    startParams = [1; 0.1; 1; 0.4; 0.05; 0.5];

    % Sample!
    fprintf('Running MCMC sampling...\n')
    samples=MCMCsampler.blockSample(SamplerParams,model,data,proposalScheme,startParams);

    fprintf('Saving MCMC samples...\n')
    save(strcat(pathstr,'/../../Results/',name, '_' , num2str(replicate) , '_',num2str(data_tres) ,'ms_Siek.mat'))

    %% Perform the inference with missed events
    clearvars -except filenames pathstr name SamplerParams generativeParams replicate rng_setting data_tres
    model = FourState_6Param_AT();
    MSEC = 1000; %convert to seconds
    
    tres = data_tres/MSEC; %sampling resolution time in seconds
    data_tres = data_tres/MSEC; %resolution time of the data in seconds
    tcrit = 9999; %treat as one long interval
    concs = 1; %agonist concentration is irrelevent
    
    %parse these data files
    bursts=cell(1,length(concs));
    for i=1:length(concs)
        [~,intervaldata]=DataController.read_scn_file(filenames{i});
        intervaldata.intervals=intervaldata.intervals/(MSEC^2); %convert intervals to seconds

        resolvedData= RecordingManipulator.imposeResolution(intervaldata,data_tres);
        rawbursts = RecordingManipulator.getBursts(resolvedData,tcrit(i));
        stripped_bursts = [rawbursts.withinburst];
        bursts{i} = {stripped_bursts.intervals};
    end

    data.bursts = bursts;
    data.concs = concs;
    data.tres = tres; %in seconds
    data.tcrit = tcrit; %treat all data as one 'burst' interval
    data.data_tres = data_tres;
    data.useChs = 0;

    % Set up the sampler
    MCMCsampler = Sampler();

    %proposal defined
    proposalScheme = LogRwmhProposal(eye(model.k,model.k),1);
    startParams = [1; 0.1; 1; 0.4; 0.05; 0.5] * MSEC;

    % Sample!
    fprintf('Running MCMC sampling...\n')
    samples=MCMCsampler.cwSample(SamplerParams,model,data,proposalScheme,startParams);
    fprintf('Saving samples...\n')
    save(strcat(pathstr,'/../../Results/',name, '_' , num2str(replicate) , '_',num2str(data_tres*MSEC) ,'ms_MissedEvents.mat'))
    
end
