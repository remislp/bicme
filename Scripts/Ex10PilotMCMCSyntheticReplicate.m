function Ex10PilotMCMCSyntheticReplicate(replicate)

    fprintf('Running the Pilot MCMC scheme on synthetically generated data... \n')

    rng('shuffle')
    rng_setting=rng;
    fprintf('Using random number generator %s with seed %s...\n', rng_setting.Type, num2str(rng_setting.Seed))

    [pathstr,name,~] = fileparts(mfilename('fullpath'));
    sprintf('Generating data... \n')

    tres =  [2e-5,2e-5,2e-5];
    concs = [0.00000003 0.0000001 0.00001];
    tcrit = [0.0035 0.0035 0.005 ];
    useChs= [1 1 0];
    required_transitions = [20000 20000 20000];

    load([pathstr , '/../Data/Synthetic/SevenStateGuessesAndParams.mat'])
    generativeParams = true1(thirteen_param_keys);
    desensParams = [generativeParams 5 1.4];

    filenames = generateData(SevenState_13Param_QET(),concs(1:2),required_transitions(1:2),generativeParams);
    filenames(3) = generateData(EightState_15Param_AT(),concs(3),required_transitions(3),desensParams);

    %parse these data files
    bursts=cell(1,length(concs));
    openIntervals = cell(1,length(concs));
    shutIntervals = cell(1,length(concs));
    for i=1:length(concs)
        [~,data]=DataController.read_scn_file(filenames{i});
        data.intervals=data.intervals/1000;
        resolvedData = RecordingManipulator.imposeResolution(data,tres(i));

        %get open and closed resolved intervals
        [openScn, shutScn] = RecordingManipulator.getPeriods(resolvedData);
        rawbursts = RecordingManipulator.getBursts(resolvedData,tcrit(i));
        stripped_bursts = [rawbursts.withinburst];
        bursts{i} = {stripped_bursts.intervals};
        openIntervals{i} = openScn.intervals;
        shutIntervals{i} = shutScn.intervals;
    end

    save(strcat(pathstr,'/../Data/Synthetic/Ach', num2str(replicate), '.mat'),'tres','concs','tcrit','useChs','generativeParams','openIntervals','shutIntervals','bursts')

    clearvars -except pathstr name replicate rng_setting;

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

    data = load(strcat(pathstr,'/../Data/Synthetic/Ach', num2str(replicate), '.mat'));

    %start params
    load([pathstr , '/../Data/Synthetic/SevenStateGuessesAndParams.mat'])
    startParams=guess2(ten_param_keys);

    proposalScheme = LogRwmhProposal(eye(model.k,model.k),1);

    %% Set up the sampler
    MCMCsampler = Sampler();

    %% Sample!
    fprintf('Running up MCMC sampling... \n')
    samples=MCMCsampler.cwSample(SamplerParams,model,data,proposalScheme,startParams');

    fprintf('Saving results... \n')

    if ~isequal(exist(strcat(pathstr,'/../Results/'), 'dir'),7)
        mkdir(strcat(pathstr,'/../Results/'))
    end

    save(strcat(pathstr,'/../Results/',name,num2str(replicate),'.mat'))
end
