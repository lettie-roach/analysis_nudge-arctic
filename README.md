Code for the figures and analysis in `Observed winds crucial for September Arctic sea ice loss'

Citation: Roach, L. A., & Blanchard-Wrigglesworth, E. (2022). Observed winds crucial for September Arctic sea ice loss. Geophysical Research Letters, 49, e2022GL097884. https://doi.org/10.1029/2022GL097884

Analysis code developed by LR.

This repository contains:

- my_utils.py - a file containing Python functions used in multiple notebooks.
 
- processing/ - a directory containing Python notebooks that were used to process model output from the CESM1 LENS1, nudging experiments conducted for this study, and observational data (from NSIDC, ERA-Interim, GISTEMP, HADISST, HADCRUT). These are specific to Cheyenne

- nudge-arctic_figs*.ipynb - the notebooks used to produce all figures in the above paper. Anyone should be able to run these after downloading this repository and the processed netcdf files in the associated Zenodo repository https://doi.org/10.5281/zenodo.6313665 

