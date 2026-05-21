import pandas as pd
import unicodedata
import os
import warnings

warnings.filterwarnings('ignore')

# Path setup
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(script_dir)


def normalize_name(name):
    name = unicodedata.normalize('NFKD', str(name))
    name = ''.join(c for c in name if not unicodedata.combining(c))
    return ''.join(name.strip().split()).lower()


def clean_draft_data(df):
    # Rename columns
    df = df.rename(columns={
        'Round 1_Player': 'Player',
        'Round 1_College': 'College',
        'Totals_G': 'G',
        'Totals_MP': 'MP',
        'Totals_PTS': 'PTS',
        'Totals_TRB': 'TRB',
        'Totals_AST': 'AST',
        'Shooting_FG%': 'FG%',
        'Shooting_3P%': '3P%',
        'Shooting_FT%': 'FT%',
        'Per Game_PTS': 'PTS_pg',
        'Per Game_TRB': 'TRB_pg',
        'Per Game_AST': 'AST_pg',
        'Per Game_MP': 'MP_pg',
        'Advanced_WS': 'WS',
        'Advanced_WS/48': 'WS48',
        'Advanced_BPM': 'BPM',
        'Advanced_VORP': 'VORP'
    })

    # Remove repeated header rows
    df = df[df['Pk'] != 'Pk']
    df = df[df['Pk'].notna()].copy()

    # Convert numeric columns
    numeric_cols = ['Pk', 'Yrs', 'G', 'MP', 'PTS', 'TRB', 'AST',
                    'FG%', '3P%', 'FT%', 'PTS_pg', 'TRB_pg', 'AST_pg',
                    'MP_pg', 'WS', 'WS48', 'BPM', 'VORP']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Fill in zeros for stats of players that never played
    stats_cols = ['G', 'MP', 'PTS', 'TRB', 'AST', 'WS', 'BPM', 'VORP', 'Yrs']
    df[stats_cols] = df[stats_cols].fillna(0)

    # Normalize player names for merging
    df['name_clean'] = df['Player'].apply(normalize_name)

    # Drop unnecessary Rk column
    df = df.drop(columns=['Rk'], errors='ignore')

    # Reset index
    df = df.reset_index(drop=True)

    return df


if __name__ == '__main__':
    os.makedirs(os.path.join(base_dir, 'data', 'processed'), exist_ok=True)

    df_raw = pd.read_csv(os.path.join(base_dir, 'data', 'raw', 'draft_raw.csv'))
    df_clean = clean_draft_data(df_raw)

    df_clean.to_csv(os.path.join(base_dir, 'data', 'processed', 'draft_clean.csv'), index=False)
    print(f"Clean data saved. {len(df_clean)} rows.")
    print(df_clean.dtypes)
    print(df_clean.head(10))
