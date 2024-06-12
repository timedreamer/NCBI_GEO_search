# This script uses plotnine to plot the library count. The plotting function is still much harder than R-ggplot2. So I will use ggplot2 to plot.

# Author: Ji Huang
# Date: 2024-06-08


import pandas as pd


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

os.getcwd()

df = pd.read_csv('../result/ArZeOr_sra_2008_to_2023_df_20240608.tsv', sep='\t')

from plotnine import ggplot, geom_point, aes, stat_smooth, facet_wrap, theme, theme_bw, element_text, ylab, labs, scale_color_brewer
from plotnine.data import mtcars

(
    ggplot(mtcars, aes("wt", "mpg", color="factor(gear)"))
    + geom_point()
    + stat_smooth(method="lm")
    + facet_wrap("gear")
)

p1 = (
    ggplot(df, aes("Year", "lib_count", color="factor(Species)"))
    + geom_point()
    + facet_wrap("Source", scales="free_y")
    + ylab("Library Count")
    + labs(color = "Species")
    + scale_color_brewer(type="qualitative", palette="Set2", direction=1)
    + theme_bw()
    + theme(text=element_text(size=12), 
            axis_title=element_text(size=14), 
            legend_title=element_text(size=13)) 
)

p1.save("result/sra_2000_to_2023_df_20240608.pdf", width=10, height=4)
# %%
