classdef TestModelSevenState_10Param_AT < matlab.unittest.TestCase
    properties
        model
        params
        data
    end
    
    methods (TestClassSetup)
        function createExperiment(testCase)
            
            [pathstr,~,~] = fileparts(mfilename('fullpath'));
          
            testCase.model = SevenState_10Param_AT();
            testCase.params=[1500 50000 2000 20 80000 300 1e8 1000 20000 1e8]'; %guess2 rate constants
            testCase.data.tres = 0.000025;
            testCase.data.concs = 3e-8;
            testCase.data.tcrit = 0.0035;
            [testCase.data.bursts,~] = loadData(strcat(pathstr, {'/Data/test_1.scn'}),testCase.data.tres,testCase.data.tcrit);
            testCase.data.useChs=1;
        end
    end
    
    methods(Test)
        function testProperties(testCase)
            
            %check defaults
            testCase.verifyEqual(testCase.model.kA,3);
            testCase.verifyEqual(testCase.model.h,0.01);
            testCase.verifyEqual(testCase.model.k,10);
            
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
            %from 2003 blue book
            testCaseQ=[-1500.0000000000,0.0000000000,0.0000000000,50000.0000000000,0.0000000000,0.0000000000,0.0000000000,0.0000000000,-2000.0000000000,0.0000000000,0.0000000000,20.0000000000,0.0000000000,0.0000000000,0.0000000000,0.0000000000,-80000.0000000000,0.0000000000,0.0000000000,300.0000000000,0.0000000000,1500.0000000000,0.0000000000,0.0000000000,-71000.0000000000,100000000.0000000000,100000000.0000000000,0.0000000000,0.0000000000,2000.0000000000,0.0000000000,20000.0000000000,-100001020.0000000000,0.0000000000,100000000.0000000000,0.0000000000,0.0000000000,80000.0000000000,1000.0000000000,0.0000000000,-100020300.0000000000,100000000.0000000000,0.0000000000,0.0000000000,0.0000000000,0.0000000000,1000.0000000000,20000.0000000000,-200000000.0000000000 ]';
            testCase.verifyEqual(Q(:),testCaseQ,'AbsTol', 1e-6);
            
            Q=testCase.model.generateQ(testCase.params,0.01);
            testCaseQ=[-1500.0000000000,0.0000000000,0.0000000000,50000.0000000000,0.0000000000,0.0000000000,0.0000000000,0.0000000000,-2000.0000000000,0.0000000000,0.0000000000,20.0000000000,0.0000000000,0.0000000000,0.0000000000,0.0000000000,-80000.0000000000,0.0000000000,0.0000000000,300.0000000000,0.0000000000,1500.0000000000,0.0000000000,0.0000000000,-71000.0000000000,1000000.0000000000,1000000.0000000000,0.0000000000,0.0000000000,2000.0000000000,0.0000000000,20000.0000000000,-1001020.0000000000,0.0000000000,1000000.0000000000,0.0000000000,0.0000000000,80000.0000000000,1000.0000000000,0.0000000000,-1020300.0000000000,1000000.0000000000,0.0000000000,0.0000000000,0.0000000000,0.0000000000,1000.0000000000,20000.0000000000,-2000000.0000000000 ]';
            testCase.verifyEqual(Q(:),testCaseQ,'AbsTol', 1e-10);
            
            params2=[1500,50000,12000,50,14000,10,100000000,6000,5000,200000000];
            Q=testCase.model.generateQ(params2,0.00001);
            testCaseQ=[-1500.0000000000,0.0000000000,0.0000000000,50000.0000000000,0.0000000000,0.0000000000,0.0000000000,0.0000000000,-12000.0000000000,0.0000000000,0.0000000000,50.0000000000,0.0000000000,0.0000000000,0.0000000000,0.0000000000,-14000.0000000000,0.0000000000,0.0000000000,10.0000000000,0.0000000000,1500.0000000000,0.0000000000,0.0000000000,-61000.0000000000,2000.0000000000,1000.0000000000,0.0000000000,0.0000000000,12000.0000000000,0.0000000000,5000.0000000000,-8050.0000000000,0.0000000000,1000.0000000000,0.0000000000,0.0000000000,14000.0000000000,6000.0000000000,0.0000000000,-6010.0000000000,2000.0000000000,0.0000000000,0.0000000000,0.0000000000,0.0000000000,6000.0000000000,5000.0000000000,-3000.0000000000  ]';
            testCase.verifyEqual(Q(:),testCaseQ,'AbsTol', 1e-10);            
            
        end
        
        function testLikelihood(testCase)
            testCase.verifyEqual(testCase.model.calcLogLikelihood(testCase.params,testCase.data),3.858668411122054e+04,'AbsTol', 1e-6);
            testCase.verifyEqual(testCase.model.calcLogLikelihood([15000,50000,13000,50,15000,10,150000000,6000,5000,150000000],testCase.data),3.355036228698904e+04,'AbsTol', 1e-6)
            testCase.verifyEqual(testCase.model.calcLogLikelihood([1500,50000,18000,50,15700,17,2e8,4000,5000,100000000],testCase.data),3.852808259951792e+04,'AbsTol', 1e-6)
            testCase.verifyEqual(testCase.model.calcLogLikelihood([150,5000,130000,500,1500,10,2e8,8000,7000,50000000],testCase.data),3.349705432531993e+04,'AbsTol', 1e-6)
        end
        
        function testCalcLogPosterior(testCase)
            testCase.verifyEqual(testCase.model.calcLogPosterior(testCase.params,testCase.data),3.843010832496134e+04,'AbsTol', 1e-6)
        end
        
        
        function testCalcLogPrior(testCase)
            testCase.verifyEqual(testCase.model.calcLogPrior(testCase.params),-1.565757862435931e+02,'AbsTol', 1e-6)
            testCase.verifyEqual(testCase.model.calcLogPrior([-1; -1;-1; -1; -1; -1 ;-1; -1; -1;-1]),-Inf)
        end
        
        function testSamplePrior(testCase)
            rng(1)
            testCase.verifyEqual(testCase.model.samplePrior,1.0e+09 * [0.000417022010532;0.000720324496239;0.000000114384816;0.000302332579609;0.000146755899350;0.000092338603845;1.862602113784847;0.000345560733587;0.000396767480263;5.388167340038181],'AbsTol', 1e-6)
            rng('shuffle', 'twister')
        end
    end
    
    methods (TestMethodTeardown)
        function destroyExperiment(testCase)
            clear testCase.experiment
        end
    end    
    
end