# Simulation pipeline for validation of quasi-Laplace approximation

We use B-LORE to perform quasi-Laplace approximation for multiple logistic regression.
We compare quasi-Laplace multiple logistic regression with:
 * multiple probit regression (piMASS, GEMMA)
 * multiple logistic regression with linear approximation (FINEMAP)
 * multiple linear regression (piMASS)

In our simulations, we vary the following parameters:
 * heritability (h)
 * maximum number of causal SNPs allowed (c)
 * ratio of cases to controls (&lambda;)

We compare the posterior inclusion probabilities (PIPs) with the following settings:
 - [ ] varying h = 0.2, 0.4, 0.6 and 0.8 (fixed c = 2, &lambda; = 1)
 - [ ] varying c = 2, 3, 4 and 5 (fixed h = 0.4, &lambda; = 1)
 - [ ] varying &lambda; = 0.5, 0.75, 1 (fixed h = 0.4, c = 2)
 - [ ] including covariates (fixed h = 0.4, c = 2, &lambda; = 1)

## Method
We used the original genotype and sample files from the five GerMIFS studies (total 13082 patients)
to select 40000 SNPs distributed over 200 loci as input.
We performed the following tasks in this pipeline:
 - [x] find the SNPs which are common to all studies
 - [x] perform SNPTEST / META analysis with the original phenotype
 - [x] find the LD matrix for each loci (requires META analysis for proper ordering of SNPs)
 - [x] simulate the phenotype using different parameters
 - [ ] apply different methods
 - [ ] perform the analyses.

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
