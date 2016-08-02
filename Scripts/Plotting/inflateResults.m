function samples = inflateResults(siekmannResultsFile, noSamples, noParams) 
        samplesIter = dlmread(siekmannResultsFile,'\t',1,1);%[q_12 q_21 q_13 q_31 q_24 q_42];
        Iterations = dlmread(siekmannResultsFile,'\t',[ 1 0 length(samplesIter) 0]);

        Iteration_No = length(Iterations);
        samples = zeros(noSamples,noParams);
        currentParams = zeros(1,noParams);
        j=2;
        for i=1:noSamples 
            if j <= Iteration_No
                if i-1 == Iterations(j)  %base index 0 but the first step is the initiate
                    currentParams = samplesIter(j,:);
                    j=j+1;
                end
            end
            samples(i,:) = currentParams;
        end
end