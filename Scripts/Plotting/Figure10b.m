function Figure10b()

    [pathname,~,~] = fileparts(mfilename('fullpath'));
    
    LEFTBORDER = 0.2; %charting
    TITLE_POSITION = [-0.25,1.20]; %charting
    fontSizeTicks = 8;
    fontSizeAxis = 12;
    
    %these are the mapping parameter names and values 
    %from the HJC model to the Siekmann model which has close states to start
    %and open states on the bottom. This is so we can compare plots on
    %Siekmann's model directly.
    
    %the actual ordering for the HJC model (with HJC notation) runs k_13, k_24, k_31, k_34, k_42, k_43.
    
    hjcParamNames = {'k_{13}','k_{24}','k_{31}','k_{34}','k_{42}','k_{43}'};
    hjcParamValues = [3.5, 0.05,7,0.4,0.1,0.5] * 1000;

    HJCRes{1} = strcat(pathname,'/../../Results/ExperimentAHJC_12_0ms_HJC.mat');
    HJCRes{2} = strcat(pathname,'/../../Results/ExperimentAHJC_12_1e-05ms_HJC.mat');
    HJCRes{3} = strcat(pathname,'/../../Results/ExperimentAHJC_12_2e-05ms_HJC.mat');
    HJCRes{4} = strcat(pathname,'/../../Results/ExperimentAHJC_12_3e-05ms_HJC.mat');
    HJCRes{5} = strcat(pathname,'/../../Results/ExperimentAHJC_12_4e-05ms_HJC.mat');
    HJCRes{6} = strcat(pathname,'/../../Results/ExperimentAHJC_12_5e-05ms_HJC.mat');
    resolutions = [0.00, 0.01, 0.02, 0.03, 0.04, 0.05];
    
    %indices for HJC params to plot to compare with Siekmann
    hjcIndices = [1 3];
    
    PLOT_PARAM = hjcIndices(2); %plot k_31
    
    
    CONVERSION_FACTOR = 1;
    
    fig = figure;
    fig2 = figure;
    for j=1:6
        results = load(HJCRes{j});
        
        %convert parameter values of ms instead of s
        plottedSamples = results.samples.params/CONVERSION_FACTOR; 
        burnin = results.SamplerParams.Burnin + 1;
        set(groot, 'CurrentFigure',fig)
        
        hold on
        plot(plottedSamples(:,PLOT_PARAM),'DisplayName',[ num2str(resolutions(j)*1000) ' \mu s res']);
        hold off;

        title(hjcParamNames{PLOT_PARAM})
        set(groot, 'CurrentFigure',fig2)
        
        [y1 ,x1] = ksdensity(plottedSamples(burnin:end,PLOT_PARAM));
        hold on
        
        if resolutions(j) == 0
            plot(x1,y1,'DisplayName', 'Perfect res','LineWidth',1);
        else
            plot(x1,y1,'DisplayName',[ num2str(resolutions(j)*1000) ' \mus'],'LineWidth',1);
        end
        hold off
    end    
    
    
    set(groot,'CurrentFigure',fig)
    
    [h,icons,plots,str] = legend(gca,'show','location','southeast')
    
    %title(['Parameter ' hjcParamNames{hjcIndices(1)}],'Interpreter', 'tex','FontSize',20)  
    
    hold on
    ylimits = ylim;
    line([ylimits(1),ylimits(2)],[hjcParamValues(PLOT_PARAM),hjcParamValues(PLOT_PARAM)],'LineStyle','--','Color','r')
    hold off
    title(['Parameter ' hjcParamNames{PLOT_PARAM}],'Interpreter', 'tex','FontSize',20,'FontName','sans-serif')  
    xlabel('MCMC Iteration','FontSize',14)
    ylabel('$$k_{31}$, $s^{-1}$$','FontSize',16,'interpreter','latex')
    
    set(groot,'CurrentFigure',fig2)

    [h,icons,~, ~] = legend(gca,'show','location','southeast');
    
    
    set(h, 'FontSize',8,'Location','northwest')
    lineFactor = 2.5;
    h = get(icons(7), 'xdata');
    set(icons(7),'xdata',[h(1) * lineFactor, h(2)])
    
    h = get(icons(9), 'xdata');
    set(icons(9),'xdata',[h(1) * lineFactor, h(2)])
    
    h = get(icons(11), 'xdata');
    set(icons(11),'xdata',[h(1) *lineFactor, h(2)])
    
    h = get(icons(13), 'xdata');
    set(icons(13),'xdata',[h(1) * lineFactor, h(2)])
    
    h = get(icons(15), 'xdata');
    set(icons(15),'xdata',[h(1) * lineFactor, h(2)])
    
    h = get(icons(17), 'xdata');
    set(icons(17),'xdata',[h(1) * lineFactor, h(2)])
    
    
    text(0.2,0.93, 'Resolution', 'FontSize', 8, 'Units', 'normalized', 'FontWeight', 'bold')
    hold on
    ylimits = ylim;
    line([hjcParamValues(PLOT_PARAM),hjcParamValues(PLOT_PARAM)], [ylimits(1),ylimits(2)],'LineStyle','--','Color','r') 
    hold off
    xlabel('$$k_{31}$,  $s^{-1}$$','FontSize',24,'interpreter','latex')
    
    ylabel('Density','FontSize',24,'FontName','sans-serif')
    %title(['Parameter ' hjcParamNames{PLOT_PARAM}],'Interpreter', 'tex','FontSize',24,'FontName','sans-serif') 
    text(TITLE_POSITION(1), TITLE_POSITION(2), 'B', 'FontName',  'sans-serif','FontWeight', 'bold', 'FontSize', fontSizeAxis, 'Units', 'normalized')
    
    set(gca,'FontSize',24)
    
    xlimits = [4500,8250];
    xtickRefs = { [5000,6000,7000,8000] };
    
    xlim(xlimits(:))
    set(gca,'XTick',xtickRefs{1})
    
    close(fig);
    Plot1By1(fig2,1,[pathname '/../../Results/Figures/Paper/Figure10b_HJCParamDensities'],fontSizeTicks,fontSizeAxis, LEFTBORDER, [0, 0, 3.25, 2])
    close(fig2);
end