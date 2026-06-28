import pandas as pd

def assess_k_anonymity(df, qis, threshold):
    """Evaluates if the dataframe meets k-anonymity."""
    cluster_sizes = df.groupby(qis, dropna=False).size().reset_index(name="cluster_size")
    cluster_sizes[f"k_is_{threshold}_met"] = cluster_sizes["cluster_size"] >= threshold
    return bool(cluster_sizes["cluster_size"].min() >= threshold)

def assess_l_diversity(df, qis, private_col, l_val):
    """Evaluates if equivalence classes contain enough distinct sensitive values."""
    metrics = []
    for qi_combo, subset in df.groupby(qis, dropna=False):
        qi_tuple = qi_combo if isinstance(qi_combo, tuple) else (qi_combo,)
        unique_secrets = sorted(subset[private_col].unique())
        
        row_data = dict(zip(qis, qi_tuple))
        row_data.update({
            "total_rows": len(subset),
            "unique_secrets_count": len(unique_secrets),
            "secrets_list": unique_secrets,
            f"l_{l_val}_met": len(unique_secrets) >= l_val
        })
        metrics.append(row_data)
        
    evaluation_df = pd.DataFrame(metrics)
    print(evaluation_df.to_string(index=False))
    return bool(evaluation_df[f"l_{l_val}_met"].all())

def construct_otaku_clinic_data():
    """Generates the OtakuHealth dataset."""
    return pd.DataFrame({
        "patient": [f"P{n:02d}" for n in range(1, 13)],
        "demographic": ["Teen (13-19)"]*3 + ["Adult (20-35)"]*3 + ["Senior (36+)"]*3 + ["Adult (20-35)"]*3,
        "ward": ["Shibuya"]*3 + ["Harajuku"]*3 + ["Akihabara"]*3 + ["Shibuya"]*3,
        "event_role": ["Attendee"]*3 + ["Cosplayer"]*3 + ["Vendor"]*3 + ["Volunteer"]*3,
        "ailment": ["Anxiety", "Anxiety", "Anxiety", "Back Pain", "Back Pain", "Migraine", 
                    "Fatigue", "Fatigue", "Fatigue", "Dehydration", "Exhaustion", "Dehydration"]
    })

if __name__ == "__main__":
    print("--- LAB 2.1: OTAKUHEALTH HOMOGENEITY CHECK ---")
    clinic_df = construct_otaku_clinic_data()
    otaku_qis = ["demographic", "ward", "event_role"]
    
    print("\nl-Diversity Check (l=2):")
    assess_l_diversity(clinic_df, otaku_qis, "ailment", l_val=2)
    
    # Simulating Homogeneity Attack on P07
    target_ec = clinic_df[
        (clinic_df['demographic'] == 'Senior (36+)') &
        (clinic_df['ward'] == 'Akihabara') &
        (clinic_df['event_role'] == 'Vendor')
    ]
    print("\n--- ISOLATED EC FOR P07 ---")
    print(target_ec[['demographic', 'ward', 'event_role', 'ailment']])
    print(f"Inferred Diagnosis with 100% certainty: {target_ec['ailment'].unique()[0]}")