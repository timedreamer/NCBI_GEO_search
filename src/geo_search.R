# This script queries the NCBI GEO database for the number of gene expression microarray and 
# sequencing datasets for a given species each year.

# Output:
# "result/per_year_per_type_geo_for_{species}.pdf"
# "result/per_year_array_v_seq_for_{species}.pdf"
# "result/geo_query_result_for_{species}.tsv"

# 0. Prep -----------------------------------------------------------------

library(here)
library(rentrez)
library(tidyverse)
library(ggh4x)

theme_set(cowplot::theme_minimal_hgrid())

# Define two functions.
# Function to query NCBI GEO for given parameters. I want the number of studies each year.
query_ncbi_geo <- function(term, species, start_year, end_year) {
    results <- map_dfr(start_year:end_year, function(year) {
        query <- paste(term, "[DataSet Type]", "AND", year, "[PDAT]", "AND", species, "[ORGN]", sep = " ")
        search <- entrez_search(db = "gds", term = query)
        tibble(Year = year, Count = search$count, DataSetType = term)
    })
    return(results)
}

# Function to reorder factor levels based on total count
order_facet_by_total_count <- function(data) {
    total_counts <- data %>%
        group_by(DataSetType) %>%
        summarise(TotalCount = sum(Count)) %>%
        arrange(desc(TotalCount))
    data %>%
        mutate(DataSetType = factor(DataSetType, levels = total_counts$DataSetType))
}

# 1. Set up query terms ---------------------------------------------------

# Set inputs
start_year <- 2000
end_year <- 2023
species <- "Zea mays" # Arabidopsis thaliana, Oryza sativa, Zea mays, Homo sapiens

# Define the terms for gene expression microarray and Sequencing
terms <- list(
    microarray = c(
        "expression profiling by array",
        "expression profiling by genome tiling array",
        "expression profiling by snp array",
        "genome binding/occupancy profiling by array",
        "genome binding/occupancy profiling by genome tiling array",
        "genome binding/occupancy profiling by snp array",
        "genome variation profiling by array",
        "genome variation profiling by genome tiling array",
        "genome variation profiling by snp array",
        "methylation profiling by array",
        "methylation profiling by genome tiling array",
        "methylation profiling by snp array",
        "non coding rna profiling by array",
        "non coding rna profiling by genome tiling array",
        "protein profiling by protein array",
        "snp genotyping by snp array"
    ),
    sequencing = c(
        "expression profiling by high throughput sequencing",
        "genome binding/occupancy profiling by high throughput sequencing",
        "genome variation profiling by high throughput sequencing",
        "methylation profiling by high throughput sequencing",
        "non coding rna profiling by high throughput sequencing"
    )
)

# 2. Query the NCBI -------------------------------------------------------

# Query NCBI GEO for gene expression microarray and sequencing data
result_all <- map_dfr(names(terms), function(type) {
    map_dfr(terms[[type]], query_ncbi_geo, species, start_year, end_year) %>%
        mutate(Type = type)
})

# Reorder the DataSetType factor based on total counts
result_all_order <- order_facet_by_total_count(result_all)

# Summarize data by year and type
year_sum <- result_all_order %>%
    group_by(Year, Type) %>%
    summarise(TotalCount = sum(Count))

# 3. Plot -----------------------------------------------------------------

# Plotting microarray data
p_mic <- ggplot(result_all_order %>% filter(Type == "microarray"), aes(x = Year, y = Count)) +
    geom_point() +
    geom_smooth(se = FALSE, color = "#0072B2") +
    ylab("Number of GEO Datasets") +
    ggtitle(paste0("Number of array datasets in GEO for ", species)) +
    facet_wrap2(~ DataSetType, scales = "free_y", nrow = 4, ncol = 4, trim_blank = FALSE) +
    theme(strip.background = element_rect(fill = "grey80"),
          strip.text = element_text(color = "black", hjust = 0))

# Plotting sequencing data
p_seq <- ggplot(result_all_order %>% filter(Type == "sequencing"), aes(x = Year, y = Count)) +
    geom_point() +
    geom_smooth(se = FALSE, color = "#D55E00") +
    ylab("Number of GEO Datasets") +
    ggtitle(paste0("Number of sequencing datasets in GEO for ", species)) +
    facet_wrap2(~ DataSetType, scales = "free_y", nrow = 4, ncol = 4, trim_blank = FALSE) +
    theme(strip.background = element_rect(fill = "grey80"),
          strip.text = element_text(color = "black", hjust = 0))

# Plotting the total number of GEO datasets each year
p_year <- ggplot(year_sum, aes(Year, TotalCount, fill = Type)) +
    geom_bar(stat = "identity", position = position_dodge()) +
    scale_fill_manual(values = c("microarray" = "#0072B2", 
                                 "sequencing" = "#D55E00")) +
    labs(y = "Number of GEO datasets each year",
         title = paste0("Total number of GEO datasets for ", species))

# 4. Save plots and result table ------------------------------------------

pdf(here("result", paste0("per_year_per_type_geo_for_", gsub(" ", "", species), ".pdf")),
    width = 12, height = 8)
print(p_mic) 
print(p_seq)
dev.off()

pdf(here("result", paste0("per_year_array_v_seq_for_", gsub(" ", "", species), ".pdf")),
    width = 6, height = 4)
print(p_year)
dev.off()

write_tsv(result_all_order, 
          file = here("result",
                      paste0("geo_query_result_for_", gsub(" ", "", species), ".tsv")))
