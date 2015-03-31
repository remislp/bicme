classdef TestSiekmannProposal < matlab.unittest.TestCase
    properties
        proposal
        model
        params
        data
    end
    
    methods (TestClassSetup)
        function createExperiment(testCase)
            [pathstr,~,~] = fileparts(mfilename('fullpath'));
            
            testCase.proposal = SiekmannProposal(0.05);
            testCase.model=NormalModel();
            testCase.params=[0; 10];
            a=load(strcat(pathstr, '/Data/NormData.mat'));
            testCase.data = a.data;
        end
    end
    
    methods(Test)
        function testProperties(testCase)
            
            %check defaults
            testCase.verifyEqual(testCase.proposal.delta,0.05);
            
            %check delta
            try
                testCase.proposal.delta = -0.05;
            catch ME
                testCase.verifyEqual(ME.identifier,'SiekmannProposal:delta:notPos');
            end
            
            %check componentwise           
            testCase.proposal.componentwise=0;
            testCase.verifyEqual(testCase.proposal.componentwise,0);
            try
                testCase.proposal.componentwise=1;
            catch ME
                testCase.verifyEqual(ME.identifier,'SiekmannProposal:componentwise:invalidComponent');                
            end
                     
        end
        
        %test joint proposal
        function testProposeBegin(testCase)
            rng(1);
            currInfo = testCase.model.calcGradInformation(testCase.params,testCase.data,SiekmannProposal.RequiredInfo);
            testCase.verifyEqual(currInfo.LogPosterior,testCase.model.calcLogLikelihood(testCase.params,testCase.data)+testCase.model.calcLogPrior(testCase.params),'AbsTol', 1e-10);

            [alpha,propParams,propInfo] = testCase.proposal.propose(testCase.model,testCase.data,testCase.params,currInfo);
            testCase.verifyEqual(alpha,0,'AbsTol', 1e-10);
            testCase.verifyEqual(testCase.model.calcLogLikelihood(propParams,testCase.data),-1110.0964849830336334,'AbsTol', 1e-10);
            testCase.verifyEqual(propInfo.LogPosterior,-1118.3905346231356361,'AbsTol', 1e-10);
            testCase.verifyEqual(propParams,[0.0220324493442158; 9.9500114374817343],'AbsTol', 1e-10);
            
            [alpha,propParams,propInfo] = testCase.proposal.propose(testCase.model,testCase.data,testCase.params,currInfo);
            testCase.verifyEqual(alpha,0,'AbsTol', 1e-10);
            testCase.verifyEqual(testCase.model.calcLogLikelihood(propParams,testCase.data),-1110.1274411603369572,'AbsTol', 1e-10);
            testCase.verifyEqual(propInfo.LogPosterior,-1118.4214908004389599,'AbsTol', 1e-10);
            testCase.verifyEqual(propParams,[0.0038816734003357; 9.9919194514403298],'AbsTol', 1e-10);
            rng('shuffle', 'twister')
        end
        function testProposePositiveProposals(testCase)
            rng(1);

            currInfo = testCase.model.calcGradInformation(testCase.params,testCase.data,SiekmannProposal.RequiredInfo);
            testCase.verifyEqual(currInfo.LogPosterior,testCase.model.calcLogLikelihood(testCase.params,testCase.data)+testCase.model.calcLogPrior(testCase.params),'AbsTol', 1e-10);

            for i = 1 :100
                [~,propParams,~] = testCase.proposal.propose(testCase.model,testCase.data,testCase.params,currInfo);
                testCase.verifyThat(propParams(1)>0, matlab.unittest.constraints.IsTrue)
                testCase.verifyThat(propParams(2)>0, matlab.unittest.constraints.IsTrue)
            end
            
            rng('shuffle', 'twister')
        end
    end
    
    methods (TestMethodTeardown)
        function destroyExperiment(testCase)
            clear testCase
        end
    end    
    
end