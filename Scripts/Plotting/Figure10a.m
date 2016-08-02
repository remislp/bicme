function Figure10a()
    
    
    [pathname,~,~] = fileparts(mfilename('fullpath'));

    CONVERSION_FACTOR = 1000; %convert to s from msec
    LEFTBORDER = 0.2; %charting
    TITLE_POSITION = [-0.25,1.20];
    fontSizeTicks = 8;
    fontSizeAxis = 12;
    
    %compare Siekmann data at perfect resolution and 0.05ms resolution
    %need Siek param names in HJC notation
    
    %original_param_names_in_array = {'k_{12}','k_{21}','k_{13}','k_{31}','k_{24}','k_{42}'};
    siek_param_names_in_hjc = {'k_{34}','k_{43}','k_{31}','k_{13}','k_{42}','k_{24}'};
    siek_true_values = [0.4,0.5,7,3.5,0.1,0.05] * CONVERSION_FACTOR;
    
    siekRes{1} = strcat(pathname,'/../../Results/0ms_Nrates.dat');
    siekRes{2} = strcat(pathname,'/../../Results/0.01ms_Nrates.dat');
    siekRes{3} = strcat(pathname,'/../../Results/0.02ms_Nrates.dat');
    siekRes{4} = strcat(pathname,'/../../Results/0.03ms_Nrates.dat');
    siekRes{5} = strcat(pathname,'/../../Results/0.04ms_Nrates.dat');
    siekRes{6} = strcat(pathname,'/../../Results/0.05ms_Nrates.dat');
    resolutions = [0, 10, 20, 30, 40, 50];
    
    SAMPLES = 30000;
    BURNIN = 10001;
    NO_PARAMS=6;
    
    %indices for Siekmann params to plot to show the two fastest rate
    %constants
    SiekIndices = [3 4];
    PLOT_PARAM = SiekIndices(1); %plot k_31 in HJC notation
    
    fig = figure;
    fig2 = figure;
    for j=1:6
        samples = inflateResults(siekRes{j}, SAMPLES, NO_PARAMS)*CONVERSION_FACTOR;
        set(groot,'CurrentFigure',fig)
        
        hold on
        plot(samples(:,PLOT_PARAM),'DisplayName',[ num2str(resolutions(j)) ' \mus res']);
        hold off;

        title(siek_param_names_in_hjc{PLOT_PARAM})
        set(groot, 'CurrentFigure',fig2)
        
        [y1 ,x1] = ksdensity(samples(BURNIN:end,PLOT_PARAM));
        hold on
        plot(x1,y1,'DisplayName',[ num2str(resolutions(j)) ' \mus res'],'LineWidth',1);
        hold off
        
         
    end
    
    set(groot,'CurrentFigure',fig)
    legend(gca,'show','location','southeast')
    set(get(gca,'xlabel'),'FontSize',24)
    set(get(gca,'ylabel'),'FontSize',24) 
    %title(['Parameter ' siek_param_names_in_hjc{PLOT_PARAM}],'Interpreter', 'tex','FontSize',24)  
    
    hold on
    ylimits = ylim;
    line([ylimits(1),ylimits(2)],[siek_true_values(PLOT_PARAM),siek_true_values(PLOT_PARAM)],'LineStyle','--','Color','r')
    hold off
    xlabel('MCMC Iteration','FontSize',16,'FontName','sans-serif')
    ylabel('k_{31} Parameter Value, s^{-1}','FontSize',16,'interpreter','tex')
    
    set(groot,'CurrentFigure',fig2)
    %legend(gca,'show')
    %h=legend(gca,'show');
    %set(h,'FontSize',8,'Location','northeast')
    %title(['Parameter ' siek_param_names_in_hjc{PLOT_PARAM}],'Interpreter', 'tex','FontSize',24)  
    hold on
    ylimits = ylim;
    line([siek_true_values(PLOT_PARAM),siek_true_values(PLOT_PARAM)], [ylimits(1),ylimits(2)],'LineStyle','--','Color','r') 
    

    xlabel('$$k_{31}$, $s^{-1}$$','FontSize',fontSizeAxis,'interpreter', 'latex')
    ylabel('Density','FontSize',24,'FontName','sans-serif')
    text(TITLE_POSITION(1), TITLE_POSITION(2), 'A', 'FontName',  'sans-serif','FontWeight', 'bold', 'FontSize', fontSizeAxis, 'Units', 'normalized')
    hold off

    
    set(gca,'FontSize',12)
    set(get(gca,'xlabel'),'FontSize',12)
    set(get(gca,'ylabel'),'FontSize',12)
    
    xlimits = [4500,8250];
    xtickRefs = { [5000,6000,7000,8000] };
    
    xlim(xlimits(:))
    set(gca,'XTick',xtickRefs{1})
    
    Plot1By1(fig2,1,[pathname '/../../Results/Figures/Paper/Figure10a_SiekmannParamDensities'],fontSizeTicks,fontSizeAxis, LEFTBORDER, [0, 0, 3.25, 2])

end