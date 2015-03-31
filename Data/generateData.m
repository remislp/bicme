function filenames = generateData(model,concs,required_transitions,params)

    %% Generate data for a model

    %example parameters
    %model = SevenState_10Param_AT();
    %concs = [0.0000003,0.000001];
    %required_transitions = [10000,10000];
    
    dc=DataController;
    filenames=cell(length(concs),1);
    [pathstr,~,~] = fileparts(mfilename('fullpath'));
    savedir = strcat(pathstr, '/Generated/');
    
    if ~isequal(exist(savedir, 'dir'),7)
        mkdir(savedir)
    end
    
    for set=1:length(concs)
        recording = simulateData(params,model,concs(set),required_transitions(set));
        [~,tmpname,~]=fileparts(tempname);
        filenames{set} = strcat(pathstr, '/Generated/', num2str(required_transitions(set)),'_' ,tmpname,'_Synth_Ach_',num2str(concs(set)),'.scn');
        handle = fopen(filenames{set},'w');
        dc.write_scn_file(handle,recording);
    end

end