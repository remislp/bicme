function Figure3(replicate)

    ALPHA_2 = 1; %the location of Alpha_2 in the samples
    BETA_2 = 2;
    LEFTBORDER = 0.35;
    INIT_SAMPLES = 20;
    fontSizeTicks = 8;
    fontSizeAxis = 10;
    TITLE_POSITION = [-0.45,1.25];
    
    [pathname,~,~] = fileparts(mfilename('fullpath'));

    %% Fig 3A
    load(strcat(pathname,'/../../Results/Experiment2PilotMWGSyntheticMCMC',num2str(replicate),'.mat'))
    Burnin = SamplerParams.Burnin + 1;
    
    max_post = max(samples.posteriors(:));
    
    fig=figure('visible','on');
    plot(samples.posteriors(INIT_SAMPLES:end,ALPHA_2));
    xlabel('Iteration','fontname','sans-serif')
    ylabel('Model Log-Posterior','fontname','sans-serif', 'FontSize', fontSizeAxis);
    hold on
    line([0,samples.N-INIT_SAMPLES],[max_post,max_post],'LineStyle','--','Color','r')
    %title('a)', 'FontName', 'sans-serif' ,'FontSize', fontSizeAxis)
    text(TITLE_POSITION(1), TITLE_POSITION(2), 'A', 'FontName', 'sans-serif', 'FontWeight', 'bold', 'FontSize', fontSizeAxis, 'Units', 'normalized')    
    hold off
    
    Plot1By1(fig, 1, [pathname '/../../Results/Figures/Paper/Figure3A_pilot_convergence'],fontSizeTicks, fontSizeAxis, LEFTBORDER);
    close(fig)

    %% Fig 3B
    fig=figure('Visible','on');
    [acf, lags, ~] = autocorr(samples.params(Burnin+1:end,ALPHA_2),100);
    scatter(lags, acf, 2); 
    xlabel('Lag','fontname','sans-serif'); 
    ylabel('\gamma(l)', 'interpreter', 'tex');
    hold on;
    ylim([-0.05 1]); 
    text(TITLE_POSITION(1), TITLE_POSITION(2), 'B', 'FontName', 'sans-serif', 'FontWeight', 'bold', 'FontSize', fontSizeAxis, 'Units', 'normalized')
    
    Plot1By1(fig,1,[pathname '/../../Results/Figures/Paper/Figure3B_pilot_autocorrelations'],fontSizeTicks,fontSizeAxis, LEFTBORDER)
    close(fig)

    %% Fig 3C
    fig = figure('Visible','on');
    
    %we need to sample a reasonable number of points so the plot isn't too
    %big in terms of MB
    SAMPLES=5000;
    [posterior_samples, idx] = datasample(samples.params(SamplerParams.Burnin+1:end,ALPHA_2:BETA_2),SAMPLES,'Replace',false);
    idx = idx + SamplerParams.Burnin;
    proposed_samples = samples.proposals(idx,ALPHA_2:BETA_2);
    
    scatter(proposed_samples(:,ALPHA_2) , proposed_samples(:,BETA_2),'r','.');
    hold on;
    scatter(posterior_samples(:,ALPHA_2) , posterior_samples(:,BETA_2),'b','.');
    
    xlabel('\alpha_2'); 
    ylabel('\beta_2');
    xlim([1400 2800]);
    ylim([40000 65000]);

    text(TITLE_POSITION(1), TITLE_POSITION(2), 'C', 'FontName', 'sans-serif', 'FontWeight', 'bold', 'FontSize', fontSizeAxis, 'Units', 'normalized')

    Plot1By1(fig,1,[pathname '/../../Results/Figures/Paper/Figure3C_diliganded_correlations'],fontSizeTicks,fontSizeAxis, LEFTBORDER)
    close(fig)

    clearvars -except pathname fontSizeTicks fontSizeAxis ALPHA_2 BETA_2 replicate INIT_SAMPLES LEFTBORDER TITLE_POSITION 
    
    %% Fig 3D
    load(strcat(pathname,'/../../Results/Experiment2AdaptiveSyntheticMCMC', num2str(replicate),'.mat'))
    Burnin = SamplerParams.Burnin + 1;
    
    max_post = max(samples.posteriors(:));
    fig=figure('visible','on');
    plot(samples.posteriors(INIT_SAMPLES:end,ALPHA_2));
    xlabel('Iteration','fontname','sans-serif')
    ylabel('Model Log-Posterior','fontname','sans-serif');
    hold on
    line([0,samples.N-INIT_SAMPLES],[max_post,max_post],'LineStyle','--','Color','r')
    hold off
    
    ylim([122400 122650]);
    
    text(TITLE_POSITION(1), TITLE_POSITION(2), 'D', 'FontName', 'sans-serif', 'FontWeight', 'bold', 'FontSize', fontSizeAxis, 'Units', 'normalized')

    Plot1By1(fig,1,[pathname '/../../Results/Figures/Paper/Figure3D_adaptive_convergence'],fontSizeTicks, fontSizeAxis, LEFTBORDER);
    close(fig)

    %% Fig 3E
    
    fig=figure('Visible','on');
    [acf, lags, ~] = autocorr(samples.params(Burnin:end,ALPHA_2),100);
    scatter(lags, acf, 2); 
    xlabel('Lag','fontname','sans-serif'); 
    ylabel('\gamma(l)', 'interpreter', 'tex');
    hold on;
    ylim([-0.05 1]);
    text(TITLE_POSITION(1), TITLE_POSITION(2), 'E', 'FontName', 'sans-serif', 'FontWeight', 'bold', 'FontSize', fontSizeAxis, 'Units', 'normalized')

    Plot1By1(fig,1,[pathname '/../../Results/Figures/Paper/Figure3E_autocorrelations'],fontSizeTicks, fontSizeAxis, LEFTBORDER)
    close(fig)
    
    %% Fig 3F
    
    fig = figure('Visible','on');
    
    SAMPLES=5000;
    [posterior_samples, idx] = datasample(samples.params(SamplerParams.Burnin+1:end,ALPHA_2:BETA_2),SAMPLES,'Replace',false);
    idx = idx + SamplerParams.Burnin;
    proposed_samples = samples.proposals(idx,ALPHA_2:BETA_2);
    
    scatter(proposed_samples(:,ALPHA_2) , proposed_samples(:,BETA_2), 'r', '.');
    hold on;
    scatter(posterior_samples(:,ALPHA_2) , posterior_samples(:,BETA_2), 'b', '.');
    
    xlabel('\alpha_2'); 
    ylabel('\beta_2');
    xlim([1400 2800]);
    ylim([40000 65000]);
    
    text(TITLE_POSITION(1), TITLE_POSITION(2), 'F', 'FontName', 'sans-serif', 'FontWeight', 'bold', 'FontSize', fontSizeAxis, 'Units', 'normalized')

    Plot1By1(fig,1,[pathname '/../../Results/Figures/Paper/Figure3F_diliganded_correlations'],fontSizeTicks,fontSizeAxis, LEFTBORDER)
    close(fig)    
    
end