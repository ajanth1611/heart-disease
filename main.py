from pathlib import Path
import os

import pandas as pd


project_root = Path(__file__).resolve().parent
csv_path = project_root / "data" / "heart.csv"
processed_dir = project_root / "data" / "processed"
clean_csv_path = processed_dir / "heart_clean.csv"

df = pd.read_csv(str(csv_path))

print("=" * 50)
print("first 5 rows")
print("=" * 50)
print(df.head())

print("=" * 50)
print("datashape")
print("=" * 50)
print(df.shape)

print("=" * 50)
print("columns")
print("=" * 50)
print(df.columns)

print("\n" + "=" * 50)
print("Dataset Information")
print("=" * 50)
print(df.info())

print("\n" + "=" * 50)
print("Statistical Summary")
print("=" * 50)
print(df.describe())

print("\n" + "=" * 50)
print("Missing Values")
print("=" * 50)
print(df.isnull().sum())

print("\n" + "=" * 50)
print("Duplicate Rows")
print("=" * 50)
print(df.duplicated().sum())

print("\n" + "=" * 50)
print("Target Distribution")
print("=" * 50)
print(df["target"].value_counts())

df = df.drop_duplicates()

print("\n" + "=" * 50)
print("Duplicate Rows")
print("=" * 50)
print(df.duplicated().sum())

print("\n" + "=" * 50)
print("shape after remove duplicates")
print("=" * 50)
print(df.shape)

print("\n" + "=" * 50)
print("datatype")
print(df.dtypes)

print("\n" + "=" * 50)
df["oldpeak"] = df["oldpeak"].astype(int)
print(df.dtypes)

os.makedirs(str(processed_dir), exist_ok=True)
df.to_csv(str(clean_csv_path), index=False)

print("Cleaned dataset saved successfully.")
df = pd.read_csv(str(clean_csv_path))
print(df.shape)
