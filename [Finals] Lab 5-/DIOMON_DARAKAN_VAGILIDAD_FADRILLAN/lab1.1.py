import pandas as pd
import numpy as np
from collections import Counter

#B: DataFrame Construction
data = {
    'user_id':   ['U001', 'U002', 'U003', 'U004', 'U005', 'U006', 'U007', 'U008', 'U009', 'U010', 'U011', 'U012'],
    'age':       [17, 18, 17, 19, 22, 22, 25, 24, 23, 19, 18, 25],
    'region':    ['NCR', 'NCR', 'Cebu', 'NCR', 'Davao', 'Davao', 'NCR', 'Cebu', 'Cebu', 'NCR', 'Davao', 'Davao'],
    'genre':     ['Shonen', 'Shonen', 'Isekai', 'Romance', 'Shonen', 'Isekai', 'Horror', 'Romance', 'Horror', 'Isekai', 'Shonen', 'Romance'],
    'sub_plan':  ['Basic', 'Premium', 'Basic', 'Premium', 'Standard', 'Basic', 'Premium', 'Standard', 'Basic', 'Standard', 'Basic', 'Premium'],
}

df = pd.DataFrame(data)
print(df.head())
print(df.dtypes) # Confirming 'age' is int64

#C: Generalization Functions

def generalize_age(age, level=1):
    """
    Returns a generalized string for the given age.
    level=1 -> 5-year range, level=2 -> 10-year range, level=3 -> 'Any'
    """
    if level == 1:
        low = (age // 5) * 5
        high = low + 4
        return f'[{low}-{high}]'
    elif level == 2:
        low = (age // 10) * 10
        high = low + 9
        return f'[{low}-{high}]'
    else:
        return 'Any'

def generalize_region(region, level=1):
    """
    Returns a generalized string for the given region.
    level=1 -> island group, level=2 -> 'Philippines'
    """
    region_map = {'NCR': 'Luzon', 'Cebu': 'Visayas', 'Davao': 'Mindanao'}
    
    if level == 1:
        return region_map.get(region, region)
    else:
        return 'Philippines'

def generalize_genre(genre, level=1):
    """
    Returns a generalized string for the given genre.
    level=1 -> broad category, level=2 -> 'Anime'
    """
    genre_map = {
        'Shonen': 'Action/Adventure', 
        'Isekai': 'Action/Adventure',
        'Romance': 'Drama/Thriller', 
        'Horror': 'Drama/Thriller'
    }
    
    if level == 1:
        return genre_map.get(genre, genre)
    else:
        return 'Anime'

#D: K-Anonymity Check Function
def check_k_anonymity(df, qi_cols, k):
    """
    Returns True if ALL equivalence classes have >= k records.
    Also prints each EC and its size.
    """
    # Group df by qi_cols and count records per group
    # The hint suggests using df.groupby(qi_cols).size() and .reset_index()
    ec_counts = df.groupby(qi_cols).size().reset_index(name='count')
    
    # Print each EC and its size so you can see what's happening
    print(f"\n--- Equivalence Classes Check ---")
    print(ec_counts.to_string(index=False))
    
    # Return True only if the minimum count across all classes is >= k
    return ec_counts['count'].min() >= k

# 1. Create a copy of the original DataFrame to hold the anonymized data
df_anon = df.copy() 

# 2. Apply your level 1 generalization functions to the specific columns
df_anon['age']    = df_anon['age'].apply(lambda x: generalize_age(x, level=2))
df_anon['region'] = df_anon['region'].apply(lambda x: generalize_region(x, level=2))
df_anon['genre']  = df_anon['genre'].apply(lambda x: generalize_genre(x, level=2)) 

# 3. Define your Quasi-Identifiers
qi = ['age', 'region', 'genre'] 

# 4. Run the check function and store the boolean output in the 'result' variable
result = check_k_anonymity(df_anon, qi, k=3) 

print(f'\nk=3 satisfied (Level 2): {result}')


#E: Verify and Display Equivalence Classes ---
print("\n--- Final Equivalence Class Summary ---")
ec_summary = df_anon.groupby(qi).size().reset_index(name='count')
ec_summary['k=3_satisfied'] = ec_summary['count'] >= 3
print(ec_summary.to_string(index=False))