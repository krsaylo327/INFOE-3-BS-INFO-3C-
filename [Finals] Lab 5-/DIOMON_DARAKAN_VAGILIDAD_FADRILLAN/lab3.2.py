import pandas as pd
import numpy as np

#A: Build the Dataset ---
data = {
    'patient_id':  ['M01', 'M02', 'M03', 'M04', 'M05', 'M06', 'M07', 'M08', 'M09', 'M10', 'M11', 'M12', 'M13', 'M14', 'M15', 'M16'],
    'age_group':   ['18-22', '18-22', '18-22', '18-22', '23-30', '23-30', '23-30', '23-30', '31-40', '31-40', '31-40', '31-40', '41+', '41+', '41+', '41+'],
    'cosplay':     ['Shonen Hero', 'Shonen Hero', 'Shonen Hero', 'Shonen Hero', 'Magical Girl', 'Magical Girl', 'Magical Girl', 'Magical Girl', 'Mecha Pilot', 'Mecha Pilot', 'Mecha Pilot', 'Mecha Pilot', 'Classic Villain', 'Classic Villain', 'Classic Villain', 'Classic Villain'],
    'days':        ['1 Day', '1 Day', '1 Day', '1 Day', '2 Days', '2 Days', '2 Days', '2 Days', '3 Days', '3 Days', '3 Days', '3 Days', '2 Days', '2 Days', '2 Days', '2 Days'],
    'condition':   ['Normal', 'Normal', 'Anemia', 'Anemia', 'Normal', 'Pre-diabetic', 'Hypertensive', 'Normal', 'Hypertensive', 'Hypertensive', 'Hypertensive', 'Pre-diabetic', 'Normal', 'Anemia', 'Hypertensive', 'Pre-diabetic']
}
df = pd.DataFrame(data)

overall_dict = df['condition'].value_counts(normalize=True).to_dict()

#C: Design Generalizations ---
def assign_equivalence_classes(df):
    df_anon = df.copy()
    
    # 1. Generalize Age Group
    df_anon['age_group'] = df_anon['age_group'].replace({
        '18-22': '18-30', 
        '23-30': '18-30',
        '31-40': '31+',   
        '41+':   '31+'
    })
    
    # 2. Generalize Cosplay Type
    df_anon['cosplay'] = df_anon['cosplay'].replace({
        'Shonen Hero':     'Popular Anime', 
        'Magical Girl':    'Popular Anime',
        'Mecha Pilot':     'Classic Anime', 
        'Classic Villain': 'Classic Anime'
    })
    
    # 3. Generalize Days Attended
    # Since Group 1 stayed 1 day, and Group 2 stayed 2 days -> '1-2 Days'
    df_anon.loc[df_anon['age_group'] == '18-30', 'days'] = '1-2 Days'
    # Since Group 3 stayed 3 days, and Group 4 stayed 2 days -> '2-3 Days'
    df_anon.loc[df_anon['age_group'] == '31+', 'days'] = '2-3 Days'
    
    # 4. Assign the EC label by combining the generalized columns
    df_anon['ec'] = df_anon['age_group'] + "_" + df_anon['cosplay'] + "_" + df_anon['days']
    
    return df_anon

# --- Helper Functions ---
def check_k_anonymity(df, qi_cols, k):
    ec_counts = df.groupby(qi_cols).size().reset_index(name='count')
    passed = ec_counts['count'].min() >= k
    print(ec_counts.to_string(index=False))
    print(f"-> k={k} Satisfied: {passed}\n")

def check_l_diversity(df, qi_cols, sensitive_col, l):
    ec_summary = df.groupby(qi_cols)[sensitive_col].nunique().reset_index(name='distinct_count')
    passed = (ec_summary['distinct_count'] >= l).all()
    print(ec_summary.to_string(index=False))
    print(f"-> l={l} Satisfied: {passed}\n")

def compute_emd_unordered(ec_dist, overall_dist):
    categories = set(ec_dist.keys()).union(set(overall_dist.keys()))
    emd_sum = sum(abs(ec_dist.get(cat, 0.0) - overall_dist.get(cat, 0.0)) for cat in categories)
    return 0.5 * emd_sum

def check_t_closeness(df, ec_col, sensitive_col, overall_dist, t):
    all_pass = True
    for ec_name, group in df.groupby(ec_col):
        ec_dist = group[sensitive_col].value_counts(normalize=True).to_dict()
        emd = compute_emd_unordered(ec_dist, overall_dist)
        passes = emd <= t
        if not passes: all_pass = False
        print(f'{ec_name}: EMD={emd:.4f}  Pass={passes}')
    print(f"-> t={t} Satisfied: {all_pass}\n")

# --- Execute All Checks ---
df_anon = assign_equivalence_classes(df)
print("=== k=4 CHECK ===")
check_k_anonymity(df_anon, ['ec'], k=4)
print("=== l=2 CHECK ===")
check_l_diversity(df_anon, ['ec'], 'condition', l=2)
print("=== t=0.30 CHECK ===")
check_t_closeness(df_anon, 'ec', 'condition', overall_dict, t=0.30)