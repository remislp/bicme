function Figure5(replicate)

    fontSizeTicks = 24;
    fontSizeAxis = 28;
    fontSizePanel = 32;
    LEFTBORDER = 0.25;
    TITLE_POSITION = [-0.35,1.25];

    [pathname,~,~] = fileparts(mfilename('fullpath'));
    load(strcat(pathname,'/../../Results/Experiment2AdaptiveSyntheticMCMC', num2str(replicate),'.mat'))


    %% Fig 5 - Posterior predictive distributions at low concentration
    SAMPLES=100;

    experiment.startParams = samples.params(end,:)';
    posterior_samples = datasample(samples.params(SamplerParams.Burnin+1:end,:),SAMPLES,'Replace',false);
    experiment.model = model;

    i = 1; %low conc
    
    experiment.data.tres = data.tres(i);
    experiment.data.tcrit = data.tcrit(i);
    experiment.data.concs = data.concs(i);

     open_distribution = generate_unconditional_plot(experiment,data.filenames(i),'Synthetic',posterior_samples,1,1,1,model.kA,4,model.options);
     
     text(TITLE_POSITION(1), TITLE_POSITION(2), 'A', 'FontName', 'sans-serif', 'FontWeight', 'bold', 'FontSize', fontSizePanel, 'Units', 'normalized')    
     Plot1By1(open_distribution,1,[pathname '/../../Results/Figures/Paper/Figure5A_open_distributions' '_' num2str(experiment.data.concs)], fontSizeTicks, fontSizeAxis, LEFTBORDER, [0, 0, 6, 6])
     close(open_distribution)

     shut_distribution = generate_unconditional_plot(experiment,data.filenames(i),'Synthetic',posterior_samples,0,1,1,model.kA,4,model.options);
     text(TITLE_POSITION(1), TITLE_POSITION(2), 'B', 'FontName', 'sans-serif', 'FontWeight', 'bold', 'FontSize', fontSizePanel, 'Units', 'normalized')    

     Plot1By1(shut_distribution,1,[pathname '/../../Results/Figures/Paper/Figure5B_shut_distributions' '_' num2str(experiment.data.concs)],fontSizeTicks, fontSizeAxis, LEFTBORDER, [0, 0, 6, 6])
     close(shut_distribution)

     tint = [0.025 0.05;0.05 0.1; 0.1 0.2; 0.2 2; 2 20; 20 200; 200 2000;]/1000;
     conditional_open_mean_density = generate_conditional_mean_plot(experiment,data.filenames(i),'Synthetic',posterior_samples,1,1,1,model.kA,4,tint,model.options);
     text(TITLE_POSITION(1), TITLE_POSITION(2), 'C', 'FontName', 'sans-serif', 'FontWeight', 'bold', 'FontSize', fontSizePanel, 'Units', 'normalized')    
    
     Plot1By1(conditional_open_mean_density,1,[pathname '/../../Results/Figures/Paper/Figure5C_conditional_mean_distributions' '_' num2str(experiment.data.concs)],fontSizeTicks, fontSizeAxis, LEFTBORDER, [0, 0, 6, 6])
     close(conditional_open_mean_density)

    %% Fig 5 (cont) - Posterior distributions at high concentration

    i = 3; %high conc

    experiment.data.tres = data.tres(i);
    experiment.data.tcrit = data.tcrit(i);
    experiment.data.concs = data.concs(i);

    open_distribution = generate_unconditional_plot(experiment,data.filenames(i),'Synthetic',posterior_samples,1,1,1,model.kA,4,model.options);
    text(TITLE_POSITION(1), TITLE_POSITION(2), 'D', 'FontName', 'sans-serif', 'FontWeight', 'bold', 'FontSize', fontSizePanel, 'Units', 'normalized')    
    Plot1By1(open_distribution,1,[pathname '/../../Results/Figures/Paper/Figure5D_open_distributions' '_' num2str(experiment.data.concs)],fontSizeTicks, fontSizeAxis, LEFTBORDER, [0, 0, 6, 6])
    close(open_distribution)

    shut_distribution = generate_unconditional_plot(experiment,data.filenames(i),'Synthetic',posterior_samples,0,1,1,model.kA,4,model.options);
    text(TITLE_POSITION(1), TITLE_POSITION(2), 'E', 'FontName', 'sans-serif', 'FontWeight', 'bold', 'FontSize', fontSizePanel, 'Units', 'normalized')    
    Plot1By1(shut_distribution,1,[pathname '/../../Results/Figures/Paper/Figure5E_shut_distributions' '_' num2str(experiment.data.concs)],fontSizeTicks, fontSizeAxis, LEFTBORDER, [0, 0, 6, 6])
    close(shut_distribution)

    tint = [0.025 0.05;0.05 0.1; 0.1 0.2; 0.2 2; 2 20; 20 200; 200 2000;]/1000;
    conditional_open_mean_density = generate_conditional_mean_plot(experiment,data.filenames(i),'Synthetic',posterior_samples,1,1,1,model.kA,4,tint,model.options);
    text(TITLE_POSITION(1), TITLE_POSITION(2), 'F', 'FontName', 'sans-serif', 'FontWeight', 'bold', 'FontSize', fontSizePanel, 'Units', 'normalized')    

    Plot1By1(conditional_open_mean_density,1,[pathname '/../../Results/Figures/Paper/Figure5F_conditional_mean_distributions' '_' num2str(experiment.data.concs)],fontSizeTicks, fontSizeAxis, LEFTBORDER, [0, 0, 6, 6])
    close(conditional_open_mean_density)

end

