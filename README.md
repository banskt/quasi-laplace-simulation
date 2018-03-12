# Simulations for quasi-Laplace approximation using B-LORE

We use the original genotype and sample file as input to the simulations. 
The input genotype have 40000 SNPs from 5 studies (13082 patients total) were distributed over 200 loci.
Tasks performed in this pipeline:
 - [x] find the common SNPs
 - [x] perform SNPTEST / META analysis
 - [x] find the LD matrix for each loci (requires META analysis for proper ordering of SNPs)
 - [x] simulate the phenotype
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
