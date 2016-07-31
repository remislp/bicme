function [fig,xis,yis] = generate_kd_param_plot(param_no,rows,cols,param_samples,param_names,varargin)
    plotComparisonParams = 0;
    KD_POINTS = 1000;
    if ~isempty(varargin)
        %do we want a comparitor set of params on the graph?
        paramComparison = varargin{1};
        plotComparisonParams = 1;
    end
    
    xis = zeros(param_no,KD_POINTS);
    yis = zeros(param_no,KD_POINTS);

    fig=figure('Visible','on');
    for i=1:param_no
        h=subplot(cols,rows,i);
        [y1, x1] = ksdensity(param_samples(:,i),'npoints',1000);
        plot (x1, y1,'LineWidth',2);
        titleText = sprintf('$%s$',param_names{i});
        text(0.63,0.9 ,titleText,'FontSize',16,'Units','normalized','Interpreter','latex','FontName', 'sans-serif')
        
        limits = ylim;
        if plotComparisonParams
            line([paramComparison(i),paramComparison(i)],[limits(1),limits(2)],'LineStyle','--','Color','k')
        end
        % save the kd estimates
        xis(i , :) = x1;
        yis(i , :) = y1;
    end
end


