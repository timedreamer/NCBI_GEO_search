# README

Author: Ji Huang
Date: 2024-05-27

I wrote a simple R script `geo_search.R` to query the NCBI-GEO datasets to see whether microarrays are still been used for several species. I also query the sequencing datasets.

This is not a perfect search as I only queried the GEO. Many sequencing libraries are only at SRA. Also, some early day microarray data is probably not on GEO. Besides, I only counted the number of *datasets*, not the samples within the datasets.

With that being said, I'm likely underestimate the sequencing data. 

A while back, I also wrote some Python code to query the number of DNA and RNA sequencing libraies on SRA. See `SRA_search.ipynb`.