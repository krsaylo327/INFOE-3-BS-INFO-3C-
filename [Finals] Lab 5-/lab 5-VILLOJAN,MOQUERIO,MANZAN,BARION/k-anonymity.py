import pandas as pd

def initialize_anime_data():
    """Generates the original AnimeVault dataset as a DataFrame."""
    raw_records = {
        "user_id": [f"U{num:03d}" for num in range(1, 13)],
        "age": [17, 18, 17, 19, 22, 22, 25, 24, 23, 19, 18, 25],
        "region": [
            "NCR", "NCR", "Cebu", "NCR", "Davao", "Davao",
            "NCR", "Cebu", "Cebu", "NCR", "Davao", "Davao",
        ],
        "fav_genre": [
            "Shonen", "Shonen", "Isekai", "Romance", "Shonen", "Isekai",
            "Horror", "Romance", "Horror", "Isekai", "Shonen", "Romance",
        ],
        "subscription": [
            "Basic", "Premium", "Basic", "Premium", "Standard", "Basic",
            "Premium", "Standard", "Basic", "Standard", "Basic", "Premium",
        ],
    }
    return pd.DataFrame(raw_records)

def mask_age(age_val, strength=1):
    """Generalizes the age attribute based on the required strength level."""
    if strength == 1:
        floor = (int(age_val) // 5) * 5
        return f"[{floor}-{floor+4}]"
    elif strength == 2:
        floor = (int(age_val) // 10) * 10
        return f"[{floor}-{floor+9}]"
    return "Any Age"

def mask_region(region_val, strength=1):
    """Generalizes the geographical region attribute."""
    if strength == 1:
        geography_map = {"NCR": "Luzon/Visayas", "Cebu": "Luzon/Visayas", "Davao": "Mindanao"}
        return geography_map.get(region_val, "Unknown")
    return "Philippines"

def mask_genre(genre_val, strength=1):
    """Generalizes the user's favorite genre."""
    if strength == 1:
        genre_map = {
            "Shonen": "Action/Adventure", "Isekai": "Action/Adventure",
            "Romance": "Drama/Thriller", "Horror": "Drama/Thriller"
        }
        return genre_map.get(genre_val, "Other")
    return "Anime"

def validate_k_anonymity(dataframe, quasi_identifiers, k_target):
    """Groups records by QIs and checks if the minimum cluster size meets k."""
    cluster_counts = dataframe.groupby(quasi_identifiers, dropna=False).size().reset_index(name="cluster_size")
    cluster_counts[f"meets_k{k_target}"] = cluster_counts["cluster_size"] >= k_target
    print(cluster_counts.to_string(index=False))
    
    is_compliant = cluster_counts["cluster_size"].min() >= k_target
    return is_compliant

def apply_k_anonymity(df, k_val):
    """Iteratively applies stronger generalizations until k-anonymity is satisfied."""
    qis = ["age", "region", "fav_genre"]
    
    for lvl_age in range(1, 4):
        for lvl_region in range(1, 3):
            for lvl_genre in range(1, 3):
                test_df = df.copy()
                test_df["age"] = test_df["age"].apply(lambda a: mask_age(a, lvl_age))
                test_df["region"] = test_df["region"].apply(lambda r: mask_region(r, lvl_region))
                test_df["fav_genre"] = test_df["fav_genre"].apply(lambda g: mask_genre(g, lvl_genre))
                
                print(f"\n--- Testing Hierarchy: Age(L{lvl_age}), Region(L{lvl_region}), Genre(L{lvl_genre}) ---")
                if validate_k_anonymity(test_df, qis, k_val):
                    return test_df, (lvl_age, lvl_region, lvl_genre)
                    
    raise RuntimeError("Unable to satisfy k-anonymity with existing hierarchies.")

if __name__ == "__main__":
    base_df = initialize_anime_data()
    print("--- RAW ANIMEVAULT DATA ---")
    print(base_df.to_string(index=False))
    
    anonymized_df, final_levels = apply_k_anonymity(base_df, k_val=3)
    
    print("\n--- FINAL SECURE DATASET (k=3) ---")
    print(anonymized_df.to_string(index=False))