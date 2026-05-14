import pandas as pd
import numpy as np
import unicodedata
import re


def normalize_name(name):
    name = unicodedata.normalize('NFKD', str(name))
    name = ''.join(c for c in name if not unicodedata.combining(c))
    return ''.join(name.strip().split()).lower()

def clean_draft_data(df):

    # Remove junk header rows
    df = df[df['Player'] != 'Player']
    df = df[df['Player'].notna()].copy()

    # Convert into numeric columns
    numeric_cols = ['Pk', 'Age', 'G', 'PTS', 'TRB', 'AST', 'WS']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Normalize names for merging
    df['name_clean'] = df['Player'].apply(normalize_name)

    return df
