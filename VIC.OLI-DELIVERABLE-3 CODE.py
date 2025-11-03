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















