# q2-convexhull2

convexhull2 is a tool for visualizing and calculating dispersion across a set of microbial samples over time through the calculation of a convex hull volume. It produces visualizations that track how group dispersion changes over time, and also how an individual's dispersion changes over time, which can be seen as a meaasure of individual volatility.

Necessary inputs:
- **Ordination** (or biplot)
- **Metadata**
- **Column:** grouping column
- **Column:** numeric time column
- **Column:** subject id column

If starting from a `biom.Table` see the tutorial `01-ch-visualizations-tutorial.ipynb` for how to generate an ordination using RPCA. A working QIIME2 environment is required for this step.
### Installation

Clone this repo and navigate into the directory to install. The `-e` flag will install in edit mode.
```
git clone https://github.com/dpear/q2-convexhull2
cd q2-convexhull2
pip install -e .

```

