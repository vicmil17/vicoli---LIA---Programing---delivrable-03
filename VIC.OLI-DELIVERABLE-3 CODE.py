# ================================================================
# File: VIC.OLI-DELIVERABLE-3 CODE.py
# Author: OLIVIA MARAGOS and VICTORIA MILIOTO 
# Course: Python Programming 
# Date: November 2025
# Description:
#  This delievrable will be used to perform an Exploratory Data Analysis (EDA) 
#  to our dataset. 

# ================================================================
# Initial Data Inspection
# ---------------------------------------------------------------
# THOUGHT PROCESS 
# data.head() displays the first five rows, 
# allowing a quick look at the columns and how data is formatted.
# data.shape returns the dataset’s dimensions. 
    #For example, (149, 20) would mean 149 countries (rows) and 20 variables (columns).
# data.info() provides data types and shows which columns contain missing values.
# data.describe() summarizes the central tendency and 
# spread (mean, median, min, max, quartiles) of all numeric columns.
# ---------------------------------------------------------------

import pandas as pd
data = pd.read_csv("world-happiness-report-2021.csv")

# View the first 5 rows
print(data.head())

# Check the dimensions (rows, columns)
print("Shape of dataset:", data.shape)

# Summary of column names, data types, and missing values
print(data.info())

# Statistical summary of numeric columns
print(data.describe())

# ================================================================
# Handling Duplicate Entries
# ---------------------------------------------------------------
# THOUGHT PROCESS
# data.duplicated().sum() counts how many rows appear more than once.
# drop_duplicates() removes those redundant rows.
# ---------------------------------------------------------------

duplicates = data.duplicated().sum()
print ("Number of duplicate rows:", duplicates)

data = data.drop_duplicates()

# ================================================================
# Identifying and Managing Missing Values
# ---------------------------------------------------------------
# THOUGHT PROCESS
# .isnull() checks every single cell in the dataset 
# and returns True if that cell is missing (blank, NaN, or None) and False otherwise.
# .sum() then counts how many True values appear in each column.
# .fillna(...) replaces any NaN (missing) cells in the dataset 
# with the values you specify.
# ---------------------------------------------------------------
# JUSTIFICATION
    # Dropping rows would eliminate countries 
    # that are still valuable for broader global comparisons.
    # Filling numeric gaps with the mean preserves 
    # dataset size while maintaining reasonable averages.
    # Replacing missing text data with “Unknown” avoids 
    # blank cells and clarifies which values were originally absent.
# ---------------------------------------------------------------

# Check for missing values in each column
print(data.isnull().sum())

# Fill numeric missing values with column means
data = data.fillna(data.mean(numeric_only=True))

# Fill missing text data with a label
data = data.fillna("Unknown")

# Verify no missing values remain
print(data.isnull().sum())

# ================================================================
# Correcting Data Types and Formats
# ---------------------------------------------------------------
# THOUGHT PROCESS
# .pd.to_numeric() converts text-like numbers (e.g., "7.1") into 
# real floating-point numbers.and confirmed the results using .info() again.
# errors="coerce" argument forces any non-numeric entries to become NaN (placeholder for missing values)
# ---------------------------------------------------------------

# Convert numeric-looking columns stored as text
data["Ladder score"] = pd.to_numeric(data["Ladder score"], errors="coerce")
data["Logged GDP per capita"] = pd.to_numeric(data["Logged GDP per capita"], errors="coerce")
data["Freedom to make life choices"] = pd.to_numeric(data["Freedom to make life choices"], errors="coerce")

# Recheck the structure
print(data.info())

# ================================================================
# PART 3
# ---------------------------------------------------------------
# Univariate non-graphical EDA
# ---------------------------------------------------------------
# THOUGHT PROCESS 
# \n adds a blank line before the table output.
# .iloc[] selects the first row (by position)
# numeric_only=True -> ignore text columns and only calculate using numeric data
# ---------------------------------------------------------------

print(data.nunique())
print("Unique categories per column:\n", data.nunique())
print("\nFrequency counts for Region:\n", data["Regional indicator"].value_counts())
print("\nProportion (%):\n", (data["Regional indicator"].value_counts(normalize=True) * 100).round(2))
print("\nMost frequent category (mode):", data["Regional indicator"].mode()[0])

print(data.describe())
print("Mode:\n", data.mode().iloc[0])
print("Variance:\n",  data.var(numeric_only=True))
print("Skewness:\n",  data.skew(numeric_only=True))
print("Kurtosis:\n",  data.kurt(numeric_only=True))

# ---------------------------------------------------------------
# INTERPRETATION -- added for section 3 
# Moderate variance acorss most numeric values -> diverse country conditions
# ladder score shows low skewness, representing symmetrical happiness distributions worldwide.
#  Kurtosis values near zero indicate distributions without extreme outliers.

# ================================================================
# PART 4
# ---------------------------------------------------------------
# Univariate graphical EDA
# ---------------------------------------------------------------
# a) Custom bins + Kernel Density Estimation


import seaborn as sns
import matplotlib.pyplot as plt

sns.histplot(data=data, x="Ladder score", bins=12, kde=True, color="skyblue")
plt.title("Distribution of Ladder Score (Happiness)")
plt.xlabel("Ladder Score")
plt.ylabel("Number of Countries")
plt.show()
# ---------------------------------------------------------------
# INTERPRETATION
# The Ladder score is approximately normal, centered around 5.5.
# Slight left skew (longer tail on the lower end).
# No extreme outliers; most countries fall between 4 and 7.
# The median and mean are close, confirming near symmetry.
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# b) Normalized Histogram + KDE
# ---------------------------------------------------------------
# THOUGHT PROCESS 
# stat="density" normalizes the histogram so the total area = 1.
# The KDE curve overlays to show probability density.
# ---------------------------------------------------------------


sns.histplot(data=data, x="Logged GDP per capita", bins=15, kde=True, stat="density", color="lightgreen")
plt.title("Distribution of Logged GDP per Capita")
plt.xlabel("Logged GDP per Capita")
plt.ylabel("Density")
plt.show()
# ---------------------------------------------------------------
# INTERPRETATION
# Middle-income nations dominate between values 9–10
# High-income countries form a smaller right tail
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# c) Conditioning by Region + Dodge Bars
# ---------------------------------------------------------------
# THOUGHT PROCESS 
# multiple="dodge" → creates separate side-by-side bars per region
# ---------------------------------------------------------------

sns.histplot(data=data, x="Freedom to make life choices", hue="Regional indicator", multiple="dodge", bins=10)
plt.title("Freedom to Make Life Choices by Region")
plt.xlabel("Freedom (0–1)")
plt.ylabel("Count")
plt.show()
# ---------------------------------------------------------------
# INTERPRETATION
# Western Europe and North America cluster near high freedom (0.8–0.9)
# Sub-Saharan Africa and South Asia show more low-freedom values
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# d) Stacked Histogram (Conditioning by Income Group)
# ---------------------------------------------------------------
# THOUGHT PROCESS 
# multiple="stack" → overlays histograms by category to show contribution per group.
# pd.cut() → “Cut” means “slice a numeric column into intervals.”
# ---------------------------------------------------------------

data["Income group"] = pd.cut(
    data["Logged GDP per capita"],
    bins=[0, 8.5, 9.5, 10.5, 12],
    labels=["Low", "Middle", "High", "Very High"])

sns.histplot(data=data, x="Social support", hue="Income group", multiple="stack", bins=12)
plt.title("Social Support by Income Group (Based on GDP)")
plt.xlabel("Social Support (0–1)")
plt.ylabel("Number of Countries")
plt.show()
# ---------------------------------------------------------------
# INTERPRETATION
# Low-income countries cluster on the lower end (0.55–0.75)
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# e) Kernel Density Estimation with Bandwidth Control
# ---------------------------------------------------------------

sns.kdeplot(data=data, x="Healthy life expectancy", bw_adjust=0.6, fill=True, color="orange")
plt.title("KDE of Healthy Life Expectancy")
plt.xlabel("Healthy Life Expectancy (Years)")
plt.ylabel("Density")
plt.show()
# ---------------------------------------------------------------
# INTERPRETATION
# Two peaks reflect inequality between lower-income (~55–60 yrs) and richer nations (~65–70 yrs))
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# f) Empirical Cumulative Distribution (ECDF)
# ---------------------------------------------------------------

sns.ecdfplot(data=data, x="Generosity", color="purple")
plt.title("Empirical Cumulative Distribution of Generosity")
plt.xlabel("Generosity Score")
plt.ylabel("Cumulative Probability")
plt.show()
# ---------------------------------------------------------------
# INTERPRETATION
# Over half of all countries have generosity below 0.05
# ---------------------------------------------------------------

# ================================================================
# PART 5
# ---------------------------------------------------------------
# Multivariate non-graphical EDA
# ---------------------------------------------------------------

import pandas as pd

# Group countries by income level (using Logged GDP per capita)
data["Income group"] = pd.cut(
    data["Logged GDP per capita"],
    bins=[0, 8.5, 9.5, 10.5, 12],
    labels=["Low", "Middle", "High", "Very High"])

# Group countries by freedom levels
data["Freedom group"] = pd.cut(
    data["Freedom to make life choices"],
    bins=[0, 0.4, 0.7, 1.0],
    labels=["Low", "Medium", "High"])

# Group countries by life expectancy level
data["LifeExp group"] = pd.cut(
    data["Healthy life expectancy"],
    bins=[0, 55, 70, 85],
    labels=["Low", "Medium", "High"])

# 5.1 Crosstab 1 — Income group × Region
ct1 = pd.crosstab(data["Income group"], data["Regional indicator"], normalize="columns")
print(ct1.round(2))
# ---------------------------------------------------------------
# THOUGHT PROCESS 
# crosstab -> creates a frequency table that shows how often different 
# combinations of categories appear together in our data.
# normalize= convert those counts from corsstab into proportions or percentages.
# ---------------------------------------------------------------

# 5.2 Crosstab 2 — Freedom group × Income group
ct2 = pd.crosstab(data["Freedom group"], data["Income group"], normalize="columns")
print(ct2.round(2))

# 5.3 Crosstab 3 — Region × Life Expectancy Group
ct3 = pd.crosstab(data["Regional indicator"], data["LifeExp group"], normalize="index")
print(ct3.round(2))

# 5.4 Three-Way Crosstab — Region × Income Group × Freedom Group
ct4 = pd.crosstab(
    [data["Regional indicator"], data["Income group"]],
    data["Freedom group"],
    normalize="index")
print(ct4.round(2))

# ================================================================
# PART 6
# ---------------------------------------------------------------
# Multivariate graphical EDA
# ---------------------------------------------------------------
import seaborn as sns
import matplotlib.pyplot as plt

# 6.1 Visualizing Statistical Relationships (5 plots)
    # (a) Faceting with relplot() (col parameter)

g = sns.relplot(
    data=data,
    x="Logged GDP per capita",
    y="Healthy life expectancy",
    col="Regional indicator",     # creates one subplot per region
    col_wrap=3,     
    kind="scatter",
    height=4, aspect=1.2)
plt.suptitle("GDP vs Life Expectancy by Region", y=1.05)

# Move title up and enlarge it
g.fig.suptitle("GDP vs Life Expectancy by Region", y=1.03, fontsize=18)

plt.show()
# ---------------------------------------------------------------
# INTERPRETATION
# Higher GDP regions (Western Europe, NA/ANZ) show high life expectancy
# Sub-Saharan Africa shows low GDP and low expectancy
# ---------------------------------------------------------------

# (b) Plot with 5 variables at once (x, y, hue, size, col)
g = sns.relplot(
    data=data,
    x="Logged GDP per capita",
    y="Ladder score",
    hue="Regional indicator",
    size="Healthy life expectancy",
    col="Regional indicator",
    col_wrap=4,             # ensures readable layout
    kind="scatter",
    height=5,               # bigger plots
    aspect=1.2              # wider
)

g.fig.suptitle(
    "Happiness vs GDP by Region and Life Expectancy",
    y=1.04, fontsize=20)

 # (c) Line plot emphasizing continuity
sns.relplot(
    data=data.sort_values("Ladder score"),
    x="Ladder score",
    y="Healthy life expectancy",
    kind="line",
    ci=None) #hides the confidence interval line
plt.title("Life Expectancy as Happiness Increases")
plt.show()

# (d) Plot showing Standard Deviation
sns.relplot(
data=data,
    x="Logged GDP per capita",
    y="Ladder score",
    kind="line",
    ci="sd")   # displays shaded area = standard deviation
plt.title("Mean Happiness with Standard Deviation across GDP levels")
plt.show()
# ---------------------------------------------------------------
# INTERPRETATION
# Variability decreases at higher GDP levels
# ---------------------------------------------------------------

 # (e) Linear Regression Plot
sns.lmplot(
    data=data,
    x="Logged GDP per capita",
    y="Ladder score",
    hue="Regional indicator",
    scatter_kws={"alpha":0.6}
)
plt.title("Linear Regression: GDP vs Happiness by Region")
plt.show()

# 6.2 Visualizing Categorical Data (10 plots)
    # (a) Categorical scatter plot with jitter enabled
sns.stripplot(data=data, x="Regional indicator", y="Ladder score", jitter=True)
plt.title("Happiness Distribution per Region (with Jitter)")
plt.xticks(rotation=45, ha="right")
plt.show()
# ---------------------------------------------------------------
# THOUGHT PROCESS 
# stripplot() → scatter-like plot for categorical axes
# jitter=True → spreads overlapping points horizontally
# ---------------------------------------------------------------

 # (b) Categorical scatter plot with jitter disabled
sns.scatterplot(
    data=data,
    x="Freedom to make life choices",
    y="Ladder score"
)
plt.title("Happiness vs Freedom (No Jitter)")
plt.xlabel("Freedom to make life choices")
plt.ylabel("Ladder score")
plt.show()

# ---------------------------------------------------------------
# THOUGHT PROCESS 
# Why jitter=False: Freedom scores are already continuous and well-spaced; jitter would mislead visually.
# jitter = Randomly move the points slightly along the categorical axis so that they don’t overlap.
# ---------------------------------------------------------------
 
    # (c) Beeswarm plot (3 variables)
plt.figure(figsize=(14, 8))
sns.swarmplot(data=data, x="Regional indicator", y="Ladder score", hue="Freedom to make life choices")
plt.title("Happiness by Region and Freedom")
plt.xticks(rotation=60,ha="right" )
plt.tight_layout()
plt.show()
# ---------------------------------------------------------------
# THOUGHT PROCESS 
# swarmplot() = smart jitter (prevents overlap completely)
# ---------------------------------------------------------------
 
 # (d) Box plot (3 variables)
plt.figure(figsize=(20, 10))
sns.boxplot(data=data, x="Regional indicator", y="Ladder score")
plt.title("Box Plot of Happiness by Region and Freedom", fontsize=22)
plt.xticks(rotation=60, ha="right", fontsize=16)
plt.xlabel("Regional indicator", fontsize=16)
plt.ylabel("Ladder score", fontsize=16)
plt.tight_layout()
plt.show()

# Add visible datapoints
sns.stripplot(
    data=data,
    x="Regional indicator",
    y="Ladder score",
    hue="Freedom to make life choices",
    dodge=True,
    size=8,
    alpha=0.8)

 # (e) Boxenplot showing distribution shape
sns.boxenplot(data=data, x="Regional indicator", y="Ladder score")
plt.title("Boxenplot: Detailed Happiness Distribution by Region")
plt.xticks(rotation=45)
plt.show()

 # (f) Split Violin plot (3 variables)
plt.figure(figsize=(20, 10))
sns.violinplot(data=data, x="Regional indicator", y="Ladder score", hue="Freedom to make life choices",
               split=True, bw=0.4)

# Add clear, visible datapoints on top
sns.stripplot(
    data=data,
    x="Regional indicator",
    y="Ladder score",
    hue="Freedom to make life choices",
    dodge=True,
    size=7,        # bigger points
    alpha=0.8,
)

plt.title("Split Violin Plot: Happiness vs Freedom by Region")
plt.xticks(rotation=45, ha="right", fontsize=12)
plt.xlabel("Regional indicator", fontsize=14)
plt.ylabel("Ladder score", fontsize=14)
plt.show()
# ---------------------------------------------------------------
# THOUGHT PROCESS 
# violinplot() → shows distribution shape (like mirrored KDE)
# split=True → divides each violin by hue variable
# bw= → bandwidth controls smoothness
# stripplot → displays all individual data points along a category axis, showing the raw values and their spread.
# ---------------------------------------------------------------

   # (g) Violin plot with scatter points inside
plt.figure(figsize=(18, 8)) 
sns.violinplot(data=data, x="Regional indicator", y="Ladder score", inner=None, color="lightgray")
sns.stripplot(data=data, x="Regional indicator", y="Ladder score", color="blue", size=3)
plt.title("Violin Plot with Data Points")
plt.xticks(rotation=45)
plt.show()

  # (h) Bar plot (3 variables) with 97% CI
plt.figure(figsize=(16, 8))
sns.barplot(data=data, x="Regional indicator", y="Ladder score", hue="Freedom to make life choices", ci=97)
plt.title("Bar Plot of Happiness with 97% Confidence Intervals", fontsize=18)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

    # (i) Point plot (3 variables, dashed, 90% CI)
plt.figure(figsize=(16, 10))
sns.pointplot(data=data, x="Regional indicator", y="Ladder score", hue="Freedom to make life choices",
              ci=90, linestyles="--")
plt.title("Point Plot with 90% CI (Dashed Lines)", fontsize=20)
plt.xticks(rotation=45, ha="right",fontsize=12)
plt.show()
# ---------------------------------------------------------------
# THOUGHT PROCESS 
# pointplot() → shows mean points + CI lines
# ---------------------------------------------------------------

    # (j) Bar plot of number of observations
sns.countplot(data=data, x="Regional indicator", order=data["Regional indicator"].value_counts().index)
plt.title("Number of Countries per Region")
plt.xticks(rotation=45, ha="right",fontsize=12)
plt.show()
# ---------------------------------------------------------------
# THOUGHT PROCESS 
# countplot() → counts observations per category automatically
# ---------------------------------------------------------------

#6.3 Visualizing Bivariate Distributions (3 plots)
    # (a) Heatmap with color intensity
corr = data[["Ladder score","Logged GDP per capita","Freedom to make life choices"]].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Correlation Heatmap")
plt.show()
# ---------------------------------------------------------------
# INTERPRETATION
# GDP shows strongest correlation with happiness (0.79)
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# THOUGHT PROCESS 
# corr() → calculates correlation matrix
# annot=True → show numeric values
# cmap= → color gradient
# ---------------------------------------------------------------
  
    # (b) Bivariate KDE with contours
sns.displot(data=data, x="Logged GDP per capita", y="Ladder score",
            kind="kde", fill=True, levels=10, thresh=0.05, cmap="mako")
plt.title("Bivariate Density: GDP vs Happiness")
plt.show()
# ---------------------------------------------------------------
# THOUGHT PROCESS 
# kind="kde" → 2D kernel density estimate
# levels → number of contour lines
# thresh → visibility cutoff
# ---------------------------------------------------------------

# (c) 3-variable Heatmap (kde kind)
plt.figure(figsize=(10,7))

sns.kdeplot(
    data=data,
    x="Freedom to make life choices",
    y="Ladder score",
    hue="Regional indicator",
    fill=True,
    alpha=0.5,
    bw_adjust=1.5,
    common_norm=False)

plt.title("Freedom vs Happiness by Region (Density Heatmap)")
plt.xlabel("Freedom to make life choices")
plt.ylabel("Ladder score")
plt.tight_layout()
plt.show()

# ---------------------------------------------------------------
# THOUGHT PROCESS 
# kdeplot() → continuous density with optional color dimension
# common_norm=False prevents the KDE from disappearing due to small group sizes.
# bw_adjust makes the density smooth enough to actually appear on the graph.
# ---------------------------------------------------------------





