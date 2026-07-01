import pandas as pd

#A: Build the Dataset
data = {
    'patient_id':  ['P01', 'P02', 'P03', 'P04', 'P05', 'P06', 'P07', 'P08', 'P09', 'P10', 'P11', 'P12'],
    'age_group':   ['Teen (13-19)', 'Teen (13-19)', 'Teen (13-19)', 'Adult (20-35)', 'Adult (20-35)', 'Adult (20-35)', 'Senior (36+)', 'Senior (36+)', 'Senior (36+)', 'Adult (20-35)', 'Adult (20-35)', 'Adult (20-35)'],
    'district':    ['Shibuya', 'Shibuya', 'Shibuya', 'Harajuku', 'Harajuku', 'Harajuku', 'Akihabara', 'Akihabara', 'Akihabara', 'Shibuya', 'Shibuya', 'Shibuya'],
    'role':        ['Attendee', 'Attendee', 'Attendee', 'Cosplayer', 'Cosplayer', 'Cosplayer', 'Vendor', 'Vendor', 'Vendor', 'Volunteer', 'Volunteer', 'Volunteer'],
    'diagnosis':   ['Anxiety', 'Anxiety', 'Anxiety', 'Back Pain', 'Back Pain', 'Fatigue', 'Hypertension', 'Hypertension', 'Hypertension', 'Fatigue', 'Fatigue', 'Fatigue']
}
df = pd.DataFrame(data)

#B: Implement l-Diversity Check
def check_l_diversity(df, qi_cols, sensitive_col, l):
    """
    Checks if every equivalence class has at least l distinct sensitive values.
    """
    # 1. Group the dataframe by the Quasi-Identifiers
    grouped = df.groupby(qi_cols)
    
    # 2. For each group, count the number of UNIQUE values in the sensitive column.
    # Hint: Use the .nunique() method on the sensitive_col, then .reset_index(name='distinct_count')
    # Write the logic here:
    ec_summary = grouped[sensitive_col].nunique().reset_index(name='distinct_count')

    # 3. Create a boolean column checking if 'distinct_count' >= l
    # Write the logic here:
    ec_summary['l_satisfied'] = ec_summary['distinct_count'] >= l
    
    print("\n--- l-Diversity Check ---")
    print(ec_summary.to_string(index=False))
    
    # 4. Return True ONLY if the minimum distinct_count across all classes is >= l
    # Write the logic here:
    return ec_summary['l_satisfied'].all()

# Define QI and run the check
qi = ['age_group', 'district', 'role']
check_l_diversity(df, qi, sensitive_col='diagnosis', l=2)

#D: Fix the Dataset

def fix_l_diversity(df):
    df_fixed = df.copy()
    
    # 1. Merge Districts
    df_fixed['district'] = df_fixed['district'].replace({
        'Shibuya': 'Downtown',
        'Akihabara': 'Downtown'
    })
    
    # 2. Generalize Roles
    df_fixed['role'] = df_fixed['role'].replace({
        'Volunteer': 'Convention Fan',
        'Vendor': 'Convention Fan',
        'Attendee': 'Convention Fan'
    })

    # 3. THE MISSING PIECE: Generalize Age Groups
    # We must collapse the ages so they don't keep the groups separated
    df_fixed['age_group'] = df_fixed['age_group'].replace({
        'Teen (13-19)': 'All Ages',
        'Adult (20-35)': 'All Ages',
        'Senior (36+)': 'All Ages'
    })
    
    return df_fixed

df_fixed = fix_l_diversity(df)

print("\n--- Verification After Fix ---")
check_l_diversity(df_fixed, qi, sensitive_col='diagnosis', l=2)