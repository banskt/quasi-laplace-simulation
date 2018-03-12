#!/bin/bash

source CONFIG

RANDSTRING=`cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 4 | head -n 1`
LD_JOBSUBDIR="${JOBSUBDIR}/ldjobs"
THIS_SIMDIR="${BASEDIR}/metaanalysis"

if [ ! -d ${LD_JOBSUBDIR} ];   then mkdir -p ${LD_JOBSUBDIR};   fi
cd ${LD_JOBSUBDIR}

LDSTORE_JOBNAME="ldmatrix_${RANDSTRING}"
for STUDY in ${STUDYNAMES[@]}; do
    JOBNAME="${LDSTORE_JOBNAME}_${STUDY}"
    OUTDIR="${LDBASEDIR}/${STUDY}"
    sed "s|_JOBNAME|${JOBNAME}|g;
         s|_GSTUDY_|${STUDY}|g;
         s|_USELOCI|${LOCUSNAMES}|g;
         s|_LOCIDIR|${DOSAGEDIR}/${STUDY}|g;
         s|_LDSTORE|${LDSTORE}|g;
         s|_OUTDIR_|${OUTDIR}|g;
         " ${MASTER_JOBSUBDIR}/ldstore.bsub > ${JOBNAME}.bsub
    bsub < ${JOBNAME}.bsub
done

for LOCUSPREFIX in ${LOCIPREFIX[@]}; do
    WGT_LD_JOBNAME="weighted_LD_${LOCUSPREFIX}"
    sed -e "s|_JOBNAME|${WGT_LD_JOBNAME}|g;
            s|_WGHT_LD|${LDMAP_WEIGHTED}|g;
            s|_LOCUSP_|${LOCUSPREFIX}|g;
            s|_STUDYN_|\"${STUDYNAMES[*]}\"|g;
            s|_SAMPLES|\"${STUDYSAMPLES[*]}\"|g;
            s|_SIMDIR_|${THIS_SIMDIR}|g;
            s|_LDBASE_|${LDBASEDIR}|g;
            s|_LD_DIR_|${LDMAPDIR}|g;
            " ${MASTER_JOBSUBDIR}/ldmap_weighted.bsub > ${WGT_LD_JOBNAME}.bsub
    bsub -w "done(${LDSTORE_JOBNAME}*)" < ${WGT_LD_JOBNAME}.bsub
done

STUDY="combined"
JOBNAME="${LDSTORE_JOBNAME}_${STUDY}"
OUTDIR="${LDBASEDIR}/${STUDY}"
sed "s|_JOBNAME|${JOBNAME}|g;
     s|_GSTUDY_|${STUDY}|g;
     s|_USELOCI|${LOCUSNAMES}|g;
     s|_LOCIDIR|${DOSAGEDIR}/${STUDY}|g;
     s|_LDSTORE|${LDSTORE}|g;
     s|_OUTDIR_|${OUTDIR}|g;
     " ${MASTER_JOBSUBDIR}/ldstore.bsub > ${JOBNAME}.bsub
bsub < ${JOBNAME}.bsub

cd ${CURDIR}
