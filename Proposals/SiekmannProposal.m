classdef SiekmannProposal < Proposal
    %RwmhProposal - Random-walk Metropolis Hastings proposal step
    
    properties
        delta = 0.05;
        componentwise = 0;
    end
    
    properties(Constant)
        RequiredInfo = [1 0 0 0];
    end
    
    
    methods
        function obj = SiekmannProposal(delta)
            obj.delta = delta;
            obj.componentwise = 0;
        end
        
            
        function obj = set.componentwise(obj,cw) 
            if (cw ~= 0 )
                error('SiekmannProposal:componentwise:invalidComponent', 'componentwise parameter must be 0')
            end
            obj.componentwise = cw;
        end
        
        function obj = set.delta(obj,delta)
            %must be positive definite     
            if(delta > 0)
                obj.delta = delta;
            else
                error('SiekmannProposal:delta:notPos','delta must be positive')
            end    
    
        end
        
        function [alpha,propParams,propInformation] = propose(obj,model,data,currentParams,currInfo)

            % PROPOSE  Proposes a joint metropolis-hastings step for the parameters of a model.
            %
            %   OUTPUTS 
            %   alpha - scalar, log probability of the proposed move
            %   propParams - k * 1 vector of proposed parameters
            %   propInformation - Information of the move (logPosterior only for rwmh)
            
            %   
            %   INPUTS
            %
            %   model - Object, a statistical model of type Model
            %   data - struct, a representation that the model understands
            %   currentParams, k * 1 vector of current param position
            %   currentInformation, structure current information,
            %   (logPosterior)
            
           propParams = zeros(length(currentParams),1);
           for j=1:length(currentParams)
                while true
                    propParams(j) = currentParams(j) + unifrnd(-obj.delta,obj.delta);
                    if propParams(j) > 0 
                        break;
                    end
                end
            end
           
            %propParams = currentParams + L' * randn(length(currentParams),1);
            propInformation = model.calcGradInformation(propParams,data,SiekmannProposal.RequiredInfo);
                
            %proposal distibution is symmetric so cancels in the ratio
            if isinf(propInformation.LogPosterior)
                alpha=-Inf;
            else
                alpha = min(0,((propInformation.LogPosterior)-(currInfo.LogPosterior)));
            end
                
        end 

        function [alpha,propParams,propInformation] = proposeCw(obj,model,data,currentParams,iP,currentInformation)

            % PROPOSE  Proposes a componentwise metropolis-hastings step for the parameter of a model.
            %
            %   OUTPUTS 
            %   alpha - scalar, log probability of the proposed move
            %   propParams - k * 1 vector of proposed parameters
            %   propInformation - Information of the move (logPosterior only for rwmh)
            %   
            %   
            %   INPUTS
            %
            %   model - Object, a statistical model of type Model
            %   data - struct, a representation that the model understands
            %   currentParam - k * 1 vector of current param position
            %   iP - scalar, the index of the parameter to sample
            %   currentInformation, structure current information,
            %   (logPosterior)
                        
             
            error('Componentwise proposal not enabled for Siekmann proposal');
        end         
        
        function obj=adjustScaling(obj,factor)
            %scale diagonal elements of the mass matrix
            obj.delta=obj.delta*factor;
        end
        
        function obj=adjustPwScaling(~,~,~)
            error('Not implemented for this proposal')
        end
        
    end  
end

