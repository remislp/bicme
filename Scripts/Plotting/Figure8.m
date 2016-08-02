
function Figure8(replicate)
    [pathname,~,~] = fileparts(mfilename('fullpath'));

    load(strcat(pathname,'/../../Results/Experiment3AdaptiveExperimentalMCMC',num2str(replicate),'.mat'))
    SAMPLES = 100;
    fontSizeTicks = 24;
    fontSizeAxis = 28;
    fontSizePanel = 32;
    LEFTBORDER = 0.25;
    TITLE_POSITION = [-0.35,1.25];

    experiment.startParams = samples.params(end,:)';
    posterior_samples = datasample(samples.params(SamplerParams.Burnin+1:end,:),SAMPLES,'Replace',false);
    experiment.model = model;
    
    data = load(strcat(pathname,'/../../Data/Experimental/AchRealData.mat'));

    i=1; %low conc
        
        experiment.data.tres = data.tres(i);
        experiment.data.tcrit = data.tcrit(i);
        experiment.data.concs = data.concs(i);

        % Fig 10A - Posterior shut time distributions
        open_distribution = generate_unconditional_plot(experiment,data.resolved_data(i),'Experimental',posterior_samples,1,1,1,model.kA,4,model.options);
        text(TITLE_POSITION(1), TITLE_POSITION(2), 'A', 'FontName', 'sans-serif','FontWeight', 'bold', 'FontSize', fontSizePanel, 'Units', 'normalized')

        Plot1By1(open_distribution,1,[pathname '/../../Results/Figures/Paper/Figure8A_open_distributions_real' '_' num2str(experiment.data.concs)],fontSizeTicks ,fontSizeAxis,LEFTBORDER,[0 0 6 6] )
        close(open_distribution)

        % Fig 10B - Posterior shut time distributions
        shut_distribution = generate_unconditional_plot(experiment,data.resolved_data(i),'Experimental',posterior_samples,0,1,1,model.kA,4,model.options);
        text(TITLE_POSITION(1), TITLE_POSITION(2), 'B', 'FontName', 'sans-serif','FontWeight', 'bold', 'FontSize', fontSizePanel, 'Units', 'normalized')

        Plot1By1(shut_distribution,1,[pathname '/../../Results/Figures/Paper/Figure8B_shut_distributions_real' '_' num2str(experiment.data.concs)],fontSizeTicks ,fontSizeAxis,LEFTBORDER,[0 0 6 6])
        close(shut_distribution)

        % Fig 10C - Mean conditional open time versus mean preceeding shut time distributions
        %0.025?0.05, 0.05?0.1, 0.1?0.2, 0.2?2, 2?20, 20?200 and > 200
        tint = [0.025 0.05;0.05 0.1; 0.1 0.2; 0.2 2; 2 20; 20 200; 200 2000;]/1000;
        conditional_open_mean_density = generate_conditional_mean_plot(experiment,data.resolved_data(i),'Experimental',posterior_samples,1,1,1,model.kA,4,tint,model.options);
        text(TITLE_POSITION(1), TITLE_POSITION(2), 'C', 'FontName', 'sans-serif', 'FontWeight', 'bold', 'FontSize', fontSizePanel, 'Units', 'normalized')
        Plot1By1(conditional_open_mean_density,1,[pathname '/../../Results/Figures/Paper/Figure8C_conditional_mean_distributions_real' '_' num2str(experiment.data.concs)],fontSizeTicks ,fontSizeAxis, LEFTBORDER,[0 0 6 6])
        close(conditional_open_mean_density)

    i=3; %high conc
        %generate_unconditional_plot(experiment,data,datatype,posterior_samples,isopen,rows,cols,kA,kF,dcpoptions)
        experiment.data.tres = data.tres(i);
        experiment.data.tcrit = data.tcrit(i);
        experiment.data.concs = data.concs(i);

        % Fig 10D - Posterior open time distribution
        open_distribution = generate_unconditional_plot(experiment,data.resolved_data(i),'Experimental',posterior_samples,1,1,1,model.kA,4,model.options);
        text(TITLE_POSITION(1), TITLE_POSITION(2), 'D', 'FontName', 'sans-serif','FontWeight', 'bold', 'FontSize', fontSizePanel, 'Units', 'normalized')
        Plot1By1(open_distribution,1,[pathname '/../../Results/Figures/Paper/Figure8D_open_distributions_real' '_' num2str(experiment.data.concs)],fontSizeTicks ,fontSizeAxis, LEFTBORDER,[0 0 6 6])
        close(open_distribution)

        % Fig 10E - Posterior shut time distributions
        shut_distribution = generate_unconditional_plot(experiment,data.resolved_data(i),'Experimental',posterior_samples,0,1,1,model.kA,4,model.options);
        text(TITLE_POSITION(1), TITLE_POSITION(2), 'E', 'FontName', 'sans-serif', 'FontWeight', 'bold','FontSize', fontSizePanel, 'Units', 'normalized')
        Plot1By1(shut_distribution,1,[pathname '/../../Results/Figures/Paper/Figure8E_shut_distributions_real' '_' num2str(experiment.data.concs)],fontSizeTicks ,fontSizeAxis, LEFTBORDER,[0 0 6 6])
        close(shut_distribution)

        % Fig 10F - Mean conditional open time versus mean preceeding shut time distributions
        tint = [0.025 0.05;0.05 0.1; 0.1 0.2; 0.2 2; 2 20; 20 200; 200 2000;]/1000;
        conditional_open_mean_density = generate_conditional_mean_plot(experiment,data.resolved_data(i),'Experimental',posterior_samples,1,1,1,model.kA,4,tint,model.options);
        text(TITLE_POSITION(1), TITLE_POSITION(2), 'F', 'FontName', 'sans-serif','FontWeight', 'bold', 'FontSize', fontSizePanel, 'Units', 'normalized')
        Plot1By1(conditional_open_mean_density,1,[pathname '/../../Results/Figures/Paper/Figure8F_conditional_mean_distributions_real' '_' num2str(experiment.data.concs)],fontSizeTicks ,fontSizeAxis, LEFTBORDER,[0 0 6 6])
        close(conditional_open_mean_density)
end