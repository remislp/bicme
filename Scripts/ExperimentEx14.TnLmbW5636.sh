#$ -l h_vmem=4G,tmem=4G
#$ -l h_rt=12:0:0
#$ -S /bin/bash
#$ -t 1-10:1
#$ -N BayesExpEx14VaryTres
#$ -wd /home/ucbpmep/bicme
#$ -o /home/ucbpmep/bicme/Logs/BayesExpEx14.out 
#$ -e /home/ucbpmep/bicme/Logs/BayesExpEx14.err

#pre matlab scripting
echo "script started at"
echo Tue Mar 31 14:40:26 BST 2015
echo ""
date1=$( date +"%s" )

export LD_PRELOAD=/home/ucbpmep/gcc48/usr/local/lib64/libstdc++.so.6
export LD_LIBRARY_PATH=/opt/gridengine/lib/lx26-amd64:/home/ucbpmep/anaconda/lib:gcc48/usr/local/lib64:/home/ucbpmep/anaconda/lib:gcc48/usr/local/lib64
echo ""

/share/apps/matlabR2013a/bin/matlab -nodisplay -nodesktop -nosplash -r "try addpath(genpath(pwd));fprintf('SGE %d\n',${SGE_TASK_ID});rng(${SGE_TASK_ID});treses = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1];Ex14InitialAllTogether_Vary_Res(${SGE_TASK_ID},treses(${SGE_TASK_ID}));catch err; disp(err.message); end; quit();"

echo "script finished at"
echo $( date )
date2=$( date +"%s" )
diff=$(( $date2-$date1 ))
echo "$(( $diff / 60 )) minutes and $(( $diff % 60 )) seconds elapsed."

