%pilot charts to show A: convergence and B: inefficient sampling
function Figure4(replicate)

[pathname,~,~] = fileparts(mfilename('fullpath'));

%% Fig 4 FULL POSTERIORS

    %find the MAP estimate

    load(strcat(pathname,'/../../Results/Experiment2AdaptiveSyntheticMCMC', num2str(replicate),'.mat'))
    load(strcat(pathname,'/../../Data/Synthetic/SevenStateGuessesAndParams.mat'))
    
    Burnin = SamplerParams.Burnin + 1;
    
    [~,idx] =max(samples.posteriors(Burnin:end));
    idx = idx+SamplerParams.Burnin; %index into the param array

    [fig, x1, y1] = generate_kd_param_plot(10,5,2,samples.params(Burnin:end,:),param_names(ten_param_keys),true1(ten_param_keys));
    %get the MAP from the kd-estimates
    
    [~,MAP_idx] = max(y1,[],2);
    
    %the MAP_x give the parameter values that correspond to the MAP
    %estimate
    MAP_x = zeros(length(MAP_idx),1);
    for i=1:length(MAP_idx)
        MAP_x(i) = x1(i,MAP_idx(i)); 
    end
    
    %calculate the Observed Information at the MAP.
    if isa(model,'SevenState_10Param_AT') 
        %we need the more exact Hessian calc
        modelB = SevenState_10Param_QET();
        hessian = modelB.calcMetricTensor(MAP_x,data);
    else
        hessian = model.calcMetricTensor(MAP_x,data);
    end
    
    covariance = hessian^-1;
        
    ax = flip(fig.Children);
    for i=1:model.k
        
        if i==model.k
           %ylabel('Frequency Density') 
           %xlabel('Rate constant estimate') 
        end
        
        subplot(ax(i));
        
        %add a normal fitting onto the density at the MAP
        hold on;
        xl=xlim;
        x = linspace(xl(1),xl(2),100);
        gauss = normpdf(x,MAP_x(i),sqrt(covariance(i,i)));
        plot(x, gauss,'r','LineWidth',1);
        hold off;

        %destroy the current power scale
        currXtickLabel = get(gca, 'XTickLabel');

        set(gca, 'XTickLabel',[0,1])
        set(gca, 'XTickLabel',currXtickLabel)

        counter = 0;
        xticks = (get(gca, 'XTick'));
        
        while max(xticks) > 10 %hack to manually fix xlabels!
            counter = counter + 1;
            xticks = xticks./10;
        end
        set(gca, 'XTickLabel',num2str(xticks(:)),'FontSize',8,'FontName','sans-serif')
        %text(0.79,0.07 ,['$\mathsf{\times10^{' num2str(counter), '}}$'],'FontSize',8,'Units','normalized','interpreter', 'latex')
        text(0.79,0.07 ,['\times10^{' num2str(counter), '}'],'FontSize',8,'Units','normalized','interpreter', 'tex')
        counter = 0;
        yticks = (get(gca, 'YTick'));
        while max(yticks) < 10 %hack to manually fix ylabels!
            counter = counter + 1;
            yticks = yticks.*10;
        end
        set(gca, 'YTickLabel',num2str(yticks(:)),'FontSize',8,'FontName','sans-serif')
        
        text(0.05,1.00 ,['\times10^{' num2str(-counter), '}'],'FontSize',8,'Units','normalized','interpreter', 'tex')
        
        %if i==2
        %   xlabel('Rate const. estimate, s^{-1}/s^{-1}M^{-1}','FontSize',10,'Units','normalized','FontName','Arial')
        %   ylabel('Probability density','FontSize',10,'Units','normalized','FontName','sans-serif', 'interpreter', 'tex') 
        %end
    
    end
    %(fig,N,M,hastitle,axisFontSize,varargin)
    PlotNByM(fig,2,5,1,10,[pathname '/../../Results/Figures/Paper/Figure4_SyntheticDataParameterDistributions'])
    close(fig)
end