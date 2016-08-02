%pilot charts to show A: convergence and B: inefficient sampling
function Figure7(replicate)

    [pathname,~,~] = fileparts(mfilename('fullpath'));

    %% Fig 9 - Real Data Parameters

    load(strcat(pathname,'/../../Results/Experiment3AdaptiveExperimentalMCMC',num2str(replicate),'.mat'))
    load(strcat(pathname,'/../../Data/Synthetic/SevenStateGuessesAndParams.mat'))
    %find the MAP estimate
    [~,idx] =max(samples.posteriors(SamplerParams.Burnin+1:end));
    idx = idx+SamplerParams.Burnin; %index into the param array

    %MLE from this dataset from HJCFit
    mlest = [2109 , 46184, 257 , 2, 12034 , 1 ,38275700, 131, 17099, 70277900 ];
    
    [fig, x1, y1] = generate_kd_param_plot(10,5,2,samples.params(SamplerParams.Burnin+1:end,:),param_names(ten_param_keys));

    %add the MAP estimates in addition to the mle
    [~,MAP_idx] = max(y1,[],2);
    
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
    xlimits = [1900,2500 ; 4.3*10^4, 5.2*10^4; 0.5*10^4, 1.25*10^4; 1,1.6; 0, 3*10^5; 0 800; 2.5*10^7, 5.5*10^7; 50, 275; 1.60*10^4, 1.9*10^4; 6.5 * 10^7, 8.5 * 10^7];
    xtickRefs = { [1900,2100,2300,2500], [4.3*10^4,4.6*10^4,4.9*10^4,5.2*10^4], [0.5*10^4,0.75*10^4,1*10^4,1.25*10^4] ...
        [1.00, 1.2, 1.4, 1.60],  [0.00 , 1*10^5, 2*10^5 , 3*10^5],  [0,250,500,750],  [2.5*10^7, 3.5*10^7,4.5*10^7, 5.5*10^7],  [50, 125 ,200, 275],...
        [1.60*10^4, 1.7*10^4, 1.8*10^4, 1.9*10^4],[6.5 * 10^7, 7.5 * 10^7, 8.5 * 10^7]};
    
    for i=1:model.k
        subplot(ax(i));
        xlim(xlimits(i,:))
        set(gca,'XTick',xtickRefs{i})
        
        limits = ylim;
        %line([mlest(i),mlest(i)],[limits(1),limits(2)],'LineStyle','--','Color','g')

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
        
        %NumTicks = 4;
        %L = get(gca,'XLim');
        %set(gca,'XTick',linspace(L(1),L(2),NumTicks))
        
        set(gca, 'XTickLabel',num2str(xticks(:),'%10.1f'),'FontSize',8,'FontName','sans-serif')
        text(0.75,0.075 ,['\times10^{' num2str(counter), '}'], 'FontSize', 8, 'Units', 'normalized', 'interpreter', 'tex')
        
        counter = 0;
        yticks = (get(gca, 'YTick'));
        while max(yticks) < 10 %hack to manually fix ylabels!
            counter = counter + 1;
            yticks = yticks.*10;
        end
        set(gca, 'YTickLabel',num2str(yticks(:),3),'FontSize',8,'FontName','sans-serif')
        
        text(0.05,1.05 ,['\times10^{' num2str(-counter), '}'],'FontSize',8,'Units','normalized', 'interpreter', 'tex')
        
        if i==2
           %xlabel('Rate const. estimate, s^{-1}/s^{-1}M^{-1}','FontSize',10,'Units','normalized','FontName','Arial')
           %ylabel('Probability density','FontSize',10,'Units','normalized','FontName','sans-serif', 'interpreter', 'tex') 
        end
    
    end
    
    PlotNByM(fig,2,5,1,10,[pathname '/../../Results/Figures/Paper/Figure7_RealDataParameterDistibutions'])

end