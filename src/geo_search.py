import polars as pl
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from Bio import Entrez

Entrez.email = "xyz@email.com"


def query_ncbi_geo(term, species, start_year, end_year):
    results = []
    for year in range(start_year, end_year + 1):
        query = f"{term} [DataSet Type] AND {year} [PDAT] AND {species} [ORGN]"
        search = Entrez.esearch(db="gds", term=query)
        record = Entrez.read(search)
        results.append(
            {"Year": year, "Count": int(record["Count"]), "DataSetType": term}
        )
    return pl.DataFrame(results)


def order_by_total_count(data):
    total_counts = (
        data.groupby("DataSetType")
        .agg(pl.col("Count").sum().alias("TotalCount"))
        .sort("TotalCount", reverse=True)
    )
    ordered_categories = total_counts["DataSetType"]
    return data.with_column(
        pl.col("DataSetType").cast(pl.Categorical).cat.set_ordering(ordered_categories)
    )


terms = {
    "microarray": [
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
        "snp genotyping by snp array",
    ],
    "sequencing": [
        "expression profiling by high throughput sequencing",
        "genome binding/occupancy profiling by high throughput sequencing",
        "genome variation profiling by high throughput sequencing",
        "methylation profiling by high throughput sequencing",
        "non coding rna profiling by high throughput sequencing",
    ],
}
species = "Zea mays"
start_year = 2022
end_year = 2023

results = [
    query_ncbi_geo(term, species, start_year, end_year)
    for type_, terms_list in terms.items()
    for term in terms_list
]

results = []
for type_, terms_list in terms.items():
    for term in terms_list:
        result_df = query_ncbi_geo(term, species, start_year, end_year)
        results.append(result_df)
list(terms.values())[0][1]
list(terms.keys())
next(iter(terms.keys()))

result_all = pl.concat(results)
tt2 = result_all.to_pandas()

tt2.dtypes
pl.Enum(tt2_order)
cat_type = pd.CategoricalDtype(categories=tt2_order, ordered=True)
# Convert the string column to an ordered categorical column
tt2["DataSetType"] = tt2["DataSetType"].astype(cat_type)


print(tt2)
print(tt2["DataSetType"].dtype)  # Check the dtype to confirm it's an ordered categorical


# Directly order by total counts within the DataFrame
total_counts = result_all.groupby('DataSetType').agg(pl.col('Count').sum().alias('TotalCount'))

item_order = total_counts.sort("TotalCount", descending=True)
tt1 = total_counts.sort("TotalCount", descending=True)
tt1.to_series(0).to_list()
tt2_order = tt1.to_series().to_list()

df = result_all.with_columns(
    pl.col("DataSetType").cast(pl.Categorical).cat.set_ordering(tt2_order)
)


result_all_ordered = result_all.select(pl.col("DataSetType").cast(pl.Categorical)
)



result_all_ordered = order_by_total_count(result_all)

yearly_summary = (
    result_all.groupby(["Year", "DataSetType"])
    .agg(pl.col("Count").sum().alias("TotalCount"))
    .to_pandas()
)

sns.set(style="whitegrid")
plt.figure(figsize=(14, 7))
sns.barplot(data=yearly_summary, x="Year", y="TotalCount", hue="DataSetType")
plt.title(f"Annual Distribution of GEO Dataset Types for {species}")
plt.ylabel("Number of Datasets")
plt.xlabel("Year")
plt.legend(title="Dataset Type")
plt.tight_layout()
plt.show()
