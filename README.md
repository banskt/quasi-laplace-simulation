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
 - [x] varying h = 0.2, 0.4, 0.6 and 0.8 (fixed c = 2, &lambda; = 1)
 - [x] varying c = 2, 3, 4 and 5 (fixed h = 0.6, &lambda; = 1)
 - [x] varying &lambda; = 0.25, 0.50, 0.75, 1.00 (fixed h = 0.4, c = 2)

## Method
We used the original genotype and sample files from the five GerMIFS studies (total 13082 patients)
to select 40000 SNPs distributed over 200 loci as input.
We performed the following tasks in this pipeline:
 * create the loci using SNPs which are common to all studies
 * perform SNPTEST / META analysis with the original phenotype
 * find the LD matrix for each loci (requires META analysis for proper ordering of SNPs)
 * simulate the phenotype using different parameters
 * run SNPTEST / META, FINEMAP, PIMASS and BLORE on the data
 * plot the precision and recall values for each setting

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
./06_getplots.sh CONFIG
```

## Options in CONFIG file

Option | Description | Type | Example
:---   | :---        |:---  | :---
START | Starting simulation number (creates folders from START to END) | Integer (1 -- 999) | 1
END   | Ending simulation number | Integer (1 -- 999) | 20
HERITABILITY | Proportion of phenotypic variance explained by genotype | Float (0 -- 1) | 0.4
C_PROP | Proportion of causal SNPs | Float (0 -- 1) | 0.005
PHENO_SIM_TYPE | Type of distribution used for sampling β | String (normal, fixed, bimodal or studentsT) | "normal"
CASE_CONTROL_RATIO | Ratio of cases to controls | Float (0 -- 1) | 1.0
USE_AGESEX | Use age & sex as covariates in simulation | Boolean | false
NCAUSAL | Number of allowed causal SNPs in B-LORE | List of integers | "2 3"
NPIMASS | Number of allowed causal SNPs in PIMASS | List of integers | "2"
NFINEMAP | Number of allowed causal SNPs in FINEMAP | List of integers | "2 3"
NCAVIARBF | Number of allowed causal SNPs in CAVIARBF | List of integers | "2"
NGEMMA | Number of allowed causal SNPs in GEMMA | List of integers | "2"
NBIMBAM | Number of allowed causal SNPs in BIMBAM | List of integers | "2"
MODEL_PIMASS | Which models to use for BVSR in piMASS | List of strings (linear, probit) | "linear probit"
MODEL_GEMMA  | Which models to use for BVSR in GEMMA | List of strings (linear, probit) | "linear probit"
MUVAR | which value to use for μ in B-LORE | List of strings (0, var) | "0"
USE_BLORE_RES | whether to use π and σ learnt by B-LORE in BIMBAM and CAVIARBF | Boolean | false

The following Boolean variables control which methods to run in the pipeline:

```
bDeleteOld (deletes previous simulations -- set this to false unless needed)
bMakePheno (creates phenotype)
bRegCov (regress out the covariates, required for PIMASS, GEMMA when using covariates)
bBloreSumm (runs B-LORE summary statistics)
bBloreMeta (runs B-LORE metaanalysis)
bSnptest (runs SNPTEST)
bMeta (runs META after correcting for genomic inflation factor)
bFinemap (runs FINEMAP)
bPimass (runs piMASS)
bGemma (runs GEMMA)
bJam (runs JAM)
bBimbam (runs BIMBAM)
bCaviarbf (runs CAVIARBF)
```
