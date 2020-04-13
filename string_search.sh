#!/bin/bash

STRING=$1
SDIR=$2

grep -snIHR --color --exclude-dir=".git" --exclude-dir="jobsubs" --exclude-dir=".ipynb_checkpoints" "${STRING}" ${SDIR}
