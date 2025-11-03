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














