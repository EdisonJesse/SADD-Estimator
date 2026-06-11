import pandas as pd
import os
import re
import json

psa_dir = r"c:\AI Projects\Sarangani Earthquake\PSA"
municipal_list_path = os.path.join(psa_dir, "Municipal_List.xlsx")
difficulty_path = os.path.join(psa_dir, "hh-functional-difficulty-severity-age-group-mun-census2020.xlsx")
age_sex_path = os.path.join(psa_dir, "4_Household%20Population%20by%20Age%20Group%20and%20Sex_Philippines_2020%20CPH_rev (2).xlsx")

print("1. Loading reference list...")
df_mun = pd.read_excel(municipal_list_path)

def normalize_name(s):
    if not isinstance(s, str):
        return ""
    s = s.upper()
    s = s.replace(" (CAPITAL)", "")
    s = re.sub(r"\(.*\)", "", s)
    s = s.replace("CITY OF ", "")
    s = s.replace(" CITY", "")
    s = s.replace("Ñ", "N")
    for char in [".", ",", "-", "(", ")", "'"]:
        s = s.replace(char, " ")
    return " ".join(s.split())

df_mun['norm_mun'] = df_mun['Municipality'].apply(normalize_name)
df_mun['norm_prov'] = df_mun['Province'].apply(normalize_name)
df_mun['norm_reg'] = df_mun['Region'].apply(normalize_name)

mun_names_norm = set(df_mun['norm_mun'].unique())
prov_names_norm = set(df_mun['norm_prov'].unique())
reg_names_norm = set(df_mun['norm_reg'].unique())

print("\n2. Processing Age/Sex dataset...")
xl_age = pd.ExcelFile(age_sex_path)
age_records = []

for sheet in xl_age.sheet_names:
    if sheet == "Philippines":
        continue
    df = xl_age.parse(sheet)
    
    current_reg = None
    current_prov = None
    parent_prov = None
    
    i = 0
    while i < len(df):
        val = df.iloc[i, 0]
        if pd.isna(val):
            i += 1
            continue
            
        val_str = str(val).strip()
        norm_val = normalize_name(val_str)
        
        # Track hierarchy (using normalized sets to prevent case-sensitivity issues)
        if norm_val in reg_names_norm:
            reg_match = df_mun[df_mun['norm_reg'] == norm_val]
            if not reg_match.empty:
                current_reg = reg_match.iloc[0]['Region']
            else:
                current_reg = val_str
            i += 1
            continue
            
        if norm_val in prov_names_norm:
            # Enforce that the province belongs to the current region or is one of the manual overrides
            is_valid_prov = False
            match_prov_reg = df_mun[(df_mun['norm_prov'] == norm_val) & (df_mun['Region'] == current_reg)]
            if not match_prov_reg.empty or val_str in [
                "Sulu", "Maguindanao del Sur", "Special Geographic Area", 
                "Negros Occidental", "Negros Oriental", "Siquijor", "City of Bacolod"
            ]:
                is_valid_prov = True
                
            # Blacklist municipality names that share names with provinces
            if norm_val in [
                normalize_name("Quirino"), normalize_name("Rizal"), normalize_name("Quezon"), 
                normalize_name("City of Cotabato"), normalize_name("Sultan Kudarat")
            ] and norm_val in mun_names_norm:
                is_valid_prov = False
                
            if is_valid_prov:
                # Check if this is an HUC
                next_non_null = None
                next_idx = i + 1
                while next_idx < len(df):
                    next_val = df.iloc[next_idx, 0]
                    if pd.notna(next_val):
                        next_non_null = str(next_val).strip()
                        break
                    next_idx += 1
                
                is_huc = not df_mun[(df_mun['norm_prov'] == norm_val) & (df_mun['norm_mun'] == norm_val)].empty
                prov_match = df_mun[df_mun['norm_prov'] == norm_val]
                official_prov = prov_match.iloc[0]['Province'] if not prov_match.empty else val_str
                
                if next_non_null == "Total" and is_huc:
                    current_prov = official_prov
                    # Do NOT update parent_prov for HUCs
                else:
                    current_prov = official_prov
                    parent_prov = official_prov # Update parent_prov for geographic provinces
                    i += 1
                    continue
            
        if norm_val in mun_names_norm:
            norm_prov_curr = normalize_name(current_prov) if current_prov else ""
            mun_match = df_mun[(df_mun['norm_mun'] == norm_val) & (df_mun['norm_prov'] == norm_prov_curr)]
            
            # Revert to parent province if it matches there instead (HUC interruption handling)
            if mun_match.empty and parent_prov:
                norm_parent_prov = normalize_name(parent_prov)
                parent_match = df_mun[(df_mun['norm_mun'] == norm_val) & (df_mun['norm_prov'] == norm_parent_prov)]
                if not parent_match.empty:
                    current_prov = parent_prov
                    norm_prov_curr = norm_parent_prov
                    mun_match = parent_match
                    
            if mun_match.empty:
                # Fallback to any match in the region
                reg_match = df_mun[(df_mun['norm_mun'] == norm_val) & (df_mun['Region'] == current_reg)]
                if not reg_match.empty:
                    mun_match = reg_match
                    current_prov = reg_match.iloc[0]['Province']
            
            current_mun = mun_match.iloc[0]['Municipality'] if not mun_match.empty else val_str
            
            # The next row must be "Total"
            i += 1
            if i >= len(df):
                break
            total_row = df.iloc[i]
            if str(total_row.iloc[0]).strip() == "Total":
                tot = total_row.iloc[1]
                male = total_row.iloc[2]
                female = total_row.iloc[3]
                
                if pd.isna(tot) or tot == 0:
                    i += 1
                    continue
                    
                mun_age_dict = {
                    'sheet_reg': current_reg,
                    'sheet_prov': current_prov,
                    'sheet_mun': current_mun,
                    'Total': int(tot),
                    'Male': int(male) if pd.notna(male) else 0,
                    'Female': int(female) if pd.notna(female) else 0,
                    'Age_Groups': {},
                    'Male_Age_Groups': {},
                    'Female_Age_Groups': {}
                }
                
                # Read age groups until we see nan or another header
                i += 1
                while i < len(df):
                    age_row = df.iloc[i]
                    age_val = age_row.iloc[0]
                    if pd.isna(age_val):
                        break
                    age_str = str(age_val).strip()
                    norm_age_str = normalize_name(age_str)
                    
                    if norm_age_str in mun_names_norm or norm_age_str in prov_names_norm or norm_age_str in reg_names_norm:
                        i -= 1 # back up
                        break
                        
                    if re.match(r"^\d+\s*-\s*\d+$", age_str) or age_str.endswith("years and over"):
                        count_both = age_row.iloc[1]
                        count_male = age_row.iloc[2]
                        count_female = age_row.iloc[3]
                        
                        mun_age_dict['Age_Groups'][age_str] = int(count_both) if pd.notna(count_both) else 0
                        mun_age_dict['Male_Age_Groups'][age_str] = int(count_male) if pd.notna(count_male) else 0
                        mun_age_dict['Female_Age_Groups'][age_str] = int(count_female) if pd.notna(count_female) else 0
                    i += 1
                
                age_records.append(mun_age_dict)
        i += 1

print(f"Extracted age-sex data for {len(age_records)} municipalities.")

print("\n3. Processing Disability dataset...")
df_diff = pd.read_excel(difficulty_path)

# Group by Sex, Province, Mun, Disability, Status and sum
grouped = df_diff.groupby(['Sex', 'Province', 'Mun', 'Disability', 'Status'])['Household Population 5 Years Old and Over with Functional Difficulty'].sum().reset_index()

disability_records = {}
for idx, row in grouped.iterrows():
    sex = str(row['Sex']).strip() # 'Both Sexes', 'Male', or 'Female'
    mun = str(row['Mun']).strip()
    prov = str(row['Province']).strip()
    
    norm_mun = normalize_name(mun)
    norm_prov = normalize_name(prov)
    key = (norm_mun, norm_prov)
    
    domain = str(row['Disability']).strip()
    severity = str(row['Status']).strip().capitalize()
    count = row['Household Population 5 Years Old and Over with Functional Difficulty']
    
    if key not in disability_records:
        disability_records[key] = {}
    if sex not in disability_records[key]:
        disability_records[key][sex] = {}
    if domain not in disability_records[key][sex]:
        disability_records[key][sex][domain] = {}
        
    disability_records[key][sex][domain][severity] = int(count) if pd.notna(count) else 0

print(f"Extracted disability data for {len(disability_records)} unique pairs.")

print("\n4. Flexible merging and ratio computation...")
final_ratios = []
count_exact = 0
count_name_prov = 0
count_name_only = 0
count_unmapped = 0

for age_info in age_records:
    s_reg = age_info['sheet_reg']
    s_prov = age_info['sheet_prov']
    s_mun = age_info['sheet_mun']
    tot = age_info['Total']
    male_tot = age_info['Male']
    female_tot = age_info['Female']
    
    norm_mun = normalize_name(s_mun)
    norm_prov = normalize_name(s_prov)
    norm_reg = normalize_name(s_reg)
    
    # Try flexible matching in df_mun
    match = df_mun[(df_mun['norm_mun'] == norm_mun) & (df_mun['norm_prov'] == norm_prov)]
    if len(match) == 1:
        count_exact += 1
    else:
        # Match by name and region
        match_reg = df_mun[(df_mun['norm_mun'] == norm_mun) & (df_mun['norm_reg'] == norm_reg)]
        if len(match_reg) == 1:
            match = match_reg
            count_name_prov += 1
        else:
            # Match by name alone if unique
            match_any = df_mun[df_mun['norm_mun'] == norm_mun]
            if len(match_any) == 1:
                match = match_any
                count_name_only += 1
            elif len(match_any) > 1:
                # filter by region
                reg_filtered = match_any[match_any['Region'] == s_reg]
                if len(reg_filtered) == 1:
                    match = reg_filtered
                    count_name_only += 1
                else:
                    # check if any matches province by substring
                    sub_match = match_any[match_any['Province'].apply(normalize_name).str.contains(norm_prov) | 
                                          pd.Series(norm_prov).apply(lambda x: x in match_any['Province'].apply(normalize_name).values).values[0]]
                    if len(sub_match) == 1:
                        match = sub_match
                        count_name_prov += 1
                        
    if len(match) != 1:
        count_unmapped += 1
        print(f"Unmapped age record: Mun={s_mun}, Prov={s_prov}, Reg={s_reg}")
        continue
        
    # Get official metadata
    official_row = match.iloc[0]
    psgc = int(official_row['PSGC_Code']) if pd.notna(official_row['PSGC_Code']) else None
    o_reg = official_row['Region']
    o_prov = official_row['Province']
    o_mun = official_row['Municipality']
    
    record = {
        'PSGC_Code': psgc,
        'Region': o_reg,
        'Province': o_prov,
        'Municipality': o_mun,
        'Total_Population': tot,
        'Male_Population': male_tot,
        'Female_Population': female_tot,
        'Male_Ratio': round(male_tot / tot, 6) if tot > 0 else 0.0,
        'Female_Ratio': round(female_tot / tot, 6) if tot > 0 else 0.0,
    }
    
    # Age group ratios
    for age_gp, count in age_info['Age_Groups'].items():
        clean_age_gp = age_gp.replace(" ", "")
        record[f"Age_{clean_age_gp}_Ratio"] = round(count / tot, 6) if tot > 0 else 0.0
        
    # Male age group ratios
    for age_gp, count in age_info['Male_Age_Groups'].items():
        clean_age_gp = age_gp.replace(" ", "")
        record[f"Male_Age_{clean_age_gp}_Ratio"] = round(count / male_tot, 6) if male_tot > 0 else 0.0
        
    # Female age group ratios
    for age_gp, count in age_info['Female_Age_Groups'].items():
        clean_age_gp = age_gp.replace(" ", "")
        record[f"Female_Age_{clean_age_gp}_Ratio"] = round(count / female_tot, 6) if female_tot > 0 else 0.0
        
    # Disability ratios
    domain_map = {
        'Seeing even if wearing eyeglasses': 'Seeing',
        'Hearing even if using a hearing aid': 'Hearing',
        'Walking or climbing steps': 'Walking',
        'Remembering or concentrating': 'Remembering',
        'Self-caring (washing all over or dressing)': 'Self_Caring',
        'Communicating': 'Communicating'
    }
    
    # Initialize all domains/severities to 0 ratio for Both, Male, and Female
    for prefix in ['', 'Male_', 'Female_']:
        for short_domain in domain_map.values():
            for sev in ['Mild', 'Moderate', 'Severe', 'All']:
                record[f"{prefix}Disability_{short_domain}_{sev}_Ratio"] = 0.0
            
    # Load actual disability data using name-based lookup
    dis_info = None
    norm_o_mun = normalize_name(o_mun)
    norm_o_prov = normalize_name(o_prov)
    if (norm_o_mun, norm_o_prov) in disability_records:
        dis_info = disability_records[(norm_o_mun, norm_o_prov)]
        
    # Calculate denominators for population aged 5 and over (substracting the 0-4 cohort)
    age_0_4_tot = age_info['Age_Groups'].get('0 - 4', 0)
    age_0_4_male = age_info['Male_Age_Groups'].get('0 - 4', 0)
    age_0_4_female = age_info['Female_Age_Groups'].get('0 - 4', 0)
    
    denom_both = tot - age_0_4_tot
    denom_male = male_tot - age_0_4_male
    denom_female = female_tot - age_0_4_female

    if dis_info:
        for sex_key, sex_prefix, denom in [('Both Sexes', '', denom_both), ('Male', 'Male_', denom_male), ('Female', 'Female_', denom_female)]:
            if sex_key in dis_info and denom > 0:
                sex_dis = dis_info[sex_key]
                for long_domain, short_domain in domain_map.items():
                    matched_long = None
                    for d in sex_dis.keys():
                        if short_domain.lower() in d.lower() or d.strip() == long_domain.strip():
                            matched_long = d
                            break
                            
                    if matched_long:
                        for sev, count in sex_dis[matched_long].items():
                            clean_sev = sev.strip().capitalize()
                            if clean_sev in ['Mild', 'Moderate', 'Severe', 'All']:
                                record[f"{sex_prefix}Disability_{short_domain}_{clean_sev}_Ratio"] = round(count / denom, 6)
                        
    final_ratios.append(record)

print(f"Ratios generated: Exact={count_exact}, Name-Prov={count_name_prov}, Name-Only={count_name_only}, Unmapped={count_unmapped}")
print(f"Total mapped final ratios: {len(final_ratios)}")

# Fill in missing disability ratios for municipalities not in difficulty dataset (e.g. Peñablanca, Sasmuan)
# by using the provincial average of other municipalities in the same province.
disability_keys = [k for k in final_ratios[0].keys() if 'Disability_' in k]
for record in final_ratios:
    # If all disability ratios are 0.0, fill them in
    if sum(record[k] for k in disability_keys) == 0.0:
        prov = record['Province']
        # Find other records in the same province that have non-zero disability ratios
        others = [rec for rec in final_ratios if rec['Province'] == prov and sum(rec[k] for k in disability_keys) > 0.0]
        if others:
            for k in disability_keys:
                record[k] = round(sum(o[k] for o in others) / len(others), 6)
            print(f"Filled in disability ratios for {record['Municipality']} ({record['Province']}) using average of {len(others)} other municipalities in the province.")
        else:
            print(f"Warning: No other municipalities in province {prov} to fill in disability ratios for {record['Municipality']}.")

# 5. Export results
print("\n5. Saving outputs...")
df_ratios = pd.DataFrame(final_ratios)
df_ratios.to_csv(os.path.join(psa_dir, "municipality_ratios.csv"), index=False)
print("Saved CSV: municipality_ratios.csv")

with open(os.path.join(psa_dir, "municipality_ratios.json"), 'w') as f:
    json.dump(final_ratios, f, indent=2)
print("Saved JSON: municipality_ratios.json")

print("All ratio calculations completed successfully!")
