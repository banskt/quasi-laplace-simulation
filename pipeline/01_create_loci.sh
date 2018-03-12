#!/bin/bash

CURDIR=`pwd`
BASEDIR="/scratch/sbanerj/quasi_laplace_gwas"
COPYFROM="/scratch/sbanerj/quasi_laplace_gwas/input_files"

SCRIPTDIR="${CURDIR}/../scripts"
MASTER_JOBSUBDIR="${CURDIR}/../bsubfiles"
JOBSUBDIR="${CURDIR}/../jobsubs"

DOSAGEDIR="${BASEDIR}/loci_dosages"
REF_DOSAGEDIR="${COPYFROM}/loci_dosages"
LOCUSNAMES="${COPYFROM}/LOCUSNAMES"
CLOCICOM="${SCRIPTDIR}/create_loci.py"
QCTOOL="/usr/users/sbanerj/packages/qctool/qctool_v1.4-linux-x86_64/qctool"
STUDYNAMES=('G1' 'G2' 'G3' 'G4' 'G5')

THIS_JOBSUBDIR="${JOBSUBDIR}/create_loci"
if [ ! -d ${THIS_JOBSUBDIR} ]; then mkdir -p ${THIS_JOBSUBDIR}; fi
if [ ! -d ${DOSAGEDIR}      ]; then mkdir -p ${DOSAGEDIR}; fi
cp ${LOCUSNAMES} ${BASEDIR}/LOCUSNAMES

for STUDY in ${STUDYNAMES[@]}; do
    if [ ! -d ${DOSAGEDIR}/${STUDY} ]; then mkdir -p ${DOSAGEDIR}/${STUDY}; fi
    cp ${REF_DOSAGEDIR}/${STUDY}/*.sample ${DOSAGEDIR}/${STUDY}/
done

## ======= DO NOT CHANGE BELOW =======================

IFS=$'\r\n' GLOBIGNORE='*' command eval 'LOCIPREFIX=($(cat ${LOCUSNAMES}))'

cd ${THIS_JOBSUBDIR}

for LOCUSPREFIX in ${LOCIPREFIX[@]}; do

    JOBNAME="common_SNPs_${LOCUSPREFIX}"
    sed -e "s|_JOBNAME|${JOBNAME}|g;
            s|_SCRIPT_|${CLOCICOM}|g;
            s|_QCTOOL_|${QCTOOL}|g;
            s|_LOCUSP_|${LOCUSPREFIX}|g;
            s|_STUDYN_|\"${STUDYNAMES[*]}\"|g;
            s|_LOCIDO_|${REF_DOSAGEDIR}|g;
            s|_LOCIDN_|${DOSAGEDIR}|g;" ${MASTER_JOBSUBDIR}/create_loci.bsub > ${JOBNAME}.bsub
    bsub < ${JOBNAME}.bsub
done

cd ${CURDIR}
