function fig = generate_conditional_mean_plot(experiment,data,datatype,posterior_samples,isopen,rows,cols,kA,kF,conditional_ranges,dcpoptions)
    fig=figure('Visible','on');
    
    conc_number = length(experiment.data.concs);
    no_of_samples = size(posterior_samples,1);
    
    for conc_no=1:conc_number
        tres=experiment.data.tres(conc_no);
        conc=experiment.data.concs(conc_no);
        tcrit = experiment.data.tcrit(conc_no);
        
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
        
        subplot(rows,cols,conc_no);

        conditional_mean_open = zeros(size(conditional_ranges,1),no_of_samples);
        conditional_mean_close = zeros(size(conditional_ranges,1),no_of_samples);
        empirical_mean_open = zeros(size(conditional_ranges,1),1);
        empirical_mean_close = zeros(size(conditional_ranges,1),1);
        empirical_std_open = zeros(size(conditional_ranges,1),1);
        empirical_n_open = zeros(size(conditional_ranges,1),1);
        
        for i=1:size(conditional_ranges,1)
            for j=1:size(posterior_samples,1)
                params = posterior_samples(j,:);
                Q=experiment.model.generateQ(params',conc);
                conditional_mean_open(i,j) = ConditionalMean(Q,kA,kF,tres,conditional_ranges(i,2),conditional_ranges(i,1),dcpoptions)*1000;
                conditional_mean_close(i,j) = ConditionalMeanPreceeding(Q,kA,kF,tres,conditional_ranges(i,2),conditional_ranges(i,1),dcpoptions)*1000;
            end    
            succeeding_openings = RecordingManipulator.getSuceedingPeriodsWithRange(resolvedData,isopen,conditional_ranges(i,:));
            
            empirical_mean_open(i) = mean(succeeding_openings);
            empirical_mean_close(i) =  mean(RecordingManipulator.getPeriodsWithRange(resolvedData,~isopen,conditional_ranges(i,:)));
            empirical_std_open(i) = std(succeeding_openings);
            empirical_n_open(i) = length(succeeding_openings); 
        end

        errorbar(empirical_mean_close*1000,empirical_mean_open*1000,empirical_std_open*1000./sqrt(empirical_n_open), 'linewidth', 2)
        hold on;
        c = linspace(1,10,length(conditional_ranges));
        for j=1:size(posterior_samples,1)
            s = scatter(conditional_mean_close(:,j),conditional_mean_open(:,j) , 15, 'r', 'o');
            %sMarkers=s.MarkerHandle; %hidden marker handle
            %sMarkers.FaceColorData = uint8(255*[1;0;0;0.1]); %fourth element allows setting alpha
            %sMarkers.EdgeColorData = uint8(255*[1;0;0;0]); 
        end
        s = scatter(empirical_mean_close*1000,empirical_mean_open*1000, 30 , 'b','o');
        %s.Marker = '*';
        ylimit = ylim;
        
        line([tcrit*1000,tcrit*1000],[0, ylimit(2)],'Color','r','LineWidth',2,'LineStyle','--')
        %reset the axes
        %set(gca, 'ylim', ylimit)
        
        if strcmp(datatype , 'Experimental')
            h=text(0.3*tcrit*1000,0.05*ylimit(2),['Tc. = ' num2str(tcrit*1000) ' ms']);    
            set (h,'FontSize', 24);
        elseif strcmp(datatype, 'Synthetic')
            h=text(0.3*tcrit*1000,0.4*ylimit(2),['Tc. = ' num2str(tcrit*1000) ' ms']);
            set (h,'FontSize', 24);
        end
        
        
        
        set(h,'Rotation',90);
        
        if conc_no == conc_number
            xlabel('Mean shut time, ms')
            ylabel('Mean open time, ms')
        end        
        
        xlim([0.01 10000])
        ax = gca;
        ax.XTick = [10^-2 10^-0 10^2 10^4];
        ax.XTickLabel = {'10^{-2}', '10^{0}', '10^{2}', '10^{4}'};
        
        hold off
        set(gca,'XScale','log');

    end
end
