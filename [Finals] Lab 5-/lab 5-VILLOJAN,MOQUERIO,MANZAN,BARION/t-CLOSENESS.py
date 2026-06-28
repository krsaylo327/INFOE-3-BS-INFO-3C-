import pandas as pd

def calculate_emd(local_dist, global_dist):
    """Calculates Earth Mover's Distance between two probability distributions."""
    all_keys = set(local_dist.keys()).union(set(global_dist.keys()))
    distance = 0.5 * sum(abs(local_dist.get(key, 0) - global_dist.get(key, 0)) for key in all_keys)
    return distance

def validate_t_closeness(df, cluster_col, secret_col, global_dist_map, t_threshold):
    """Checks if distribution of secrets in every cluster mimics the global distribution within t."""
    metrics = []
    is_compliant = True
    
    for cluster_name, subset in df.groupby(cluster_col):
        local_probs = subset[secret_col].value_counts(normalize=True).to_dict()
        emd_score = calculate_emd(local_probs, global_dist_map)
        passes_t = emd_score <= t_threshold
        
        is_compliant = is_compliant and passes_t
        metrics.append({
            "Cluster": cluster_name, "Size": len(subset), 
            "EMD Score": round(emd_score, 4), "Threshold (t)": t_threshold, "Passed": passes_t
        })
        
    print(pd.DataFrame(metrics).to_string(index=False))
    return is_compliant

def generate_nihonstream_data():
    """Builds the NihonStream streaming tier dataset."""
    db_rows = []
    cluster_mappings = {
        "Group_A": ["Free", "Free", "Silver", "Free", "Silver"],
        "Group_B": ["Platinum", "Platinum", "Platinum", "Gold", "Gold", "Gold", "Silver"],
        "Group_C": ["Free", "Free", "Free", "Free", "Silver", "Silver", "Gold", "Platinum"]
    }
    for cluster, tiers in cluster_mappings.items():
        for t in tiers:
            db_rows.append({"cluster_id": cluster, "viewer_tier": t})
            
    return pd.DataFrame(db_rows)

if __name__ == "__main__":
    ns_df = generate_nihonstream_data()
    global_distribution = ns_df["viewer_tier"].value_counts(normalize=True).to_dict()
    
    print("--- GLOBAL DISTRIBUTION ---")
    for tier, prob in global_distribution.items():
        print(f"{tier}: {prob*100:.1f}%")
        
    print("\n--- T-CLOSENESS EVALUATION (t=0.25) ---")
    validate_t_closeness(ns_df, "cluster_id", "viewer_tier", global_distribution, t_threshold=0.25)