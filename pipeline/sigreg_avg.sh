#!/bin/bash

CONFIGFILE=$1

source $CONFIGFILE
source PATHS

COUNT=0
SUM=0

for (( SIM=$START; SIM<=$END; SIM++ )); do

    INDEX=`echo $SIM | awk '{printf "%03d", $1}'`
    SIMFOLDER="sim${INDEX}"
    STATFILE="${SIMDIR}/${SIMFOLDER}/blore/meta_without_feature/zmax2_mu0_pi0.01_sig0.01/blore_meta.stat"
    #STATFILE="${SIMDIR}/${SIMFOLDER}/blore_reduced_summary/meta_without_feature/zmax2_mu0_pi0.01_sig0.01/blore_meta.stat"
    SIGREG=`sed -n 3p ${STATFILE} | awk '{print $1}'`
    echo $SIMFOLDER $SIGREG
    SUM=$(echo $SUM+$SIGREG | bc )
    ((COUNT++))

done

echo $SUM $COUNT
MEAN=`echo "scale=8; $SUM / $COUNT" | bc`
echo "Average sigreg: ${MEAN}"
