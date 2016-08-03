%%Run experiment

function RunExperiment(experimentNo,replicateNo)
    switch experimentNo
        case 1
            data_tres = 0.05; %perform an analysis at 0.05ms resolution
            Experiment1VaryResolutionTime(replicateNo,data_tres);
        case 2
            sprintf('Running MCMC Algorithms on Synthetic Data');
            sprintf('Generating synthetic data');
            ExperimentGenerateSyntheticDataset(replicateNo,'independent');
            sprintf('Running experiment for Figure 5 - MWG MCMC on Synthetic Data');
            Experiment2PilotMWGSyntheticMCMC(replicateNo);
            sprintf('Running experiment for Figure 6 - Adaptive MCMC on Synthetic Data');
            Experiment2AdaptiveSyntheticMCMC(replicateNo);
        case 3
            sprintf('Running MCMC Algorithms on Real Data');
            sprintf('Running experiment for Figure 7 - MWG MCMC on Real Data');
            Experiment3PilotMWGExperimentalMCMC(replicateNo);
            sprintf('Running experiment for Figure 8 - Adaptive MCMC on Real Data');
            Experiment3AdaptiveExperimentalMCMC(replicateNo);
        otherwise 
            error('Experiment unknown - please choose one of 1, 2, 3')     
    end
end
