import pandas as pd
import os

# Gets the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Goes up one level from src/ to the project root, then into data/raw/
base_dir = os.path.dirname(script_dir)
df = pd.read_csv(os.path.join(base_dir, 'data', 'raw', 'draft_raw.csv'))

print(df.shape)  # The number of rows and columns
print(df.head(10))   # The first 10 rows
print(df.columns.tolist())   # Column names
print(df.dtypes)   # Data types for each column
print(df.isnull().sum())   # Total missing numbers per column
