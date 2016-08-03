function GenerateFigures(experimentNo, replicateNo, removePreviousFigures)

%replicateNo=10 used for paper experiments;
[pathname,~,~] = fileparts(mfilename('fullpath'));

resultsDir = [pathname , '/../../Results/Figures/Paper/'];

if (removePreviousFigures)
    if (rmdir(resultsDir,'s') == 0)
        fprintf('Results directory will be created...\n')
    elseif (removePreviousFigures) 
        fprintf('Removing previous results...\n')
    end
    mkdir(resultsDir)
else
    fprintf('Previous results NOT removed...\n')
end

switch experimentNo
    case 1
        fprintf('Generating all figures for paper...\n')
        Figure3(replicateNo);
        Figure4(replicateNo);
        Figure5(replicateNo);
        Figure6(replicateNo);
        Figure7(replicateNo);
        Figure8(replicateNo);
        Figure10a();
        Figure10b();
    case 2
        fprintf('Generating synthetic results...\n')
        Figure3(replicateNo);
        Figure4(replicateNo);
        Figure5(replicateNo);
    case 3
        fprintf('Generating experimental results...\n')
        Figure6(replicateNo);
        Figure7(replicateNo);
        Figure8(replicateNo);   
    case 4
        fprintf('Generating likelihood comparison...\n')
        Figure10a();
        Figure10b();
    otherwise
        error('Experiment unknown, please choose 1, 2, 3 or 4')
end

end
