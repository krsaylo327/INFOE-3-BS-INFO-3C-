import pandas as pd
import numpy as np

# --- Part A: Build the Dataset ---
records = []
ec1_tiers = ['Free', 'Free', 'Silver', 'Free', 'Silver']
ec2_tiers = ['Platinum', 'Platinum', 'Platinum', 'Gold', 'Gold', 'Gold', 'Silver']
ec3_tiers = ['Free', 'Free', 'Free', 'Free', 'Silver', 'Silver', 'Gold', 'Platinum']

# Populate the DataFrame
for tier in ec1_tiers: records.append({'ec':'EC1', 'viewer_tier': tier})
for tier in ec2_tiers: records.append({'ec':'EC2', 'viewer_tier': tier})
for tier in ec3_tiers: records.append({'ec':'EC3', 'viewer_tier': tier})
df = pd.DataFrame(records)

# Compute overall distribution for the entire dataset
overall_dist = df['viewer_tier'].value_counts(normalize=True).sort_index()
overall_dict = overall_dist.to_dict()
print('--- Overall Distribution ---')
print(overall_dist)

# --- Part B: Implement EMD Calculation ---
def compute_emd_unordered(ec_dist, overall_dist):
    """
    Computes Earth Mover's Distance for unordered categorical data.
    Formula: EMD = (1/2) * sum(|p_i - q_i|)
    """
    # 1. Grab all unique categories from both dictionaries
    categories = set(ec_dist.keys()).union(set(overall_dist.keys()))
    
    emd_sum = 0
    # 2. Iterate through each category to find the difference in proportions
    for cat in categories:
        # Get the proportion (default to 0.0 if the category is missing)
        p_i = ec_dist.get(cat, 0.0) 
        q_i = overall_dist.get(cat, 0.0)
        
        # 3. Add the absolute difference to our running total
        emd_sum += abs(p_i - q_i)
        
    return 0.5 * emd_sum

# --- Part C: Check t-Closeness ---
def check_t_closeness(df, ec_col, sensitive_col, overall_dist, t):
    all_pass = True
    print(f"\n--- t-Closeness Check (t={t}) ---")
    
    for ec_name, group in df.groupby(ec_col):
        # Calculate the distribution for THIS specific equivalence class
        ec_dist = group[sensitive_col].value_counts(normalize=True).to_dict()
        
        # Compare it to the overall distribution using our EMD function
        emd = compute_emd_unordered(ec_dist, overall_dist)
        
        passes = emd <= t
        if not passes: all_pass = False
        print(f'{ec_name}: EMD={emd:.4f}  t={t}  Pass={passes}')
        
    return all_pass

# Run the check with a threshold of t=0.25
check_t_closeness(df, 'ec', 'viewer_tier', overall_dict, t=0.25)

#D: Propose a Fix and Analyze Trade-offs
df_fixed = df.copy()
df_fixed['ec'] = df_fixed['ec'].replace({'EC1': 'EC1_2', 'EC2': 'EC1_2'})

print("\n--- Verifying t=0.25-Closeness After Fix ---")
# Re-run the check using the overall_dict created in Part C
check_t_closeness(df_fixed, 'ec', 'viewer_tier', overall_dict, t=0.25)