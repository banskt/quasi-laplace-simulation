#!/bin/bash

source CONFIG

SUBDIR="${CURDIR}/utils"
#CHAIN_JOBS="True"
CHAIN_JOBS="False"

for (( SIM=$START; SIM<=$END; SIM++ )); do

    INDEX=`echo $SIM | awk '{printf "%03d", $1}'`
    SIMFOLDER="sim${INDEX}"
    RANDSTRING=`cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 4 | head -n 1`

    THIS_JOBSUBDIR="${JOBSUBDIR}/${SIMFOLDER}"
    THIS_SIMDIR="${SIMDIR}/${SIMFOLDER}"

    ##if [   -d ${THIS_JOBSUBDIR} ]; then rm -rf ${THIS_JOBSUBDIR}; fi
    ##if [   -d ${THIS_SIMDIR} ];    then rm -rf ${THIS_SIMDIR};    fi

    if [ ! -d ${THIS_JOBSUBDIR} ]; then mkdir -p ${THIS_JOBSUBDIR}; fi
    if [ ! -d ${THIS_SIMDIR} ];    then mkdir -p ${THIS_SIMDIR};    fi

    cd ${THIS_JOBSUBDIR}

    BLORE_JOBSUBDIR="blore"
    SNPTEST_JOBSUBDIR="snptest"
    FINEMAP_JOBSUBDIR="finemap"
    PIMASS_JOBSUBDIR="pimass"

    BLORE_RESDIR="blore"

    source ${SUBDIR}/create_phenotype

    cd ${CURDIR}

done