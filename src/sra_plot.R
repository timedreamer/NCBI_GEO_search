# This script plots the SRA DNA and RNA libraries for three plant species and three mammalian species. The inputs were from `sra_search.py`.

# Author: Ji Huang
# Date: 2024-06-09

library(here)
library(tidyverse)
library(cowplot)
library(scales)
library(ggh4x)

theme_set(cowplot::theme_minimal_hgrid())

df_plant <- read_tsv(here("result", "ArZeOr_sra_2008_to_2023_df_20240608.tsv"))

df_mammal <- read_tsv(here("result", "HoMuRa_sra_2008_to_2023_df_20240609.tsv"))

p_plant  <- ggplot(df_plant, aes(Year, lib_count, color = Species)) +
    geom_point() +
    geom_line(linewidth = 0.2) +
    facet_grid2(~Source, scales = "free_y", independent = "y") +
    scale_color_brewer(palette = "Set2") +
    labs(y = "Number of SRA libraries") +
    scale_y_continuous(labels = label_number(scale_cut = cut_short_scale()),
        breaks = breaks_pretty())

p_mammal <- ggplot(df_mammal, aes(Year, lib_count, color = Species)) +
    geom_point() +
    geom_line(linewidth = 0.2) +
    facet_grid2(~Source, scales = "free_y", independent = "y") +
    scale_color_brewer(palette = "Set2") +
    labs(y = "Number of SRA libraries") +
    scale_y_continuous(labels = label_number(scale_cut = cut_short_scale()),
        breaks = breaks_pretty())

pdf(here("result", "sra_library_plot.pdf"), width = 8, height = 4)
print(p_plant)
print(p_mammal)
dev.off()

