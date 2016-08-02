REPLICATE_NO = 10;
[pathname,~,~] = fileparts(mfilename('fullpath'));

if ~isequal(exist(strcat(pathname,'/../../Results/'), 'dir'),7)
    mkdir(strcat(pathstr,'/../../Results/'))
end

RunExperiment(2,REPLICATE_NO);
RunExperiment(3,REPLICATE_NO);
RunExperiment(4,REPLICATE_NO);

GenerateFigures(2,REPLICATE_NO);
GenerateFigures(3,REPLICATE_NO);
GenerateFigures(4,REPLICATE_NO);