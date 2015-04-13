%% Script to compare the Siekmann likelihood with missed events with the same data
function Ex5InitialAllTogetherPerfectResolution(replicate)

    fprintf('Generating data...\n')
    %% Data Generation - perfect resolution
    [pathstr,name,~] = fileparts(mfilename('fullpath'));
    intervals = 18000; %about 100,000 data points as per Siekmann 2012
    model = FourState_6Param_S();
    generativeParams=[3.5; 0.1; 7; 0.4; 0.05; 0.5]; 

    concs = 1; %agonist concentration is irrelevent
    tres = 0.05; %sampling resolution time
    tcrit = 9999; %treat as one long interval
    filenames = generateData(model,concs,intervals,generativeParams);

    %parse these data files
    bursts=cell(1,length(concs));
    openIntervals = cell(1,length(concs));
    shutIntervals = cell(1,length(concs));
    for i=1:length(concs)
        [~,intervaldata]=DataController.read_scn_file(filenames{i});
        intervaldata.intervals=intervaldata.intervals/1000; %intervals are factored up by 1,000 relative to time scale

        resolvedData= RecordingManipulator.imposeResolution(intervaldata, 0.0); %impose with perfect resolution
        rawbursts = RecordingManipulator.getBursts(resolvedData , tcrit(1));
        stripped_bursts = [rawbursts.withinburst];
        bursts{i} = {stripped_bursts.intervals};
    end

    data.bursts = bursts;
    data.concs = concs;
    data.tres = tres; %in msec
    data.tcrit = tcrit; %treat all data as one 'burst' interval

    %% Perform the Siekmann analysis
    % MCMC Sampling
    fprintf('Experiment 1: Performing experiment as per Siekmann 2012...\n')
    fprintf('Setting up MCMC parameters for first experiment...\n')
    %%sampler params here
    SamplerParams.Samples=30000;
    SamplerParams.Burnin=10000;
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
    fprintf('Running MCMC sampling for first experiment...\n')
    rng('shuffle')
    t=rng;
    samples=MCMCsampler.blockSample(SamplerParams,model,data,proposalScheme,startParams);

    fprintf('Saving MCMC samples from first experiment...\n')
    
    if ~isequal(exist(strcat(pathstr,'/../Results/'), 'dir'),7)
        mkdir(strcat(pathstr,'/../Results/'))
    end
    
    save(strcat(pathstr,'/../Results/',name, '_' , replicate ,'_Siek.mat'))

    %% Perform the inference with missed events
    fprintf('Experiment 2: Performing experiment with missed events...\n')
    clearvars -except filenames pathstr name SamplerParams generativeParams

    model = FourState_6Param_AT();
    tres = 0.0; %sampling resolution time in seconds
    tcrit = 9999; %treat as one long interval
    concs = 1; %agonist concentration is irrelevent
    MSEC = 1000; %need to adjust data into seconds

    %parse these data files
    bursts=cell(1,length(concs));
    for i=1:length(concs)
        [~,intervaldata]=DataController.read_scn_file(filenames{i});
        intervaldata.intervals=intervaldata.intervals/(MSEC^2); %intervals in seconds

        resolvedData= RecordingManipulator.imposeResolution(intervaldata,0.0);
        rawbursts = RecordingManipulator.getBursts(resolvedData,tcrit(i));
        stripped_bursts = [rawbursts.withinburst];
        bursts{i} = {stripped_bursts.intervals};
    end

    data.bursts = bursts;
    data.concs = concs;
    data.tres = tres; %in msec
    data.tcrit = tcrit; %treat all data as one 'burst' interval
    data.useChs = 0;

    % Set up the sampler
    MCMCsampler = Sampler();

    %proposal defined
    proposalScheme = LogRwmhProposal(eye(model.k,model.k),1);
    startParams = [1; 0.1; 1; 0.4; 0.05; 0.5] * MSEC;

    % Sample!
    fprintf('Performing MCMC sampling for second experiment...\n')
    rng('shuffle')
    t=rng;
    samples=MCMCsampler.cwSample(SamplerParams,model,data,proposalScheme,startParams);
    fprintf('Saving samples for second experiment...\n')
    save(strcat(pathstr,'/../Results/',name, '_' , replicate , '_MissedEvents.mat'))

end
