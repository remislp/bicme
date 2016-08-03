REPLICATE_NO = 10;
REMOVE_PREVIOUS_FIGURES = 1;
GENERATE_ALL_FIGURES = 1;

[pathname,~,~] = fileparts(mfilename('fullpath'));

if ~isequal(exist(strcat(pathname,'/../../Results/'), 'dir'),7)
    mkdir(strcat(pathstr,'/../../Results/'))
end

RunExperiment(2, REPLICATE_NO);
RunExperiment(3, REPLICATE_NO);

GenerateFigures(GENERATE_ALL_FIGURES, REPLICATE_NO, REMOVE_PREVIOUS_FIGURES);