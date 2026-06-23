"""
DecodeLabs Industrial Training Kit - Batch 2026
Project 1: Data Cleaning & Preparation
Author: Data Analyst Intern
Description: End-to-end data scrubbing workflow handling strategic imputation,
             deduplication, and universal string/date normalization.
"""

import pandas as pd
import numpy as np

# ----------------------------------------------------
# STEP 1: SIMULATE THE RAW MESSY DATASET
# ----------------------------------------------------
print("--- Step 1: Loading Raw Data ---")
raw_data = {
    "Order_ID": ["#44902", "#44902", "#44903", "#44904", "#44905", "#44905", "#44906"],
    "Product": ["Nexus-X", "Nexus-X", " Quantum-V", "Nexus-X", "Aero-Z", "Aero-Z", "Nexus-X"],
    "Qty": [3, 3, np.nan, 1, 2, 2, 5],
    "Value": [1499.971, 1499.971, 850.0, 499.99, np.nan, np.nan, 2499.85],
    "Status": ["Processing", "Processing", "Shipped", "Delivered", "Processing", "Processing", "Pending"],
    "Timestamp": ["2024-01-15T14:32:21Z", "2024-01-15T14:32:21Z", "16/01/2024", "2024-01-17", "2024-01-18 11:00", "2024-01-18 11:00", "2024-01-19"],
    "City": ["Bangalore", "Bangalore", "mumbai", "Bengaluru", "MUMBAI", "MUMBAI", "BLR"]
}

df = pd.DataFrame(raw_data)
print("Initial Dataset Shape:", df.shape)
print(df)
print("\n" + "="*50 + "\n")

# ----------------------------------------------------
# STEP 2: STRATEGIC IMPUTATION (Handling Missing Values)
# ----------------------------------------------------
print("--- Step 2: Strategic Imputation ---")
# Impute Qty using Mode (most common quantity ordered)
qty_mode = df["Qty"].mode()[0]
df["Qty"] = df["Qty"].fillna(qty_mode)
print(f"Imputed missing Qty values using Mode: {qty_mode}")

# Impute Value using Median (safeguards against statistical outliers)
value_median = df["Value"].median()
df["Value"] = df["Value"].fillna(value_median)
print(f"Imputed missing Value entries using Median: {value_median}")
print("\n" + "="*50 + "\n")

# ----------------------------------------------------
# STEP 3: THE INTEGRITY AUDIT (Deduplication)
# ----------------------------------------------------
print("--- Step 3: Deduplication Audit ---")
# Check for exact row duplicates matching our unique Order IDs
duplicate_count = df.duplicated().sum()
print(f"Identified duplicate records: {duplicate_count}")

# Remove the duplicates to maintain true transaction integrity
df = df.drop_duplicates().reset_index(drop=True)
print("Dataset Shape after removing duplicates:", df.shape)
print("\n" + "="*50 + "\n")

# ----------------------------------------------------
# STEP 4: STANDARDIZATION (Speaking One Language)
# ----------------------------------------------------
print("--- Step 4: Formatting & Normalization ---")

# 1. Clean up Text: Trim trailing spaces and unify City values to strict naming conventions
df["Product"] = df["Product"].str.strip()
df["City"] = df["City"].str.strip().str.upper()

# Map irregular abbreviations down to clean unified entities
city_mapping = {
    "BANGALORE": "Bengaluru",
    "BLR": "Bengaluru",
    "BENGALURU": "Bengaluru",
    "MUMBAI": "Mumbai"
}
df["City"] = df["City"].map(city_mapping)

# 2. Numeric Precision: Restrict financial value structures to 2 decimal places max
df["Value"] = df["Value"].round(2)

# 3. Date Parsing: Convert all inconsistent dates into clean ISO 8601 (YYYY-MM-DD) format
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors='coerce').dt.strftime('%Y-%m-%d')

print("Cleaned and Standardized Dataset:")
print(df)
print("\n" + "="*50 + "\n")

# ----------------------------------------------------
# STEP 5: VALIDATION CHECK
# ----------------------------------------------------
print("--- Step 5: Final Validation Check ---")
final_duplicates = df.duplicated(subset=["Order_ID"]).sum()
final_null_dates = df["Timestamp"].isnull().sum()

print(f"Verification - Duplicate IDs remaining: {final_duplicates}")
print(f"Verification - Incorrect/Null Dates remaining: {final_null_dates}")

if final_duplicates == 0 and final_null_dates == 0:
    print("\nSUCCESS: Dataset verified for Gold Standard quality! Ready for production.")
else:
    print("\nWARNING: Verification failed. Review data pipelines.")