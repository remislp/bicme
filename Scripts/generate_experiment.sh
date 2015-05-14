PROJECT_ROOT=$1
EXPERIMENT=$2
RUNHOURS=$3
MEMORY=$4
INSTANCE=$5

if  [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ] || [ -z "$5" ] ; then
    echo "Not all parameters are set!"
    echo "PROJECT_ROOT=/path/to/code/root"
    echo "EXPERIMENT=1"
    echo "RUNHOURS=3"
    echo "MEMORY=4"
    echo "INSTANCE=1"
    echo "eg generate_experiment.sh /home/ucbpmep/bayesiancode 1 3 3G 10"
    exit 1
fi

echo "Generating script with the following parameters:"
echo "project_root=${PROJECT_ROOT}"
echo "experiment no=${EXPERIMENT}"

SCRIPTFILE=$(mktemp /tmp/Experiment${EXPERIMENT}.XXXXXXXXXX) || exit 1
mv $SCRIPTFILE $SCRIPTFILE.sh
SCRIPTFILE="$SCRIPTFILE.sh"
chmod u+x ${SCRIPTFILE}

cat > ${SCRIPTFILE} << EOF
#$ -l h_vmem=${MEMORY},tmem=${MEMORY}
#$ -l h_rt=${RUNHOURS}:0:0
#$ -S /bin/bash
#$ -N BayesExp${EXPERIMENT}_${INSTANCE}
#$ -wd $PROJECT_ROOT
#$ -o /home/ucbpmep/bayesiancode/ExperimentLogs/BayesExp${EXPERIMENT}_${INSTANCE}.out 
#$ -e /home/ucbpmep/bayesiancode/ExperimentLogs/BayesExp${EXPERIMENT}_${INSTANCE}.err

#pre matlab scripting
echo "script started at"
echo $( date )
echo ""
date1=\$( date +"%s" )

export LD_PRELOAD=/home/ucbpmep/gcc48/usr/local/lib64/libstdc++.so.6
export LD_LIBRARY_PATH=/opt/gridengine/lib/lx26-amd64:/home/ucbpmep/anaconda/lib:gcc48/usr/local/lib64:/home/ucbpmep/anaconda/lib:gcc48/usr/local/lib64
echo ""

/share/apps/matlabR2013a/bin/matlab -nodisplay -nodesktop -nosplash -r "try setenv('P_HOME','/home/ucbpmep/bayesiancode');addpath(genpath(pwd));${EXPERIMENT}(${INSTANCE});catch err; disp(err.message); end; quit();"

echo "script finished at"
echo \$( date )
date2=\$( date +"%s" )
diff=\$(( \$date2-\$date1 ))
echo "\$(( \$diff / 60 )) minutes and \$(( \$diff % 60 )) seconds elapsed."

EOF

echo "qsub ${SCRIPTFILE}"
qsub ${SCRIPTFILE}
