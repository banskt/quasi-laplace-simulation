# Simulation pipeline for validation of quasi-Laplace approximation

B-LORE uses quasi-Laplace approximation for multiple logistic regression.
In this simulation pipeline, we compare quasi-Laplace multiple logistic regression with other methods:
 * multiple probit regression (piMASS, GEMMA) using point-normal prior
 * multiple logistic regression with linear approximation (FINEMAP) using point-normal prior
 * multiple linear regression (piMASS, GEMMA) using point-normal prior
 * simple logistic regression (SNPTEST)

In our simulations, we vary the following parameters:
 * heritability (h)
 * maximum number of causal SNPs allowed (c)
 * ratio of cases to controls (&lambda;)

We compare the posterior inclusion probabilities (PIPs) with the following settings:
 - [ ] varying h = 0.2, 0.4, 0.6 and 0.8 (fixed c = 2, &lambda; = 1)
 - [ ] varying c = 2, 3, 4 and 5 (fixed h = 0.4, &lambda; = 1)
 - [ ] varying &lambda; = 0.25, 0.50, 0.75, 1.00 (fixed h = 0.4, c = 2)
 - [ ] including covariates (fixed h = 0.4, c = 2, &lambda; = 1)

## Method
We used the original genotype and sample files from the five GerMIFS studies (total 13082 patients)
to select 40000 SNPs distributed over 200 loci as input.
We performed the following tasks in this pipeline:
 * create the loci using SNPs which are common to all studies
 * perform SNPTEST / META analysis with the original phenotype
 * find the LD matrix for each loci (requires META analysis for proper ordering of SNPs)
 * simulate the phenotype using different parameters
 * run SNPTEST / META, FINEMAP, PIMASS, GEMMA and BLORE on the data

## Input files
The pipeline expects input genotype and phenotype to be organized in the following way:
```
{DOSAGEDIR}
   -- {STUDY}
         -- {LOCUSPREFIX}.gen
         -- {LOCUSPREFIX}.map
         -- {STUDY}{SAMPLEPREFIX}.sample
```
There could be multiple ```{STUDY}``` folders in the ```{DOSAGEDIR}``` and multiple ```{LOCUSPREFIX}``` within each study. 
However the ```{LOCUSPREFIX}``` should be exactly same in each study. 

The genotype and sample files are in the Oxford format.
Additionally, the sample file should contain covariates called 'sex' and 'age'. 
The binary phenotype should be in the last column, which should be named 'pheno'.

## How to run
The simulation can be run from the ```pipeline``` folder. Update the ```CONFIG``` and ```PATHS``` file and run:
```
./01_create_loci.sh
./02_run_snptest_meta.sh
./03_create_ldmatrix.sh
./04_find_loci_with_max_snps.sh
./05_simulate.sh CONFIG
```
