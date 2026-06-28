import pandas as pd

def generate_lab1_2_data():
    """Builds both the anonymized HeroRank (k=2) dataset and the Anime Wiki dataset."""
    hr_data = pd.DataFrame({
        "record_id": ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8"],
        "power_min": [8000, 8000, 5000, 5000, 9500, 9500, 3000, 3000],
        "power_max": [9000, 9000, 6000, 6000, 10500, 10500, 4000, 4000],
        "territory": ["Eastern Kingdom", "Eastern Kingdom", "Northern Wastes", "Northern Wastes", 
                      "Capital City", "Capital City", "Southern Isles", "Southern Isles"],
        "combat_style": ["Sword", "Sword", "Magic Staff", "Magic Staff", 
                         "Bare Hands", "Spear", "Bow", "Bow"],
        "weakness": ["Fire", "Ice", "Dark Magic", "Holy Light", 
                     "None", "Poison", "Close Combat", "Thunder"]
    })
    
    wiki_data = pd.DataFrame({
        "character_name": ["Arthur", "Lancelot", "Merlin", "Morgana", "Brawler", "Knight", "Archer1", "Archer2"],
        "exact_power": [8500, 8200, 5500, 5800, 10000, 9800, 3500, 3200],
        "hometown": ["East", "East", "North", "North", "Capital", "Capital", "South", "South"],
        "weapon_type": ["Sword", "Sword", "Staff", "Staff", "Fists", "Polearm", "Bow", "Bow"]
    })
    return hr_data, wiki_data

def normalize_wiki_attributes(wiki_df):
    """Maps Wiki terminology to match HeroRank schemas for linkage."""
    region_mapping = {
        "East": "Eastern Kingdom", "North": "Northern Wastes", 
        "Capital": "Capital City", "South": "Southern Isles"
    }
    weapon_mapping = {
        "Sword": "Sword", "Staff": "Magic Staff", 
        "Fists": "Bare Hands", "Polearm": "Spear", "Bow": "Bow"
    }
    wiki_df["mapped_region"] = wiki_df["hometown"].map(region_mapping)
    wiki_df["mapped_weapon"] = wiki_df["weapon_type"].map(weapon_mapping)
    return wiki_df

def execute_linkage_attack(herorank, wiki):
    """Performs the linkage attack logic joining external knowledge with anonymized data."""
    wiki = normalize_wiki_attributes(wiki)
    compromised_records = []
    
    for _, wiki_row in wiki.iterrows():
        # Match condition logic
        matches = herorank[
            (herorank["power_min"] <= wiki_row["exact_power"]) & 
            (herorank["power_max"] >= wiki_row["exact_power"]) & 
            (herorank["territory"] == wiki_row["mapped_region"]) &
            (herorank["combat_style"] == wiki_row["mapped_weapon"])
        ]
        
        for _, hr_row in matches.iterrows():
            compromised_records.append({
                "Target Character": wiki_row["character_name"],
                "HeroRank ID": hr_row["record_id"],
                "Exposed Weakness": hr_row["weakness"]
            })
            
    return pd.DataFrame(compromised_records)

def apply_k4_reanonymization(df):
    """Upgrades dataset to k=4 by aggressively suppressing and generalizing attributes."""
    df_k4 = df.copy()
    # Generalize regions into broad zones
    df_k4["territory"] = df_k4["territory"].map({
        "Eastern Kingdom": "Outer Realms", "Northern Wastes": "Outer Realms",
        "Capital City": "Inner Realms", "Southern Isles": "Inner Realms"
    })
    # Simplify power brackets
    df_k4["power_min"] = df_k4["power_min"].apply(lambda x: 3000 if x < 9000 else 8000)
    df_k4["power_max"] = df_k4["power_max"].apply(lambda x: 9000 if x <= 9000 else 11000)
    # Suppress weapon type entirely
    df_k4["combat_style"] = "*"
    
    return df_k4

if __name__ == "__main__":
    hr_db, wiki_db = generate_lab1_2_data()
    print("--- SUCCESSFUL LINKAGE ATTACK ON k=2 ---")
    attack_results = execute_linkage_attack(hr_db, wiki_db)
    print(attack_results.to_string(index=False))
    
    exact_matches = attack_results.groupby("Target Character").size().eq(1).sum()
    print(f"\nCharacters uniquely compromised: {exact_matches} out of {len(wiki_db)}")
    
    print("\n--- SECURED HR DATASET (RE-ANONYMIZED TO k=4) ---")
    hr_k4 = apply_k4_reanonymization(hr_db)
    print(hr_k4.drop(columns=["weakness"]).to_string(index=False)) # Showing QIs only