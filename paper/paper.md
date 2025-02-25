---
title: 'q2-convexhull: quantifying and visualizing longitudinal dispersion in mircobiome datasets'
tags:
- microbiome
- beta diversity
- metagenomics
- bioinformatics
authors:
- name: Daniela S Perry
  orcid: 0000-0001-6870-1194
  affiliation: 1
- name: Cameron Martino
  orcid: 0000-0001-9334-1258
  affiliation: 1
- name: Daniel McDonald
  orcid: 0000-0003-0876-9060
  affiliation: 1
- name: Celeste Allaband
  orcid: 0000-0003-1832-4858
  affiliation: 1
- name: Rob Knight
  orcid: 0000-0002-0975-9019
  affiliation: "1, 2, 3, 4, 5, 6"
affiliations:
- name: Department of Pediatrics, University of California San Diego, La Jolla, CA, USA
  index: 1
- name: Human Milk Institute (HMI), University of California San Diego, La Jolla, CA, USA
  index: 2
- name: Center for Microbiome Innovation, University of California San Diego, La Jolla, CA, USA
  index: 3
- name: Department of Computer Science and Engineering, University of California San Diego, La Jolla, CA, USA
  index: 4
- name: Shu Chien-Gene Lay Department of Bioengineering, University of California San Diego, La Jolla, CA, USA
  index: 5
- name: Halıcıoğlu Data Science Institute, University of California San Diego, La Jolla, CA, USA
  index: 6
date: 13 February 2025
bibliography: references.bib
---

## Summary

q2-convexhull is a package for assessing longitudinal changes in group dispersion in microbiome data over time by calculating convex hull volumes and visualizing them in 3D and quantifying dispersion of individuals over time. It is integrated with the popular QIIME2 microbial data analysis suite [@Bolyen2019-oo] (Bolyen et al. 2019), and provides standalone functionality in python. It is applicable to a wide range of data types including a variety of ‘omics, such as microbiome(Song et al. 2021) and metabolome (Boardman 1993), that undergo dimensionality reduction. In this package, 3D hulls are displayed over each group of interest at each timepoint (Figure 1A). A group analysis employs a bootstrapping technique described below to plot the distribution of dispersion of all groups over time (Figure 1B). An individual analysis calculates the convex hull volume over a single individual’s multiple time points, and compares these volumes of individuals from different groups (Figure 1C).

A sample metadata (.csv file) with column names defining group, individual, and time (optional), as well as an ordination are given as input. Optional parameters include rotation display for 3D plots and 3D axis visibility, along with the ability for a user to define subsampling depth and number of iterations for the bootstrapping step. 

We utilize ConvexHull from scipy (Virtanen et al. 2020) that wraps the Qhull library, which implements the Quickhull algorithm (Barber, Dobkin, and Huhdanpaa 1996) in 3D, a divide and conquer algorithm that works similarly to QuickSort in O(n log n) time. In our package, pandas(McKinney 2010) is used for data manipulation and scikit-bio(citation) is is used for ordination manipulations; seaborn(Waskom 2021) and matplotlib(The Matplotlib Development Team 2024) are used to produce plots.

# Acknowledgments
TODO

# References
TODO
