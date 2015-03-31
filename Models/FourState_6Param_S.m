classdef FourState_6Param_S < SiekmannIonModel
    %FourStateExactIonModel with Tr prior (Siekmann)
    
    properties

    end
    
    methods(Access=public,Static)
        
        function obj = FourState_6Param_S(~)
            obj.kA=2;
            obj.h=0.01;
            obj.k = 6;
        
        end
        
        function Q = generateQ(params,~)
            Q=zeros(4,4);
            
            %params(1) = k_13 
            %params(2) = k_24
            %params(3) = k_31
            %params(4) = k_34
            %params(5) = k_42
            %params(6) = k_43
            
            Q(1,1) = -params(1); 
            Q(1,2) = 0; 
            Q(1,3) = params(1);
            Q(1,4) = 0;
            
            Q(2,1) = 0; 
            Q(2,2) = -params(2);
            Q(2,3) = 0; 
            Q(2,4) = params(2);             

            Q(3,1) = params(3);
            Q(3,2) = 0;
            Q(3,3) = -(params(3) + params(4)); 
            Q(3,4) = params(4);   

            Q(4,1) = 0; 
            Q(4,2) = params(5);
            Q(4,3) = params(6);
            Q(4,4) = -(params(5) + params(6));       
 
        end
        
        function sample = samplePrior()
            %in this model we have two uniform priors
            error('Not implemented')         
        end
        
        function logPrior = calcLogPrior(params)
            if size(params,1) < size(params,2)
                params=params';
            end
            p = 30;
            Q = FourState_6Param_AT.generateQ(params);
            logPrior = trace(Q)/p;
        end
        
        function derivLogPrior = calcDerivLogPrior(params)
            if isinf(FourState_6Param_AT.calcLogPrior(params))
                derivLogPrior = -Inf;
            else
                derivLogPrior = 0;
            end   
        end
    end
end

