%[pathstr,~,~] = fileparts(mfilename('fullpath'));
%normal test case parameters
normal.model = NormalModel();       
a=load('/Data/NormData.mat');
normal.startParams=[2; 10];  
normal.data=a.data;
normal.rwmhProposalScheme = RwmhProposal(eye(2,2),0);    
normal.SamplerParams.Samples=10;
normal.SamplerParams.Burnin=5;
normal.SamplerParams.AdjustmentLag=5;
normal.SamplerParams.NotifyEveryXSamples=10;
normal.SamplerParams.LowerAcceptanceLimit=0.3;
normal.SamplerParams.UpperAcceptanceLimit=0.7;
normal.SamplerParams.ScaleFactor=0.5;            
            
sampler = Sampler();


rng(1)


samples = sampler.blockSample(normal.SamplerParams,normal.model,normal.data,normal.rwmhProposalScheme,normal.startParams);
            %check samples, likelihoods  
