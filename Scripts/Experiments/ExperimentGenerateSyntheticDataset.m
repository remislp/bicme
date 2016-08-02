function ExperimentGenerateSyntheticDataset(replicate,binding)    
    rng_setting=rng(replicate);
    fprintf('Using random number generator %s with seed %d...\n', rng_setting.Type, num2str(rng_setting.Seed))

    [pathstr,~,~] = fileparts(mfilename('fullpath'));
    sprintf('Generating data... \n')



    load([pathstr , '/../../Data/Synthetic/SevenStateGuessesAndParams.mat'])
    
    switch binding
        
        case 'independent'
            generativeParams = true1(thirteen_param_keys);
            tres =  [2.5e-5,2.5e-5,2.5e-5];
            concs = [0.00000003 0.0000001 0.00001];
            tcrit = [0.0035 0.0035 0.005 ];
            useChs= [1 1 0];
            required_transitions = [20000 20000 20000];
            desensParams = [generativeParams 5 1.4];

            filenames = generateData(SevenState_13Param_QET(),concs(1:2),required_transitions(1:2),generativeParams);
            filenames(3) = generateData(EightState_15Param_AT(),concs(3),required_transitions(3),desensParams);            
        case 'dependent'
            generativeParams = true2(thirteen_param_keys);
            tres =  [1e-5,1e-5,1e-5];
            concs = [0.00000001 0.00000003 0.0000001];
            tcrit = [0.0035 0.0035 0.0035 ];
            useChs= [1 1 1];
            required_transitions = [20000 20000 20000];
            filenames = generateData(SevenState_13Param_QET(),concs,required_transitions,generativeParams);
        otherwise
            error(['Unknown binding type ' binding])
    end
    



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

    save(strcat(pathstr,'/../../Data/Synthetic/Ach', num2str(replicate), '.mat'),'filenames','tres','concs','tcrit','useChs','generativeParams','openIntervals','shutIntervals','bursts')
end