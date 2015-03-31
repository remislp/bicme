classdef TestBursts < matlab.unittest.TestCase
    properties
        bursts
        bursts2
        description
        description2
    end
    
    methods (TestMethodSetup)
        function createExperiment(testCase)

            tres=2.5e-05;
            tcrit=0.0035;

            [pathstr,~,~] = fileparts(mfilename('fullpath'));

            datafiles={[pathstr '/Data/test_1.scn']};
            [testCase.bursts,testCase.description] = loadData(datafiles,tres,tcrit);
            
            %second test case with a different input file
            datafiles2={[getenv('P_HOME') '/Data/test_2.scn']};
            [testCase.bursts2,testCase.description2] = loadData(datafiles2,tres,tcrit);
        end
    end
    
    methods(Test)
        function testBurst1(testCase)
            testCase.verifyEqual(testCase.description.dataset(1).interval_no,20001);
            testCase.verifyEqual(testCase.description.dataset(1).burst_no,4142);
            testCase.verifyEqual(testCase.description.dataset(1).average_openings_per_burst,1.179623370,'AbsTol',sqrt(eps));
        end
        
        function testBurst2(testCase)
            testCase.verifyEqual(testCase.description2.dataset(1).interval_no,20001);
            testCase.verifyEqual(testCase.description2.dataset(1).burst_no,4060);
            testCase.verifyEqual(testCase.description2.dataset(1).average_openings_per_burst,1.194088670,'AbsTol',sqrt(eps));
        end
    end
    
    methods (TestMethodTeardown)
        function destroyExperiment(testCase)
            clear testCase.*
        end
    end    
    
end

