%pilot charts to show A: convergence and B: inefficient sampling
function Figure6(replicate)

    ALPHA_2 = 1; %the location of Alpha_2 in the samples
    BETA_2 = 2;
    LEFTBORDER = 0.4;
    INIT_SAMPLES=20;
    fontSizeTicks = 8;
    fontSizeAxis = 10;
    TITLE_POSITION = [-0.45,1.25];
    [pathname,~,~] = fileparts(mfilename('fullpath'));

    %% Fig 6A
    load(strcat(pathname,'/../../Results/Experiment3AdaptiveExperimentalMCMC', num2str(replicate),'.mat'))
    Burnin = SamplerParams.Burnin + 1;
    
    max_post = max(samples.posteriors(:));
    fig=figure('visible','on');

    plot(samples.posteriors(INIT_SAMPLES:end,ALPHA_2));
    xlabel('Iteration')
    ylabel('Model Log-Posterior', 'fontname','sans-serif', 'FontSize', fontSizeAxis);
    hold on
    text(TITLE_POSITION(1), TITLE_POSITION(2), 'A', 'FontName', 'sans-serif', 'FontWeight', 'bold', 'FontSize', fontSizeAxis, 'Units', 'normalized')    

    line([0,samples.N-INIT_SAMPLES],[max_post,max_post],'LineStyle','--','Color','r')
    hold off
    
    ylim([240750 241050]);
        
    Plot1By1(fig,1,[pathname '/../../Results/Figures/Paper/Figure6A_adaptive_convergence'],fontSizeTicks, fontSizeAxis, LEFTBORDER);
    close(fig)

    %% Fig 6B
    
    fig=figure('Visible','off');

    [acf, lags, ~] = autocorr(samples.params(Burnin:end,ALPHA_2),100);
    scatter(lags, acf, 2); 
    xlabel('Lag','fontname','sans-serif'); 
    ylabel('\gamma(l)', 'interpreter', 'tex');
    hold on;
    ylim([0.0 1]); 
    text(TITLE_POSITION(1), TITLE_POSITION(2), 'B', 'FontName', 'sans-serif', 'FontWeight', 'bold', 'FontSize', fontSizeAxis, 'Units', 'normalized')    

    Plot1By1(fig,1,[pathname '/../../Results/Figures/Paper/Figure6B_autocorrelations'],fontSizeTicks, fontSizeAxis, LEFTBORDER)
    close(fig)
    
    %% Fig 6C
    
    fig = figure('Visible','off');

    SAMPLES=5000;
    [posterior_samples, idx] = datasample(samples.params(SamplerParams.Burnin+1:end,ALPHA_2:BETA_2),SAMPLES,'Replace',false);
    idx = idx + SamplerParams.Burnin;
    proposed_samples = samples.proposals(idx,ALPHA_2:BETA_2);
    
    scatter(proposed_samples(:,ALPHA_2) , proposed_samples(:,BETA_2),'r','.');
    hold on;
    scatter(posterior_samples(:,ALPHA_2) , posterior_samples(:,BETA_2),'b','.');

    xlim([1400 2800]);
    ylim([40000 65000]);
    
    xlabel('\alpha_2'); 
    ylabel('\beta_2');
    xlim([1400 2800]);
    ylim([40000 65000]);

    text(-0.45, TITLE_POSITION(2), 'C', 'FontName', 'sans-serif', 'FontWeight', 'bold', 'FontSize', fontSizeAxis, 'Units', 'normalized')

    Plot1By1(fig,1,[pathname '/../../Results/Figures/Paper/Figure6C_diliganded_correlations'],fontSizeTicks, fontSizeAxis, LEFTBORDER)
    close(fig)    
    
end