# Description: This script searches the SRA database for the number of libraries for a given species and source in a given year range.

# Author: Ji Huang
# Date: 2024-06-08


import Bio.Entrez as Entrez
import pandas as pd
import os
from itertools import product
from datetime import datetime

def search_sra(year, species, source):
    query_term = f"{species}[ORGN] AND {source}[SRC] AND {year}[PDAT]"

    try:
        handle = Entrez.esearch(db="sra", retmax=10, term=query_term)
        record = Entrez.read(handle)
        handle.close()
        return record['Count']
    except Exception as e:
        print(f"Error searching SRA: {e}")

def main(start_year, end_year, species_list, source_list):
    Entrez.email = "Your.Name.Here@example.org"

    df = pd.DataFrame(columns=["Year", "Species", "Source", "lib_count"])
    
    for year, (species, source) in product(range(start_year, end_year + 1), product(species_list, source_list)):
        
        lib_count = search_sra(year = year , species = species, source = source)

        result = [year, species, source, lib_count]
        df.loc[len(df)] = result

    return df

if __name__ == "__main__":
    start_year = 2008
    end_year = 2023
    species_list = ["Homo sapien", "Mus musculus", "Rattus norvegicus"]
    # species_list = ["Arabidopsis thaliana", "Zea mays", "Oryza sativa"]
    source_list = ["transcriptomic", "genomic"]
    df = main(start_year, end_year, species_list, source_list)

    # Ensure the result directory exists
    os.makedirs("result", exist_ok=True)
    current_date = datetime.now().strftime("%Y%m%d")
    
    species_initials = ''.join([species[:2] for species in species_list])

    df.to_csv(f"result/{species_initials}_sra_{start_year}_to_{end_year}_df_{current_date}.tsv", sep='\t', index=False)
    print(df)
