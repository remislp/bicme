classdef TestModelFourState_6Param_AT < matlab.unittest.TestCase
    properties
        model
        params
        data
        MSEC
    end
    
    methods (TestClassSetup)
        function createExperiment(testCase)
            
            [pathstr,~,~] = fileparts(mfilename('fullpath'));
            testCase.MSEC = 1000; %need to adjust Siekmann data into seconds
            testCase.model = FourState_6Param_AT();
            testCase.params=[3.5; 0.1; 7; 0.4; 0.05; 0.5]' * testCase.MSEC; %Siekmann 2012 generative rate constants in s^-1
            testCase.data.tres = 0.0; % in seconds, assume perfect resolution for this test
            testCase.data.concs = 1;
            testCase.data.tcrit = 9999;
            [testCase.data.bursts,~] = loadData(strcat(pathstr, {'/Data/SiekmannTest.scn'}),testCase.data.tres,testCase.data.tcrit);
            testCase.data.bursts{1}{1} = testCase.data.bursts{1}{1}/testCase.MSEC; %need duration represented in seconds
            testCase.data.useChs=0;
        end
    end
    
    methods(Test)
        function testProperties(testCase)
            
            %check defaults
            testCase.verifyEqual(testCase.model.kA,2);
            testCase.verifyEqual(testCase.model.h,0.01);
            testCase.verifyEqual(testCase.model.k,6);
            
            %check non-accessibilty
            try
                testCase.model.kA=3;
            catch ME
                testCase.verifyEqual(ME.identifier,'MATLAB:class:SetProhibited');                
            end

            try
                testCase.model.k=4;
            catch ME
                testCase.verifyEqual(ME.identifier,'MATLAB:class:SetProhibited');                
            end
            
            %check accessibilty
            testCase.model.h=0.1;
            testCase.verifyEqual(testCase.model.h,0.1);
            testCase.model.h=0.01;
            testCase.verifyEqual(testCase.model.h,0.01);
        end
        
        %test Q generation
        function testQ(testCase)
            Q=testCase.model.generateQ(testCase.params,1);
            %from 2012 paper
            testCaseQ = [-3.5 , 0 , 7 , 0; 0 , -0.1 , 0 , 0.05; 3.5, 0, -7.4, 0.5; 0 , 0.1, 0.4, -0.55 ]' * testCase.MSEC;
            testCase.verifyEqual(Q,testCaseQ,'AbsTol', 1e-6);
            
            %concnetration invariant
            Q=testCase.model.generateQ(testCase.params,0.01);
            testCaseQ = [-3.5 , 0 , 7 , 0; 0 , -0.1 , 0 , 0.05; 3.5, 0, -7.4, 0.5; 0 , 0.1, 0.4, -0.55 ]' * testCase.MSEC;
            testCase.verifyEqual(Q,testCaseQ,'AbsTol', 1e-10);
            
            params2=[1.5; 1.1; 4; 0.2; 0.02; 0.1]' * testCase.MSEC;
            Q=testCase.model.generateQ(params2,1);
            testCaseQ=[-1.5 , 0 , 4 , 0; 0 , -1.1 , 0 , 0.02; 1.5, 0, -4.2, 0.1; 0 , 1.1, 0.2, -0.12 ]' * testCase.MSEC;
            testCase.verifyEqual(Q,testCaseQ,'AbsTol', 1e-10);            
            
        end
        
        function testLikelihood(testCase)
            testCase.verifyEqual(testCase.model.calcLogLikelihood(testCase.params,testCase.data),132582.458563601,'AbsTol', 1e-10);
            testCase.verifyEqual(testCase.model.calcLogLikelihood([1.5; 1.1; 4; 0.2; 0.02; 0.1]*testCase.MSEC,testCase.data),128610.6340009236,'AbsTol', 1e-10)
        end
        
        function testCalcLogPosterior(testCase)
            testCase.verifyEqual(testCase.model.calcLogPosterior(testCase.params,testCase.data),132582.073563601,'AbsTol', 1e-10)
        end
          
        function testCalcLogPrior(testCase)
            testCase.verifyEqual(testCase.model.calcLogPrior(testCase.params),-0.385,'AbsTol', 1e-10)
            testCase.verifyEqual(testCase.model.calcLogPrior([-1; -1;-1; -1; -1; -1 ;-1; -1; -1;-1]),2e-4)
        end
    end
    
    methods (TestMethodTeardown)
        function destroyExperiment(testCase)
            clear testCase.experiment
        end
    end    
    
end