
function ExperimentCalculateESS(replicate)
    ALPHA_2 = 1;

    fprintf('Calculating ESS statistics for synthetic MWG and Adaptive samplers... \n')
    [pathstr,~,~] = fileparts(mfilename('fullpath'));
    % sampling parameters
    mwg = load(strcat(pathstr,'/../../Results/Experiment2PilotMWGSyntheticMCMC',num2str(replicate),'.mat'));
    mwg_burnin = mwg.SamplerParams.Burnin + 1;
    
    %calculate the autocorrelation coefficients and the bounds
    [acf,~,bounds] = autocorr(mwg.samples.params(mwg_burnin:end,ALPHA_2),200);
    
    %calculate the first furthest significant lag
    significantLag = find(acf < bounds(1), 1) - 1;
    [~,~,essvalsnorm,essvalestime] = CalculateESS( mwg.samples,mwg.SamplerParams, significantLag);
    sprintf ('For parameter alpha_2 and MWG: Number of significant lags = %i, ESS per sample: %.2f, ESS per minute: %.2f ', significantLag, essvalsnorm(ALPHA_2),essvalestime(ALPHA_2)  )
    
    %now for the adaptive samples

    adapt = load(strcat(pathstr,'/../../Results/Experiment2AdaptiveSyntheticMCMC',num2str(replicate),'.mat'));
    adapt_burnin = adapt.SamplerParams.Burnin + 1;
    
    %calculate the autocorrelation coefficients and the bounds
    [acf,~,bounds] = autocorr(adapt.samples.params(adapt_burnin:end,ALPHA_2),200);
    
    %calculate the first furthest significant lag
    significantLag = find(acf < bounds(1), 1) - 1;
    [~,~,essvalsnorm,essvalestime] = CalculateESS( adapt.samples,adapt.SamplerParams, significantLag);
    sprintf ('For parameter alpha_2 and Adaptive: Number of significant lags = %i, ESS per sample: %.2f, ESS per minute: %.2f ', significantLag, essvalsnorm(ALPHA_2),essvalestime(ALPHA_2)  )
    
    
    
end

