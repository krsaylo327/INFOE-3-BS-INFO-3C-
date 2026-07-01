import pandas as pd

#A: Build Datasets
herorank = pd.DataFrame({
    'record':    ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8'],
    'power_low': [8000, 8000, 5000, 5000, 9500, 9500, 3000, 3000],
    'power_high':[9000, 9000, 6000, 6000, 10500, 10500, 4000, 4000],
    'region':    ['Eastern Kingdom', 'Eastern Kingdom', 'Northern Wastes', 'Northern Wastes', 'Capital City', 'Capital City', 'Southern Isles', 'Southern Isles'],
    'weapon':    ['Sword', 'Sword', 'Magic Staff', 'Magic Staff', 'Bare Hands', 'Spear', 'Bow', 'Bow'],
    'weakness':  ['Fire', 'Ice', 'Dark Magic', 'Holy Light', 'None', 'Poison', 'Close Combat', 'Thunder']
})

wiki = pd.DataFrame({
    'name':       ['Kyo Ashura', 'Nami Frost', 'Zephyr Moon', 'Seraphiel', 'Riku Darkwind'],
    'power':      [8450, 8720, 5300, 9800, 3200],
    'hometown':   ['Ryugawa City (East)', 'Ryugawa City (East)', 'Frostholm (North)', 'Solaris (Capital)', 'Shimaoka (South)'],
    'weapon_raw': ['Katana (Sword)', 'Ice Blade (Sword)', 'Rune Staff (Magic)', 'None (Bare Hands)', 'Longbow (Bow)']
})

def normalize_weapon(raw_weapon):
    weapon = raw_weapon.split('(')[-1].rstrip(')')
    # .split('(') breaks the string into two pieces: ['Katana ', 'Sword)']
    # [-1] grabs the last piece: 'Sword)'
    # .rstrip(')') removes the closing parenthesis: 'Sword'
    if weapon == 'Magic':
        return 'Magic Staff'
    
    return raw_weapon.split('(')[-1].rstrip(')')

def linkage_attack(herorank_df, wiki_df):
    results = []
    
    # Mapping dict to convert Wiki hometowns to HeroRank regions
    region_map = {
        'Ryugawa City (East)': 'Eastern Kingdom',
        'Frostholm (North)': 'Northern Wastes',
        'Solaris (Capital)': 'Capital City',
        'Shimaoka (South)': 'Southern Isles'
    }

    for _, char in wiki_df.iterrows():
        norm_weapon = normalize_weapon(char['weapon_raw'])
        
        # COMPLETE THIS LINE: Look up the char['hometown'] in the region_map
        norm_region = region_map.get(char['hometown']) 
        
        # The Attack Query: Find where all 3 conditions are true
        matches = herorank_df[
            (herorank_df['power_low'] <= char['power']) &
            (char['power'] <= herorank_df['power_high']) &
            (herorank_df['region'] == norm_region) &
            (herorank_df['weapon'] == norm_weapon)
        ]
        
        for _, row in matches.iterrows():
            results.append({
                'character':  char['name'],
                'matched_record': row['record'],
                'weakness': row['weakness'] # The stolen sensitive data
            })
            
    return results

# Run the attack
attack_results = linkage_attack(herorank, wiki)
print("--- Linkage Attack Results ---")
print(pd.DataFrame(attack_results))

#C: Re-Anonymize to k=4

def re_anonymize_k4(herorank_df):
    """
    Merges records to create two large equivalence classes of 4 records each.
    Class 1: High Power (Mainland)
    Class 2: Low Power (Outskirts)
    """
    df = herorank_df.copy()
    
    # 1. Merge Regions 
    # We group Eastern Kingdom and Capital City together, and Northern Wastes and Southern Isles together.
    df['region'] = df['region'].replace({
        'Eastern Kingdom': 'Mainland',
        'Capital City': 'Mainland',
        'Northern Wastes': 'Outskirts',
        'Southern Isles': 'Outskirts'
    })
    
    # 2. Suppress Weapons 
    # Weapons are too specific. We will hide them completely by replacing everything with an asterisk.
    df['weapon'] = '*'
    
    # 3. Widen Power Levels 
    # Standardize the high-power bounds
    df.loc[df['power_low'] >= 8000, 'power_low'] = 8000
    df.loc[df['power_high'] >= 8000, 'power_high'] = 11000
    
    # Standardize the low-power bounds
    df.loc[df['power_high'] <= 7000, 'power_low'] = 3000
    df.loc[df['power_high'] <= 7000, 'power_high'] = 7000
    
    return df

# Execute the transformation
herorank_k4 = re_anonymize_k4(herorank)
print("\n--- Re-Anonymized Dataset (k=4) ---")
print(herorank_k4)
print(pd.DataFrame(linkage_attack(herorank_k4, wiki)))