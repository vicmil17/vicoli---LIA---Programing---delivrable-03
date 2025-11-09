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

# ================================================================
# PART 4
# ---------------------------------------------------------------
# Univariate graphical EDA
# ---------------------------------------------------------------
# a) Custom bins + Kernel Density Estimation
# ---------------------------------------------------------------
# INTERPRETATION
# The Ladder score is approximately normal, centered around 5.5.
# Slight left skew (longer tail on the lower end).
# No extreme outliers; most countries fall between 4 and 7.
# The median and mean are close, confirming near symmetry.
# ---------------------------------------------------------------

import seaborn as sns
import matplotlib.pyplot as plt

sns.histplot(data=data, x="Ladder score", bins=12, kde=True, color="skyblue")
plt.title("Distribution of Ladder Score (Happiness)")
plt.xlabel("Ladder Score")
plt.ylabel("Number of Countries")
plt.show()

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
# e) Kernel Density Estimation with Bandwidth Control
# ---------------------------------------------------------------

sns.kdeplot(data=data, x="Healthy life expectancy", bw_adjust=0.6, fill=True, color="orange")
plt.title("KDE of Healthy Life Expectancy")
plt.xlabel("Healthy Life Expectancy (Years)")
plt.ylabel("Density")
plt.show()

# ---------------------------------------------------------------
# f) Empirical Cumulative Distribution (ECDF)
# ---------------------------------------------------------------

sns.ecdfplot(data=data, x="Generosity", color="purple")
plt.title("Empirical Cumulative Distribution of Generosity")
plt.xlabel("Generosity Score")
plt.ylabel("Cumulative Probability")
plt.show()

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
# normalize=, convert those counts from corsstab into proportions or percentages.
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

sns.relplot(
    data=data,
    x="Logged GDP per capita",
    y="Healthy life expectancy",
    col="Regional indicator",     # creates one subplot per region
    kind="scatter",
    height=4, aspect=1)
plt.suptitle("GDP vs Life Expectancy by Region", y=1.05)
plt.show()

# (b) Plot with 5 variables at once (x, y, hue, size, col)
sns.relplot(
    data=data,
    x="Logged GDP per capita",
    y="Ladder score",
    hue="Regional indicator",       # color shows region
    size="Healthy life expectancy", # marker size = life expectancy
    col="Freedom to make life choices", # small multiples per freedom level
    kind="scatter",
    height=4, aspect=1)
plt.suptitle("Happiness vs GDP by Region, Freedom, and Life Expectancy", y=1.05)
plt.show()


 










