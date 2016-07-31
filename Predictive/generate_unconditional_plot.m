function fig = generate_unconditional_plot(experiment,data,datatype,posterior_samples,isopen,rows,cols,kA,kF,dcpoptions)
    MSEC=1000;
    fig=figure('Visible','on');
    
    
    %determine a consistent scale length for all the plots
    Q=experiment.model.generateQ(experiment.startParams,experiment.data.concs(1));
    max_root = max(-1./dcpFindRoots(Q,experiment.model.kA,experiment.data.tres(1),isopen,dcpoptions));
    t = logspace(log10(0.00001),log10(max_root*20),512)';
    
    conc_number = length(experiment.data.concs);
    
    for conc_no=1:conc_number
        tres=experiment.data.tres(conc_no);
        conc=experiment.data.concs(conc_no);        
        
        if strcmp(datatype , 'Experimental')
            resolvedData = data{conc_no};
            %we have experimental data equivalent to the function call RecordingManipulator.imposeResolution(data,tres);            
            
        elseif strcmp(datatype, 'Synthetic')
            %use scn files
            [~,sequence]=DataController.read_scn_file(data{conc_no});
            sequence.intervals=sequence.intervals/1000;
            resolvedData = RecordingManipulator.imposeResolution(sequence,tres);
        else
            error('Datafiles not recognised!')
        end
        
        if isopen
            [intervals, ~] = RecordingManipulator.getPeriods(resolvedData);
        else
            [~, intervals] = RecordingManipulator.getPeriods(resolvedData);
        end
        
        subplot(rows,cols,conc_no)

        hold on;  
        %title(strcat('Concentration = ', num2str(conc),' M'),'FontSize',16)

        for i=1:size(posterior_samples,1)
            params = posterior_samples(i,:);
            Q=experiment.model.generateQ(params',conc);
            pdf =  UnconditionalExactPDF(Q,kA,kF,tres,t,isopen,dcpoptions);
            p = semilogx(t*MSEC,pdf, 'r','LineWidth', 0.05);
            set(p,'linewidth',0.01)
            p.Color(4)=0.8;
            pdf_i = UnconditionalIdealPDF(Q,kA,kF,tres,t,isopen,dcpoptions);
            p = semilogx(t*MSEC,pdf_i,'g','LineWidth',0.05);
            set(p,'linewidth',0.01)
            p.Color(4)=0.8;         
        end
        
        %add the data on as an overview.
        
        %don't plot the intervals that are flagged as bad
        [buckets,frequency,dx] =  Histogram(intervals.intervals(intervals.status ~= 8),tres);
        semilogx(buckets*MSEC,frequency./(length(intervals.intervals)*log10(dx)*2.30259),'LineWidth', 2);
        
        set(gca,'XScale','log');
        
        if ~isopen
            %add the t_crit onto the chart
            tcrit = experiment.data.tcrit(conc_no);
            ylimit = ylim;
            line([tcrit*1000,tcrit*1000],[0,ylimit(2)],'Color','r','LineWidth', 2, 'LineStyle','--')
            h=text(0.3*tcrit*1000,0.5*ylimit(2),['Tc. = ' num2str(tcrit*1000) ' ms'],'FontName','sans-serif');
            set (h,'Rotation',90);
            set (h,'FontSize',24)
        end
            
        if conc_no == conc_number
            if isopen
                xlabel('Open duration, ms')
                xlim([0.01 10^4])
                ax = gca;
                ax.XTick = [10^-2 10^-0 10^2 10^4];
                ax.XTickLabel = {'10^{-2}', '10^{0}', '10^{2}', '10^{4}'};                
            else
                xlabel('Shut duration, ms')
                xlim([10^-2 10^5])
                ax = gca;
                ax.XTick = [10^-2 10^-0 10^2 10^4];
                ax.XTickLabel = {'10^{-2}', '10^{0}', '10^{2}', '10^{4}'};
            end
            ylabel('Probability density')
        end
        
        hold off
    end
end
