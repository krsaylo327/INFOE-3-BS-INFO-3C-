import pandas as pd

#A: Build Dataset
data = {
    'fan_id':    ['F01', 'F02', 'F03', 'F04', 'F05', 'F06', 'F07', 'F08', 'F09', 'F10', 'F11', 'F12', 'F13', 'F14', 'F15'],
    'age_range': ['15-19', '15-19', '15-19', '20-25', '20-25', '20-25', '26-35', '26-35', '26-35', '36+', '36+', '36+', '15-19', '15-19', '15-19'],
    'region':    ['Luzon', 'Luzon', 'Luzon', 'Visayas', 'Visayas', 'Visayas', 'Mindanao', 'Mindanao', 'Mindanao', 'Luzon', 'Luzon', 'Luzon', 'Visayas', 'Visayas', 'Visayas'],
    'series':    ['One Piece', 'One Piece', 'Naruto', 'Attack on Titan', 'Attack on Titan', 'Attack on Titan', 'Dragon Ball Z', 'Dragon Ball Z', 'Dragon Ball Z', 'Sailor Moon', 'Sailor Moon', 'Sailor Moon', 'Demon Slayer', 'Demon Slayer', 'Demon Slayer'],
    'knowledge': ['Novice', 'Novice', 'Intermediate', 'Expert', 'Expert', 'Master', 'Intermediate', 'Intermediate', 'Intermediate', 'Master', 'Master', 'Expert', 'Novice', 'Novice', 'Intermediate']
}
df = pd.DataFrame(data)

#B: Build Equivalence Class Summary
qi = ['age_range', 'region', 'series']

# Using .agg() to calculate multiple metrics simultaneously
ec_summary = (
    df.groupby(qi)['knowledge']
    .agg(
        records='count', 
        distinct=pd.Series.nunique, 
        levels=list
    )
    .reset_index()
)

# Check if distinct values meet the l=3 threshold
ec_summary['l3_satisfied'] = ec_summary['distinct'] >= 3

print("\n--- Initial l=3 Diversity Check ---")
print(ec_summary.to_string(index=False))

#C: Generalize to l=3
df_anon = df.copy()

# 1. Generalize Region and Age completely to force merging
df_anon['region'] = 'Philippines'
df_anon['age_range'] = 'All Ages'

# 2. Generalize Series to ensure diverse knowledge levels
series_map = {
    'Dragon Ball Z': 'Classic Anime',
    'Sailor Moon': 'Classic Anime',
    'Naruto': 'Classic Anime',
    'One Piece': 'Classic Anime',
    'Attack on Titan': 'Modern Anime',
    'Demon Slayer': 'Modern Anime'
}
df_anon['series'] = df_anon['series'].map(series_map)

# --- Re-run the l=3 Check ---
ec_summary_anon = (
    df_anon.groupby(qi)['knowledge']
    .agg(
        records='count', 
        distinct=pd.Series.nunique, 
        levels=list
    )
    .reset_index()
)
ec_summary_anon['l3_satisfied'] = ec_summary_anon['distinct'] >= 3

print("\n--- After Generalization l=3 Check ---")
print(ec_summary_anon.to_string(index=False))